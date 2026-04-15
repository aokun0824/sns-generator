from flask import Flask, render_template, request, jsonify
import anthropic
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    shop_name = data.get("shop_name", "")
    product = data.get("product", "")
    message = data.get("message", "")
    instagram_account = data.get("instagram_account", "").strip()

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    account_line = f"Instagramアカウント: {instagram_account}（投稿文の末尾に自然に入れてください）" if instagram_account else ""

    prompt = f"""以下の情報をもとに、Instagramの投稿文を作成してください。

お店・作家名: {shop_name}
商品・サービス: {product}
伝えたいこと: {message}
{account_line}

以下の形式で出力してください：

【Instagram投稿文】
（絵文字を使った魅力的な投稿文を200〜300文字で。読んだ人が「いいね！」したくなる文章）

【ハッシュタグ】
（日本語・英語合わせて15〜20個。改行なしでスペース区切り）

【X（旧Twitter）用】
（140文字以内の短縮版）"""

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    return jsonify({"result": response.content[0].text})

if __name__ == "__main__":
    app.run(debug=True, port=5050)
