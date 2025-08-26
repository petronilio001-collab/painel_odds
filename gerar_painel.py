import pandas as pd
import os

csv_file = "odds_monitoramento.csv"
if not os.path.exists(csv_file):
    raise FileNotFoundError(f"O arquivo {csv_file} não foi encontrado.")

df = pd.read_csv(csv_file)
df['timestamp'] = pd.to_datetime(df['timestamp'])

grouped = df.groupby('times')
datasets = []
colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'cyan', 'magenta']
color_index = 0

for match, data in grouped:
    data = data.sort_values('timestamp')
    timestamps = data['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist()
    odds = data['odd_over'].tolist()
    datasets.append({
        'label': match,
        'data': [{'x': t, 'y': o} for t, o in zip(timestamps, odds)],
        'borderColor': colors[color_index % len(colors)],
        'fill': False
    })
    color_index += 1

html_content = f"""<!DOCTYPE html>
<html>
<head>
<title>Painel de Odds</title>
<script src='https://cdn.jsdelivr.net/npm/chart.js'></script>
</head>
<body>
<h2>Tabela de Odds</h2>
<table border='1' cellpadding='5' cellspacing='0'>
<tr>
<th>Timestamp</th>
<th>Times</th>
<th>Horário</th>
<th>Odd Over 2.5</th>
<th>Odd Under 2.5</th>
</tr>
"""

for _, row in df.iterrows():
    html_content += f"""
<tr>
<td>{row['timestamp']}</td>
<td>{row['times']}</td>
<td>{row['horario']}</td>
<td>{row['odd_over']}</td>
<td>{row['odd_under']}</td>
</tr>
"""

html_content += f"""
</table>
<h2>Variação da Odd Over 2.5</h2>
<canvas id='oddsChart' width='1000' height='400'></canvas>
<script>
const ctx = document.getElementById('oddsChart').getContext('2d');
const chart = new Chart(ctx, {{
    type: 'line',
    data: {{
        datasets: {str(datasets).replace("'", '"')}
    }},
    options: {{
        scales: {{
            x: {{
                type: 'time',
                time: {{
                    tooltipFormat: 'YYYY-MM-DD HH:mm:ss',
                    displayFormats: {{
                        hour: 'HH:mm'
                    }}
                }},
                title: {{
                    display: true,
                    text: 'Timestamp'
                }}
            }},
            y: {{
                title: {{
                    display: true,
                    text: 'Odd Over 2.5'
                }}
            }}
        }}
    }}
}});
</script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Arquivo index.html gerado com sucesso.")
