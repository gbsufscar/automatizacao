"""
Excel Automation Package
Automação de tratamento de dados do Excel usando Python
"""

from .data_processor import ExcelDataProcessor
from .data_analyzer import DataAnalyzer
from .data_visualizer import DataVisualizer
from .excel_handler import ExcelHandler

__version__ = "1.0.0"
__author__ = "Automação Team"

__all__ = [
    "ExcelDataProcessor",
    "DataAnalyzer", 
    "DataVisualizer",
    "ExcelHandler"
]