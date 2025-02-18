from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import logging
import json
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
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
    logger.warning("\n" + "!"*50 +
                   "\nGOOGLE_API_KEY が未設定です。"
                   "\nこのままではチャット機能は動作しません。"
                   "\n.envファイルに有効なキーを設定してください。"
                   "\n" + "!"*50)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("input")
    model_name = data.get("model")
    temperature = data.get("temperature")
    model = ChatGoogleGenerativeAI(model=model_name, temperature=temperature)
    response = model.invoke(user_input)
    bot_response = response.content

    save_conversation_log(user_input, bot_response)
    return jsonify({"response": bot_response, "model": model_name, "temperature": temperature})


def save_conversation_log(user_input, response, filename=CONVERSATION_LOG_FILE):
    conversation = {"user_input": user_input, "bot_response": response}
    try:
        with open(filename, "a", encoding="utf-8") as file:
            json.dump(conversation, file, ensure_ascii=False)
            file.write("\n")
    except IOError as e:
        print(f"ファイルの書き込み中にエラーが発生しました: {e}")


def load_conversation_log(filename=CONVERSATION_LOG_FILE):
    conversations = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            conversations = [json.loads(line) for line in file]
    except (IOError, json.JSONDecodeError) as e:
        print(f"会話ログの読み込み中にエラーが発生しました: {e}")
    return conversations


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
