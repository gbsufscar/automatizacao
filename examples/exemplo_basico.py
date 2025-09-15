"""
Exemplo básico de automação Excel com Python
Este script demonstra como usar o pacote excel_automation para:
1. Ler arquivos Excel
2. Processar e limpar dados
3. Realizar análises
4. Criar visualizações
5. Salvar resultados
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from excel_automation import ExcelHandler, ExcelDataProcessor, DataAnalyzer, DataVisualizer
import pandas as pd
import numpy as np


def exemplo_completo():
    """Exemplo completo de automação Excel"""
    
    print("=" * 60)
    print("🚀 EXEMPLO DE AUTOMAÇÃO EXCEL COM PYTHON")
    print("=" * 60)
    
    # 1. CRIAR DADOS DE EXEMPLO
    print("\n📋 1. Criando dados de exemplo...")
    dados_vendas = criar_dados_exemplo()
    
    # 2. INICIALIZAR COMPONENTES
    print("\n🔧 2. Inicializando componentes...")
    excel_handler = ExcelHandler()
    processor = ExcelDataProcessor()
    analyzer = DataAnalyzer()
    visualizer = DataVisualizer()
    
    # 3. SALVAR DADOS EM EXCEL
    print("\n💾 3. Salvando dados em Excel...")
    excel_path = "../data/vendas_exemplo.xlsx"
    excel_handler.write_excel(dados_vendas, excel_path, sheet_name="Vendas")
    
    # 4. LER DADOS DO EXCEL
    print("\n📖 4. Lendo dados do Excel...")
    df = excel_handler.read_excel(excel_path)
    print(f"   Dados carregados: {df.shape[0]} linhas, {df.shape[1]} colunas")
    
    # 5. PROCESSAR E LIMPAR DADOS
    print("\n🧹 5. Processando e limpando dados...")
    
    # Limpar dados
    df_clean = processor.clean_data(df, remove_duplicates=True, handle_missing='fill')
    
    # Transformar colunas
    transformations = {
        'produto': 'upper',
        'vendedor': 'title',
        'valor_venda': 'numeric'
    }
    df_clean = processor.transform_columns(df_clean, transformations)
    
    # Criar colunas calculadas
    calculations = {
        'valor_total': 'valor_venda * quantidade',
        'desconto_aplicado': 'valor_venda * desconto / 100'
    }
    df_clean = processor.create_calculated_columns(df_clean, calculations)
    
    # 6. ANÁLISE DOS DADOS
    print("\n📊 6. Realizando análises...")
    
    # Análise descritiva
    desc_analysis = analyzer.descriptive_analysis(df_clean)
    
    # Análise de correlação
    corr_analysis = analyzer.correlation_analysis(df_clean)
    
    # Detecção de outliers
    outlier_analysis = analyzer.outlier_detection(df_clean)
    
    # Gerar insights
    insights = analyzer.generate_insights(df_clean)
    print("\n💡 Insights gerados:")
    for insight in insights:
        print(f"   {insight}")
    
    # 7. ANÁLISES AGREGADAS
    print("\n📈 7. Criando análises agregadas...")
    
    # Vendas por vendedor
    vendas_vendedor = processor.group_and_aggregate(
        df_clean, 
        'vendedor', 
        {'valor_total': 'sum', 'quantidade': 'sum'}
    )
    
    # Vendas por produto
    vendas_produto = processor.group_and_aggregate(
        df_clean, 
        'produto', 
        {'valor_total': ['sum', 'mean'], 'quantidade': 'sum'}
    )
    
    # 8. VISUALIZAÇÕES
    print("\n📈 8. Criando visualizações...")
    
    # Criar diretório para gráficos
    os.makedirs("../plots", exist_ok=True)
    
    # Distribuições
    visualizer.plot_distribution(df_clean)
    
    # Correlações
    visualizer.plot_correlation_heatmap(df_clean)
    
    # Análise categórica
    visualizer.plot_categorical_analysis(df_clean)
    
    # Dashboard interativo
    dashboard = visualizer.create_interactive_dashboard(df_clean, "Dashboard de Vendas")
    visualizer.export_interactive_html(dashboard, "../plots/dashboard_vendas.html")
    
    # 9. SALVAR RESULTADOS
    print("\n💾 9. Salvando resultados...")
    
    # Criar múltiplas planilhas com resultados
    resultados = {
        'Dados_Limpos': df_clean,
        'Vendas_por_Vendedor': vendas_vendedor,
        'Vendas_por_Produto': vendas_produto
    }
    
    excel_handler.write_excel(resultados, "../data/relatorio_vendas.xlsx")
    
    # 10. RELATÓRIO FINAL
    print("\n📋 10. Relatório Final")
    print("-" * 40)
    print(f"✓ Dados processados: {df_clean.shape[0]} registros")
    print(f"✓ Colunas analisadas: {df_clean.shape[1]}")
    print(f"✓ Vendedores únicos: {df_clean['vendedor'].nunique()}")
    print(f"✓ Produtos únicos: {df_clean['produto'].nunique()}")
    print(f"✓ Valor total de vendas: R$ {df_clean['valor_total'].sum():,.2f}")
    print(f"✓ Ticket médio: R$ {df_clean['valor_total'].mean():,.2f}")
    
    # Mostrar log de processamento
    print("\n📝 Log de processamento:")
    for log_entry in processor.get_processing_log():
        print(f"   {log_entry}")
    
    print("\n🎉 Automação concluída com sucesso!")
    print(f"   📁 Resultados salvos em: ../data/")
    print(f"   📈 Dashboard interativo: ../plots/dashboard_vendas.html")
    

def criar_dados_exemplo():
    """Cria dados de exemplo para demonstração"""
    
    np.random.seed(42)
    
    vendedores = ['Ana Silva', 'João Santos', 'Maria Oliveira', 'Pedro Costa', 'Julia Lima']
    produtos = ['Notebook', 'Mouse', 'Teclado', 'Monitor', 'Webcam', 'Headset']
    regioes = ['Norte', 'Sul', 'Leste', 'Oeste', 'Centro']
    
    n_records = 1000
    
    dados = {
        'data_venda': pd.date_range('2023-01-01', periods=n_records, freq='D')[:n_records],
        'vendedor': np.random.choice(vendedores, n_records),
        'produto': np.random.choice(produtos, n_records),
        'regiao': np.random.choice(regioes, n_records),
        'quantidade': np.random.randint(1, 10, n_records),
        'valor_venda': np.random.uniform(50, 2000, n_records).round(2),
        'desconto': np.random.uniform(0, 20, n_records).round(1),
        'custo': np.random.uniform(20, 1500, n_records).round(2)
    }
    
    # Adicionar alguns valores ausentes para demonstrar limpeza
    indices_na = np.random.choice(n_records, size=50, replace=False)
    dados_df = pd.DataFrame(dados)
    dados_df.loc[indices_na[:25], 'desconto'] = np.nan
    dados_df.loc[indices_na[25:], 'custo'] = np.nan
    
    # Adicionar algumas duplicatas
    dados_df = pd.concat([dados_df, dados_df.head(20)], ignore_index=True)
    
    return dados_df


def exemplo_simples():
    """Exemplo simples para iniciantes"""
    
    print("🔰 EXEMPLO SIMPLES - AUTOMATIZANDO EXCEL")
    print("-" * 50)
    
    # 1. Ler arquivo Excel
    handler = ExcelHandler()
    
    # Criar dados simples
    dados = pd.DataFrame({
        'Nome': ['Ana', 'João', 'Maria'],
        'Idade': [25, 30, 28],
        'Salario': [5000, 6000, 5500]
    })
    
    # 2. Salvar em Excel
    handler.write_excel(dados, "../data/funcionarios.xlsx")
    print("✓ Dados salvos em Excel")
    
    # 3. Ler dados
    df = handler.read_excel("../data/funcionarios.xlsx")
    print("✓ Dados lidos do Excel:")
    print(df)
    
    # 4. Processar dados
    processor = ExcelDataProcessor()
    
    # Criar coluna calculada
    df_processado = processor.create_calculated_columns(
        df, 
        {'salario_anual': 'Salario * 12'}
    )
    
    print("\n✓ Dados processados:")
    print(df_processado)
    
    # 5. Análise simples
    analyzer = DataAnalyzer()
    analise = analyzer.descriptive_analysis(df_processado)
    
    print(f"\n✓ Média salarial: R$ {df_processado['Salario'].mean():,.2f}")
    print(f"✓ Idade média: {df_processado['Idade'].mean():.1f} anos")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Exemplos de automação Excel')
    parser.add_argument('--tipo', choices=['simples', 'completo'], 
                       default='completo', help='Tipo de exemplo a executar')
    
    args = parser.parse_args()
    
    if args.tipo == 'simples':
        exemplo_simples()
    else:
        exemplo_completo()