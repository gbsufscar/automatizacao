"""
DataVisualizer - Módulo para visualização de dados
Fornece funcionalidades para criar gráficos e visualizações dos dados
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Optional, Tuple, Any, Union
import warnings
warnings.filterwarnings('ignore')

# Configurar estilo dos gráficos
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")


class DataVisualizer:
    """Classe para visualização de dados"""
    
    def __init__(self, figsize: Tuple[int, int] = (12, 8)):
        self.figsize = figsize
        self.color_palette = px.colors.qualitative.Set3
        
    def plot_distribution(self, df: pd.DataFrame, 
                         columns: Optional[List[str]] = None,
                         plot_type: str = 'hist',
                         save_path: Optional[str] = None) -> None:
        """
        Plota distribuição de variáveis numéricas
        
        Args:
            df: DataFrame com dados
            columns: Colunas específicas para plotar
            plot_type: Tipo de gráfico ('hist', 'box', 'violin', 'kde')
            save_path: Caminho para salvar o gráfico
        """
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if not columns:
            print("⚠ Nenhuma coluna numérica encontrada")
            return
        
        n_cols = min(3, len(columns))
        n_rows = (len(columns) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 5, n_rows * 4))
        if n_rows == 1:
            axes = [axes] if n_cols == 1 else axes
        else:
            axes = axes.flatten()
        
        for i, col in enumerate(columns):
            ax = axes[i] if len(columns) > 1 else axes
            data = df[col].dropna()
            
            if plot_type == 'hist':
                ax.hist(data, bins=30, alpha=0.7, edgecolor='black')
                ax.set_title(f'Histograma: {col}')
            
            elif plot_type == 'box':
                ax.boxplot(data)
                ax.set_title(f'Box Plot: {col}')
            
            elif plot_type == 'violin':
                parts = ax.violinplot(data, showmeans=True)
                ax.set_title(f'Violin Plot: {col}')
            
            elif plot_type == 'kde':
                data.plot.kde(ax=ax)
                ax.set_title(f'Densidade: {col}')
            
            ax.set_xlabel(col)
            ax.grid(True, alpha=0.3)
        
        # Remover subplots vazios
        for i in range(len(columns), len(axes)):
            fig.delaxes(axes[i])
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Gráfico salvo em: {save_path}")
        
        plt.show()
    
    def plot_correlation_heatmap(self, df: pd.DataFrame, 
                               method: str = 'pearson',
                               save_path: Optional[str] = None) -> None:
        """
        Cria mapa de calor de correlações
        
        Args:
            df: DataFrame com dados
            method: Método de correlação
            save_path: Caminho para salvar o gráfico
        """
        numeric_df = df.select_dtypes(include=[np.number])
        
        if numeric_df.empty:
            print("⚠ Nenhuma coluna numérica encontrada para correlação")
            return
        
        corr_matrix = numeric_df.corr(method=method)
        
        plt.figure(figsize=self.figsize)
        
        # Criar máscara para o triângulo superior
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        
        sns.heatmap(corr_matrix, 
                   mask=mask,
                   annot=True, 
                   cmap='RdBu_r', 
                   center=0,
                   square=True,
                   fmt='.2f',
                   cbar_kws={"shrink": .8})
        
        plt.title(f'Mapa de Correlação ({method.title()})')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Mapa de correlação salvo em: {save_path}")
        
        plt.show()
    
    def plot_categorical_analysis(self, df: pd.DataFrame, 
                                columns: Optional[List[str]] = None,
                                plot_type: str = 'bar',
                                top_n: int = 10,
                                save_path: Optional[str] = None) -> None:
        """
        Plota análise de variáveis categóricas
        
        Args:
            df: DataFrame com dados
            columns: Colunas categóricas específicas
            plot_type: Tipo de gráfico ('bar', 'pie', 'count')
            top_n: Número máximo de categorias para mostrar
            save_path: Caminho para salvar o gráfico
        """
        if columns is None:
            columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        if not columns:
            print("⚠ Nenhuma coluna categórica encontrada")
            return
        
        n_cols = min(2, len(columns))
        n_rows = (len(columns) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 6, n_rows * 4))
        if n_rows == 1 and n_cols == 1:
            axes = [axes]
        elif n_rows == 1:
            axes = axes
        else:
            axes = axes.flatten()
        
        for i, col in enumerate(columns):
            ax = axes[i] if len(columns) > 1 else axes[0]
            
            # Obter top N valores
            value_counts = df[col].value_counts().head(top_n)
            
            if plot_type == 'bar':
                value_counts.plot(kind='bar', ax=ax, color=sns.color_palette("husl", len(value_counts)))
                ax.set_title(f'Top {top_n} valores: {col}')
                ax.set_xlabel('')
                ax.tick_params(axis='x', rotation=45)
            
            elif plot_type == 'pie':
                ax.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%')
                ax.set_title(f'Distribuição: {col}')
            
            elif plot_type == 'count':
                sns.countplot(data=df, x=col, ax=ax, order=value_counts.index)
                ax.set_title(f'Contagem: {col}')
                ax.tick_params(axis='x', rotation=45)
            
            ax.grid(True, alpha=0.3)
        
        # Remover subplots vazios
        if len(columns) < len(axes):
            for i in range(len(columns), len(axes)):
                fig.delaxes(axes[i])
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Gráfico categórico salvo em: {save_path}")
        
        plt.show()
    
    def plot_time_series(self, df: pd.DataFrame, 
                        date_column: str,
                        value_columns: List[str],
                        resample_period: Optional[str] = None,
                        save_path: Optional[str] = None) -> None:
        """
        Plota séries temporais
        
        Args:
            df: DataFrame com dados
            date_column: Nome da coluna de data
            value_columns: Colunas com valores para plotar
            resample_period: Período para reagrupar dados (ex: 'M', 'W', 'D')
            save_path: Caminho para salvar o gráfico
        """
        if date_column not in df.columns:
            print(f"⚠ Coluna de data '{date_column}' não encontrada")
            return
        
        df_temp = df.copy()
        df_temp[date_column] = pd.to_datetime(df_temp[date_column])
        df_temp = df_temp.set_index(date_column).sort_index()
        
        # Reagrupar se especificado
        if resample_period:
            df_temp = df_temp[value_columns].resample(resample_period).sum()
        
        plt.figure(figsize=self.figsize)
        
        for i, col in enumerate(value_columns):
            if col in df_temp.columns:
                plt.plot(df_temp.index, df_temp[col], 
                        label=col, linewidth=2, marker='o', markersize=4)
        
        plt.title('Análise de Série Temporal')
        plt.xlabel('Data')
        plt.ylabel('Valores')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Gráfico de série temporal salvo em: {save_path}")
        
        plt.tight_layout()
        plt.show()
    
    def plot_scatter_matrix(self, df: pd.DataFrame, 
                           columns: Optional[List[str]] = None,
                           save_path: Optional[str] = None) -> None:
        """
        Cria matriz de dispersão para variáveis numéricas
        
        Args:
            df: DataFrame com dados
            columns: Colunas específicas para incluir
            save_path: Caminho para salvar o gráfico
        """
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(columns) < 2:
            print("⚠ Pelo menos 2 colunas numéricas são necessárias")
            return
        
        # Limitar a 5 variáveis para legibilidade
        if len(columns) > 5:
            columns = columns[:5]
            print(f"ℹ️ Limitando a {len(columns)} variáveis para melhor visualização")
        
        pd.plotting.scatter_matrix(df[columns], 
                                 figsize=(len(columns)*3, len(columns)*3),
                                 alpha=0.7,
                                 diagonal='hist')
        
        plt.suptitle('Matriz de Dispersão', size=16)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Matriz de dispersão salva em: {save_path}")
        
        plt.tight_layout()
        plt.show()
    
    def create_interactive_dashboard(self, df: pd.DataFrame, 
                                   title: str = "Dashboard Interativo") -> go.Figure:
        """
        Cria dashboard interativo com Plotly
        
        Args:
            df: DataFrame com dados
            title: Título do dashboard
        
        Returns:
            Figura Plotly interativa
        """
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        # Criar subplots
        if len(numeric_cols) >= 2 and len(categorical_cols) >= 1:
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Correlação', 'Distribuição', 'Categorias', 'Box Plot'),
                specs=[[{"type": "scatter"}, {"type": "histogram"}],
                       [{"type": "bar"}, {"type": "box"}]]
            )
            
            # Gráfico de correlação
            if len(numeric_cols) >= 2:
                fig.add_trace(
                    go.Scatter(x=df[numeric_cols[0]], 
                             y=df[numeric_cols[1]], 
                             mode='markers',
                             name=f'{numeric_cols[0]} vs {numeric_cols[1]}'),
                    row=1, col=1
                )
            
            # Histograma
            fig.add_trace(
                go.Histogram(x=df[numeric_cols[0]], 
                           name=f'Distribuição {numeric_cols[0]}'),
                row=1, col=2
            )
            
            # Gráfico categórico
            if categorical_cols:
                cat_counts = df[categorical_cols[0]].value_counts().head(10)
                fig.add_trace(
                    go.Bar(x=cat_counts.index, 
                          y=cat_counts.values,
                          name=f'Contagem {categorical_cols[0]}'),
                    row=2, col=1
                )
            
            # Box plot
            fig.add_trace(
                go.Box(y=df[numeric_cols[0]], 
                      name=f'Box Plot {numeric_cols[0]}'),
                row=2, col=2
            )
        
        else:
            # Dashboard simplificado
            fig = go.Figure()
            if numeric_cols:
                fig.add_trace(go.Histogram(x=df[numeric_cols[0]], 
                                         name=f'Distribuição {numeric_cols[0]}'))
        
        fig.update_layout(
            title=title,
            height=800,
            showlegend=True,
            template="plotly_white"
        )
        
        return fig
    
    def plot_outliers(self, df: pd.DataFrame, 
                     columns: Optional[List[str]] = None,
                     method: str = 'box',
                     save_path: Optional[str] = None) -> None:
        """
        Visualiza outliers nos dados
        
        Args:
            df: DataFrame com dados
            columns: Colunas específicas para analisar
            method: Método de visualização ('box', 'scatter', 'violin')
            save_path: Caminho para salvar o gráfico
        """
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if not columns:
            print("⚠ Nenhuma coluna numérica encontrada")
            return
        
        n_cols = min(3, len(columns))
        n_rows = (len(columns) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 4, n_rows * 4))
        if n_rows == 1:
            axes = [axes] if n_cols == 1 else axes
        else:
            axes = axes.flatten()
        
        for i, col in enumerate(columns):
            ax = axes[i] if len(columns) > 1 else axes
            data = df[col].dropna()
            
            if method == 'box':
                ax.boxplot(data)
                ax.set_title(f'Outliers: {col}')
                ax.set_ylabel(col)
            
            elif method == 'scatter':
                ax.scatter(range(len(data)), data, alpha=0.6)
                ax.set_title(f'Dispersão: {col}')
                ax.set_xlabel('Índice')
                ax.set_ylabel(col)
            
            elif method == 'violin':
                parts = ax.violinplot(data, showmeans=True, showextrema=True)
                ax.set_title(f'Violin Plot: {col}')
                ax.set_ylabel(col)
            
            ax.grid(True, alpha=0.3)
        
        # Remover subplots vazios
        for i in range(len(columns), len(axes)):
            fig.delaxes(axes[i])
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Gráfico de outliers salvo em: {save_path}")
        
        plt.show()
    
    def save_all_plots(self, df: pd.DataFrame, 
                      output_dir: str = "plots",
                      formats: List[str] = ['png']) -> None:
        """
        Salva todos os tipos de gráficos principais
        
        Args:
            df: DataFrame com dados
            output_dir: Diretório para salvar os gráficos
            formats: Formatos para salvar ('png', 'pdf', 'svg')
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        for fmt in formats:
            # Distribuições
            self.plot_distribution(df, save_path=f"{output_dir}/distribuicoes.{fmt}")
            
            # Correlações
            self.plot_correlation_heatmap(df, save_path=f"{output_dir}/correlacoes.{fmt}")
            
            # Categóricas
            self.plot_categorical_analysis(df, save_path=f"{output_dir}/categoricas.{fmt}")
            
            # Outliers
            self.plot_outliers(df, save_path=f"{output_dir}/outliers.{fmt}")
        
        print(f"✓ Todos os gráficos salvos em: {output_dir}/")
    
    def export_interactive_html(self, fig: go.Figure, 
                              file_path: str = "dashboard.html") -> None:
        """
        Exporta gráfico interativo como HTML
        
        Args:
            fig: Figura Plotly
            file_path: Caminho para salvar o arquivo HTML
        """
        fig.write_html(file_path)
        print(f"✓ Dashboard interativo salvo em: {file_path}")