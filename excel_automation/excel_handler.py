"""
ExcelHandler - Módulo para manipulação de arquivos Excel
Fornece funcionalidades básicas para ler, escrever e manipular arquivos Excel
"""

import pandas as pd
from typing import Dict, List, Optional, Union
import os
from pathlib import Path


class ExcelHandler:
    """Classe para manipular arquivos Excel"""
    
    def __init__(self):
        self.supported_formats = ['.xlsx', '.xls', '.xlsm']
    
    def read_excel(self, 
                   file_path: str, 
                   sheet_name: Optional[Union[str, int]] = None,
                   header: Optional[int] = 0,
                   usecols: Optional[Union[str, List]] = None) -> pd.DataFrame:
        """
        Lê um arquivo Excel e retorna um DataFrame
        
        Args:
            file_path: Caminho para o arquivo Excel
            sheet_name: Nome ou índice da planilha (None para a primeira)
            header: Linha que contém os cabeçalhos (None se não houver)
            usecols: Colunas específicas para ler
            
        Returns:
            DataFrame com os dados do Excel
        """
        try:
            if not self._validate_file(file_path):
                raise ValueError(f"Arquivo não encontrado ou formato inválido: {file_path}")
            
            df = pd.read_excel(
                file_path,
                sheet_name=sheet_name,
                header=header,
                usecols=usecols,
                engine='openpyxl'
            )
            
            # Se sheet_name é None e retornou dict, pegar a primeira planilha
            if isinstance(df, dict):
                first_sheet = list(df.keys())[0]
                df = df[first_sheet]
                print(f"✓ Arquivo lido com sucesso: {file_path} (planilha: {first_sheet})")
            else:
                print(f"✓ Arquivo lido com sucesso: {file_path}")
            
            print(f"  Dimensões: {df.shape[0]} linhas x {df.shape[1]} colunas")
            
            return df
            
        except Exception as e:
            print(f"✗ Erro ao ler arquivo Excel: {e}")
            raise
    
    def read_multiple_sheets(self, file_path: str) -> Dict[str, pd.DataFrame]:
        """
        Lê todas as planilhas de um arquivo Excel
        
        Args:
            file_path: Caminho para o arquivo Excel
            
        Returns:
            Dicionário com nome das planilhas como chaves e DataFrames como valores
        """
        try:
            if not self._validate_file(file_path):
                raise ValueError(f"Arquivo não encontrado ou formato inválido: {file_path}")
            
            sheets_dict = pd.read_excel(file_path, sheet_name=None, engine='openpyxl')
            
            print(f"✓ Múltiplas planilhas lidas de: {file_path}")
            for sheet_name, df in sheets_dict.items():
                print(f"  {sheet_name}: {df.shape[0]} linhas x {df.shape[1]} colunas")
            
            return sheets_dict
            
        except Exception as e:
            print(f"✗ Erro ao ler múltiplas planilhas: {e}")
            raise
    
    def write_excel(self, 
                    data: Union[pd.DataFrame, Dict[str, pd.DataFrame]], 
                    file_path: str,
                    index: bool = False,
                    sheet_name: str = 'Sheet1') -> bool:
        """
        Escreve dados em um arquivo Excel
        
        Args:
            data: DataFrame ou dicionário de DataFrames para escrever
            file_path: Caminho onde salvar o arquivo
            index: Se deve incluir o índice do DataFrame
            sheet_name: Nome da planilha (usado apenas para DataFrame único)
            
        Returns:
            True se bem-sucedido, False caso contrário
        """
        try:
            # Criar diretório se não existir
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                if isinstance(data, pd.DataFrame):
                    data.to_excel(writer, sheet_name=sheet_name, index=index)
                    print(f"✓ DataFrame salvo em: {file_path} (planilha: {sheet_name})")
                
                elif isinstance(data, dict):
                    for sheet_name, df in data.items():
                        df.to_excel(writer, sheet_name=sheet_name, index=index)
                    print(f"✓ {len(data)} planilhas salvas em: {file_path}")
                
                else:
                    raise ValueError("Dados devem ser DataFrame ou dicionário de DataFrames")
            
            return True
            
        except Exception as e:
            print(f"✗ Erro ao escrever arquivo Excel: {e}")
            return False
    
    def get_sheet_names(self, file_path: str) -> List[str]:
        """
        Obtém os nomes de todas as planilhas em um arquivo Excel
        
        Args:
            file_path: Caminho para o arquivo Excel
            
        Returns:
            Lista com nomes das planilhas
        """
        try:
            if not self._validate_file(file_path):
                raise ValueError(f"Arquivo não encontrado ou formato inválido: {file_path}")
            
            xl_file = pd.ExcelFile(file_path)
            sheet_names = xl_file.sheet_names
            
            print(f"✓ Planilhas encontradas em {file_path}:")
            for i, name in enumerate(sheet_names, 1):
                print(f"  {i}. {name}")
            
            return sheet_names
            
        except Exception as e:
            print(f"✗ Erro ao obter nomes das planilhas: {e}")
            return []
    
    def _validate_file(self, file_path: str) -> bool:
        """
        Valida se o arquivo existe e tem formato suportado
        
        Args:
            file_path: Caminho para o arquivo
            
        Returns:
            True se válido, False caso contrário
        """
        if not os.path.exists(file_path):
            return False
        
        file_extension = Path(file_path).suffix.lower()
        return file_extension in self.supported_formats
    
    def get_excel_info(self, file_path: str) -> Dict:
        """
        Obtém informações detalhadas sobre um arquivo Excel
        
        Args:
            file_path: Caminho para o arquivo Excel
            
        Returns:
            Dicionário com informações do arquivo
        """
        try:
            if not self._validate_file(file_path):
                raise ValueError(f"Arquivo não encontrado ou formato inválido: {file_path}")
            
            info = {
                'file_path': file_path,
                'file_size': os.path.getsize(file_path),
                'sheets': {}
            }
            
            xl_file = pd.ExcelFile(file_path)
            
            for sheet_name in xl_file.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
                info['sheets'][sheet_name] = {
                    'rows': df.shape[0],
                    'columns': df.shape[1],
                    'column_names': list(df.columns),
                    'data_types': dict(df.dtypes.astype(str))
                }
            
            return info
            
        except Exception as e:
            print(f"✗ Erro ao obter informações do Excel: {e}")
            return {}