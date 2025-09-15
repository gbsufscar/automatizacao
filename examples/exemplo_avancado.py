"""
Exemplo Avançado - Automação Excel com recursos complexos
Demonstra funcionalidades avançadas como análise temporal, filtros complexos e relatórios executivos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Backend não-interativo

from excel_automation import ExcelHandler, ExcelDataProcessor, DataAnalyzer, DataVisualizer
from datetime import datetime, timedelta


def gerar_dados_vendas_avancados():
    """Gera dados de vendas mais complexos para demonstração"""
    
    np.random.seed(42)
    
    # Configurações
    n_records = 2000
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    # Listas de dados
    vendedores = ['Ana Silva', 'João Santos', 'Maria Oliveira', 'Pedro Costa', 
                 'Julia Lima', 'Carlos Ferreira', 'Lucia Martins', 'Roberto Alves']
    
    produtos = ['Notebook Dell', 'Mouse Logitech', 'Teclado Mecânico', 'Monitor 24"', 
               'Webcam HD', 'Headset Gamer', 'SSD 500GB', 'Impressora Laser',
               'Tablet Android', 'Smartphone', 'Roteador Wi-Fi', 'Cabo HDMI']
    
    categorias = {'Notebook Dell': 'Computadores', 'Mouse Logitech': 'Periféricos',
                 'Teclado Mecânico': 'Periféricos', 'Monitor 24"': 'Monitores',
                 'Webcam HD': 'Periféricos', 'Headset Gamer': 'Periféricos',
                 'SSD 500GB': 'Armazenamento', 'Impressora Laser': 'Impressoras',
                 'Tablet Android': 'Dispositivos Móveis', 'Smartphone': 'Dispositivos Móveis',
                 'Roteador Wi-Fi': 'Rede', 'Cabo HDMI': 'Cabos'}
    
    regioes = ['Norte', 'Sul', 'Leste', 'Oeste', 'Centro']
    cidades = {'Norte': ['Manaus', 'Belém'], 'Sul': ['Porto Alegre', 'Curitiba'],
              'Leste': ['Rio de Janeiro', 'Vitória'], 'Oeste': ['Campo Grande', 'Cuiabá'],
              'Centro': ['Brasília', 'Goiânia']}
    
    # Gerar dados
    dados = []
    
    for i in range(n_records):
        # Data aleatória no período
        random_days = np.random.randint(0, (end_date - start_date).days)
        data_venda = start_date + timedelta(days=random_days)
        
        # Selecionar valores correlacionados
        vendedor = np.random.choice(vendedores)
        produto = np.random.choice(produtos)
        categoria = categorias[produto]
        regiao = np.random.choice(regioes)
        cidade = np.random.choice(cidades[regiao])
        
        # Valores baseados no produto (preços realistas)
        precos_base = {
            'Notebook Dell': (2000, 5000), 'Mouse Logitech': (50, 150),
            'Teclado Mecânico': (200, 500), 'Monitor 24"': (800, 1500),
            'Webcam HD': (100, 300), 'Headset Gamer': (150, 400),
            'SSD 500GB': (300, 600), 'Impressora Laser': (500, 1200),
            'Tablet Android': (800, 2000), 'Smartphone': (1000, 3000),
            'Roteador Wi-Fi': (100, 400), 'Cabo HDMI': (20, 80)
        }
        
        preco_min, preco_max = precos_base[produto]
        valor_venda = np.random.uniform(preco_min, preco_max)
        
        # Quantidade baseada no tipo de produto
        if categoria in ['Computadores', 'Dispositivos Móveis']:
            quantidade = np.random.randint(1, 3)
        elif categoria in ['Monitores', 'Impressoras']:
            quantidade = np.random.randint(1, 5)
        else:
            quantidade = np.random.randint(1, 10)
        
        # Desconto baseado na quantidade
        if quantidade >= 5:
            desconto = np.random.uniform(5, 15)
        elif quantidade >= 3:
            desconto = np.random.uniform(2, 8)
        else:
            desconto = np.random.uniform(0, 5)
        
        # Custo (margem entre 20% e 40%)
        margem = np.random.uniform(0.2, 0.4)
        custo = valor_venda * (1 - margem)
        
        # Canal de venda
        canal = np.random.choice(['Online', 'Loja Física', 'Telefone'], 
                                p=[0.6, 0.3, 0.1])
        
        # Status do pedido
        status = np.random.choice(['Concluído', 'Processando', 'Cancelado'], 
                                 p=[0.85, 0.1, 0.05])
        
        dados.append({
            'data_venda': data_venda,
            'vendedor': vendedor,
            'produto': produto,
            'categoria': categoria,
            'regiao': regiao,
            'cidade': cidade,
            'canal': canal,
            'quantidade': quantidade,
            'valor_unitario': round(valor_venda, 2),
            'desconto_pct': round(desconto, 2),
            'custo_unitario': round(custo, 2),
            'status': status
        })
    
    df = pd.DataFrame(dados)
    
    # Adicionar algumas inconsistências para demonstrar limpeza
    # Valores ausentes
    indices_na = np.random.choice(len(df), size=100, replace=False)
    df.loc[indices_na[:50], 'desconto_pct'] = np.nan
    df.loc[indices_na[50:], 'custo_unitario'] = np.nan
    
    # Duplicatas
    duplicatas = df.sample(50)
    df = pd.concat([df, duplicatas], ignore_index=True)
    
    # Dados inconsistentes
    df.loc[100:110, 'vendedor'] = df.loc[100:110, 'vendedor'].str.lower()
    
    return df


def exemplo_analise_vendas_avancada():
    """Exemplo completo de análise de vendas avançada"""
    
    print("🚀 ANÁLISE AVANÇADA DE VENDAS - AUTOMAÇÃO EXCEL")
    print("=" * 60)
    
    # 1. GERAR E PREPARAR DADOS
    print("\n📊 1. Gerando dados de vendas avançados...")
    df_vendas = gerar_dados_vendas_avancados()
    print(f"   Dados gerados: {df_vendas.shape[0]} registros")
    
    # Inicializar componentes
    handler = ExcelHandler()
    processor = ExcelDataProcessor()
    analyzer = DataAnalyzer()
    visualizer = DataVisualizer()
    
    # 2. SALVAR DADOS ORIGINAIS
    print("\n💾 2. Salvando dados originais...")
    os.makedirs("../data", exist_ok=True)
    handler.write_excel(df_vendas, "../data/vendas_brutas.xlsx")
    
    # 3. LIMPEZA E PROCESSAMENTO AVANÇADO
    print("\n🧹 3. Limpeza e processamento avançado...")
    
    # Limpeza básica
    df_clean = processor.clean_data(
        df_vendas, 
        remove_duplicates=True, 
        handle_missing='fill',
        standardize_text=True
    )
    
    # Transformações avançadas
    transformations = {
        'vendedor': 'title',
        'produto': 'title', 
        'categoria': 'title',
        'valor_unitario': 'numeric',
        'desconto_pct': 'numeric'
    }
    df_clean = processor.transform_columns(df_clean, transformations)
    
    # Colunas calculadas complexas
    calculations = {
        'valor_bruto': 'valor_unitario * quantidade',
        'valor_desconto': 'valor_bruto * desconto_pct / 100',
        'valor_liquido': 'valor_bruto - valor_desconto',
        'custo_total': 'custo_unitario * quantidade',
        'lucro_bruto': 'valor_liquido - custo_total',
        'margem_lucro': 'lucro_bruto / valor_liquido * 100',
        'ticket_medio': 'valor_liquido / quantidade'
    }
    df_processed = processor.create_calculated_columns(df_clean, calculations)
    
    # Filtros avançados
    filtros = {
        'status': 'Concluído',  # Apenas vendas concluídas
        'valor_liquido': {'min': 50},  # Vendas acima de R$ 50
        'quantidade': {'min': 1, 'max': 50}  # Quantidades válidas
    }
    df_filtered = processor.filter_data(df_processed, filtros)
    
    print(f"   Dados após processamento: {df_filtered.shape[0]} registros")
    
    # 4. ANÁLISES AVANÇADAS
    print("\n📈 4. Realizando análises avançadas...")
    
    # Análise descritiva completa
    desc_analysis = analyzer.descriptive_analysis(df_filtered)
    
    # Análise de correlação
    corr_analysis = analyzer.correlation_analysis(df_filtered, min_correlation=0.3)
    
    # Detecção de outliers
    outlier_analysis = analyzer.outlier_detection(df_filtered, method='iqr')
    
    # Análise temporal
    trend_analysis = analyzer.trend_analysis(
        df_filtered, 
        'data_venda', 
        ['valor_liquido', 'lucro_bruto'], 
        period='M'
    )
    
    # Insights automáticos
    insights = analyzer.generate_insights(df_filtered)
    
    # 5. AGREGAÇÕES EXECUTIVAS
    print("\n📊 5. Criando agregações executivas...")
    
    # Vendas por vendedor
    vendas_vendedor = processor.group_and_aggregate(
        df_filtered,
        'vendedor',
        {
            'valor_liquido': ['sum', 'mean', 'count'],
            'lucro_bruto': 'sum',
            'quantidade': 'sum'
        }
    )
    
    # Vendas por categoria
    vendas_categoria = processor.group_and_aggregate(
        df_filtered,
        'categoria',
        {
            'valor_liquido': 'sum',
            'lucro_bruto': 'sum',
            'margem_lucro': 'mean'
        }
    )
    
    # Vendas por região e canal
    vendas_regiao_canal = processor.group_and_aggregate(
        df_filtered,
        ['regiao', 'canal'],
        {
            'valor_liquido': 'sum',
            'quantidade': 'sum'
        }
    )
    
    # Tabela dinâmica: Vendedor vs Categoria
    pivot_vendedor_categoria = processor.pivot_data(
        df_filtered,
        index='vendedor',
        columns='categoria',
        values='valor_liquido',
        aggfunc='sum'
    )
    
    # 6. ANÁLISES TEMPORAIS DETALHADAS
    print("\n📅 6. Análises temporais detalhadas...")
    
    # Adicionar colunas de tempo
    df_temporal = df_filtered.copy()
    df_temporal['ano'] = df_temporal['data_venda'].dt.year
    df_temporal['mes'] = df_temporal['data_venda'].dt.month
    df_temporal['trimestre'] = df_temporal['data_venda'].dt.quarter
    df_temporal['dia_semana'] = df_temporal['data_venda'].dt.day_name()
    
    # Vendas por mês
    vendas_mensais = processor.group_and_aggregate(
        df_temporal,
        ['ano', 'mes'],
        {
            'valor_liquido': 'sum',
            'lucro_bruto': 'sum',
            'quantidade': 'sum'
        }
    )
    
    # Vendas por dia da semana
    vendas_dia_semana = processor.group_and_aggregate(
        df_temporal,
        'dia_semana',
        {
            'valor_liquido': ['sum', 'mean'],
            'quantidade': 'sum'
        }
    )
    
    # 7. RELATÓRIO EXECUTIVO
    print("\n📋 7. Criando relatório executivo...")
    
    # Métricas principais
    metricas_principais = {
        'Receita Total': df_filtered['valor_liquido'].sum(),
        'Lucro Total': df_filtered['lucro_bruto'].sum(),
        'Margem Média': df_filtered['margem_lucro'].mean(),
        'Ticket Médio': df_filtered['valor_liquido'].mean(),
        'Vendas Totais': len(df_filtered),
        'Produtos Únicos': df_filtered['produto'].nunique(),
        'Vendedores Ativos': df_filtered['vendedor'].nunique(),
        'Regiões Ativas': df_filtered['regiao'].nunique()
    }
    
    # Top performers
    top_vendedores = vendas_vendedor.nlargest(5, 'valor_liquido_sum')
    top_produtos_data = processor.group_and_aggregate(
        df_filtered,
        'produto',
        {'valor_liquido': 'sum'}
    )
    top_produtos = top_produtos_data.nlargest(10, 'valor_liquido')
    
    # 8. SALVAR RELATÓRIOS COMPLETOS
    print("\n💾 8. Salvando relatórios completos...")
    
    # Relatório principal
    relatorio_principal = {
        'Dados_Processados': df_filtered,
        'Vendas_por_Vendedor': vendas_vendedor,
        'Vendas_por_Categoria': vendas_categoria,
        'Vendas_Regiao_Canal': vendas_regiao_canal,
        'Vendas_Mensais': vendas_mensais,
        'Vendas_Dia_Semana': vendas_dia_semana,
        'Top_Vendedores': top_vendedores,
        'Top_Produtos': top_produtos,
        'Pivot_Vendedor_Categoria': pivot_vendedor_categoria
    }
    
    handler.write_excel(relatorio_principal, "../data/relatorio_vendas_completo.xlsx")
    
    # Relatório executivo
    metricas_df = pd.DataFrame([metricas_principais]).T.reset_index()
    metricas_df.columns = ['Métrica', 'Valor']
    
    relatorio_executivo = {
        'Resumo_Executivo': metricas_df,
        'Top_5_Vendedores': top_vendedores,
        'Top_10_Produtos': top_produtos,
        'Insights_Automaticos': pd.DataFrame({'Insight': insights})
    }
    
    handler.write_excel(relatorio_executivo, "../data/relatorio_executivo.xlsx")
    
    # 9. RELATÓRIO FINAL
    print("\n📊 9. RELATÓRIO FINAL")
    print("-" * 50)
    print(f"💰 Receita Total: R$ {metricas_principais['Receita Total']:,.2f}")
    print(f"💼 Lucro Total: R$ {metricas_principais['Lucro Total']:,.2f}")
    print(f"📈 Margem Média: {metricas_principais['Margem Média']:.1f}%")
    print(f"🎫 Ticket Médio: R$ {metricas_principais['Ticket Médio']:,.2f}")
    print(f"📦 Total de Vendas: {metricas_principais['Vendas Totais']:,}")
    print(f"👥 Vendedores Ativos: {metricas_principais['Vendedores Ativos']}")
    print(f"🗺️ Regiões Ativas: {metricas_principais['Regiões Ativas']}")
    
    print(f"\n🏆 TOP VENDEDOR: {top_vendedores.iloc[0]['vendedor']}")
    print(f"   Vendas: R$ {top_vendedores.iloc[0]['valor_liquido_sum']:,.2f}")
    
    print(f"\n⭐ PRODUTO MAIS VENDIDO: {top_produtos.iloc[0]['produto']}")
    print(f"   Receita: R$ {top_produtos.iloc[0]['valor_liquido']:,.2f}")
    
    print("\n💡 PRINCIPAIS INSIGHTS:")
    for i, insight in enumerate(insights[:5], 1):
        print(f"   {i}. {insight}")
    
    print("\n📁 ARQUIVOS GERADOS:")
    print("   📊 ../data/vendas_brutas.xlsx - Dados originais")
    print("   📋 ../data/relatorio_vendas_completo.xlsx - Relatório detalhado")
    print("   🎯 ../data/relatorio_executivo.xlsx - Resumo executivo")
    
    print("\n🎉 ANÁLISE AVANÇADA CONCLUÍDA COM SUCESSO!")
    
    return df_filtered, relatorio_principal


if __name__ == "__main__":
    exemplo_analise_vendas_avancada()