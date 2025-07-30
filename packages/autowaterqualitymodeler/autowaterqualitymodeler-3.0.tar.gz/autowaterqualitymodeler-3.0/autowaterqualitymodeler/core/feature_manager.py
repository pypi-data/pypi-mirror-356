"""
特征管理模块，连接配置管理和特征计算
"""

import pandas as pd
import numpy as np
import os
import logging
from typing import Dict, List, Optional, Union, Any, Tuple

# 导入项目组件
from ..features.calculator import FeatureCalculator
from .config_manager import ConfigManager

# 获取模块日志记录器
logger = logging.getLogger(__name__)

class FeatureManager:
    """特征管理器，处理特征定义和计算"""
    
    def __init__(self, config_manager: ConfigManager, tris_coeff_path: Optional[str] = None):
        """
        初始化特征管理器
        
        Args:
            config_manager: 配置管理器实例
            tris_coeff_path: 三刺激值系数表路径，如果为None则使用默认路径
        """
        self.config_manager = config_manager
        
        # 加载三刺激值系数表
        self.tris_coeff = self._load_tris_coefficients(tris_coeff_path)
        
        # 创建特征计算器
        self.calculator = FeatureCalculator(tris_coeff=self.tris_coeff)
    
    def _load_tris_coefficients(self, tris_coeff_path: Optional[str] = None) -> pd.DataFrame:
        """
        加载三刺激值系数表
        
        Args:
            tris_coeff_path: 三刺激值系数表路径，如果为None则使用默认路径
            
        Returns:
            pd.DataFrame: 三刺激值系数表
        """
        try:
            # 如果未提供路径，使用默认路径
            if tris_coeff_path is None:
                tris_coeff_path = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                    'resources', 
                    'D65xCIE.xlsx'
                )
            
            # 加载三刺激值系数表
            tris_coeff = pd.read_excel(tris_coeff_path, header=0, index_col=0)
            logger.info(f"成功加载三刺激值系数表: {tris_coeff_path}")
            return tris_coeff
            
        except Exception as e:
            logger.warning(f"加载三刺激值系数表失败: {e}", exc_info=True)
            # 返回空DataFrame
            return pd.DataFrame()
    
    def calculate_features(self, spectrum_data: pd.DataFrame, data_type: str, metric_name: str) -> pd.DataFrame:
        """
        计算指定数据类型和指标的特征
        
        Args:
            spectrum_data: 光谱数据DataFrame
            data_type: 数据类型
            metric_name: 指标名称
            
        Returns:
            pd.DataFrame: 计算的特征数据
        """
        try:
            # 获取特征定义
            feature_definitions = self.config_manager.get_feature_definitions(data_type, metric_name)
            
            if not feature_definitions:
                logger.warning(f"未找到 {data_type} 下 {metric_name} 指标的特征定义")
                return pd.DataFrame(index=spectrum_data.index)
            
            # 计算特征
            features = self.calculator.calculate_features(spectrum_data, feature_definitions)
            
            if features.empty:
                logger.warning(f"{metric_name} 指标的特征计算结果为空")
                
            return features
            
        except Exception as e:
            logger.error(f"计算 {data_type} 下 {metric_name} 指标的特征时出错: {e}", exc_info=True)
            return pd.DataFrame(index=spectrum_data.index)
    
    def get_feature_importance(self, features: pd.DataFrame, target: pd.Series) -> Dict[str, float]:
        """
        计算特征重要性（基于幂函数模型a*x^b的拟合效果）
        
        Args:
            features: 特征数据
            target: 目标变量
            
        Returns:
            Dict[str, float]: 特征重要性字典，键为特征名，值为基于模型的相关性
        """
        try:
            if features.empty:
                return {}
                
            importance = {}
            
            
            # 计算每个特征的重要性
            for feature_name in features.columns:
                # 去除缺失值和负值（幂函数模型的限制）
                valid_mask = (features[feature_name] > 0) & (target > 0) & (~features[feature_name].isna()) & (~target.isna())
                if valid_mask.sum() < 3:  # 至少需要3个点才能拟合模型
                    logger.warning(f"特征 {feature_name} 的有效数据点少于3个，无法拟合模型")
                    continue
                
                x = features.loc[valid_mask, feature_name].values
                y = target.loc[valid_mask].values

                # 记录原始数据范围
                logger.info(f"特征：{feature_name} 拟合数据范围 - x: {np.min(x)}-{np.max(x)}, y: {np.min(y)}-{np.max(y)}")
                
                try:
                    # 拟合幂函数模型
                    params = self.perform_power_fitting(x, y)
                    if params:
                        a, b, corr, rmse, r2 = params
                        importance[feature_name] = {
                        'a': float(a), 'b': float(b), 'corr': float(corr), 
                        'rmse': float(rmse), 'r2': float(r2)
                    }

                except Exception as e:
                    logger.error(f"拟合特征 {feature_name} 失败: {e}", exc_info=True)
            
            return importance
            
        except Exception as e:
            logger.error(f"计算特征重要性时出错: {e}", exc_info=True)
            return {}


    def perform_power_fitting(self, x_valid, y_valid, initial_guess=None):
        """执行幂函数拟合: y = a * x^b"""
        from scipy.optimize import curve_fit
        from scipy.stats import pearsonr
        import warnings
        
        # 定义拟合函数并捕获警告
        def fit_function(x, a, b):
            # 捕获幂运算中的警告并记录参数值
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                result = a * np.power(x, b)
                
                # 如果有警告产生，则记录参数信息
                if len(w) > 0 and issubclass(w[-1].category, RuntimeWarning):
                    # 记录产生警告时的参数值
                    logger.warning(f"幂运算溢出警告! 参数值: a={a}, b={b}")
                    logger.warning(f"x值范围: {np.min(x)} - {np.max(x)}")
                    
                    # 寻找导致溢出的具体x值
                    problem_indices = np.isnan(result) | np.isinf(result)
                    if np.any(problem_indices):
                        problem_x = x[problem_indices]
                        logger.warning(f"导致问题的x值: {problem_x[:10]} ...")
            
            return result
        
        try:
            
            
            # 初始猜测值
            if initial_guess is None:
                initial_guess = [1.0, 1.0]
            
            # 设置参数约束，防止产生极端参数值
            # a参数通常不需要太大，b参数应该在合理范围内
            bounds = (
                [-100000, -50],  # 下限：a可以为负，但b不应过度负值
                [100000, 50]     # 上限：限制a和b的绝对值
            )
            
            # 执行拟合，添加参数约束
            popt, pcov = curve_fit(
                fit_function, 
                x_valid, 
                y_valid, 
                p0=initial_guess, 
                maxfev=10000, 
                method='trf',   # 使用trust-region方法支持边界约束
                bounds=bounds
            )
            
            # 获取参数
            a, b = popt

            # 检查参数是否接近边界
            if abs(a) > bounds[1][0] * 0.9 or abs(b) > bounds[1][1] * 0.9:
                logger.warning(f"拟合参数接近边界值，可能需要扩大参数范围: a={a}, b={b}")

                # # 绘制模型曲线和数据点图片
                # try:
                #     import matplotlib.pyplot as plt
                #     from matplotlib.font_manager import FontProperties
                #     import os
                    
                #     # 设置中文字体
                #     try:
                #         font = FontProperties(family='SimHei')
                #     except:
                #         logger.warning("无法加载SimHei字体，将使用系统默认字体")
                #         font = FontProperties()
                    
                #     # 创建图形
                #     plt.figure(figsize=(10, 6))
                    
                #     # 绘制散点图（原始数据点）
                #     plt.scatter(x_valid, y_valid, color='blue', alpha=0.6, label='实际数据')
                    
                #     # 生成平滑曲线的x值
                #     x_smooth = np.linspace(min(x_valid), max(x_valid), 100)
                    
                #     # 计算拟合曲线
                #     y_smooth = fit_function(x_smooth, a, b)
                    
                #     # 绘制拟合曲线
                #     plt.plot(x_smooth, y_smooth, color='red', linewidth=2, label=f'拟合曲线: y = {a:.4f} * x^{b:.4f}')
                    
                #     # 添加标题和标签
                #     plt.title('幂函数拟合模型', fontproperties=font)
                #     plt.xlabel('特征值', fontproperties=font)
                #     plt.ylabel('目标值', fontproperties=font)
                    
                #     # 添加图例
                #     plt.legend(prop=font)
                #     plt.grid(True, linestyle='--', alpha=0.7)
                    
                #     # 保存图片
                #     os.makedirs('output/model_plots', exist_ok=True)
                #     import time
                #     plot_path = f'output/model_plots/power_model_fit_{time.strftime("%Y%m%d_%H%M%S")}.png'
                #     plt.savefig(plot_path, dpi=300, bbox_inches='tight')
                #     plt.close()
                    
                #     logger.info(f"模型拟合图已保存至: {plot_path}")
                # except Exception as e:
                #     logger.error(f"绘制模型图片失败: {e}", exc_info=True)
            
            # 计算参数估计的标准误差
            perr = np.sqrt(np.diag(pcov))
            logger.info(f"拟合参数: a={a}±{perr[0]}, b={b}±{perr[1]}")
            
            # 计算预测值
            y_pred = fit_function(x_valid, a, b)
            
            # 计算评价指标
            # 在调用pearsonr之前添加检查
            if len(set(y_valid)) > 1 and len(set(y_pred)) > 1:
                corr_coef, _ = pearsonr(y_valid, y_pred)
            else:
                # 当输入为常量时的处理
                logger.error(f"无法计算相关系数：输入数组是常量，导致相关系数为NaN，手动设置为0.1")
                corr_coef = 0.1  # 设置为一个不为0的数
            rmse = np.sqrt(np.mean((y_pred - y_valid) ** 2))
            ss_res = np.sum((y_valid - y_pred) ** 2)
            ss_tot = np.sum((y_valid - np.mean(y_valid)) ** 2)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
            
            # 记录拟合质量
            logger.info(f"拟合质量: 相关系数={corr_coef:.4f}, RMSE={rmse:.4f}, R²={r_squared:.4f}")
            
            return a, b, corr_coef, rmse, r_squared
        except Exception as e:
            logger.error(f"拟合失败: {e}", exc_info=True)
            return None
    
    def select_top_features(self, features: pd.DataFrame, target: pd.Series, top_n: int | str = 'all') -> List[str]:
        """
        根据重要性选择前N个特征
        
        Args:
            features: 特征数据
            target: 目标变量
            top_n: 选择的特征数量
            
        Returns:
            List[str]: 选择的特征名列表
        """
        try:
            # 计算特征重要性
            importance = self.get_feature_importance(features, target)
            
            if not importance:
                return []
                
            # 按重要性排序
            sorted_features = sorted(importance.items(), 
                                key=lambda x: abs(x[1]['corr']), 
                                reverse=True)
            
            if isinstance(top_n, int):
                # 选择前N个特征
                selected = sorted_features[:top_n]
            elif top_n == 'all':
                selected = sorted_features
            else:
                raise ValueError(f"top_n 必须是数字或 'all'")
            
            return selected
        except Exception as e:
            logger.error(f"选择特征时出错: {e}", exc_info=True)
            return []
    