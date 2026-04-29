import json

with open('scratch/retention_data.json', 'r') as f:
    data = json.load(f)

html = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Análise de Clientes (Novos x Recorrentes) - Olist 2018</title>
    <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>
    <script src='https://cdn.jsdelivr.net/npm/chart.js'></script>
    <style>
        body {{ background-color: #f8fafc; font-family: 'Inter', sans-serif; padding: 40px 0; }}
        .header-section {{ background: linear-gradient(135deg, #3498db, #2980b9); color: white; padding: 40px; border-radius: 24px; margin-bottom: 40px; }}
        .card {{ border: none; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); background: white; margin-bottom: 30px; }}
        .chart-container {{ height: 450px; padding: 20px; }}
        .btn-back {{ background: rgba(255,255,255,0.2); border: 1px solid rgba(255,255,255,0.3); color: white; text-decoration: none; border-radius: 12px; padding: 8px 16px; }}
        .btn-back:hover {{ background: rgba(255,255,255,0.3); color: white; }}
        .insight-box {{ border-left: 5px solid #3498db; background: #f0f7ff; padding: 25px; border-radius: 16px; height: 100%; }}
        .highlight {{ color: #2980b9; font-weight: bold; }}
    </style>
</head>
<body>
    <div class='container'>
        <div class="header-section text-center position-relative shadow-lg">
            <a href="dashboard_2018.html" class="btn-back position-absolute top-0 start-0 m-4">← Voltar</a>
            <h1 class="fw-bold">👥 Novos vs Recorrentes: Olist 2018</h1>
            <p class="opacity-90">Análise de aquisição e fidelização de clientes</p>
        </div>

        <div class="row g-4">
            <!-- Gráfico Principal -->
            <div class="col-md-12">
                <div class="card p-4">
                    <h5 class="fw-bold mb-4">📊 Evolução Mensal de Novos e Recorrentes</h5>
                    <div class="chart-container"><canvas id="retentionChart"></canvas></div>
                </div>
            </div>

            <!-- Insights -->
            <div class="col-md-6">
                <div class="insight-box shadow-sm">
                    <h5 class="fw-bold">🚀 Dependência Crítica de Novos Clientes</h5>
                    <p class="text-muted small">O modelo de negócio da Olist em 2018 era altamente dependente de aquisição. Novos clientes representam mais de <span class="highlight">96%</span> do volume mensal. Em Junho, houve uma queda de <span class="highlight">10,3%</span> na entrada de novos usuários comparado à média do 1º trimestre, o que explica diretamente a perda de faturamento.</p>
                </div>
            </div>
            <div class="col-md-6">
                <div class="insight-box shadow-sm" style="border-left-color: #e67e22; background: #fffaf0;">
                    <h5 class="fw-bold">📉 O Desafio da Recorrência</h5>
                    <p class="text-muted small">A taxa de recorrência (clientes que compram mais de uma vez) mante-se estagnada em cerca de <span class="highlight">3,8%</span>. Durante os meses de crise (Jun-Ago), não houve um aumento na base fiel para compensar a queda na aquisição, deixando o ecossistema vulnerável às oscilações externas (Greve/Copa).</p>
                </div>
            </div>
        </div>

        <!-- Conclusão -->
        <div class="card p-4 mt-4 border-0 shadow-sm text-center" style="background: #2c3e50; color: white;">
            <h5 class="fw-bold mb-2">VEREDITO TÉCNICO</h5>
            <p class="opacity-75 small mb-0">A queda de performance no meio de 2018 foi um <strong>problema de aquisição</strong>. Com a baixa fidelização do marketplace, o negócio perdeu fôlego quando o fluxo de novos clientes esfriou. A estratégia de longo prazo deve focar em transformar os mais de 50 mil clientes "One-Shot" de 2018 em compradores recorrentes para blindar o faturamento contra crises sazonais.</p>
        </div>
    </div>

    <script>
        const ctx = document.getElementById('retentionChart').getContext('2d');
        const labels = {json.dumps(data['labels'])};
        const newCustomers = {json.dumps(data['new_customers'])};
        const recurringCustomers = {json.dumps(data['recurring_customers'])};

        new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: labels,
                datasets: [
                    {{
                        label: 'Novos Clientes',
                        data: newCustomers,
                        backgroundColor: '#3498db',
                        borderRadius: 8
                    }},
                    {{
                        label: 'Clientes Recorrentes',
                        data: recurringCustomers,
                        backgroundColor: '#e67e22',
                        borderRadius: 8
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ position: 'bottom' }},
                    tooltip: {{ mode: 'index', intersect: false }}
                }},
                scales: {{
                    x: {{ stacked: true }},
                    y: {{ 
                        stacked: true, 
                        title: {{ display: true, text: 'Quantidade de Pedidos' }},
                        beginAtZero: true
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

with open('scratch/customer_analysis_2018.html', 'w') as f:
    f.write(html)

print("Page generated: scratch/customer_analysis_2018.html")
