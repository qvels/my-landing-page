import os
import requests
from flask import Flask, jsonify, render_template, request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8809642977:AAGuXSw0liulGmqhe9Yp-1qiGEhmp4XptBk")
CHAT_ID = os.environ.get("CHAT_ID", "1015699073")


# Главная страница (должна быть ТОЛЬКО ОДНА такая функция)
@app.route("/")
def index():
  return render_template("index.html")


# Отправка формы в Telegram
@app.route("/api/submit", methods=["POST"])
def send_lead():
  try:
    # Безопасно получаем данные: сначала проверяем JSON, затем обычную форму
    data = request.get_json(silent=True) or request.form

    name = data.get("name", "Не указано")
    phone = data.get("phone", "Не указано")

    text = f"🎯 Новая заявка!\n\n👤 Имя: {name}\n📞 Телефон: {phone}"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}

    response = requests.post(url, json=payload, timeout=10)

    if response.status_code == 200:
      return jsonify({"status": "success", "message": "Заявка отправлена!"})
    else:
      return (
          jsonify({
              "status": "error",
              "message": f"Ошибка Telegram: {response.text}",
          }),
          500,
      )

  except Exception as e:
    return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
  app.run(debug=True)
