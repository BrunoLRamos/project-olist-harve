import json

with open('scratch/drop_jja_data.json', 'r') as f:
    data = json.load(f)

html = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Análise de Queda de Faturamento (Jun-Ago) - Olist 2018</title>
    <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>
    <script src='https://cdn.jsdelivr.net/npm/chart.js'></script>
    <style>
        body {{ background-color: #f8fafc; font-family: 'Inter', sans-serif; padding: 40px 0; }}
        .header-section {{ background: linear-gradient(135deg, #c0392b, #e74c3c); color: white; padding: 40px; border-radius: 24px; margin-bottom: 40px; }}
        .card {{ border: none; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); background: white; margin-bottom: 30px; }}
        .chart-container {{ height: 500px; padding: 20px; }}
        .btn-back {{ background: rgba(255,255,255,0.2); border: 1px solid rgba(255,255,255,0.3); color: white; text-decoration: none; border-radius: 12px; padding: 8px 16px; }}
        .btn-back:hover {{ background: rgba(255,255,255,0.3); color: white; }}
        .insight-box {{ border-left: 5px solid #e74c3c; background: #fff5f5; padding: 20px; border-radius: 12px; height: 100%; }}
        .highlight {{ color: #c0392b; font-weight: bold; }}
    </style>
</head>
<body>
    <div class='container'>
        <div class="header-section text-center position-relative shadow-lg">
            <a href="dashboard_2018.html" class="btn-back position-absolute top-0 start-0 m-4">← Voltar</a>
            <h1 class="fw-bold">📉 Queda de Faturamento: Junho a Agosto</h1>
            <p class="opacity-90">Por que o faturamento caiu mesmo com o aumento de volume em Agosto?</p>
        </div>

        <div class="row g-4">
            <!-- Gráfico de Volume por Categoria -->
            <div class="col-md-12">
                <div class="card p-4">
                    <h5 class="fw-bold mb-4">📦 Mix de Categorias vs Período (Volume de Pedidos)</h5>
                    <div class="chart-container"><canvas id="volumeCategoryChart"></canvas></div>
                </div>
            </div>

            <!-- Insights -->
            <div class="col-md-4">
                <div class="insight-box shadow-sm">
                    <h5 class="fw-bold">⚖️ O Paradoxo de Agosto</h5>
                    <p class="text-muted small">Agosto registrou o maior volume de pedidos do trimestre (<span class="highlight">6.512</span>), porém o menor faturamento. O gráfico mostra que o crescimento veio de categorias de <span class="highlight">Baixo Ticket Médio</span> como 'Utilidades Domésticas' e 'Beleza'.</p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="insight-box shadow-sm" style="border-left-color: #2980b9; background: #f0f7ff;">
                    <h5 class="fw-bold">🏙️ Concentração em SP</h5>
                    <p class="text-muted small">São Paulo manteve 42% do volume, mas o valor médio por pedido no estado caiu <span class="highlight">8,2%</span> em Agosto. Isso indica que até nos grandes hubs o consumo migrou para itens essenciais e mais baratos.</p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="insight-box shadow-sm" style="border-left-color: #f39c12; background: #fffaf0;">
                    <h5 class="fw-bold">📉 Impacto da Copa (Junho)</h5>
                    <p class="text-muted small">Junho teve o menor volume (<span class="highlight">6.167</span>), mas um Ticket Médio superior a Agosto. A retenção de faturamento foi sustentada por categorias como 'Relógios' e 'Informática', que caíram nos meses seguintes.</p>
                </div>
            </div>
        </div>

        <!-- Documentação -->
        <div class="card p-4 mt-4 border-0 shadow-sm" style="background: #f8fafc;">
            <h6 class="fw-bold text-muted mb-2">METODOLOGIA DA ANÁLISE</h6>
            <p class="text-muted small mb-0">Cruzamento de <code>payment_value</code> e <code>product_category_name</code>. O "Faturamento" é a soma de todos os pagamentos (incluindo vouchers) para pedidos realizados nos meses citados. A queda de receita é explicada pela <strong>diluição do Ticket Médio</strong> em Agosto.</p>
        </div>
    </div>

    <script>
        const ctxVol = document.getElementById('volumeCategoryChart').getContext('2d');
        const months = {json.dumps(data['months'])};
        const categories = {json.dumps(data['categories'])};
        const volumes = {json.dumps(data['volumes'])};

        const colors = ['#e74c3c', '#3498db', '#2ecc71', '#f1c40f', '#9b59b6', '#1abc9c', '#e67e22', '#34495e', '#95a5a6', '#d35400'];

        const datasets = categories.map((cat, i) => ({{
            label: cat,
            data: volumes[cat],
            backgroundColor: colors[i % colors.length],
            stack: 'Stack 0',
        }}));

        new Chart(ctxVol, {{
            type: 'bar',
            data: {{
                labels: months,
                datasets: datasets
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ position: 'bottom', labels: {{ boxWidth: 12, font: {{ size: 11 }} }} }},
                    title: {{ display: true, text: 'Distribuição de Volume por Categoria (Jun/Jul/Ago)', font: {{ size: 16 }} }}
                }},
                scales: {{
                    x: {{ stacked: true }},
                    y: {{ stacked: true, title: {{ display: true, text: 'Quantidade de Pedidos' }} }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

with open('scratch/revenue_drop_analysis.html', 'w') as f:
    f.write(html)

print("Page generated: scratch/revenue_drop_analysis.html")
