import json
import logging
import os

import google.generativeai as genai
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from langchain_google_genai import ChatGoogleGenerativeAI

app = Flask(__name__)
# CORS(app)  # 追加
CORS(app, resources={r"/chat": {"origins": ["http://localhost:8080", "https://localhost:8080"], "methods": ["POST", "OPTIONS"]}})

logging.basicConfig(level=logging.DEBUG)

CONVERSATION_LOG_FILE = "conversation_log.json"


@app.route("/")
def index():
    conversations = load_conversation_log()
    return render_template("bot.html", conversations=conversations)


load_dotenv()

# genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
os.environ.get("GOOGLE_API_KEY")
check_api_key = os.environ.get("GOOGLE_API_KEY")
if not check_api_key or check_api_key == "xxx":
    logger.warning("\n" + "!" * 50 + "\nGOOGLE_API_KEY が未設定です。" "\nこのままではチャット機能は動作しません。" "\n.envファイルに有効なキーを設定してください。" "\n" + "!" * 50)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("input")
    model_name = data.get("model")
    temperature = data.get("temperature")

    if not user_input:
        return jsonify({"error": "Missing input"}), 400

    try:
        model = ChatGoogleGenerativeAI(model=model_name, temperature=temperature)
        response = model.invoke(user_input)
        bot_response = response.content if hasattr(response, "content") else None

        if bot_response is None:
            return jsonify({"error": "No response from model"}), 500

        save_conversation_log(user_input, bot_response)
        response_data = {"response": bot_response, "model": model_name, "temperature": temperature}
        logging.debug(f"Sending response: {response_data}")  # レスポンスデータのログ
        return jsonify(response_data)

    except Exception as e:
        logging.error(f"Error in chat(): {e}")
        return jsonify({"error": "Internal server error"}), 500


def save_conversation_log(user_input, response, filename=CONVERSATION_LOG_FILE):
    conversation = {"user_input": user_input, "bot_response": response}
    try:
        with open(filename, "a", encoding="utf-8") as file:
            json.dump(conversation, file, ensure_ascii=False)
            file.write("\n")
    except IOError as e:
        logging.error(f"ファイルの書き込み中にエラーが発生しました: {e}")


def load_conversation_log(filename=CONVERSATION_LOG_FILE):
    conversations = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            conversations = [json.loads(line) for line in file]
    except (IOError, json.JSONDecodeError) as e:
        logging.error(f"会話ログの読み込み中にエラーが発生しました: {e}")
    return conversations


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
