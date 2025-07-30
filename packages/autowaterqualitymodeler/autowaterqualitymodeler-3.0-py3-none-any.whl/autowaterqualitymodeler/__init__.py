"""
AutoWaterQualityModeler - 自动水质光谱建模工具

提供了一键式水质建模、预测和评估功能。
"""

from ._version import __version__

# 导出主要类
from .core.modeler import AutoWaterQualityModeler
from .preprocessing.spectrum_processor import SpectrumProcessor
from .features.calculator import FeatureCalculator
from .models.builder import ModelBuilder

__all__ = [
    'AutoWaterQualityModeler',
    'SpectrumProcessor',
    'FeatureCalculator',
    'ModelBuilder',
    '__version__'
] 