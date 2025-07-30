"""
配置管理模块，提供特征配置文件的加载和访问功能
"""

import json
import os
import logging
from typing import Dict, List, Any, Optional

# 获取模块日志记录器
logger = logging.getLogger(__name__)

class ConfigManager:
    """配置管理器，处理特征配置文件加载和访问"""
    
    # 默认支持的数据类型
    DATA_TYPES = ["warning_device", "shore_data", "smart_water", "aerospot"]
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化配置管理器
        
        Args:
            config_path: 特征配置文件路径，如果为None，则使用默认路径
        """
        if config_path is None:
            # 使用默认配置文件路径
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                'config', 
                'features_config.json'
            )
            logger.info(f"使用默认配置文件: {config_path} (存在: {os.path.exists(config_path)})")
            
        self.config_path = config_path
        self.config = self._load_config(config_path)
    
    def _load_config(self, config_path: str) -> Dict:
        """
        加载特征配置文件
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            Dict: 加载的配置对象
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 验证配置文件格式
            if not all(data_type in config for data_type in self.DATA_TYPES):
                missing = [dt for dt in self.DATA_TYPES if dt not in config]
                logger.warning(f"配置文件中缺少以下数据类型: {missing}")
                # 为缺失类型创建空配置
                for dt in missing:
                    config[dt] = {}
                    
            logger.info(f"成功加载配置文件: {config_path}")
            return config
        except Exception as e:
            logger.error(f"加载特征配置文件失败: {e}", exc_info=True)
            # 返回空配置
            return {data_type: {} for data_type in self.DATA_TYPES}
    
    def get_feature_definitions(self, data_type: str, metric_name: str) -> List[Dict]:
        """
        获取指定数据类型和指标的特征定义
        
        Args:
            data_type: 数据类型，必须是DATA_TYPES中的一种
            metric_name: 指标名称
            
        Returns:
            List[Dict]: 特征定义列表
        """
        if data_type not in self.DATA_TYPES:
            logger.warning(f"不支持的数据类型: {data_type}")
            return []
            
        # 尝试获取数据类型下的指标特征
        if data_type in self.config and metric_name in self.config[data_type]:
            features = self.config[data_type][metric_name].get("features", [])
            logger.debug(f"找到 {data_type} 下 {metric_name} 指标的 {len(features)} 个特征定义")
        elif data_type in self.config and "default" in self.config[data_type]:
            features = self.config[data_type]["default"].get("features", [])
            logger.debug(f"{data_type} 下 {metric_name} 指标采用默认的 {len(features)} 个特征")
        else:
            logger.warning(f"未找到 {data_type} 下 {metric_name} 指标的特征定义")
            return []
        
        # 获取完整的特征定义
        full_definitions = []
        for ref in features:
            if "feature_id" not in ref:
                logger.warning(f"特征引用缺少feature_id: {ref}")
                continue
                
            feature_id = ref["feature_id"]
            
            # 获取基础特征定义
            if "features" in self.config and feature_id in self.config["features"]:
                base_definition = self.config["features"][feature_id].copy()
                
                # 如果有自定义波段映射，则合并
                if "bands" in ref:
                    base_definition["bands"] = ref["bands"]
                    
                full_definitions.append(base_definition)
            else:
                logger.warning(f"未找到特征ID为 {feature_id} 的定义")
        
        return full_definitions

    def get_model_params(self, data_type: Optional[str] = None, metric_name: Optional[str] = None) -> Dict:
        """
        获取模型参数，根据优先级依次尝试：指标级别 > 数据类型级别 > 全局级别
        
        Args:
            data_type: 数据类型，如果为None则只返回全局参数
            metric_name: 指标名称，如果为None则返回数据类型级别的参数
            
        Returns:
            Dict: 合并后的模型参数
        """
        model_params = {}
        
        # 1. 获取全局模型参数（最低优先级）
        global_params = self.config.get("model_params", {})
        model_params.update(global_params)
        
        # 2. 获取数据类型级别的模型参数（中等优先级）
        if data_type and data_type in self.config:
            data_type_params = self.config[data_type].get("model_params", {})
            if data_type_params:
                model_params.update(data_type_params)
        
        # 3. 获取指标级别的模型参数（最高优先级）
        if data_type and metric_name and data_type in self.config and metric_name in self.config[data_type]:
            metric_params = self.config[data_type][metric_name].get("model_params", {})
            if metric_params:
                model_params.update(metric_params)
        
        return model_params
    
    def get_supported_metrics(self, data_type: str) -> List[str]:
        """
        获取指定数据类型支持的指标列表
        
        Args:
            data_type: 数据类型
            
        Returns:
            List[str]: 支持的指标列表
        """
        if data_type not in self.DATA_TYPES:
            logger.warning(f"不支持的数据类型: {data_type}")
            return []
            
        if data_type in self.config:
            # 过滤掉model_params键，它不是指标
            metrics = [key for key in self.config[data_type].keys() if key != "model_params"]
            return metrics
        
        return [] 