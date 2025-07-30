"""
模型构建模块，提供模型拟合和评估功能
"""

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import logging
from typing import Dict, List, Tuple, Optional, Any, Union, Callable

# 获取模块日志记录器
logger = logging.getLogger(__name__)

class ModelBuilder:
    """模型构建器，处理模型拟合和评估"""
    
    def __init__(self):
        """初始化模型构建器"""
        self.logger = logger
    
    def _fit_power_model(self, x: np.ndarray, y: np.ndarray) -> Dict:
        """
        拟合幂函数模型 y = a * x^b
        
        Args:
            x: 特征数据
            y: 目标变量
            
        Returns:
            Dict: 模型结果字典
        """
        try:
            # 检查数据有效性
            if np.any(x <= 0) or np.any(y <= 0):
                self.logger.warning("幂函数模型要求输入数据为正值，检测到非正值")
                # 过滤非正值
                valid_mask = (x > 0) & (y > 0)
                if np.sum(valid_mask) < 3:
                    self.logger.warning("过滤非正值后，数据点少于3个，无法拟合幂函数模型")
                    return {}
                x = x[valid_mask]
                y = y[valid_mask]
            
            # 定义幂函数模型
            def power_func(x, a, b):
                return a * np.power(x, b)
            
            # 初始猜测值
            initial_guess = [1.0, 1.0]
            
            # 拟合模型
            try:
                params, cov = curve_fit(power_func, x, y, p0=initial_guess)
                a, b = params
                
                # 计算预测值
                y_pred = power_func(x, a, b)
                
                # 计算评估指标
                r2 = r2_score(y, y_pred)
                rmse = np.sqrt(mean_squared_error(y, y_pred))
                
                return {
                    'type': 'power',
                    'params': {'a': a, 'b': b},
                    'metrics': {'r2': r2, 'rmse': rmse},
                    'formula': f"y = {a:.6f} * x^{b:.6f}"
                }
                
            except Exception as e:
                self.logger.warning(f"幂函数拟合失败: {e}，尝试线性模型")
                # 如果幂函数拟合失败，尝试线性模型
                return self._fit_linear_model(x, y)
                
        except Exception as e:
            self.logger.error(f"幂函数模型拟合失败: {e}", exc_info=True)
            return {}
    
    def _fit_linear_model(self, x: np.ndarray, y: np.ndarray) -> Dict:
        """
        拟合线性模型 y = a * x + b
        
        Args:
            x: 特征数据
            y: 目标变量
            
        Returns:
            Dict: 模型结果字典
        """
        try:
            # 重塑特征数据
            X = x.reshape(-1, 1)
            
            # 拟合线性模型
            model = LinearRegression()
            model.fit(X, y)
            
            # 获取参数
            a = model.coef_[0]
            b = model.intercept_
            
            # 计算预测值
            y_pred = model.predict(X)
            
            # 计算评估指标
            r2 = r2_score(y, y_pred)
            rmse = np.sqrt(mean_squared_error(y, y_pred))
            
            return {
                'type': 'linear',
                'params': {'a': a, 'b': b},
                'metrics': {'r2': r2, 'rmse': rmse},
                'formula': f"y = {a:.6f} * x + {b:.6f}"
            }
            
        except Exception as e:
            self.logger.error(f"线性模型拟合失败: {e}", exc_info=True)
            return {}
    
    def tune_linear(self, predicted: pd.Series, measured: pd.Series) -> float | None:
        """
        通过线性回归微调模型
        
        Args:
            predicted: 预测值
            measured: 实测值
            
        Returns:
            Dict: 调整后的模型参数
        """
        try:
            # 去除缺失值
            valid_data = pd.concat([predicted, measured], axis=1).dropna()
            
            if len(valid_data) < 2:
                self.logger.warning("有效数据点少于2个，无法进行线性调整")
                return None
            
            x = valid_data.iloc[:, 0].values.reshape(-1, 1)  # 预测值
            y = valid_data.iloc[:, 1].values  # 实测值
            
            # 拟合线性模型（强制通过原点）
            model = LinearRegression(fit_intercept=False)
            model.fit(x, y)
            
            # 获取系数
            a = model.coef_[0]
            
            # 计算预测值
            y_pred = model.predict(x)
            
            # 计算评估指标
            r2 = r2_score(y, y_pred)
            rmse = np.sqrt(mean_squared_error(y, y_pred))
            
            # 记录拟合结果到日志
            logger.info(f"指标 {measured.name} 拟合完成: 系数 = {a:.4f}, "f"R² = {r2:.4f}, RMSE = {rmse:.4f}, 样本数 = {len(valid_data)}")
            return a
            
        except Exception as e:
            self.logger.error(f"线性调整失败: {e}", exc_info=True)
            return None
    