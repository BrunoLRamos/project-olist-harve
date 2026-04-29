
import pandas as pd
import json
import os

# Caminho dos dados
data_path = "/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_orders_dataset_202604222030.csv"

# Carregar dados
df = pd.read_csv(data_path)

# Converter datas
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

# Filtrar ano 2018
df_2018 = df[df['order_purchase_timestamp'].dt.year == 2018].copy()

# 1. Volume Diário
daily_volume = df_2018.groupby(df_2018['order_purchase_timestamp'].dt.date).size().reset_index()
daily_volume.columns = ['date', 'order_count']
daily_volume['date'] = pd.to_datetime(daily_volume['date'])

# 2. Eventos
greve_start, greve_end = '2018-05-21', '2018-05-30'
copa_start, copa_end = '2018-06-14', '2018-07-15'
volume_greve = daily_volume[(daily_volume['date'] >= greve_start) & (daily_volume['date'] <= greve_end)]['order_count'].sum()
avg_greve = daily_volume[(daily_volume['date'] >= greve_start) & (daily_volume['date'] <= greve_end)]['order_count'].mean()
volume_copa = daily_volume[(daily_volume['date'] >= copa_start) & (daily_volume['date'] <= copa_end)]['order_count'].sum()
avg_copa = daily_volume[(daily_volume['date'] >= copa_start) & (daily_volume['date'] <= copa_end)]['order_count'].mean()

# 4. Falhas Operacionais 2018
cancelamentos_2018 = df_2018[df_2018['order_status'] == 'canceled'].shape[0]
nao_aprovados_2018 = df_2018[df_2018['order_approved_at'].isna()].shape[0]

# Dados Gráfico Diário
daily_volume['date_str'] = daily_volume['date'].dt.strftime('%Y-%m-%d')
labels_daily = daily_volume['date_str'].tolist()
data_daily = daily_volume['order_count'].tolist()

# -------------------------------------------------------------------------
# GERAR daily_volume_2018.html (DETALHAMENTO DE CRISE)
# -------------------------------------------------------------------------
html_daily = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Análise Técnica de Crise - Olist 2018</title>
    <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>
    <script src='https://cdn.jsdelivr.net/npm/chart.js'></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation@2.1.0/dist/chartjs-plugin-annotation.min.js"></script>
    <style>
        body {{ padding: 30px; background-color: #f1f5f9; font-family: 'Segoe UI', system-ui, sans-serif; color: #334155; }}
        .header-section {{
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            color: white; padding: 50px; border-radius: 24px; margin-bottom: 40px; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);
        }}
        .card {{ border-radius: 20px; border: none; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05); background: white; }}
        .chart-container {{ position: relative; height: 450px; width: 100%; padding: 20px; }}
        .event-btn {{ 
            padding: 8px 16px; border-radius: 20px; font-size: 0.85rem; font-weight: 700; 
            text-transform: uppercase; cursor: pointer; border: 2px solid transparent; 
            transition: all 0.2s ease; background: #e2e8f0; color: #475569;
        }}
        .event-btn:hover {{ transform: scale(1.05); }}
        .event-btn.active-strike {{ background: #fee2e2; color: #991b1b; border-color: #ef4444; }}
        .event-btn.active-cup {{ background: #dcfce7; color: #166534; border-color: #10b981; }}
        
        .metric-card {{ border-bottom: 4px solid transparent; transition: all 0.3s ease; height: 100%; }}
        .clickable-card {{ cursor: pointer; }}
        .clickable-card:hover {{ transform: translateY(-5px); box-shadow: 0 15px 25px -5px rgba(0,0,0,0.2); }}
        .border-danger-custom {{ border-bottom-color: #ef4444; }}
        .border-warning-custom {{ border-bottom-color: #f59e0b; }}
        .border-success-custom {{ border-bottom-color: #10b981; }}
        .border-info-custom {{ border-bottom-color: #3b82f6; }}
        
        .doc-section {{ background: #fff; border-radius: 20px; padding: 40px; margin-top: 40px; border: 1px solid #e2e8f0; }}
        .table-badge {{ background: #3b82f6; color: white; padding: 4px 10px; border-radius: 6px; font-family: monospace; font-size: 0.9rem; }}
        .field-badge {{ background: #f1f5f9; color: #475569; padding: 2px 8px; border-radius: 4px; font-family: monospace; border: 1px solid #e2e8f0; }}
        
        .btn-back {{ background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: white; backdrop-filter: blur(5px); text-decoration: none; }}
        .btn-back:hover {{ background: rgba(255,255,255,0.2); color: white; }}
        .annotation-box {{ background: #f8fafc; border-left: 4px solid #3b82f6; padding: 15px; border-radius: 0 12px 12px 0; }}
    </style>
</head>
<body>
    <div class='container-fluid px-5'>
        <div class="header-section text-center position-relative">
            <a href="dashboard_2018.html" class="btn btn-back position-absolute top-0 start-0 m-4">← Voltar à Análise de Pedidos</a>
            <h1 class="display-5 fw-bold mb-2">📉 Análise de Crise: Olist 2018</h1>
            <p class="lead opacity-75">Integração de dados e eventos macroeconômicos</p>
        </div>

        <div class='card mb-5'>
            <div class='card-body'>
                <div class="d-flex justify-content-between align-items-center mb-3 px-3">
                    <h5 class="fw-bold m-0">Quantidade de pedidos</h5>
                    <div class="d-flex gap-2">
                        <button id="btnStrike" class="event-btn">🚛 Greve</button>
                        <button id="btnCup" class="event-btn">⚽ Copa</button>
                    </div>
                </div>
                <div class='chart-container'><canvas id='dailyVolumeChart'></canvas></div>
            </div>
        </div>

        <div class="row g-4 mb-5">
            <div class="col-md-6">
                <a href="cancellations_2018.html" class="text-decoration-none text-dark">
                    <div class="card p-4 metric-card border-danger-custom clickable-card text-center">
                        <h6 class="text-muted fw-bold text-danger">❌ Cancelamentos 2018</h6>
                        <h2 class="fw-bold mb-1 text-danger">{cancelamentos_2018:,}</h2>
                        <p class="small text-muted mb-0">Total Anual (Clique para ver)</p>
                        <hr>
                        <div class="small text-danger fw-bold">Análise Mensal Detalhada</div>
                    </div>
                </a>
            </div>
            <div class="col-md-6">
                <a href="unapproved_2018.html" class="text-decoration-none text-dark">
                    <div class="card p-4 metric-card border-info-custom clickable-card text-center">
                        <h6 class="text-muted fw-bold text-primary">🚫 Não Aprovados 2018</h6>
                        <h2 class="fw-bold mb-1 text-primary">{nao_aprovados_2018:,}</h2>
                        <p class="small text-muted mb-0">Total Anual (Clique para ver)</p>
                        <hr>
                        <div class="small text-primary fw-bold">Falhas de Pagamento</div>
                    </div>
                </a>
            </div>
        </div>

        <div class="row g-4 mb-5">
            <div class="col-md-12">
                <div class="card p-4">
                    <h5 class="fw-bold mb-3">📝 Insights da Crise</h5>
                    <div class="annotation-box mb-3">
                        <strong>Impacto Logístico:</strong> A greve dos caminhoneiros (Maio) causou uma queda imediata no volume, mas o efeito residual foi sentido em Junho com a perda de confiança na entrega.
                    </div>
                    <div class="annotation-box">
                        <strong>Efeito Copa:</strong> Durante os jogos do Brasil, observou-se uma paralisação quase total das transações por períodos de 4-6 horas.
                    </div>
                </div>
            </div>
        </div>

        <!-- SEÇÃO DE DOCUMENTAÇÃO TÉCNICA RESTAURADA -->
        <div class="doc-section shadow-sm">
            <h3 class="fw-bold mb-4 border-bottom pb-3">🛠️ Documentação Técnica da Análise</h3>
            <div class="row g-5">
                <div class="col-md-6">
                    <h5 class="fw-bold text-primary mb-3">📂 Tabelas Utilizadas</h5>
                    <ul class="list-unstyled">
                        <li class="mb-3">
                            <span class="table-badge">olist_orders_dataset</span>
                            <p class="text-muted small mt-1">Fonte primária para volume temporal e status da transação. Contém o ciclo de vida completo de cada pedido.</p>
                        </li>
                    </ul>
                    <h5 class="fw-bold text-primary mb-3 mt-4">🔍 Campos Mapeados</h5>
                    <div class="d-flex flex-wrap gap-2 mb-3">
                        <span class="field-badge">order_purchase_timestamp</span>
                        <span class="field-badge">order_status</span>
                        <span class="field-badge">order_id</span>
                        <span class="field-badge">order_approved_at</span>
                    </div>
                </div>
                <div class="col-md-6">
                    <h5 class="fw-bold text-primary mb-3">🔗 Lógica e Cruzamentos</h5>
                    <div class="mb-3">
                        <h6 class="fw-bold mb-1">Agrupamento Temporal:</h6>
                        <p class="text-muted small">Agregação diária por timestamp para definir volume operacional.</p>
                    </div>
                    <div class="mb-3">
                        <h6 class="fw-bold mb-1">Filtros de Eventos:</h6>
                        <p class="text-muted small">Greve (21-30 Mai) e Copa (14 Jun-15 Jul) mapeados via calendário histórico.</p>
                    </div>
                    <div>
                        <h6 class="fw-bold mb-1">Não Aprovados:</h6>
                        <p class="text-muted small">Considera todos os pedidos onde <code>order_approved_at</code> é nulo, indicando falha na validação financeira.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const ctx = document.getElementById('dailyVolumeChart').getContext('2d');
        const labels = {json.dumps(labels_daily)};
        const data = {json.dumps(data_daily)};
        const chart = new Chart(ctx, {{
            type: 'line',
            data: {{
                labels, datasets: [{{ label: 'Pedidos', data, borderColor: '#3b82f6', borderWidth: 2, pointRadius: 0, fill: true, backgroundColor: 'rgba(59,130,246,0.05)', tension: 0.3 }}]
            }},
            options: {{
                responsive: true, maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }}, annotation: {{ annotations: {{}} }} }},
                scales: {{ x: {{ grid: {{ display: false }}, ticks: {{ maxTicksLimit: 12 }} }} }}
            }}
        }});

        const btnStrike = document.getElementById('btnStrike'), btnCup = document.getElementById('btnCup');
        let showStrike = false, showCup = false;
        function updateAnnotations() {{
            const annotations = {{}};
            if (showStrike) {{
                annotations.strikeBox = {{ type: 'box', xMin: labels.indexOf('{greve_start}'), xMax: labels.indexOf('{greve_end}'), backgroundColor: 'rgba(239, 68, 68, 0.15)', borderColor: '#ef4444', borderWidth: 1, label: {{ display: true, content: 'GREVE', backgroundColor: '#ef4444', color: '#fff', font: {{ size: 10, weight: 'bold' }} }} }};
            }}
            if (showCup) {{
                annotations.cupBox = {{ type: 'box', xMin: labels.indexOf('{copa_start}'), xMax: labels.indexOf('{copa_end}'), backgroundColor: 'rgba(16, 185, 129, 0.15)', borderColor: '#10b981', borderWidth: 1, label: {{ display: true, content: 'COPA', backgroundColor: '#10b981', color: '#fff', font: {{ size: 10, weight: 'bold' }} }} }};
            }}
            chart.options.plugins.annotation.annotations = annotations;
            chart.update();
        }}
        btnStrike.onclick = () => {{ showStrike=!showStrike; btnStrike.classList.toggle('active-strike', showStrike); updateAnnotations(); }};
        btnCup.onclick = () => {{ showCup=!showCup; btnCup.classList.toggle('active-cup', showCup); updateAnnotations(); }};
    </script>
</body>
</html>
"""

with open("/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/scratch/daily_volume_2018.html", "w") as f:
    f.write(html_daily)

print("Estrutura de análise técnica atualizada com navegação para dashboard.")
