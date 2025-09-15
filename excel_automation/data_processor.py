"""
DataProcessor - Módulo para processamento e limpeza de dados
Fornece funcionalidades para limpar, transformar e processar dados do Excel
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Union, Any
import re
from datetime import datetime


class ExcelDataProcessor:
    """Classe para processamento e limpeza de dados do Excel"""
    
    def __init__(self):
        self.processing_log = []
    
    def clean_data(self, df: pd.DataFrame, 
                   remove_duplicates: bool = True,
                   handle_missing: str = 'drop',
                   standardize_text: bool = True) -> pd.DataFrame:
        """
        Limpa dados do DataFrame
        
        Args:
            df: DataFrame para limpar
            remove_duplicates: Se deve remover duplicatas
            handle_missing: Como tratar valores ausentes ('drop', 'fill', 'keep')
            standardize_text: Se deve padronizar texto
            
        Returns:
            DataFrame limpo
        """
        df_clean = df.copy()
        initial_shape = df_clean.shape
        
        # Remover duplicatas
        if remove_duplicates:
            before_dup = df_clean.shape[0]
            df_clean = df_clean.drop_duplicates()
            removed_dup = before_dup - df_clean.shape[0]
            if removed_dup > 0:
                self._log(f"Removidas {removed_dup} linhas duplicadas")
        
        # Tratar valores ausentes
        if handle_missing == 'drop':
            before_na = df_clean.shape[0]
            df_clean = df_clean.dropna()
            removed_na = before_na - df_clean.shape[0]
            if removed_na > 0:
                self._log(f"Removidas {removed_na} linhas com valores ausentes")
        
        elif handle_missing == 'fill':
            # Preencher valores numéricos com média, texto com 'N/A'
            for column in df_clean.columns:
                if df_clean[column].dtype in ['int64', 'float64']:
                    df_clean[column].fillna(df_clean[column].mean(), inplace=True)
                else:
                    df_clean[column].fillna('N/A', inplace=True)
            self._log("Valores ausentes preenchidos")
        
        # Padronizar texto
        if standardize_text:
            text_columns = df_clean.select_dtypes(include=['object']).columns
            for column in text_columns:
                df_clean[column] = df_clean[column].astype(str).str.strip().str.title()
            self._log(f"Texto padronizado em {len(text_columns)} colunas")
        
        final_shape = df_clean.shape
        self._log(f"Limpeza concluída: {initial_shape} → {final_shape}")
        
        return df_clean
    
    def filter_data(self, df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """
        Filtra dados baseado em critérios
        
        Args:
            df: DataFrame para filtrar
            filters: Dicionário com critérios de filtro
                    Exemplo: {'coluna1': 'valor', 'coluna2': {'min': 10, 'max': 100}}
        
        Returns:
            DataFrame filtrado
        """
        df_filtered = df.copy()
        initial_rows = len(df_filtered)
        
        for column, criteria in filters.items():
            if column not in df_filtered.columns:
                print(f"⚠ Coluna '{column}' não encontrada")
                continue
            
            if isinstance(criteria, dict):
                # Filtro por range numérico
                if 'min' in criteria:
                    df_filtered = df_filtered[df_filtered[column] >= criteria['min']]
                if 'max' in criteria:
                    df_filtered = df_filtered[df_filtered[column] <= criteria['max']]
            
            elif isinstance(criteria, list):
                # Filtro por lista de valores
                df_filtered = df_filtered[df_filtered[column].isin(criteria)]
            
            else:
                # Filtro por valor exato
                df_filtered = df_filtered[df_filtered[column] == criteria]
        
        final_rows = len(df_filtered)
        self._log(f"Filtro aplicado: {initial_rows} → {final_rows} linhas")
        
        return df_filtered
    
    def transform_columns(self, df: pd.DataFrame, 
                         transformations: Dict[str, str]) -> pd.DataFrame:
        """
        Aplica transformações em colunas
        
        Args:
            df: DataFrame para transformar
            transformations: Dicionário com transformações
                           Exemplo: {'coluna1': 'upper', 'coluna2': 'lower', 'coluna3': 'numeric'}
        
        Returns:
            DataFrame com colunas transformadas
        """
        df_transformed = df.copy()
        
        for column, transform_type in transformations.items():
            if column not in df_transformed.columns:
                print(f"⚠ Coluna '{column}' não encontrada")
                continue
            
            try:
                if transform_type == 'upper':
                    df_transformed[column] = df_transformed[column].astype(str).str.upper()
                
                elif transform_type == 'lower':
                    df_transformed[column] = df_transformed[column].astype(str).str.lower()
                
                elif transform_type == 'numeric':
                    # Remover caracteres não numéricos e converter
                    df_transformed[column] = pd.to_numeric(
                        df_transformed[column].astype(str).str.replace(r'[^\d.,]', '', regex=True),
                        errors='coerce'
                    )
                
                elif transform_type == 'date':
                    df_transformed[column] = pd.to_datetime(df_transformed[column], errors='coerce')
                
                elif transform_type == 'remove_spaces':
                    df_transformed[column] = df_transformed[column].astype(str).str.replace(' ', '')
                
                elif transform_type == 'clean_text':
                    # Remove caracteres especiais, mantém apenas letras, números e espaços
                    df_transformed[column] = df_transformed[column].astype(str).str.replace(
                        r'[^a-zA-Z0-9\s]', '', regex=True
                    )
                
                self._log(f"Transformação '{transform_type}' aplicada à coluna '{column}'")
                
            except Exception as e:
                print(f"✗ Erro ao transformar coluna '{column}': {e}")
        
        return df_transformed
    
    def create_calculated_columns(self, df: pd.DataFrame, 
                                 calculations: Dict[str, str]) -> pd.DataFrame:
        """
        Cria colunas calculadas baseadas em outras colunas
        
        Args:
            df: DataFrame base
            calculations: Dicionário com nome da nova coluna e fórmula
                         Exemplo: {'total': 'preco * quantidade', 'margem': '(preco - custo) / preco * 100'}
        
        Returns:
            DataFrame com novas colunas calculadas
        """
        df_calc = df.copy()
        
        for new_column, formula in calculations.items():
            try:
                # Substituir nomes de colunas por referências do DataFrame
                eval_formula = formula
                for col in df_calc.columns:
                    if col in formula:
                        eval_formula = eval_formula.replace(col, f"df_calc['{col}']")
                
                df_calc[new_column] = eval(eval_formula)
                self._log(f"Coluna calculada criada: '{new_column}' = {formula}")
                
            except Exception as e:
                print(f"✗ Erro ao criar coluna calculada '{new_column}': {e}")
        
        return df_calc
    
    def group_and_aggregate(self, df: pd.DataFrame, 
                           group_by: Union[str, List[str]], 
                           aggregations: Dict[str, Union[str, List[str]]]) -> pd.DataFrame:
        """
        Agrupa dados e aplica funções de agregação
        
        Args:
            df: DataFrame para agrupar
            group_by: Coluna(s) para agrupar
            aggregations: Dicionário com colunas e funções de agregação
                         Exemplo: {'vendas': 'sum', 'preco': ['mean', 'max']}
        
        Returns:
            DataFrame agrupado
        """
        try:
            grouped = df.groupby(group_by).agg(aggregations)
            
            # Achatar colunas multi-nível se necessário
            if isinstance(grouped.columns, pd.MultiIndex):
                grouped.columns = ['_'.join(col).strip() for col in grouped.columns.values]
            
            grouped = grouped.reset_index()
            
            self._log(f"Dados agrupados por {group_by} com {len(aggregations)} agregações")
            
            return grouped
            
        except Exception as e:
            print(f"✗ Erro ao agrupar dados: {e}")
            return df
    
    def pivot_data(self, df: pd.DataFrame, 
                   index: Union[str, List[str]], 
                   columns: str, 
                   values: str,
                   aggfunc: str = 'sum') -> pd.DataFrame:
        """
        Cria tabela dinâmica dos dados
        
        Args:
            df: DataFrame fonte
            index: Coluna(s) para índice
            columns: Coluna para colunas da tabela dinâmica
            values: Coluna com valores para agregar
            aggfunc: Função de agregação
        
        Returns:
            DataFrame com tabela dinâmica
        """
        try:
            pivot_table = pd.pivot_table(
                df, 
                index=index, 
                columns=columns, 
                values=values, 
                aggfunc=aggfunc,
                fill_value=0
            )
            
            pivot_table = pivot_table.reset_index()
            
            self._log(f"Tabela dinâmica criada: {index} vs {columns}")
            
            return pivot_table
            
        except Exception as e:
            print(f"✗ Erro ao criar tabela dinâmica: {e}")
            return df
    
    def get_data_quality_report(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Gera relatório de qualidade dos dados
        
        Args:
            df: DataFrame para analisar
        
        Returns:
            Dicionário com métricas de qualidade
        """
        report = {
            'shape': df.shape,
            'memory_usage': df.memory_usage(deep=True).sum(),
            'dtypes': dict(df.dtypes),
            'missing_values': dict(df.isnull().sum()),
            'duplicates': df.duplicated().sum(),
            'numeric_stats': {},
            'text_stats': {}
        }
        
        # Estatísticas para colunas numéricas
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            report['numeric_stats'] = df[numeric_cols].describe().to_dict()
        
        # Estatísticas para colunas de texto
        text_cols = df.select_dtypes(include=['object']).columns
        for col in text_cols:
            report['text_stats'][col] = {
                'unique_values': df[col].nunique(),
                'most_common': df[col].value_counts().head(3).to_dict() if not df[col].empty else {}
            }
        
        return report
    
    def _log(self, message: str):
        """Adiciona mensagem ao log de processamento"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.processing_log.append(log_entry)
        print(f"✓ {message}")
    
    def get_processing_log(self) -> List[str]:
        """Retorna o log de processamento"""
        return self.processing_log.copy()
    
    def clear_log(self):
        """Limpa o log de processamento"""
        self.processing_log.clear()