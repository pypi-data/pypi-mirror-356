"""
自动水质建模器主模块，提供一键式建模功能
"""

import pandas as pd
import numpy as np
import json
import os
import logging
from typing import Dict, List, Tuple, Optional, Any, Union
from datetime import datetime

# 导入项目组件
from .config_manager import ConfigManager
from .feature_manager import FeatureManager
from ..preprocessing.spectrum_processor import SpectrumProcessor
from ..models.builder import ModelBuilder
from ..utils.encryption import encrypt_data_to_file, decrypt_file

# 获取模块日志记录器
logger = logging.getLogger(__name__)

class AutoWaterQualityModeler:
    """自动水质建模器，支持一键式建模流程"""
    
    def __init__(self, 
                 config_path: Optional[str] = None,
                 min_wavelength: int = 400, 
                 max_wavelength: int = 900,
                 smooth_window: int = 11, 
                 smooth_order: int = 3):
        """
        初始化自动水质建模器
        
        Args:
            config_path: 特征配置文件路径
            min_wavelength: 最小波长
            max_wavelength: 最大波长
            smooth_window: 平滑窗口大小
            smooth_order: 平滑多项式阶数
        """
        # 创建组件
        self.config_manager = ConfigManager(config_path)
        self.feature_manager = FeatureManager(self.config_manager)
        self.processor = SpectrumProcessor(
            min_wavelength=min_wavelength,
            max_wavelength=max_wavelength,
            smooth_window=smooth_window,
            smooth_order=smooth_order
        )
        self.model_builder = ModelBuilder()
        
        # 保存配置
        self.min_wavelength = min_wavelength
        self.max_wavelength = max_wavelength
        self.smooth_window = smooth_window
        self.smooth_order = smooth_order
    
    def fit(self, 
            spectrum_data: pd.DataFrame, 
            metric_data: pd.DataFrame,
            data_type: str = "aerospot",
            matched_idx = None,
            origin_merged_data = pd.DataFrame) -> Tuple[Dict, pd.DataFrame, pd.DataFrame] | Tuple[Dict, pd.DataFrame]:
        """
        一键式建模流程
        
        Args:
            spectrum_data: 光谱数据DataFrame（列名为波段，每行是一条光谱样本）
            metric_data: 实测值DataFrame（每列是一个水质指标）
            data_type: 数据类型，必须是"warning_device"、"shore_data"、"smart_water"或"aerospot"之一
            matched_idx: 匹配的索引，如果为None则使用全部数据
            origin_merged_data: 原始合并数据，用于模型微调
            
        Returns:
            Tuple[Dict, pd.DataFrame, pd.DataFrame] | Tuple[Dict, pd.DataFrame]: 
                - 模型字典
                - 匹配样本的预测结果
                - 所有样本的预测结果（仅当matched_idx不为None或提供了all_merged_data时才返回）
        """
        try:
            # 验证数据类型
            supported_types = self.config_manager.DATA_TYPES
            if data_type not in supported_types:
                raise ValueError(f"不支持的数据类型: {data_type}，必须是 {supported_types} 之一")
                
            logger.info(f"开始建模，数据类型: {data_type}")
            
            # 获取模型参数
            model_params = self.config_manager.get_model_params(data_type)
            min_samples = model_params.get("min_samples", 6)
            
            # 预处理光谱数据
            processed_spectrum = self.processor.preprocess(spectrum_data)
            
            # 准备实测数据
            # 过滤掉不需要的列
            filter_metric_data = metric_data.drop(['index', 'latitude', 'longitude'], axis=1, errors='ignore')
            
            # 如果提供了匹配索引，使用匹配的数据进行建模
            if matched_idx is not None:
                filter_merged_data = origin_merged_data.drop(['index', 'latitude', 'longitude'], axis=1, errors='ignore')
                merged_data = filter_merged_data.iloc[matched_idx]
                merged_data.index = filter_metric_data.index
            else:
                merged_data = origin_merged_data
                # 判断merged_data和metric_data的样本量是否一致
                if len(merged_data) != len(filter_metric_data):
                    raise ValueError("merged_data和metric_data的样本量不一致")
            
            # 判断样本量，决定建模策略
            if len(filter_metric_data) >= min_samples:
                logger.info(f"样本量：{len(filter_metric_data)}，满足{data_type}类型数据默认最小样本量：{min_samples}，采用自动建模")
                
                # 构建完整模型
                build_result = self._build_full_models(
                    processed_spectrum, 
                    filter_metric_data, 
                    data_type, 
                    model_params,
                    matched_idx
                )
                
                # 根据返回值的数量处理结果
                if matched_idx is not None:
                    models_dict, pred_dict, all_pred_dict = build_result
                else:
                    models_dict, pred_dict = build_result
                    all_pred_dict = pd.DataFrame()  # 创建空DataFrame作为占位符
                
                # 格式化模型结果
                models_dict = self._format_result(models_dict, 1, merged_data)
                logger.info("自动建模格式化模型格式成功")
                
            else:
                logger.info(f"样本量：{len(filter_metric_data)}，不满足{data_type}类型数据默认最小样本量：{min_samples}，采用模型微调")
                
                # 如果没有提供匹配数据，无法进行微调
                if merged_data is None:
                    raise ValueError("样本量不足且未提供匹配数据，无法进行模型微调")
                
                # 模型微调
                tune_result = self._tune_models(
                    merged_data, 
                    filter_metric_data, 
                    filter_merged_data if matched_idx is not None else None
                )
                
                # 根据返回值的数量处理结果
                if matched_idx is not None:
                    models_dict, pred_dict, all_pred_dict = tune_result
                else:
                    models_dict, pred_dict = tune_result
                    all_pred_dict = pd.DataFrame()  # 创建空DataFrame作为占位符
                
                # 格式化模型结果
                models_dict = self._format_result(models_dict, 0, merged_data)
                logger.info("模型微调格式化模型格式成功")
            
            # 根据matched_idx决定返回值
            if matched_idx is not None:
                return models_dict, pred_dict, all_pred_dict
            else:
                return models_dict, pred_dict
            
        except Exception as e:
            logger.error(f"建模失败: {e}", exc_info=True)
            # 根据matched_idx决定异常时的返回值
            if matched_idx is not None:
                return {}, pd.DataFrame(), pd.DataFrame()
            else:
                return {}, pd.DataFrame()
    
    def _build_full_models(self, 
                          spectrum_data: pd.DataFrame, 
                          metric_data: pd.DataFrame,
                          data_type: str,
                          model_params: Dict,
                          matched_idx = None) -> Tuple[Dict, pd.DataFrame, pd.DataFrame] | Tuple[Dict, pd.DataFrame]:
        """
        构建完整模型
        
        Args:
            spectrum_data: 预处理后的光谱数据
            metric_data: 实测值数据
            data_type: 数据类型
            model_params: 模型参数
            matched_idx: 匹配的索引
            
        Returns:
            Tuple[Dict, pd.DataFrame, pd.DataFrame]: 
                - 模型字典
                - 匹配样本的预测结果
                - 所有样本的预测结果（仅当matched_idx不为None时才有意义）
        """
        # 收集模型结果
        models_dict = {}
        
        # 收集预测结果
        pred_dict = pd.DataFrame()
        all_pred_dict = pd.DataFrame()
        
        # 获取指标列表
        metrics = metric_data.columns.tolist()
        
        # 为每个指标建模
        for metric_name in metrics:
            logger.info(f"开始为 {metric_name} 指标构建模型")
            # 获取模型参数
            model_params = self.config_manager.get_model_params(data_type, metric_name)

            # 计算特征
            features = self.feature_manager.calculate_features(spectrum_data, data_type, metric_name)
            
            if features.empty:
                logger.warning(f"指标 {metric_name} 的特征计算结果为空，跳过")
                continue
            
            # 1. 先利用matched_idx对齐features和metric_data
            if matched_idx is not None:
                if len(matched_idx) != len(metric_data):
                    raise ValueError("matched_idx的长度与metric_data的长度不一致，请检查matched_idx")
                # 筛选匹配的特征
                matched_features = features.iloc[matched_idx].copy()
                # 将索引调整为与metric_data一致
                
                matched_features.index = metric_data.index
                working_features = matched_features
            else:
                # 如果没有匹配索引，使用原始features
                working_features = features
            
            # 2. 获取指标并筛选非负值
            metric_series = metric_data[metric_name]
            
            # 选择特征
            top_n = model_params.get('max_features', 5)

            # 返回根据相关性排序的特征，并返回特征的模型参数
            best_models = self.feature_manager.select_top_features(working_features, metric_series, top_n)
            
            if not best_models:
                logger.warning(f"指标 {metric_name} 无法选择有效特征，跳过")
                continue
            
            if isinstance(top_n, int):
                init_n = 1
            elif top_n == 'all':
                init_n = len(best_models)
            else:
                raise ValueError(f"top_n 必须是数字或 'all'")
            
            final_model = {}
            best_combination = None
            best_corr = 0
            
            for n in range(init_n, len(best_models) + 1):
                selected_features = best_models[:n]
                logger.info(f"选择特征: {[name for name, _ in selected_features]}")
                total_weight = sum(abs(f[1]['corr']) for f in selected_features)
                weights = {f[0]: abs(f[1]['corr']) / total_weight for f in selected_features}

                inverted_values = {}
                # 只在需要匹配样本时计算all_inverted_values
                all_inverted_values = {} if matched_idx is not None else None
                
                for feature_name, params in selected_features:
                    x_data = working_features[feature_name].dropna()
                    x_data = x_data[x_data > 0]
                    
                    inverted = params['a'] * np.power(x_data.values, params['b'])
                    inverted_values[feature_name] = pd.Series(inverted, index=x_data.index)

                    # 只在需要匹配样本时计算all_inverted
                    if matched_idx is not None:
                        all_x_data = features[feature_name].dropna()
                        all_x_data = all_x_data[all_x_data > 0]
                        all_inverted = params['a'] * np.power(all_x_data.values, params['b'])
                        all_inverted_values[feature_name] = pd.Series(all_inverted, index=all_x_data.index)
                
                if inverted_values:
                    # 计算匹配样本的共同索引和预测结果
                    common_indices = set.intersection(*[set(series.index) for series in inverted_values.values()])
                    
                    if common_indices:
                        common_indices_list = list(common_indices)
                        weighted_result = pd.Series(0, index=common_indices_list, name=metric_name)
                        
                        for feature_name in inverted_values:
                            weighted_result += inverted_values[feature_name].loc[common_indices_list] * weights[feature_name]
                        
                        y_true = metric_series.loc[weighted_result.index]
                        corr = np.corrcoef(weighted_result, y_true)[0, 1]
                        rmse = np.sqrt(np.mean((weighted_result - y_true) ** 2))
                        
                        # 构建最佳组合
                        if corr > best_corr:
                            best_corr = corr
                            best_combination = {
                                'n_features': n,
                                'features': best_models[:n],
                                'weights': weights,
                                'corr': corr,
                                'rmse': rmse,
                                'pred_data': pd.Series(weighted_result, index=metric_series.index, name=metric_name)
                            }
                            
                            # 只在需要匹配样本时计算all_pred_data
                            if matched_idx is not None:
                                all_common_indices = set.intersection(*[set(series.index) for series in all_inverted_values.values()])
                                if all_common_indices:
                                    all_common_indices_list = list(all_common_indices)
                                    all_weighted_result = pd.Series(0, index=all_common_indices_list, name=metric_name)
                                    
                                    for feature_name in all_inverted_values:
                                        all_weighted_result += all_inverted_values[feature_name].loc[all_common_indices_list] * weights[feature_name]
                                    
                                    best_combination['all_pred_data'] = pd.Series(all_weighted_result, index=spectrum_data.index, name=metric_name)
            
            if best_combination:
                for feature_name, params in best_combination['features']:
                    final_model[feature_name] = {
                        'w': best_combination['weights'][feature_name],
                        'a': params['a'],
                        'b': params['b']
                        }
            models_dict[metric_name] = final_model
            pred_dict[metric_name] = best_combination['pred_data']
            
            # 只在需要匹配样本时添加all_pred_dict
            if matched_idx is not None and 'all_pred_data' in best_combination:
                all_pred_dict[metric_name] = best_combination['all_pred_data']
        
        if matched_idx is not None:
            return models_dict, pred_dict, all_pred_dict
        else:
            return models_dict, pred_dict

    
    def _tune_models(self, 
                    merged_data: pd.DataFrame, 
                    metric_data: pd.DataFrame,
                    all_merged_data = None) -> Tuple[Dict, pd.DataFrame, pd.DataFrame] | Tuple[Dict, pd.DataFrame]:
        """
        微调模型
        
        Args:
            merged_data: 匹配样本的合并数据
            metric_data: 实测值数据
            all_merged_data: 所有样本的合并数据，如果为None则不计算所有样本的预测结果
            
        Returns:
            Tuple[Dict, pd.DataFrame, pd.DataFrame] | Tuple[Dict, pd.DataFrame]: 
                - 模型字典
                - 匹配样本的预测结果
                - 所有样本的预测结果（仅当all_merged_data不为None时才返回）
        """
        # 收集模型结果
        models_dict = {}
        
        # 收集预测结果
        pred_dict = pd.DataFrame(index=metric_data.index)
        
        # 只在all_merged_data不为None时初始化all_pred_dict
        all_pred_dict = pd.DataFrame(index=all_merged_data.index) if all_merged_data is not None else pd.DataFrame()
        
        # 遍历所有指标
        for metric_name in metric_data.columns:
            # 检查指标是否在两个数据集中都存在
            if metric_name not in merged_data.columns:
                logger.warning(f"指标 {metric_name} 不在合并数据中，跳过")
                continue
            
            # 获取实测值和预测值
            measured = metric_data[metric_name].dropna()
            predicted = merged_data[metric_name].loc[measured.index]
            
            # 微调模型
            tuned_A = self.model_builder.tune_linear(predicted, measured)
            
            if not tuned_A:
                logger.warning(f"指标 {metric_name} 模型微调失败，跳过")
                continue
            
            # 保存模型结果
            models_dict[metric_name] = tuned_A
            
            # 匹配样本的预测结果
            adjusted_pred = tuned_A * predicted
            adjusted_pred.name = metric_name
            pred_dict[metric_name] = adjusted_pred
            
            # 只在all_merged_data不为None时计算所有样本的预测结果
            if all_merged_data is not None and metric_name in all_merged_data.columns:
                all_adjusted = tuned_A * all_merged_data[metric_name]
                all_adjusted.name = metric_name
                all_pred_dict[metric_name] = all_adjusted
            
            logger.info(f"成功为 {metric_name} 指标微调模型，系数: {tuned_A:.4f}")
        
        # 将预测结果中的负值替换为NaN
        pred_dict = np.where(pred_dict < 0, np.nan, pred_dict)
        
        # 只在all_merged_data不为None时处理all_pred_dict
        if all_merged_data is not None:
            all_pred_dict = np.where(all_pred_dict < 0, np.nan, all_pred_dict)

        logger.info("模型微调完成")
        
        # 根据all_merged_data是否为None返回不同的结果
        if all_merged_data is not None:
            return models_dict, pred_dict, all_pred_dict
        else:
            return models_dict, pred_dict
    
    def _format_result(self, result, type: int, merged_data: pd.DataFrame):
        if type not in [0, 1]:
            raise ValueError("type 必须是 0 或 1")
        index=['turbidity', 'ss', 'sd', 'do', 'codmn', 'codcr', 'chla', 'tn', 'tp', 'chroma', 'nh3n']
        columns=[f'STZ{i}' for i in range(1, 20)]

        # 创建水质参数系数矩阵
        w_coefficients = pd.DataFrame(0.0, 
            index=index,
            columns=columns,
            dtype=float
        )
        a_coefficients = pd.DataFrame(0.0, 
            index=index,
            columns=columns,
            dtype=float
        )
        b_coefficients = pd.DataFrame(0.0, 
            index=index,
            columns=columns,
            dtype=float
        )
        A_coefficients = pd.DataFrame(1.0,
            index=index,
            columns=['A'],
            dtype=float
        )

        Range_coefficients = pd.DataFrame(0.0,
            index=index,
            columns=['m', 'n'],
            dtype=float
        )

        # 解析result并填充系数矩阵
        if result:
            if type == 1:
                try:
                    logger.info("开始解析建模结果并填充系数矩阵")
                    
                    # 遍历result中的每个水质参数
                    for param_key, param_data in result.items():
                        # 检查参数是否在系数矩阵的索引中
                        if param_key in w_coefficients.index:
                            # 遍历每个测站的数据
                            for station_key, station_data in param_data.items():
                                # 检查测站是否在系数矩阵的列中
                                if station_key in w_coefficients.columns:
                                    # 根据三级key将系数填入对应的矩阵
                                    
                                    if 'w' in station_data:
                                        w_coefficients.loc[param_key, station_key] = station_data['w']
                                    if 'a' in station_data:
                                        a_coefficients.loc[param_key, station_key] = station_data['a']
                                    if 'b' in station_data:
                                        b_coefficients.loc[param_key, station_key] = station_data['b']

                    
                    logger.info("系数矩阵填充完成")
                except Exception as e:
                    logger.error(f"填充系数矩阵时出错: {str(e)}")
            elif type == 0:
                try:
                    logger.info("开始解析模型微调结果并只填充A系数矩阵")

                    for param_key, param_data in result.items():
                        if param_key in A_coefficients.index:
                            A_coefficients.loc[param_key, 'A'] = param_data
                except Exception as e:
                    logger.error(f"填充系数矩阵时出错: {str(e)}")

        # 将系数矩阵转换为列表
        format_result = dict()
        # 将系数矩阵展开成一维列表
        format_result['type'] = type
        if type == 1:
            format_result['w'] = w_coefficients.values.T.flatten().tolist()
            format_result['a'] = a_coefficients.values.T.flatten().tolist()
            format_result['b'] = b_coefficients.values.flatten().tolist()
        format_result['A'] = A_coefficients.values.flatten().tolist()

        # 获取各指标上下限，并填充到Range_coefficients中
        for index in Range_coefficients.index:
            if index in merged_data.columns:
                min_value = merged_data[index].min()
                max_value = merged_data[index].max()
                if min_value == max_value:
                    logger.warning(f"指标：{index} 上下限相同，无法计算范围系数，可能是样本量太少：{len(merged_data)}")
                Range_coefficients.loc[index, 'm'] = max(0, min_value - merged_data[index].std())
                Range_coefficients.loc[index, 'n'] = max_value + merged_data[index].std()

        format_result['Range'] = Range_coefficients.values.flatten().tolist()

        return format_result
    

    