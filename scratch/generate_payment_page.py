import json

with open('scratch/payment_data.json', 'r') as f:
    data = json.load(f)

html = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Análise de Meios de Pagamento - Olist 2018</title>
    <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>
    <script src='https://cdn.jsdelivr.net/npm/chart.js'></script>
    <style>
        body {{ background-color: #f4f7f6; font-family: 'Inter', sans-serif; padding: 40px 0; }}
        .header-section {{ background: linear-gradient(135deg, #2ecc71, #27ae60); color: white; padding: 40px; border-radius: 24px; margin-bottom: 40px; }}
        .card {{ border: none; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); background: white; margin-bottom: 30px; }}
        .chart-container {{ height: 450px; padding: 20px; }}
        .btn-back {{ background: rgba(255,255,255,0.2); border: 1px solid rgba(255,255,255,0.3); color: white; text-decoration: none; border-radius: 12px; padding: 8px 16px; }}
        .btn-back:hover {{ background: rgba(255,255,255,0.3); color: white; }}
        .metric-card {{ background: white; padding: 20px; border-radius: 16px; text-align: center; border-bottom: 4px solid #2ecc71; }}
        .metric-value {{ font-size: 1.8rem; font-weight: bold; color: #2c3e50; }}
        .metric-label {{ color: #7f8c8d; font-size: 0.9rem; text-transform: uppercase; }}
        .insight-highlight {{ color: #27ae60; font-weight: bold; }}
    </style>
</head>
<body>
    <div class='container'>
        <div class="header-section text-center position-relative shadow-lg">
            <a href="dashboard_2018.html" class="btn-back position-absolute top-0 start-0 m-4">← Voltar</a>
            <h1 class="fw-bold">💳 Meios de Pagamento: Março a Agosto</h1>
            <p class="opacity-90">Análise de representatividade e impacto no faturamento</p>
        </div>

        <div class="row g-4 mb-4">
            <div class="col-md-3">
                <div class="metric-card shadow-sm">
                    <div class="metric-label">Queda Cartão Crédito</div>
                    <div class="metric-value text-danger">- 2.5%</div>
                    <div class="small text-muted">Share de Pedidos</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card shadow-sm" style="border-bottom-color: #3498db;">
                    <div class="metric-label">Salto Cartão Débito</div>
                    <div class="metric-value text-primary">+ 244%</div>
                    <div class="small text-muted">Crescimento de Share</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card shadow-sm" style="border-bottom-color: #f1c40f;">
                    <div class="metric-label">Representatividade CC</div>
                    <div class="metric-value">75.0%</div>
                    <div class="small text-muted">Média em Agosto</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="metric-card shadow-sm" style="border-bottom-color: #e67e22;">
                    <div class="metric-label">Faturamento CC (P2)</div>
                    <div class="metric-value">R$ 2.41M</div>
                    <div class="small text-muted">Total Jun-Ago</div>
                </div>
            </div>
        </div>

        <div class="row g-4">
            <div class="col-md-8">
                <div class="card p-4">
                    <h5 class="fw-bold mb-4">📈 Evolução da Representatividade (%)</h5>
                    <div class="chart-container"><canvas id="paymentShareChart"></canvas></div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card p-4 h-100">
                    <h5 class="fw-bold mb-4">💡 Insights Estratégicos</h5>
                    <div class="mb-4">
                        <h6 class="fw-bold text-success">1. Retração do Crédito Parcelado</h6>
                        <p class="small text-muted">A queda de <span class="insight-highlight">2,5 pontos percentuais</span> no share de Cartão de Crédito correlaciona-se com a queda nas categorias de alto valor (Móveis e Tech). Sem o parcelamento, o ticket médio total do marketplace foi diluído.</p>
                    </div>
                    <div class="mb-4">
                        <h6 class="fw-bold text-primary">2. Explosão do Débito</h6>
                        <p class="small text-muted">O uso do cartão de débito saltou de <span class="insight-highlight">1% para 3,6%</span> do volume total. Esse comportamento indica uma migração para compras imediatas de menor valor, típicas das categorias de giro rápido (Beleza/Saúde) que dominaram o período pós-crise.</p>
                    </div>
                    <div>
                        <h6 class="fw-bold text-dark">3. Estabilidade do Boleto</h6>
                        <p class="small text-muted">O Boleto manteve-se estável em ~18%. No entanto, em períodos de incerteza, o boleto pode ter taxas de conversão menores, o que também impacta indiretamente no faturamento final aprovado.</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="card p-4 mt-4 border-0 shadow-sm" style="background: #eafaf1;">
            <h6 class="fw-bold text-success mb-2">CONCLUSÃO DA ANÁLISE</h6>
            <p class="text-muted small mb-0">A queda de faturamento entre Junho e Agosto não foi apenas uma questão de volume, mas de <strong>perfil financeiro</strong>. A redução no uso do Cartão de Crédito e o aumento do Débito mostram que o consumidor da Olist em 2018 priorizou <strong>pagamentos à vista e itens de menor valor</strong>, abandonando as compras parceladas de bens duráveis que sustentavam o faturamento nos meses de pico.</p>
        </div>
    </div>

    <script>
        const ctx = document.getElementById('paymentShareChart').getContext('2d');
        const months = {json.dumps(data['months'])};
        const pt_types = {json.dumps(data['payment_types'])};
        const m_data = {json.dumps(data['monthly_data'])};

        const colors = {{
            'credit_card': '#2ecc71',
            'boleto': '#f1c40f',
            'debit_card': '#3498db',
            'voucher': '#e67e22',
            'not_defined': '#95a5a6'
        }};

        const datasets = pt_types.map(pt => ({{
            label: pt.replace('_', ' ').toUpperCase(),
            data: m_data[pt],
            borderColor: colors[pt] || '#000',
            backgroundColor: (colors[pt] || '#000') + '22',
            fill: true,
            tension: 0.4
        }}));

        new Chart(ctx, {{
            type: 'line',
            data: {{
                labels: months,
                datasets: datasets
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ position: 'bottom' }},
                    tooltip: {{ callbacks: {{ label: (ctx) => ctx.dataset.label + ': ' + ctx.raw.toFixed(2) + '%' }} }}
                }},
                scales: {{
                    y: {{ 
                        beginAtZero: true, 
                        max: 100,
                        title: {{ display: true, text: 'Participação (%) no Volume de Pedidos' }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

with open('scratch/payment_analysis_2018.html', 'w') as f:
    f.write(html)

print("Page generated: scratch/payment_analysis_2018.html")
