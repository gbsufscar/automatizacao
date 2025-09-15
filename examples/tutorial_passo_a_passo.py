"""
Tutorial Passo a Passo - Automação Excel com Python
Este tutorial mostra como automatizar tarefas comuns do Excel
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from excel_automation import ExcelHandler, ExcelDataProcessor, DataAnalyzer, DataVisualizer
import pandas as pd
import numpy as np


class TutorialExcelAutomacao:
    """Tutorial interativo para automação Excel"""
    
    def __init__(self):
        self.handler = ExcelHandler()
        self.processor = ExcelDataProcessor()
        self.analyzer = DataAnalyzer()
        self.visualizer = DataVisualizer()
        
        print("🎓 TUTORIAL: AUTOMAÇÃO EXCEL COM PYTHON")
        print("=" * 50)
    
    def passo_1_leitura_excel(self):
        """Passo 1: Como ler arquivos Excel"""
        
        print("\n📖 PASSO 1: Lendo Arquivos Excel")
        print("-" * 30)
        
        # Criar dados de exemplo
        dados_exemplo = pd.DataFrame({
            'ID': range(1, 101),
            'Nome': [f'Cliente_{i}' for i in range(1, 101)],
            'Valor': np.random.uniform(100, 1000, 100).round(2),
            'Data': pd.date_range('2023-01-01', periods=100, freq='D')
        })
        
        # Salvar dados
        arquivo_exemplo = "../data/tutorial_dados.xlsx"
        self.handler.write_excel(dados_exemplo, arquivo_exemplo)
        
        print("✅ Dados de exemplo criados")
        
        # Demonstrar diferentes formas de ler
        print("\n🔍 Diferentes formas de ler Excel:")
        
        # Leitura básica
        df1 = self.handler.read_excel(arquivo_exemplo)
        print(f"   📄 Leitura básica: {df1.shape}")
        
        # Leitura de colunas específicas
        df2 = self.handler.read_excel(arquivo_exemplo, usecols=['Nome', 'Valor'])
        print(f"   🎯 Colunas específicas: {df2.shape}")
        
        # Obter informações do arquivo
        info = self.handler.get_excel_info(arquivo_exemplo)
        print(f"   ℹ️ Informações do arquivo: {info['file_size']} bytes")
        
        return df1
    
    def passo_2_limpeza_dados(self, df):
        """Passo 2: Limpeza e processamento de dados"""
        
        print("\n🧹 PASSO 2: Limpeza de Dados")
        print("-" * 30)
        
        # Adicionar alguns problemas nos dados para demonstrar limpeza
        df_sujo = df.copy()
        
        # Adicionar valores ausentes
        df_sujo.loc[5:10, 'Valor'] = np.nan
        df_sujo.loc[15:20, 'Nome'] = np.nan
        
        # Adicionar duplicatas
        df_sujo = pd.concat([df_sujo, df_sujo.head(5)], ignore_index=True)
        
        # Adicionar dados inconsistentes
        df_sujo.loc[25:30, 'Nome'] = df_sujo.loc[25:30, 'Nome'].str.lower()
        
        print(f"📊 Dados antes da limpeza: {df_sujo.shape}")
        print(f"   ❌ Valores ausentes: {df_sujo.isnull().sum().sum()}")
        print(f"   ❌ Duplicatas: {df_sujo.duplicated().sum()}")
        
        # Limpar dados
        df_limpo = self.processor.clean_data(
            df_sujo, 
            remove_duplicates=True, 
            handle_missing='drop',
            standardize_text=True
        )
        
        print(f"\n📊 Dados após limpeza: {df_limpo.shape}")
        
        # Transformações adicionais
        transformations = {
            'Nome': 'upper',
            'Valor': 'numeric'
        }
        
        df_transformado = self.processor.transform_columns(df_limpo, transformations)
        
        print("✅ Transformações aplicadas")
        
        return df_transformado
    
    def passo_3_analise_dados(self, df):
        """Passo 3: Análise de dados"""
        
        print("\n📊 PASSO 3: Análise de Dados")
        print("-" * 30)
        
        # Análise descritiva
        desc = self.analyzer.descriptive_analysis(df)
        
        print("🔍 Estatísticas principais:")
        if 'Valor' in desc['numeric_summary']:
            stats = desc['numeric_summary']['Valor']
            print(f"   💰 Valor médio: R$ {stats['mean']:.2f}")
            print(f"   📈 Valor máximo: R$ {stats['max']:.2f}")
            print(f"   📉 Valor mínimo: R$ {stats['min']:.2f}")
        
        # Análise de correlação
        if len(df.select_dtypes(include=[np.number]).columns) > 1:
            corr = self.analyzer.correlation_analysis(df)
            print(f"🔗 Correlações analisadas: {len(corr.get('variables_analyzed', []))}")
        
        # Detecção de outliers
        outliers = self.analyzer.outlier_detection(df)
        total_outliers = outliers['summary']['total_outliers']
        print(f"🎯 Outliers detectados: {total_outliers}")
        
        # Insights automáticos
        insights = self.analyzer.generate_insights(df)
        print("\n💡 Insights automáticos:")
        for insight in insights[:3]:  # Mostrar apenas os 3 primeiros
            print(f"   {insight}")
        
        return desc
    
    def passo_4_agregacoes(self, df):
        """Passo 4: Agregações e agrupamentos"""
        
        print("\n📈 PASSO 4: Agregações de Dados")
        print("-" * 30)
        
        # Adicionar categorias para demonstrar agrupamento
        df_agg = df.copy()
        df_agg['Categoria'] = np.random.choice(['A', 'B', 'C'], len(df_agg))
        df_agg['Regiao'] = np.random.choice(['Norte', 'Sul'], len(df_agg))
        
        # Agrupamento simples
        grupo_categoria = self.processor.group_and_aggregate(
            df_agg, 
            'Categoria', 
            {'Valor': ['sum', 'mean', 'count']}
        )
        
        print("📋 Resumo por categoria:")
        print(grupo_categoria.head())
        
        # Agrupamento múltiplo
        grupo_multiplo = self.processor.group_and_aggregate(
            df_agg, 
            ['Categoria', 'Regiao'], 
            {'Valor': 'sum'}
        )
        
        print(f"\n📋 Agrupamento múltiplo: {grupo_multiplo.shape[0]} grupos")
        
        # Tabela dinâmica
        pivot = self.processor.pivot_data(
            df_agg, 
            index='Categoria', 
            columns='Regiao', 
            values='Valor'
        )
        
        print("🔄 Tabela dinâmica criada")
        print(pivot)
        
        return grupo_categoria
    
    def passo_5_visualizacoes(self, df):
        """Passo 5: Criação de visualizações"""
        
        print("\n📈 PASSO 5: Visualizações")
        print("-" * 30)
        
        print("🎨 Criando visualizações...")
        
        # Criar diretório
        os.makedirs("../plots/tutorial", exist_ok=True)
        
        # Histogramas
        self.visualizer.plot_distribution(
            df, 
            plot_type='hist',
            save_path="../plots/tutorial/distribuicoes.png"
        )
        
        # Gráficos de correlação
        if len(df.select_dtypes(include=[np.number]).columns) > 1:
            self.visualizer.plot_correlation_heatmap(
                df,
                save_path="../plots/tutorial/correlacoes.png"
            )
        
        # Outliers
        self.visualizer.plot_outliers(
            df,
            save_path="../plots/tutorial/outliers.png"
        )
        
        # Dashboard interativo
        dashboard = self.visualizer.create_interactive_dashboard(
            df, 
            "Tutorial Dashboard"
        )
        
        self.visualizer.export_interactive_html(
            dashboard, 
            "../plots/tutorial/dashboard.html"
        )
        
        print("✅ Visualizações salvas em ../plots/tutorial/")
    
    def passo_6_relatorio_final(self, df, analises):
        """Passo 6: Criação de relatório final"""
        
        print("\n📋 PASSO 6: Relatório Final")
        print("-" * 30)
        
        # Criar colunas calculadas
        df_final = self.processor.create_calculated_columns(
            df, 
            {
                'Valor_Dobrado': 'Valor * 2',
                'Categoria_Valor': 'Valor > 500'
            }
        )
        
        # Gerar relatório de qualidade
        qualidade = self.processor.get_data_quality_report(df_final)
        
        # Preparar dados para Excel
        dados_relatorio = {
            'Dados_Processados': df_final,
            'Resumo_Qualidade': pd.DataFrame([{
                'Linhas': qualidade['shape'][0],
                'Colunas': qualidade['shape'][1],
                'Duplicatas': qualidade['duplicates'],
                'Memoria_MB': qualidade['memory_usage'] / 1024 / 1024
            }]),
            'Log_Processamento': pd.DataFrame({
                'Etapa': self.processor.get_processing_log()
            })
        }
        
        # Salvar relatório
        arquivo_relatorio = "../data/relatorio_tutorial.xlsx"
        self.handler.write_excel(dados_relatorio, arquivo_relatorio)
        
        print(f"✅ Relatório salvo em: {arquivo_relatorio}")
        
        # Estatísticas finais
        print("\n📊 ESTATÍSTICAS FINAIS:")
        print(f"   📏 Dimensões: {df_final.shape[0]} x {df_final.shape[1]}")
        print(f"   💰 Valor total: R$ {df_final['Valor'].sum():,.2f}")
        print(f"   📈 Valor médio: R$ {df_final['Valor'].mean():.2f}")
        print(f"   🏆 Valor máximo: R$ {df_final['Valor'].max():.2f}")
        
        return df_final
    
    def executar_tutorial_completo(self):
        """Executa o tutorial completo"""
        
        print("🚀 Iniciando tutorial completo...")
        
        # Executar todos os passos
        df = self.passo_1_leitura_excel()
        df_limpo = self.passo_2_limpeza_dados(df)
        analises = self.passo_3_analise_dados(df_limpo)
        agregacoes = self.passo_4_agregacoes(df_limpo)
        self.passo_5_visualizacoes(df_limpo)
        df_final = self.passo_6_relatorio_final(df_limpo, analises)
        
        print("\n🎉 TUTORIAL CONCLUÍDO!")
        print("=" * 50)
        print("📁 Arquivos gerados:")
        print("   📊 ../data/tutorial_dados.xlsx - Dados originais")
        print("   📋 ../data/relatorio_tutorial.xlsx - Relatório final")
        print("   📈 ../plots/tutorial/ - Visualizações")
        print("\n✨ Você agora sabe como automatizar Excel com Python!")


def main():
    """Função principal"""
    
    # Criar diretórios necessários
    os.makedirs("../data", exist_ok=True)
    os.makedirs("../plots", exist_ok=True)
    
    # Executar tutorial
    tutorial = TutorialExcelAutomacao()
    tutorial.executar_tutorial_completo()


if __name__ == "__main__":
    main()