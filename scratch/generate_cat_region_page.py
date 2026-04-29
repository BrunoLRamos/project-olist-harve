import json

with open('scratch/cat_region_data.json', 'r') as f:
    data = json.load(f)

html = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Categorias x Regiões - Olist 2018</title>
    <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>
    <script src='https://cdn.jsdelivr.net/npm/chart.js'></script>
    <style>
        body {{ background-color: #f4f7f6; font-family: 'Inter', sans-serif; padding: 40px 0; }}
        .header-section {{ background: #2c3e50; color: white; padding: 40px; border-radius: 24px; margin-bottom: 40px; }}
        .card {{ border: none; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); background: white; }}
        .chart-container {{ height: 600px; padding: 20px; }}
        .btn-back {{ background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: white; text-decoration: none; border-radius: 12px; padding: 8px 16px; }}
        .btn-back:hover {{ background: rgba(255,255,255,0.2); color: white; }}
        .doc-section {{ background: #fff; border-radius: 20px; padding: 30px; margin-top: 40px; border-left: 5px solid #2c3e50; }}
    </style>
</head>
<body>
    <div class='container-fluid px-5'>
        <div class="header-section text-center position-relative shadow-lg">
            <a href="dashboard_2018.html" class="btn-back position-absolute top-0 start-0 m-4">← Voltar</a>
            <h1 class="fw-bold">🌍 Cruzamento: Categorias x Regiões</h1>
            <p class="opacity-90">Distribuição Geográfica das Principais Categorias - 2018</p>
        </div>

        <div class='card mb-5'>
            <div class='card-body'>
                <div class='chart-container'><canvas id='catRegionChart'></canvas></div>
            </div>
        </div>

        <div class="row g-4 mb-5">
            <div class="col-md-12">
                <div class="doc-section shadow-sm">
                    <h3 class="fw-bold mb-4">🛠️ Documentação Técnica</h3>
                    <div class="row">
                        <div class="col-md-6">
                            <h5 class="fw-bold text-primary">📂 Dados e Cruzamentos</h5>
                            <ul class="text-muted small">
                                <li><strong>Tabelas:</strong> Orders + Items + Products + Customers.</li>
                                <li><strong>Chaves:</strong> <code>order_id</code>, <code>product_id</code>, <code>customer_id</code>.</li>
                                <li><strong>Filtro:</strong> Apenas transações concluídas em 2018.</li>
                            </ul>
                        </div>
                        <div class="col-md-6">
                            <h5 class="fw-bold text-primary">💡 Insight Geográfico</h5>
                            <p class="text-muted small">
                                Observa-se uma concentração massiva em <strong>São Paulo (SP)</strong> em todas as categorias. 
                                Categorias como <strong>Beleza & Saúde</strong> possuem uma distribuição mais equilibrada entre RJ e MG em comparação com <strong>Utilidades Domésticas</strong>.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const ctx = document.getElementById('catRegionChart').getContext('2d');
        const categories = {json.dumps(data['categories'])};
        const states = {json.dumps(data['states'])};
        const values = {json.dumps(data['values'])};

        const colors = [
            '#3498db', '#e74c3c', '#2ecc71', '#f1c40f', '#9b59b6', 
            '#1abc9c', '#e67e22', '#34495e', '#95a5a6', '#d35400',
            '#7f8c8d', '#27ae60', '#2980b9', '#8e44ad', '#c0392b'
        ];

        const datasets = states.slice(0, 8).map((state, index) => ({{
            label: state,
            data: values.map(catRow => catRow[index]),
            backgroundColor: colors[index % colors.length]
        }}));

        new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: categories,
                datasets: datasets
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ position: 'right' }},
                    title: {{ display: true, text: 'Top 10 Categorias por Estado (Top 8 Estados)', font: {{ size: 18 }} }}
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

with open('scratch/category_region_2018.html', 'w') as f:
    f.write(html)

print("Page generated: scratch/category_region_2018.html")
