import os
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY が設定されていません")

# 新しいライブラリの初期化方法
client = genai.Client(api_key=GEMINI_API_KEY)

PROMPT = """
あなたはゲーム内に登場する「相棒（楽しい本）」と「主人公」の会話スクリプトを作成するライターです。
今日（最新）の面白い話題、トレンド、ニュース、あるいは季節の話題をいくつか拾い上げ、以下の【仕様】に従って `セリフ.txt` を出力してください。

【仕様】
1. タグ（#最新_トレンド など）でセリフグループを作る。
2. 1つのタグの中に、1行ずつセリフを書く。
3. `serif:` は相棒（楽しい本）のセリフ、`serif1:` は主人公のセリフ。
4. 1つのタグ内に複数ペア（serifとserif1のセット）を作成する。
5. 余計な解説やMarkdownのコードブロック（```）は一切含めず、純粋なテキストのみを出力すること。
6. 出力は必ず以下のフォーマットから始めること。

#最新_トレンド
serif: 今日は〇〇が話題になってるみたいだよ！
serif1: へえ、最近流行ってるのか。

serif: そういえば最新の〇〇ニュース見た？
serif1: 相棒、どこから情報仕入れてるんだ……？

#最新_季節
serif: そういえば、もう〇〇の季節だね！
serif1: 本なのに季節を感じるんだな……。
"""

def generate():
    # 新しいライブラリでの生成メソッド
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=PROMPT,
    )
    text = response.text.strip()

    # もしAIが ``` で囲って出力してしまった場合の除去
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
    if text.endswith("```"):
        text = text.rsplit("\n", 1)[0]
    text = text.strip()

    # assets フォルダの中に 相棒セリフ.txt を保存する
    output_path = "assets/相棒セリフ.txt"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("セリフ生成完了:", output_path)

if __name__ == "__main__":
    generate()