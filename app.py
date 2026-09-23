import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# --- НАСТРОЙКИ TELEGRAM ---
BOT_TOKEN = "8809642977:AAGuXSw0liulGmqhe9Yp-1qiGEhmp4XptBk"
CHAT_ID = "1015699073"


def send_telegram_message(text: str) -> bool:
    """Функция отправки сообщения в Telegram через Bot API"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}

    try:
        response = requests.post(url, data=payload, timeout=5)
        return response.ok
    except Exception as e:
        print(f"Ошибка запроса к Telegram: {e}")
        return False


@app.route("/")
def index():
    """Отдаем главный лендинг"""
    return render_template("index.html")


@app.route("/api/submit", methods=["POST"])
def handle_submit():
    """API-эндпоинт для обработки AJAX-запроса от формы"""
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()

    # Простейшая валидация на сервере
    if not name or not phone:
        return jsonify({"success": False, "error": "Заполните все поля"}), 400

    # Красивое форматирование сообщения
    message = (
        f"🔥 <b>Новый лид с лендинга!</b>\n\n"
        f"👤 <b>Имя:</b> {name}\n"
        f"📞 <b>Телефон:</b> {phone}"
    )

    success = send_telegram_message(message)

    if success:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": " Ошибка Telegram API"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)