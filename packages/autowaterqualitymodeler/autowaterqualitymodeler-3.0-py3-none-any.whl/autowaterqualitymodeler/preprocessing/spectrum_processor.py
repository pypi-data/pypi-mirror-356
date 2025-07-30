"""
光谱数据预处理模块，提供数据清洗、重采样和平滑功能
"""

import pandas as pd
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.signal import savgol_filter
import logging
from typing import Tuple, List, Optional, Dict, Any

# 获取模块日志记录器
logger = logging.getLogger(__name__)

class SpectrumProcessor:
    """光谱数据预处理器，提供一系列预处理方法"""
    
    def __init__(self, min_wavelength: int = 400, max_wavelength: int = 900,
                 smooth_window: int = 11, smooth_order: int = 3):
        """
        初始化光谱处理器
        
        Args:
            min_wavelength: 最小波长
            max_wavelength: 最大波长
            smooth_window: 平滑窗口大小
            smooth_order: 平滑多项式阶数
        """
        self.min_wavelength = min_wavelength
        self.max_wavelength = max_wavelength
        self.smooth_window = smooth_window
        self.smooth_order = smooth_order
    
    def preprocess(self, spectrum_data: pd.DataFrame) -> pd.DataFrame:
        """
        预处理光谱数据
        
        Args:
            spectrum_data: 光谱数据DataFrame，列名为波长，每行是一条光谱样本
            
        Returns:
            pd.DataFrame: 预处理后的光谱数据
        """
        try:
            logger.info("开始预处理光谱数据...")
            
            # 1. 过滤波长范围
            filtered_data = self._filter_wavelength(spectrum_data)
            
            # 2. 过滤异常值
            filtered_data = self._filter_anomalies(filtered_data)
            
            # 3. 重采样光谱
            resampled_data = self._resample_spectrum(filtered_data)
            
            # 4. 平滑光谱
            smoothed_data = self._smooth_spectrum(resampled_data)
            
            logger.info(f"光谱预处理完成，处理前形状: {spectrum_data.shape}，处理后形状: {smoothed_data.shape}")
            return smoothed_data
            
        except Exception as e:
            logger.error(f"光谱预处理失败: {e}", exc_info=True)
            # 返回原始数据
            return spectrum_data
    
    def _filter_wavelength(self, spectrum_data: pd.DataFrame) -> pd.DataFrame:
        """
        过滤指定波长范围的数据
        
        Args:
            spectrum_data: 光谱数据DataFrame
            
        Returns:
            pd.DataFrame: 过滤后的光谱数据
        """
        try:
            # 将列名转换为float类型
            spectrum_data.columns = spectrum_data.columns.astype(float)
            
            # 过滤波长范围
            cols = [col for col in spectrum_data.columns 
                    if self.min_wavelength <= col <= self.max_wavelength]
            
            if not cols:
                logger.warning(f"在范围 {self.min_wavelength}-{self.max_wavelength} nm 内没有有效波长")
                return spectrum_data
            
            filtered_data = spectrum_data[cols]
            logger.debug(f"波长过滤完成，从 {len(spectrum_data.columns)} 个波长减少到 {len(filtered_data.columns)} 个波长")
            
            return filtered_data
            
        except Exception as e:
            logger.error(f"波长过滤失败: {e}", exc_info=True)
            return spectrum_data
    
    def _filter_anomalies(self, spectrum_data: pd.DataFrame, threshold: float = 0.1) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        过滤光谱中的异常值，检测并替换小于0或大于1的值
        
        Args:
            spectrum_data: 光谱数据DataFrame
            threshold: 阈值百分比，当一行中异常值比例超过该阈值时，整行被标记为异常
            
        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: 
                - 处理后的光谱数据
                - 异常掩码
        """
        try:
            # 创建数据副本
            processed_data = spectrum_data.copy()
            
            # 检测异常值（一次性操作）
            anomalies = (processed_data < 0) | (processed_data > 1)
            
            # 计算每行的异常值比例
            anomaly_ratio = anomalies.sum(axis=1) / anomalies.shape[1]
            
            # 识别异常行
            bad_rows = anomaly_ratio > threshold
            
            # 只在有异常行时记录日志，减少不必要的日志输出
            bad_rows_count = bad_rows.sum()
            if bad_rows_count > 0:
                logger.warning(f"检测到 {bad_rows_count} 行数据中超过 {threshold * 100}% 的值为异常值")
            
            # 创建异常掩码DataFrame用于返回
            # anomaly_mask = pd.DataFrame(anomalies, index=spectrum_data.index, columns=spectrum_data.columns)
            
            # 将异常值替换为NaN并处理无穷值
            processed_data[anomalies] = np.nan
            processed_data.replace([np.inf, -np.inf], np.nan, inplace=True)
            
            # 使用前向和后向填充处理NaN值
            processed_data = processed_data.ffill(axis=1).bfill(axis=1)
            
            return processed_data
            
        except Exception as e:
            logger.error(f"异常值过滤失败: {e}", exc_info=True)
            return spectrum_data
    
    def _resample_spectrum(self, spectrum_data: pd.DataFrame) -> pd.DataFrame:
        """
        使用三次样条插值对光谱进行重采样，将波长重采样为整数值
        
        Args:
            spectrum_data: 光谱数据DataFrame
            
        Returns:
            pd.DataFrame: 重采样后的光谱数据
        """
        try:
            from scipy.interpolate import CubicSpline
            
            # 原始波长
            wavelengths = spectrum_data.columns.values.astype(float)
            data = spectrum_data.values
            
            # 定义目标波长（整数）
            target_wavelengths = np.arange(
                int(np.ceil(self.min_wavelength)),
                int(np.floor(self.max_wavelength)) + 1,
                1
            )
            
            # 初始化重采样数据
            resampled_data = np.zeros((data.shape[0], len(target_wavelengths)))
            
            # 对每条光谱进行重采样
            for i in range(data.shape[0]):
                try:
                    # 使用三次样条插值
                    cs = CubicSpline(wavelengths, data[i, :], bc_type="not-a-knot")
                    resampled_data[i, :] = cs(target_wavelengths)
                except Exception as e:
                    # 样本插值失败时，使用线性插值作为备选
                    logger.warning(f"样本 {i} 三次样条插值失败，使用线性插值: {e}")
                    resampled = np.interp(target_wavelengths, wavelengths, data[i, :])
                    resampled_data[i, :] = resampled
            
            # 创建重采样后的DataFrame - 修改这部分以避免碎片化
            resampled_df = pd.DataFrame(
                resampled_data,
                index=spectrum_data.index,
                columns=target_wavelengths
            ).copy()  # 添加.copy()以避免碎片化
            
            logger.debug(f"光谱重采样完成，重采样前波长数: {len(wavelengths)}，重采样后波长数: {len(target_wavelengths)}")
            return resampled_df
            
        except Exception as e:
            logger.error(f"光谱重采样失败: {e}", exc_info=True)
            return spectrum_data
    
    def _smooth_spectrum(self, spectrum_data: pd.DataFrame) -> pd.DataFrame:
        """使用Savitzky-Golay滤波器平滑光谱"""
        from scipy.signal import savgol_filter
        
        data = spectrum_data.values
        
        # 确保窗口长度为奇数
        window_length = self.smooth_window
        if window_length % 2 == 0:
            window_length += 1
        
        # 确保窗口长度小于数据点数
        if window_length >= data.shape[1]:
            window_length = min(data.shape[1] - 1, 11)
            if window_length % 2 == 0:
                window_length -= 1
                
        # 确保多项式阶数小于窗口长度
        polyorder = min(self.smooth_order, window_length - 1)
        
        # 应用Savitzky-Golay滤波器
        try:
            smoothed_data = savgol_filter(data, window_length, polyorder, axis=1)
            
            # 保留窗口两端的原始数据
            half_window = window_length // 2
            smoothed_data[:, :half_window] = data[:, :half_window]
            smoothed_data[:, -half_window:] = data[:, -half_window:]
            
            return pd.DataFrame(smoothed_data, index=spectrum_data.index, columns=spectrum_data.columns)
        except Exception as e:
            logger.warning(f"平滑处理失败，返回原始数据: {e}", exc_info=True)
            return spectrum_data