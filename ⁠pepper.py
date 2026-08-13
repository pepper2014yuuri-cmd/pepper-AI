import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Renderの環境変数からAPIキーを取得
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    # OpenRouterへリクエストを送る準備
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": "Bearer " + str(OPENROUTER_API_KEY),
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta-llama/llama-3-8b-instruct:free",
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        res_data = response.json()
        ai_reply = res_data['choices'][0]['message']['content']
        return jsonify({"response": ai_reply})
    except Exception as e:
        return jsonify({"response": "エラーが発生しました: " + str(e)}), 500

if __name__ == '__main__':
    # Renderが指定するポート番号を取得して起動
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
