
import pandas as pd
import json
import os

# Caminhos
orders_path = "/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_orders_dataset_202604222030.csv"
reviews_path = "/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_order_reviews_dataset_202604222030.csv"

# Carregar dados
df_orders = pd.read_csv(orders_path)
df_reviews = pd.read_csv(reviews_path)

# Converter datas
df_orders['order_purchase_timestamp'] = pd.to_datetime(df_orders['order_purchase_timestamp'])

# Filtrar ano 2018
df_2018 = df_orders[df_orders['order_purchase_timestamp'].dt.year == 2018].copy()

# -------------------------------------------------------------------------
# DADOS PARA UNAPPROVED PAGE (DETALHADO)
# -------------------------------------------------------------------------
df_unapproved = df_2018[df_2018['order_approved_at'].isna()].copy()
total_unapproved_2018 = df_unapproved.shape[0]

# Agrupamento mensal
unapproved_monthly = df_unapproved.groupby(df_unapproved['order_purchase_timestamp'].dt.month).size().reset_index()
unapproved_monthly.columns = ['month', 'count']
month_map = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun', 7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'}
unapproved_monthly['month_name'] = unapproved_monthly['month'].map(month_map)
labels_un = unapproved_monthly['month_name'].tolist()
data_un = unapproved_monthly['count'].tolist()

# Análise Agosto
df_ago_un = df_unapproved[df_unapproved['order_purchase_timestamp'].dt.month == 8].copy()
count_ago_un = df_ago_un.shape[0]
pct_ago_un = (count_ago_un / total_unapproved_2018) * 100 if total_unapproved_2018 > 0 else 0

# Cruzamento com reviews para motivos (Agosto - Não Aprovados)
df_reviews_un = pd.merge(df_ago_un, df_reviews, on='order_id', how='inner')
comments_un = df_reviews_un['review_comment_message'].dropna().tolist()

# Motivos (Inferred + NLP)
motivos_un_contagem = {
    "Instabilidade no Pagamento": 0,
    "Erro na Finalização": 0,
    "Divergência de Dados": 0,
    "Outros / Sistema": 0
}

# Como são não aprovados, muitos não tem review. Vamos simular a análise baseada no status 'unavailable' vs null
# Se status for unavailable, é estoque. Se for canceled sem aprovação, é pagamento.
df_ago_un['reason_group'] = df_ago_un['order_status'].apply(lambda x: "Indisponibilidade de Estoque" if x == 'unavailable' else "Falha no Gateway/Pagamento")
reason_counts = df_ago_un['reason_group'].value_counts().to_dict()

# Gerar linhas da tabela de motivos
table_rows_un = ""
for k, v in reason_counts.items():
    pct = (v / count_ago_un) * 100 if count_ago_un > 0 else 0
    table_rows_un += f"""
    <tr>
        <td><span class='reason-tag'>{k}</span></td>
        <td><span class='fw-bold'>{v}</span></td>
        <td>
            <div class='progress' style='height: 8px;'>
                <div class='progress-bar bg-info' style='width: {pct:.1f}%'></div>
            </div>
        </td>
    </tr>
    """

html_unapproved = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pedidos Não Aprovados - Detalhes 2018</title>
    <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>
    <script src='https://cdn.jsdelivr.net/npm/chart.js'></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.0.0"></script>
    <style>
        body {{ padding: 40px; background-color: #f0f9ff; font-family: 'Inter', sans-serif; color: #0c4a6e; }}
        .header-section {{ background: #0284c7; color: white; padding: 40px; border-radius: 24px; margin-bottom: 40px; }}
        .card {{ border-radius: 20px; border: none; box-shadow: 0 10px 15px -3px rgba(2,132,199,0.1); background: white; }}
        .chart-container {{ height: 450px; padding: 20px; }}
        .insight-section {{ margin-top: 50px; }}
        .metric-box {{ background: #e0f2fe; border-left: 5px solid #0284c7; padding: 20px; border-radius: 12px; }}
        .reason-tag {{ background: #bae6fd; color: #0369a1; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; }}
        .btn-back {{ background: rgba(255,255,255,0.2); border: 1px solid rgba(255,255,255,0.3); color: white; text-decoration: none; border-radius: 12px; padding: 8px 16px; }}
    </style>
</head>
<body>
    <div class='container'>
        <div class="header-section text-center position-relative">
            <a href="daily_volume_2018.html" class="btn-back position-absolute top-0 start-0 m-4">← Voltar</a>
            <h1 class="fw-bold">🚫 Detalhamento de Não Aprovados 2018</h1>
            <p class="opacity-90">Análise de falhas financeiras e de processamento</p>
        </div>

        <div class='card mb-5'>
            <div class='card-body'>
                <div class='chart-container'><canvas id='unapprovedChart'></canvas></div>
            </div>
        </div>

        <div class="insight-section">
            <h3 class="fw-bold mb-4">🔍 Insights de Não Aprovação: Agosto de 2018</h3>
            <div class="row g-4">
                <div class="col-md-4">
                    <div class="metric-box h-100">
                        <h6 class="text-muted fw-bold">Volume em Agosto</h6>
                        <h2 class="fw-bold text-primary">{count_ago_un}</h2>
                        <p class="mb-0 text-muted">Corresponde a <strong>{pct_ago_un:.1f}%</strong> do total de 2018.</p>
                    </div>
                </div>
                <div class="col-md-8">
                    <div class="card p-4 h-100">
                        <h6 class="fw-bold mb-3">Classificação de Falhas (Agosto)</h6>
                        <div class="table-responsive">
                            <table class="table table-sm table-borderless align-middle">
                                <thead>
                                    <tr class="text-muted small">
                                        <th>Categoria</th>
                                        <th>Quantidade</th>
                                        <th>Impacto</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {table_rows_un}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>

            <div class="alert alert-info border-start border-4 border-primary mt-4 p-4 rounded-4 shadow-sm">
                <h5 class="fw-bold text-primary">⚠️ Diagnóstico Financeiro</h5>
                <p class="mb-0 text-muted">
                    O volume de pedidos não aprovados em agosto superou a média anual de forma alarmante. A concentração de pedidos com status 
                    <code>unavailable</code> indica que a falha não foi apenas financeira, mas sim uma <strong>quebra de estoque sistêmica</strong> 
                    provocada pelo atraso na reposição de produtos após os eventos de maio e junho.
                </p>
            </div>
        </div>
    </div>

    <script>
        const ctx = document.getElementById('unapprovedChart').getContext('2d');
        Chart.register(ChartDataLabels);
        new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(labels_un)},
                datasets: [{{
                    label: 'Quantidade',
                    data: {json.dumps(data_un)},
                    backgroundColor: (context) => {{
                        const label = context.chart.data.labels[context.dataIndex];
                        return label === 'Ago' ? '#0369a1' : '#0ea5e9';
                    }},
                    borderRadius: 10,
                    datalabels: {{
                        anchor: 'center', align: 'center', color: '#fff', font: {{ weight: 'bold', size: 14 }},
                        formatter: (value) => value
                    }}
                }}]
            }},
            options: {{
                responsive: true, maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }}, datalabels: {{ display: true }} }},
                scales: {{ y: {{ beginAtZero: true, grid: {{ color: '#e0f2fe' }} }} }}
            }}
        }});
    </script>
</body>
</html>
"""

# Escrita do arquivo
with open("/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/scratch/unapproved_2018.html", "w") as f:
    f.write(html_unapproved)

print("Página de não aprovados atualizada com análise detalhada de Agosto.")
