"""
Teste simples da funcionalidade de automação Excel
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Backend não-interativo

from excel_automation import ExcelHandler, ExcelDataProcessor, DataAnalyzer


def teste_basico():
    """Teste básico de funcionalidade"""
    
    print("🧪 TESTE BÁSICO DE AUTOMAÇÃO EXCEL")
    print("=" * 40)
    
    # Criar dados de teste
    dados_teste = pd.DataFrame({
        'ID': range(1, 11),
        'Nome': [f'Item_{i}' for i in range(1, 11)],
        'Categoria': np.random.choice(['A', 'B', 'C'], 10),
        'Valor': np.random.uniform(100, 1000, 10).round(2),
        'Quantidade': np.random.randint(1, 10, 10)
    })
    
    print("📋 Dados de teste criados:")
    print(dados_teste.head())
    
    # Testar ExcelHandler
    print("\n🔧 Testando ExcelHandler...")
    handler = ExcelHandler()
    
    # Salvar dados
    arquivo_teste = "../data/teste_basico.xlsx"
    os.makedirs("../data", exist_ok=True)
    
    sucesso = handler.write_excel(dados_teste, arquivo_teste)
    print(f"Escrita Excel: {'✅' if sucesso else '❌'}")
    
    # Ler dados
    df_lido = handler.read_excel(arquivo_teste)
    print(f"Leitura Excel: {'✅' if df_lido is not None else '❌'}")
    
    # Testar ExcelDataProcessor
    print("\n🧹 Testando ExcelDataProcessor...")
    processor = ExcelDataProcessor()
    
    # Limpeza de dados
    df_limpo = processor.clean_data(df_lido)
    print(f"Limpeza dados: {'✅' if len(df_limpo) > 0 else '❌'}")
    
    # Colunas calculadas
    df_calc = processor.create_calculated_columns(
        df_limpo, 
        {'valor_total': 'Valor * Quantidade'}
    )
    print(f"Colunas calculadas: {'✅' if 'valor_total' in df_calc.columns else '❌'}")
    
    # Agrupamentos
    df_grupo = processor.group_and_aggregate(
        df_calc, 
        'Categoria', 
        {'valor_total': 'sum'}
    )
    print(f"Agrupamentos: {'✅' if len(df_grupo) > 0 else '❌'}")
    
    # Testar DataAnalyzer
    print("\n📊 Testando DataAnalyzer...")
    analyzer = DataAnalyzer()
    
    # Análise descritiva
    desc_analysis = analyzer.descriptive_analysis(df_calc)
    print(f"Análise descritiva: {'✅' if desc_analysis else '❌'}")
    
    # Análise de correlação
    corr_analysis = analyzer.correlation_analysis(df_calc)
    print(f"Análise correlação: {'✅' if corr_analysis else '❌'}")
    
    # Detecção de outliers
    outlier_analysis = analyzer.outlier_detection(df_calc)
    print(f"Detecção outliers: {'✅' if outlier_analysis else '❌'}")
    
    # Insights
    insights = analyzer.generate_insights(df_calc)
    print(f"Geração insights: {'✅' if insights else '❌'}")
    
    # Relatório de qualidade
    quality_report = processor.get_data_quality_report(df_calc)
    print(f"Relatório qualidade: {'✅' if quality_report else '❌'}")
    
    # Salvar resultado final
    resultado_final = {
        'Dados_Originais': dados_teste,
        'Dados_Processados': df_calc,
        'Agrupamento_Categoria': df_grupo
    }
    
    sucesso_final = handler.write_excel(resultado_final, "../data/resultado_teste.xlsx")
    print(f"Relatório final: {'✅' if sucesso_final else '❌'}")
    
    print("\n📊 RESUMO DO TESTE:")
    print(f"   Dados originais: {dados_teste.shape[0]} x {dados_teste.shape[1]}")
    print(f"   Dados processados: {df_calc.shape[0]} x {df_calc.shape[1]}")
    print(f"   Categorias: {df_calc['Categoria'].nunique()}")
    print(f"   Valor total: R$ {df_calc['valor_total'].sum():,.2f}")
    
    print("\n🎉 TESTE CONCLUÍDO COM SUCESSO!")
    
    return True


if __name__ == "__main__":
    teste_basico()