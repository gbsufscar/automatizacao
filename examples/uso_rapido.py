"""
Script de Uso Rápido - Excel Automation
Execute tarefas comuns de automação Excel com comandos simples
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from excel_automation import ExcelHandler, ExcelDataProcessor, DataAnalyzer, DataVisualizer
import pandas as pd
import argparse


def processar_arquivo_excel(arquivo_entrada, arquivo_saida=None, operacoes=None):
    """
    Processa um arquivo Excel com operações especificadas
    
    Args:
        arquivo_entrada: Caminho do arquivo Excel de entrada
        arquivo_saida: Caminho do arquivo de saída (opcional)
        operacoes: Lista de operações para executar
    """
    
    print(f"📖 Lendo arquivo: {arquivo_entrada}")
    
    # Inicializar componentes
    handler = ExcelHandler()
    processor = ExcelDataProcessor()
    analyzer = DataAnalyzer()
    visualizer = DataVisualizer()
    
    # Ler dados
    try:
        df = handler.read_excel(arquivo_entrada)
    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {e}")
        return
    
    print(f"✅ Dados carregados: {df.shape[0]} linhas, {df.shape[1]} colunas")
    
    # Aplicar operações
    if operacoes:
        for operacao in operacoes:
            print(f"🔄 Executando: {operacao}")
            df = aplicar_operacao(df, operacao, processor, analyzer, visualizer)
    
    # Salvar resultado
    if arquivo_saida:
        handler.write_excel(df, arquivo_saida)
        print(f"💾 Resultado salvo em: {arquivo_saida}")
    
    # Mostrar resumo
    print("\n📊 RESUMO FINAL:")
    print(f"   Linhas: {df.shape[0]}")
    print(f"   Colunas: {df.shape[1]}")
    print(f"   Colunas numéricas: {len(df.select_dtypes(include=['number']).columns)}")
    print(f"   Colunas categóricas: {len(df.select_dtypes(include=['object']).columns)}")
    
    return df


def aplicar_operacao(df, operacao, processor, analyzer, visualizer):
    """Aplica uma operação específica aos dados"""
    
    if operacao == "limpar":
        return processor.clean_data(df)
    
    elif operacao == "analisar":
        analyzer.descriptive_analysis(df)
        return df
    
    elif operacao == "correlacao":
        analyzer.correlation_analysis(df)
        return df
    
    elif operacao == "outliers":
        analyzer.outlier_detection(df)
        return df
    
    elif operacao == "visualizar":
        visualizer.plot_distribution(df)
        visualizer.plot_correlation_heatmap(df)
        return df
    
    elif operacao == "dashboard":
        dashboard = visualizer.create_interactive_dashboard(df)
        visualizer.export_interactive_html(dashboard, "dashboard_rapido.html")
        return df
    
    elif operacao.startswith("agrupar_"):
        # Exemplo: agrupar_coluna1
        coluna = operacao.split("_")[1]
        if coluna in df.columns:
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                agg_dict = {col: 'sum' for col in numeric_cols}
                return processor.group_and_aggregate(df, coluna, agg_dict)
        return df
    
    elif operacao.startswith("filtrar_"):
        # Exemplo: filtrar_coluna=valor
        filtro_str = operacao.split("_", 1)[1]
        if "=" in filtro_str:
            coluna, valor = filtro_str.split("=", 1)
            if coluna in df.columns:
                try:
                    # Tentar converter para número se possível
                    valor_num = float(valor)
                    return processor.filter_data(df, {coluna: valor_num})
                except:
                    return processor.filter_data(df, {coluna: valor})
        return df
    
    else:
        print(f"⚠️ Operação '{operacao}' não reconhecida")
        return df


def criar_relatorio_automatico(arquivo_excel, nome_relatorio="relatorio_automatico"):
    """Cria relatório automático completo de um arquivo Excel"""
    
    print("🤖 CRIANDO RELATÓRIO AUTOMÁTICO")
    print("=" * 40)
    
    # Processar arquivo
    df = processar_arquivo_excel(
        arquivo_excel,
        f"{nome_relatorio}.xlsx",
        ["limpar", "analisar", "correlacao", "outliers"]
    )
    
    if df is None:
        return
    
    # Criar visualizações
    print("\n📊 Criando visualizações...")
    visualizer = DataVisualizer()
    
    # Salvar todos os gráficos
    os.makedirs(f"{nome_relatorio}_plots", exist_ok=True)
    visualizer.save_all_plots(df, f"{nome_relatorio}_plots")
    
    # Dashboard interativo
    dashboard = visualizer.create_interactive_dashboard(df, f"Relatório: {nome_relatorio}")
    visualizer.export_interactive_html(dashboard, f"{nome_relatorio}_dashboard.html")
    
    print(f"\n✅ Relatório completo criado:")
    print(f"   📋 Dados: {nome_relatorio}.xlsx")
    print(f"   📈 Gráficos: {nome_relatorio}_plots/")
    print(f"   🌐 Dashboard: {nome_relatorio}_dashboard.html")


def comparar_arquivos_excel(arquivo1, arquivo2, coluna_chave=None):
    """Compara dois arquivos Excel e mostra diferenças"""
    
    print("🔍 COMPARANDO ARQUIVOS EXCEL")
    print("=" * 40)
    
    handler = ExcelHandler()
    
    # Ler arquivos
    print(f"📖 Lendo arquivo 1: {arquivo1}")
    df1 = handler.read_excel(arquivo1)
    
    print(f"📖 Lendo arquivo 2: {arquivo2}")
    df2 = handler.read_excel(arquivo2)
    
    # Comparar dimensões
    print(f"\n📏 Dimensões:")
    print(f"   Arquivo 1: {df1.shape[0]} x {df1.shape[1]}")
    print(f"   Arquivo 2: {df2.shape[0]} x {df2.shape[1]}")
    
    # Comparar colunas
    colunas1 = set(df1.columns)
    colunas2 = set(df2.columns)
    
    colunas_comuns = colunas1.intersection(colunas2)
    colunas_apenas1 = colunas1 - colunas2
    colunas_apenas2 = colunas2 - colunas1
    
    print(f"\n📋 Colunas:")
    print(f"   Comuns: {len(colunas_comuns)}")
    print(f"   Apenas no arquivo 1: {len(colunas_apenas1)}")
    print(f"   Apenas no arquivo 2: {len(colunas_apenas2)}")
    
    if colunas_apenas1:
        print(f"   🔸 Exclusivas do arquivo 1: {list(colunas_apenas1)}")
    if colunas_apenas2:
        print(f"   🔸 Exclusivas do arquivo 2: {list(colunas_apenas2)}")
    
    # Comparação de dados se tiver coluna chave
    if coluna_chave and coluna_chave in colunas_comuns:
        print(f"\n🔑 Comparando por chave: {coluna_chave}")
        
        valores1 = set(df1[coluna_chave].dropna())
        valores2 = set(df2[coluna_chave].dropna())
        
        valores_comuns = valores1.intersection(valores2)
        valores_apenas1 = valores1 - valores2
        valores_apenas2 = valores2 - valores1
        
        print(f"   Valores comuns: {len(valores_comuns)}")
        print(f"   Apenas no arquivo 1: {len(valores_apenas1)}")
        print(f"   Apenas no arquivo 2: {len(valores_apenas2)}")
    
    # Salvar relatório de comparação
    relatorio = {
        'Resumo_Arquivo1': pd.DataFrame([{
            'Arquivo': arquivo1,
            'Linhas': df1.shape[0],
            'Colunas': df1.shape[1],
            'Memoria_MB': df1.memory_usage(deep=True).sum() / 1024 / 1024
        }]),
        'Resumo_Arquivo2': pd.DataFrame([{
            'Arquivo': arquivo2,
            'Linhas': df2.shape[0],
            'Colunas': df2.shape[1],
            'Memoria_MB': df2.memory_usage(deep=True).sum() / 1024 / 1024
        }])
    }
    
    if colunas_apenas1:
        relatorio['Colunas_Apenas_Arquivo1'] = pd.DataFrame({'Coluna': list(colunas_apenas1)})
    
    if colunas_apenas2:
        relatorio['Colunas_Apenas_Arquivo2'] = pd.DataFrame({'Coluna': list(colunas_apenas2)})
    
    handler.write_excel(relatorio, "comparacao_arquivos.xlsx")
    print("\n💾 Relatório de comparação salvo em: comparacao_arquivos.xlsx")


def main():
    """Função principal com interface de linha de comando"""
    
    parser = argparse.ArgumentParser(description='Automação Excel - Uso Rápido')
    parser.add_argument('comando', choices=['processar', 'relatorio', 'comparar', 'exemplo'],
                       help='Comando a executar')
    parser.add_argument('--arquivo', help='Arquivo Excel de entrada')
    parser.add_argument('--arquivo2', help='Segundo arquivo Excel (para comparação)')
    parser.add_argument('--saida', help='Arquivo de saída')
    parser.add_argument('--operacoes', nargs='+', 
                       choices=['limpar', 'analisar', 'correlacao', 'outliers', 
                               'visualizar', 'dashboard'],
                       help='Operações a executar')
    parser.add_argument('--nome', default='relatorio', help='Nome do relatório')
    parser.add_argument('--chave', help='Coluna chave para comparação')
    
    args = parser.parse_args()
    
    if args.comando == 'processar':
        if not args.arquivo:
            print("❌ Arquivo de entrada é obrigatório para processamento")
            return
        
        processar_arquivo_excel(args.arquivo, args.saida, args.operacoes)
    
    elif args.comando == 'relatorio':
        if not args.arquivo:
            print("❌ Arquivo de entrada é obrigatório para relatório")
            return
        
        criar_relatorio_automatico(args.arquivo, args.nome)
    
    elif args.comando == 'comparar':
        if not args.arquivo or not args.arquivo2:
            print("❌ Dois arquivos são obrigatórios para comparação")
            return
        
        comparar_arquivos_excel(args.arquivo, args.arquivo2, args.chave)
    
    elif args.comando == 'exemplo':
        # Criar dados de exemplo e processar
        print("🎯 Criando exemplo de uso...")
        
        import numpy as np
        
        dados_exemplo = pd.DataFrame({
            'ID': range(1, 101),
            'Nome': [f'Item_{i}' for i in range(1, 101)],
            'Categoria': np.random.choice(['A', 'B', 'C'], 100),
            'Valor': np.random.uniform(10, 1000, 100).round(2),
            'Quantidade': np.random.randint(1, 50, 100)
        })
        
        # Salvar exemplo
        from excel_automation import ExcelHandler
        handler = ExcelHandler()
        handler.write_excel(dados_exemplo, "exemplo_dados.xlsx")
        
        # Processar exemplo
        criar_relatorio_automatico("exemplo_dados.xlsx", "exemplo_relatorio")
        
        print("\n✅ Exemplo criado e processado!")
        print("   📋 Dados: exemplo_dados.xlsx")
        print("   📊 Relatório: exemplo_relatorio.xlsx")


if __name__ == "__main__":
    main()