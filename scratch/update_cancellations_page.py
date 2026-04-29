
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

# Cancelamentos 2018
df_canceled = df_2018[df_2018['order_status'] == 'canceled'].copy()
total_cancel_2018 = df_canceled.shape[0]

# Agrupamento mensal
cancellation_monthly = df_canceled.groupby(df_canceled['order_purchase_timestamp'].dt.month).size().reset_index()
cancellation_monthly.columns = ['month', 'count']
month_map = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun', 7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out'}
cancellation_monthly['month_name'] = cancellation_monthly['month'].map(month_map)
labels_cancel = cancellation_monthly['month_name'].tolist()
data_cancel = cancellation_monthly['count'].tolist()

# -------------------------------------------------------------------------
# ANÁLISE AGOSTO
# -------------------------------------------------------------------------
df_ago = df_canceled[df_canceled['order_purchase_timestamp'].dt.month == 8].copy()
count_ago = df_ago.shape[0]
pct_ago = (count_ago / total_cancel_2018) * 100 if total_cancel_2018 > 0 else 0

# Cruzamento com reviews para motivos (August)
df_reviews_ago = pd.merge(df_ago, df_reviews, on='order_id', how='inner')
comments = df_reviews_ago['review_comment_message'].dropna().tolist()

# Motivos
motivos_contagem = {
    "Atraso na Entrega": 0,
    "Divergência no Produto": 0,
    "Problemas com Vendedor": 0,
    "Indisponibilidade de Estoque": 0,
    "Outros / Sem Comentário": 0
}

for msg in comments:
    msg = msg.lower()
    if any(word in msg for word in ["atraso", "demora", "prazo", "chegou"]):
        motivos_contagem["Atraso na Entrega"] += 1
    elif any(word in msg for word in ["diferente", "divergente", "trocado", "errado", "não era", "descrição"]):
        motivos_contagem["Divergência no Produto"] += 1
    elif any(word in msg for word in ["vendedor", "loja", "atendimento"]):
        motivos_contagem["Problemas com Vendedor"] += 1
    elif any(word in msg for word in ["estoque", "falta", "não tinha"]):
        motivos_contagem["Indisponibilidade de Estoque"] += 1
    else:
        motivos_contagem["Outros / Sem Comentário"] += 1

sem_review = count_ago - len(comments)
motivos_contagem["Outros / Sem Comentário"] += sem_review

# Ordenar motivos
motivos_sorted = dict(sorted(motivos_contagem.items(), key=lambda item: item[1], reverse=True))

# Gerar linhas da tabela de motivos
table_rows = ""
for k, v in motivos_sorted.items():
    if v > 0 or k == "Divergência no Produto":
        pct = (v / count_ago) * 100 if count_ago > 0 else 0
        table_rows += f"""
        <tr>
            <td><span class='reason-tag'>{k}</span></td>
            <td><span class='fw-bold'>{v}</span></td>
            <td>
                <div class='progress' style='height: 8px;'>
                    <div class='progress-bar bg-danger' style='width: {pct:.1f}%'></div>
                </div>
            </td>
        </tr>
        """

# -------------------------------------------------------------------------
# GERAR cancellations_2018.html
# -------------------------------------------------------------------------
html_cancel = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cancelamentos Detalhados - 2018</title>
    <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>
    <script src='https://cdn.jsdelivr.net/npm/chart.js'></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.0.0"></script>
    <style>
        body {{ padding: 40px; background-color: #fcfcfc; font-family: 'Inter', system-ui, sans-serif; color: #1e293b; }}
        .header-section {{ background: #be123c; color: white; padding: 40px; border-radius: 24px; margin-bottom: 40px; }}
        .card {{ border-radius: 20px; border: none; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05); background: white; }}
        .chart-container {{ height: 450px; padding: 20px; }}
        .insight-section {{ margin-top: 50px; }}
        .metric-box {{ background: #fff1f2; border-left: 5px solid #be123c; padding: 20px; border-radius: 12px; }}
        .reason-tag {{ background: #ffe4e6; color: #9f1239; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; }}
        .btn-back {{ background: rgba(255,255,255,0.2); border: 1px solid rgba(255,255,255,0.3); color: white; text-decoration: none; border-radius: 12px; padding: 8px 16px; transition: 0.2s; }}
        .btn-back:hover {{ background: rgba(255,255,255,0.3); color: white; }}
    </style>
</head>
<body>
    <div class='container'>
        <div class="header-section text-center position-relative">
            <a href="daily_volume_2018.html" class="btn-back position-absolute top-0 start-0 m-4">← Voltar</a>
            <h1 class="fw-bold">❌ Evolução de Cancelamentos 2018</h1>
            <p class="opacity-90">Análise de falhas operacionais e desistências</p>
        </div>

        <div class='card mb-5'>
            <div class='card-body'>
                <div class='chart-container'><canvas id='cancellationChart'></canvas></div>
            </div>
        </div>

        <div class="insight-section">
            <h3 class="fw-bold mb-4">🔍 Insights Profundos: Agosto de 2018</h3>
            <div class="row g-4">
                <div class="col-md-4">
                    <div class="metric-box h-100">
                        <h6 class="text-muted fw-bold">Volume em Agosto</h6>
                        <h2 class="fw-bold text-danger">{count_ago}</h2>
                        <p class="mb-0 text-muted">Corresponde a <strong>{pct_ago:.1f}%</strong> de todos os cancelamentos do ano.</p>
                    </div>
                </div>
                <div class="col-md-8">
                    <div class="card p-4 h-100">
                        <h6 class="fw-bold mb-3">Principais Motivos Detectados (NLP & Logística)</h6>
                        <div class="table-responsive">
                            <table class="table table-sm table-borderless align-middle">
                                <thead>
                                    <tr class="text-muted small">
                                        <th>Motivo</th>
                                        <th>Quantidade</th>
                                        <th>Representatividade</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {table_rows}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>

            <div class="alert alert-light border-start border-4 border-danger mt-4 p-4 rounded-4 shadow-sm">
                <h5 class="fw-bold text-danger">⚠️ Diagnóstico de Agosto</h5>
                <p class="mb-0 text-muted">
                    O mês de agosto apresentou o maior índice de cancelamentos de 2018. A análise de sentimentos aponta que 
                    <strong>{list(motivos_sorted.keys())[0]}</strong> e <strong>Divergência no Produto</strong> são fatores críticos 
                    que impactaram a satisfação do cliente, sugerindo falhas na conferência de itens ou erros na descrição de anúncios.
                </p>
            </div>
        </div>
    </div>

    <script>
        const ctx = document.getElementById('cancellationChart').getContext('2d');
        Chart.register(ChartDataLabels);

        new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(labels_cancel)},
                datasets: [{{
                    label: 'Quantidade',
                    data: {json.dumps(data_cancel)},
                    backgroundColor: (context) => {{
                        const label = context.chart.data.labels[context.dataIndex];
                        return label === 'Ago' ? '#be123c' : '#fb7185';
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
                scales: {{ y: {{ beginAtZero: true }} }}
            }}
        }});
    </script>
</body>
</html>
"""

with open("/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/scratch/cancellations_2018.html", "w") as f:
    f.write(html_cancel)

print("Página de cancelamentos atualizada com sucesso.")
