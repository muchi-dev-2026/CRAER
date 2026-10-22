import os
from google import genai

# クライアントの初期化（環境変数 GEMINI_API_KEY から自動で読み込まれます）
client = genai.Client()

PROMPT = """
あなたはゲーム内に登場する「相棒（楽しい本）」と「主人公」の会話スクリプトを作成するライターです。
今日（最新）の面白い話題、トレンド、ニュース、あるいは季節の話題をいくつか拾い上げ、以下の【仕様】に従ってテキストを出力してください。

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

#最新_季節
serif: そういえば、もう〇〇の季節だね！
serif1: 本なのに季節を感じるんだな……。
"""

def generate():
    # 最新モデル（gemini-2.5-flash または gemini-2.0-flash）を指定
    response = client.models.generate_content(
        model='gemini-3.8-flash',  # ここを更新！
        contents=PROMPT,
    )

    text = response.text.strip()

    # 余計な ``` が混ざった場合の除去
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

if __name__ == "__main__":
    generate()
