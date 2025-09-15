# 🚀 Automação Excel com Python

Este repositório contém uma solução completa para automatizar o tratamento de dados do Excel usando Python, substituindo tarefas manuais por processos automáticos eficientes.

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Instalação](#-instalação)
- [Uso Rápido](#-uso-rápido)
- [Funcionalidades](#-funcionalidades)
- [Exemplos](#-exemplos)
- [Documentação](#-documentação)
- [Contribuição](#-contribuição)

## 🎯 Visão Geral

Esta biblioteca Python permite automatizar tarefas comuns do Excel como:

- ✅ Leitura e escrita de arquivos Excel (.xlsx, .xls, .xlsm)
- 🧹 Limpeza e processamento de dados
- 📊 Análise estatística e detecção de outliers
- 📈 Criação de visualizações e dashboards
- 🔄 Agregações e tabelas dinâmicas
- 📋 Geração de relatórios automáticos

**Substitua horas de trabalho manual por minutos de automação!**

## 🛠 Instalação

### Pré-requisitos
- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Instalação das dependências

```bash
# Clone o repositório
git clone https://github.com/gbsufscar/automatizacao.git
cd automatizacao

# Instale as dependências
pip install -r requirements.txt
```

### Dependências principais
- `pandas` - Manipulação de dados
- `openpyxl` - Leitura/escrita Excel
- `matplotlib/seaborn` - Visualizações
- `plotly` - Dashboards interativos
- `numpy` - Computação numérica

## ⚡ Uso Rápido

### Exemplo Básico

```python
from excel_automation import ExcelHandler, ExcelDataProcessor, DataAnalyzer

# 1. Ler arquivo Excel
handler = ExcelHandler()
df = handler.read_excel("dados.xlsx")

# 2. Limpar dados
processor = ExcelDataProcessor()
df_limpo = processor.clean_data(df, remove_duplicates=True)

# 3. Analisar dados
analyzer = DataAnalyzer()
analise = analyzer.descriptive_analysis(df_limpo)

# 4. Salvar resultado
handler.write_excel(df_limpo, "dados_processados.xlsx")
```

### Scripts Prontos

```bash
# Gerar relatório automático
python examples/uso_rapido.py relatorio --arquivo dados.xlsx

# Tutorial passo a passo
python examples/tutorial_passo_a_passo.py

# Exemplo completo
python examples/exemplo_basico.py
```

## 🚀 Funcionalidades

### 📖 Manipulação de Excel
- Leitura de múltiplas planilhas
- Escrita com formatação
- Informações detalhadas dos arquivos
- Suporte a diferentes formatos

### 🧹 Processamento de Dados
- Limpeza automática (duplicatas, valores ausentes)
- Transformações de texto e números
- Colunas calculadas
- Filtros avançados
- Validação de qualidade

### 📊 Análise Estatística
- Estatísticas descritivas
- Análise de correlação
- Detecção de outliers
- Análise de tendências temporais
- Insights automáticos

### 📈 Visualizações
- Histogramas e distribuições
- Mapas de correlação
- Gráficos categóricos
- Séries temporais
- Dashboards interativos

### 🔄 Agregações
- Agrupamentos por categorias
- Tabelas dinâmicas
- Múltiplas funções de agregação
- Resumos estatísticos

## 📚 Exemplos

### 1. Análise de Vendas

```python
from excel_automation import *

# Carregar dados de vendas
handler = ExcelHandler()
vendas = handler.read_excel("vendas.xlsx")

# Processar dados
processor = ExcelDataProcessor()
vendas_limpo = processor.clean_data(vendas)

# Criar colunas calculadas
vendas_calc = processor.create_calculated_columns(vendas_limpo, {
    'receita_total': 'preco * quantidade',
    'margem': '(preco - custo) / preco * 100'
})

# Análise por vendedor
vendas_vendedor = processor.group_and_aggregate(
    vendas_calc, 
    'vendedor', 
    {'receita_total': 'sum', 'quantidade': 'sum'}
)

# Visualizar resultados
visualizer = DataVisualizer()
visualizer.plot_categorical_analysis(vendas_vendedor)

# Salvar relatório
relatorio = {
    'Vendas_Processadas': vendas_calc,
    'Resumo_Vendedores': vendas_vendedor
}
handler.write_excel(relatorio, "relatorio_vendas.xlsx")
```

### 2. Dashboard Interativo

```python
# Criar dashboard interativo
dashboard = visualizer.create_interactive_dashboard(
    vendas_calc, 
    "Dashboard de Vendas"
)

# Exportar como HTML
visualizer.export_interactive_html(dashboard, "dashboard_vendas.html")
```

### 3. Comparação de Arquivos

```python
# Comparar dois arquivos Excel
python examples/uso_rapido.py comparar --arquivo dados1.xlsx --arquivo2 dados2.xlsx --chave ID
```

## 📖 Documentação

### Estrutura do Projeto

```
automatizacao/
├── excel_automation/          # Pacote principal
│   ├── __init__.py           # Inicialização
│   ├── excel_handler.py      # Manipulação Excel
│   ├── data_processor.py     # Processamento dados
│   ├── data_analyzer.py      # Análise estatística
│   └── data_visualizer.py    # Visualizações
├── examples/                 # Exemplos de uso
│   ├── exemplo_basico.py     # Exemplo básico
│   ├── tutorial_passo_a_passo.py  # Tutorial
│   └── uso_rapido.py         # Scripts utilitários
├── data/                     # Dados de exemplo
├── plots/                    # Gráficos gerados
└── requirements.txt          # Dependências
```

### Classes Principais

#### ExcelHandler
- `read_excel()` - Ler arquivos Excel
- `write_excel()` - Escrever arquivos Excel
- `get_sheet_names()` - Listar planilhas
- `get_excel_info()` - Informações do arquivo

#### ExcelDataProcessor
- `clean_data()` - Limpeza de dados
- `filter_data()` - Filtros
- `transform_columns()` - Transformações
- `create_calculated_columns()` - Colunas calculadas
- `group_and_aggregate()` - Agrupamentos

#### DataAnalyzer
- `descriptive_analysis()` - Estatísticas descritivas
- `correlation_analysis()` - Análise de correlação
- `outlier_detection()` - Detecção de outliers
- `trend_analysis()` - Análise temporal
- `generate_insights()` - Insights automáticos

#### DataVisualizer
- `plot_distribution()` - Distribuições
- `plot_correlation_heatmap()` - Mapa de correlação
- `plot_categorical_analysis()` - Análise categórica
- `create_interactive_dashboard()` - Dashboard interativo

## 🎯 Casos de Uso

### 📊 Análise Financeira
- Processamento de demonstrativos
- Análise de fluxo de caixa
- Detecção de anomalias
- Relatórios executivos

### 📈 Análise de Vendas
- Performance de vendedores
- Análise de produtos
- Tendências temporais
- Dashboards gerenciais

### 🏭 Controle de Qualidade
- Análise de defeitos
- Controle estatístico
- Relatórios de qualidade
- Monitoramento KPIs

### 📋 Relatórios Operacionais
- Consolidação de dados
- Relatórios automáticos
- Dashboards executivos
- Análises comparativas

## 🔧 Configuração Avançada

### Personalização de Visualizações

```python
# Configurar estilo
visualizer = DataVisualizer(figsize=(15, 10))

# Salvar múltiplos formatos
visualizer.save_all_plots(
    df, 
    output_dir="relatorios", 
    formats=['png', 'pdf', 'svg']
)
```

### Processamento em Lote

```python
# Processar múltiplos arquivos
import glob

for arquivo in glob.glob("dados/*.xlsx"):
    df = handler.read_excel(arquivo)
    df_processado = processor.clean_data(df)
    handler.write_excel(df_processado, f"processados/{arquivo}")
```

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para detalhes.

## ⭐ Apoie o Projeto

Se este projeto foi útil para você, considere dar uma ⭐ no repositório!

## 📞 Suporte

- 📧 Email: suporte@automatizacao.com
- 💬 Issues: [GitHub Issues](https://github.com/gbsufscar/automatizacao/issues)
- 📖 Wiki: [Documentação Completa](https://github.com/gbsufscar/automatizacao/wiki)

---

**Transforme sua análise de dados Excel em um processo automático e eficiente! 🚀**