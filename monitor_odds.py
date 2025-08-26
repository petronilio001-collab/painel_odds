import csv
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Configurações do navegador para GitHub Actions
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.binary_location = "/usr/bin/chromium-browser"

driver = webdriver.Chrome(options=options)

# Acessa a página da Oddspedia
url = "https://oddspedia.com/br/futebol"
driver.get(url)
time.sleep(5)

# Coleta de dados
dados_odds = []
partidas = driver.find_elements(By.CSS_SELECTOR, "div.event-row")

for partida in partidas:
    try:
        times = partida.find_element(By.CSS_SELECTOR, ".event-name").text
        horario = partida.find_element(By.CSS_SELECTOR, ".event-time").text
        mercados = partida.find_elements(By.CSS_SELECTOR, ".odds-value")

        if len(mercados) >= 2:
            odd_over = mercados[0].text.replace(",", ".")
            odd_under = mercados[1].text.replace(",", ".")

            if odd_over and odd_under:
                dados_odds.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "times": times,
                    "horario": horario,
                    "odd_over": float(odd_over),
                    "odd_under": float(odd_under)
                })
    except Exception:
        continue

driver.quit()

# Salvando em CSV
csv_file = "odds_monitoramento.csv"
with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["timestamp", "times", "horario", "odd_over", "odd_under"])
    if file.tell() == 0:
        writer.writeheader()
    writer.writerows(dados_odds)

print(f"{len(dados_odds)} partidas registradas.")
