import os
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY が設定されていません")

# 新しいライブラリの初期化方法
client = genai.Client(api_key=GEMINI_API_KEY)

PROMPT = """
あなたはゲーム内に登場する「相棒（楽しい本）」と「主人公」の会話スクリプトを作成するライターです。
最新のネットニュース、テクノロジー、社会問題、あるいは少しダークな話題（個人情報流出、AIの暴走、不可解な事件など）をいくつか検索して拾い上げ、以下の【仕様】に従ってセリフを出力してください。

【相棒のキャラクター】
陽気でおしゃべりな魔導書。少しメタ発言やブラックジョークを交えつつ、主人公を楽しませようとする。最新の人間社会のニュースを「面白いもの」として観察している。

【仕様】
1. タグ（#最新_ニュース など）でセリフグループを作る。
2. 1つのタグの中に、1行ずつセリフを書く。
3. `serif:` は相棒（楽しい本）のセリフ、`serif1:` は主人公のセリフ。
4. 1つのタグ内に、異なる話題のペア（serifとserif1のセット）を「最低5セット以上」作成すること。
5. 余計な解説やMarkdownのコードブロック（```）は一切含めず、純粋なテキストのみを出力すること。
6. 出力は必ず以下のフォーマットから始めること。

#最新_ニュース
serif: （ここに相棒のセリフ）
serif1: （ここに主人公のセリフ）

serif: （ここに相棒のセリフ）
serif1: （ここに主人公のセリフ）

#最新_トレンド
serif: （ここに相棒のセリフ）
serif1: （ここに主人公のセリフ）
"""

def generate():
    # 新しいライブラリでの生成メソッド
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
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