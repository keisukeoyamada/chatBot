from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
# import PIL.Image
# import PyPDF2
import os
import json
from dotenv import load_dotenv

# from pathlib import Path

app = Flask(__name__)
CONVERSATION_LOG_FILE = "conversation_log.json"


@app.route("/")
def index():
    conversations = load_conversation_log()
    return render_template("bot.html", conversations=conversations)


load_dotenv()

# genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
os.environ["GOOGLE_API_KEY"]

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("input")
    # model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

    # script_dir = Path(__file__).parent
    # user_profile = os.environ.get('USERPROFILE')
    # input = input(f"""こんにちは、{user_profile}さんご用件をお聞かせください
    #   """)
    # response = model.generate_content(user_input)
    response = model.invoke(user_input)
    # bot_response = response.get("text", "") if isinstance(response, dict) else response.text
    bot_response = response.content

    save_conversation_log(user_input, bot_response)
    # print(response.text)
    # return jsonify({"response": response.text})
    return jsonify({"response": bot_response})


def save_conversation_log(user_input, response, filename=CONVERSATION_LOG_FILE):
    # 会話内容をJSON形式で保存
    conversation = {"user_input": user_input, "bot_response": response}
    try:
        with open(filename, "a", encoding="utf-8") as file:
            json.dump(conversation, file, ensure_ascii=False)
            file.write("\n")
    except IOError as e:
        print(f"ファイルの書き込み中にエラーが発生しました: {e}")


# if __name__ == '__main__':
#     app.run(debug=True)


def load_conversation_log(filename=CONVERSATION_LOG_FILE):
    # 会話ログを読み込む
    conversations = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            conversations = [json.loads(line) for line in file]
    except (IOError, json.JSONDecodeError) as e:
        print(f"会話ログの読み込み中にエラーが発生しました: {e}")
    return conversations


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
