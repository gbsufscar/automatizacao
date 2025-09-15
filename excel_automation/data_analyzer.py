"""
DataAnalyzer - Módulo para análise estatística de dados
Fornece funcionalidades para análise descritiva, correlações e insights
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class DataAnalyzer:
    """Classe para análise estatística de dados"""
    
    def __init__(self):
        self.analysis_results = {}
    
    def descriptive_analysis(self, df: pd.DataFrame, 
                           columns: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Realiza análise descritiva dos dados
        
        Args:
            df: DataFrame para analisar
            columns: Colunas específicas para analisar (None para todas)
        
        Returns:
            Dicionário com estatísticas descritivas
        """
        if columns is None:
            columns = df.columns.tolist()
        
        analysis = {
            'shape': df.shape,
            'columns_info': {},
            'numeric_summary': {},
            'categorical_summary': {},
            'missing_data': {},
            'data_types': dict(df.dtypes)
        }
        
        # Análise de valores ausentes
        missing_data = df[columns].isnull().sum()
        missing_pct = (missing_data / len(df)) * 100
        analysis['missing_data'] = {
            'count': dict(missing_data),
            'percentage': dict(missing_pct)
        }
        
        # Análise de colunas numéricas
        numeric_cols = df[columns].select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            stats = df[numeric_cols].describe()
            analysis['numeric_summary'] = stats.to_dict()
            
            # Adicionar estatísticas extras
            for col in numeric_cols:
                col_data = df[col].dropna()
                if len(col_data) > 0:
                    analysis['numeric_summary'][col].update({
                        'variance': col_data.var(),
                        'skewness': col_data.skew(),
                        'kurtosis': col_data.kurtosis(),
                        'range': col_data.max() - col_data.min(),
                        'iqr': col_data.quantile(0.75) - col_data.quantile(0.25)
                    })
        
        # Análise de colunas categóricas
        categorical_cols = df[columns].select_dtypes(include=['object', 'category']).columns
        for col in categorical_cols:
            col_data = df[col].dropna()
            if len(col_data) > 0:
                value_counts = col_data.value_counts()
                analysis['categorical_summary'][col] = {
                    'unique_count': col_data.nunique(),
                    'most_frequent': value_counts.index[0] if len(value_counts) > 0 else None,
                    'most_frequent_count': value_counts.iloc[0] if len(value_counts) > 0 else 0,
                    'top_5_values': dict(value_counts.head(5)),
                    'entropy': self._calculate_entropy(value_counts)
                }
        
        # Informações gerais das colunas
        for col in columns:
            analysis['columns_info'][col] = {
                'dtype': str(df[col].dtype),
                'non_null_count': df[col].count(),
                'null_count': df[col].isnull().sum(),
                'unique_count': df[col].nunique(),
                'memory_usage': df[col].memory_usage(deep=True)
            }
        
        self.analysis_results['descriptive'] = analysis
        print(f"✓ Análise descritiva concluída para {len(columns)} colunas")
        
        return analysis
    
    def correlation_analysis(self, df: pd.DataFrame, 
                           method: str = 'pearson',
                           min_correlation: float = 0.5) -> Dict[str, Any]:
        """
        Analisa correlações entre variáveis numéricas
        
        Args:
            df: DataFrame para analisar
            method: Método de correlação ('pearson', 'spearman', 'kendall')
            min_correlation: Correlação mínima para destacar
        
        Returns:
            Dicionário com matriz de correlação e insights
        """
        numeric_df = df.select_dtypes(include=[np.number])
        
        if numeric_df.empty:
            print("⚠ Nenhuma coluna numérica encontrada para análise de correlação")
            return {}
        
        # Calcular matriz de correlação
        corr_matrix = numeric_df.corr(method=method)
        
        # Encontrar correlações altas
        high_correlations = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) >= min_correlation:
                    high_correlations.append({
                        'var1': corr_matrix.columns[i],
                        'var2': corr_matrix.columns[j],
                        'correlation': corr_value,
                        'strength': self._correlation_strength(abs(corr_value))
                    })
        
        # Ordenar por correlação absoluta
        high_correlations.sort(key=lambda x: abs(x['correlation']), reverse=True)
        
        analysis = {
            'correlation_matrix': corr_matrix.to_dict(),
            'high_correlations': high_correlations,
            'method': method,
            'variables_analyzed': list(numeric_df.columns),
            'summary': {
                'total_variables': len(numeric_df.columns),
                'high_correlations_count': len(high_correlations),
                'max_correlation': max([abs(x['correlation']) for x in high_correlations]) if high_correlations else 0
            }
        }
        
        self.analysis_results['correlation'] = analysis
        print(f"✓ Análise de correlação concluída: {len(high_correlations)} correlações altas encontradas")
        
        return analysis
    
    def outlier_detection(self, df: pd.DataFrame, 
                         method: str = 'iqr',
                         columns: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Detecta outliers nos dados
        
        Args:
            df: DataFrame para analisar
            method: Método de detecção ('iqr', 'zscore', 'modified_zscore')
            columns: Colunas específicas para analisar
        
        Returns:
            Dicionário com outliers detectados
        """
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        outliers_info = {}
        
        for col in columns:
            if col not in df.columns or df[col].dtype not in [np.number]:
                continue
            
            col_data = df[col].dropna()
            
            if method == 'iqr':
                outliers = self._detect_outliers_iqr(col_data)
            elif method == 'zscore':
                outliers = self._detect_outliers_zscore(col_data)
            elif method == 'modified_zscore':
                outliers = self._detect_outliers_modified_zscore(col_data)
            else:
                print(f"⚠ Método '{method}' não reconhecido")
                continue
            
            outlier_indices = col_data[outliers].index.tolist()
            outlier_values = col_data[outliers].values.tolist()
            
            outliers_info[col] = {
                'count': len(outlier_indices),
                'percentage': (len(outlier_indices) / len(col_data)) * 100,
                'indices': outlier_indices,
                'values': outlier_values,
                'min_outlier': min(outlier_values) if outlier_values else None,
                'max_outlier': max(outlier_values) if outlier_values else None
            }
        
        analysis = {
            'method': method,
            'outliers_by_column': outliers_info,
            'summary': {
                'columns_analyzed': len(outliers_info),
                'total_outliers': sum(info['count'] for info in outliers_info.values()),
                'columns_with_outliers': len([col for col, info in outliers_info.items() if info['count'] > 0])
            }
        }
        
        self.analysis_results['outliers'] = analysis
        print(f"✓ Detecção de outliers concluída: {analysis['summary']['total_outliers']} outliers encontrados")
        
        return analysis
    
    def trend_analysis(self, df: pd.DataFrame, 
                      date_column: str, 
                      value_columns: List[str],
                      period: str = 'M') -> Dict[str, Any]:
        """
        Analisa tendências temporais nos dados
        
        Args:
            df: DataFrame com dados temporais
            date_column: Nome da coluna de data
            value_columns: Colunas com valores para análise
            period: Período de agrupamento ('D', 'W', 'M', 'Q', 'Y')
        
        Returns:
            Dicionário com análise de tendências
        """
        if date_column not in df.columns:
            print(f"⚠ Coluna de data '{date_column}' não encontrada")
            return {}
        
        df_temp = df.copy()
        df_temp[date_column] = pd.to_datetime(df_temp[date_column])
        df_temp = df_temp.set_index(date_column)
        
        trends = {}
        
        for col in value_columns:
            if col not in df.columns:
                continue
            
            # Agrupar por período
            grouped = df_temp[col].resample(period).agg(['sum', 'mean', 'count'])
            
            # Calcular tendência (regressão linear simples)
            x = np.arange(len(grouped))
            y = grouped['sum'].values
            
            if len(x) > 1 and not np.isnan(y).all():
                slope = np.polyfit(x, y, 1)[0]
                trend_direction = 'crescente' if slope > 0 else 'decrescente' if slope < 0 else 'estável'
            else:
                slope = 0
                trend_direction = 'indefinido'
            
            trends[col] = {
                'trend_direction': trend_direction,
                'slope': slope,
                'periods': len(grouped),
                'data_by_period': {
                    'dates': grouped.index.strftime('%Y-%m-%d').tolist(),
                    'sum': grouped['sum'].tolist(),
                    'mean': grouped['mean'].tolist(),
                    'count': grouped['count'].tolist()
                },
                'statistics': {
                    'total': grouped['sum'].sum(),
                    'average_per_period': grouped['sum'].mean(),
                    'max_period': grouped['sum'].max(),
                    'min_period': grouped['sum'].min(),
                    'volatility': grouped['sum'].std()
                }
            }
        
        analysis = {
            'period': period,
            'date_column': date_column,
            'trends_by_column': trends,
            'date_range': {
                'start': df_temp.index.min().strftime('%Y-%m-%d'),
                'end': df_temp.index.max().strftime('%Y-%m-%d'),
                'total_days': (df_temp.index.max() - df_temp.index.min()).days
            }
        }
        
        self.analysis_results['trends'] = analysis
        print(f"✓ Análise de tendências concluída para {len(value_columns)} variáveis")
        
        return analysis
    
    def generate_insights(self, df: pd.DataFrame) -> List[str]:
        """
        Gera insights automáticos baseados nas análises realizadas
        
        Args:
            df: DataFrame analisado
        
        Returns:
            Lista de insights textuais
        """
        insights = []
        
        # Insights de dados gerais
        insights.append(f"📊 Dataset contém {df.shape[0]:,} linhas e {df.shape[1]} colunas")
        
        # Insights de qualidade de dados
        missing_pct = (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100
        if missing_pct > 10:
            insights.append(f"⚠️ Alto percentual de dados ausentes: {missing_pct:.1f}%")
        elif missing_pct > 0:
            insights.append(f"ℹ️ Percentual de dados ausentes: {missing_pct:.1f}%")
        
        # Insights de correlações
        if 'correlation' in self.analysis_results:
            corr_analysis = self.analysis_results['correlation']
            if corr_analysis['high_correlations']:
                top_corr = corr_analysis['high_correlations'][0]
                insights.append(
                    f"🔗 Maior correlação: {top_corr['var1']} e {top_corr['var2']} "
                    f"({top_corr['correlation']:.2f} - {top_corr['strength']})"
                )
        
        # Insights de outliers
        if 'outliers' in self.analysis_results:
            outlier_analysis = self.analysis_results['outliers']
            total_outliers = outlier_analysis['summary']['total_outliers']
            if total_outliers > 0:
                outlier_pct = (total_outliers / df.shape[0]) * 100
                insights.append(f"🎯 {total_outliers} outliers detectados ({outlier_pct:.1f}% dos dados)")
        
        # Insights de variáveis categóricas
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        if len(categorical_cols) > 0:
            insights.append(f"📝 {len(categorical_cols)} variáveis categóricas identificadas")
        
        # Insights de variáveis numéricas
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            insights.append(f"🔢 {len(numeric_cols)} variáveis numéricas identificadas")
        
        # Insights de tendências temporais
        if 'trends' in self.analysis_results:
            trends = self.analysis_results['trends']['trends_by_column']
            growing_trends = [col for col, data in trends.items() if data['trend_direction'] == 'crescente']
            if growing_trends:
                insights.append(f"📈 Tendência crescente detectada em: {', '.join(growing_trends)}")
        
        print(f"✓ {len(insights)} insights gerados")
        return insights
    
    def _calculate_entropy(self, value_counts: pd.Series) -> float:
        """Calcula entropia de uma série de contagem de valores"""
        probabilities = value_counts / value_counts.sum()
        return -np.sum(probabilities * np.log2(probabilities + 1e-10))
    
    def _correlation_strength(self, correlation: float) -> str:
        """Classifica a força da correlação"""
        abs_corr = abs(correlation)
        if abs_corr >= 0.9:
            return "muito forte"
        elif abs_corr >= 0.7:
            return "forte"
        elif abs_corr >= 0.5:
            return "moderada"
        elif abs_corr >= 0.3:
            return "fraca"
        else:
            return "muito fraca"
    
    def _detect_outliers_iqr(self, data: pd.Series) -> pd.Series:
        """Detecta outliers usando método IQR"""
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        return (data < lower_bound) | (data > upper_bound)
    
    def _detect_outliers_zscore(self, data: pd.Series, threshold: float = 3) -> pd.Series:
        """Detecta outliers usando Z-score"""
        z_scores = np.abs((data - data.mean()) / data.std())
        return z_scores > threshold
    
    def _detect_outliers_modified_zscore(self, data: pd.Series, threshold: float = 3.5) -> pd.Series:
        """Detecta outliers usando Z-score modificado (baseado na mediana)"""
        median = data.median()
        mad = np.median(np.abs(data - median))
        modified_z_scores = 0.6745 * (data - median) / mad
        return np.abs(modified_z_scores) > threshold