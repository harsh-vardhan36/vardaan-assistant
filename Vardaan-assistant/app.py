from flask import Flask, render_template, request, jsonify
from datetime import datetime
from vardaan_core import process_command

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")  # loads templates/index.html


@app.route("/api/chat", methods=["POST"])
def chat_api():
    data = request.get_json() or {}
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    bot_reply = process_command(user_message)

    return jsonify({
        "reply": bot_reply,
        "timestamp": datetime.now().isoformat()
    })


if __name__ == "__main__":
    app.run(debug=True)
