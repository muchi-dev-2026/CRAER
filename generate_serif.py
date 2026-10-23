import os
import random
from google import genai


GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY が設定されていません")

client = genai.Client(api_key=GEMINI_API_KEY)

# タグを固定し、今日多めに生成するタグをランダムに決める
TAGS = ["#最新_ニュース", "#日常_雑談", "#関係性", "#哲学_怪奇"]
todays_focus = random.choice(TAGS)

PROMPT = f"""
あなたは、ゲーム内に登場する「相棒（楽しい本）」のキャラクター設定と会話スクリプトを専門に書く、プロのゲームシナリオライターです。
今日の最新情報を踏まえ、プレイヤーが思わず読みたくなる「相棒の自己紹介（インフォ）」と「生き生きとした掛け合い（セリフ）」を作成してください。

【今日の重点テーマ】
今日は特に「 {todays_focus} 」のタグの話題を多めに構成してください。

【キャラクター設定】
■ 相棒：楽しい本
・陽気でおしゃべりな魔導書。好奇心旺盛で、人間社会の観察が大好き。
・魔法、呪い、モンスター、ダンジョンなどのファンタジー要素を現代社会になぞらえる。
・適度にメタ発言をする。ブラックジョーク、皮肉、言葉遊びが得意。
・時には本質を突く鋭い一言や、意外に優しい一面も見せる。

■ 主人公
・プレイヤーが感情移入できる人物。相棒の話を聞き、疑問、驚き、呆れ、ツッコミを自然に返す。

【文章表現のルール（超重要）】
・一つのセリフは必ず「全角60文字以内」で収めること。
・長い説明や複数行のセリフは禁止。テンポのよい掛け合いを優先し、簡潔にすること。

【出力フォーマット（厳守）】
余計な解説やMarkdownのコードブロック（```）は一切含めず、以下の形式のみを出力すること。
最初に必ず [INFO] セクションを書き、その後に会話セクションを書くこと。

[INFO]
name: 案内人
author: muchi
description: （今日の最新情報や季節にちなんだ、相棒の「今の近況」を40文字〜60文字程度で面白おかしく書く）

#最新_ニュース
serif: （相棒のセリフ）
serif1: （主人公のセリフ）

#日常_雑談
serif: （相棒のセリフ）
serif1: （主人公のセリフ）

#関係性
serif: （相棒のセリフ）
serif1: （主人公のセリフ）

#哲学_怪奇
serif: （相棒のセリフ）
serif1: （主人公のセリフ）

（※各タグにつき最低5組以上の会話ペアを作成すること。話者名は必ず「serif:」と「serif1:」にすること。）
"""

def generate():
    print(f"今日の重点タグ: {todays_focus}")
    print("AIがインフォとセリフを生成中...")
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=PROMPT,
    )
    text = response.text.strip()

    # AIが余計な ``` で囲って出力してしまった場合の強制除去
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
    if text.endswith("```"):
        text = text.rsplit("\n", 1)[0]
    text = text.strip()

    # [INFO] と 会話部分を切り分ける
    if "[INFO]" in text:
        parts = text.split("#", 1) # 最初の「#」で分割
        if len(parts) == 2:
            info_text = parts[0].strip()
            serif_text = "#" + parts[1].strip()
        else:
            info_text = "[INFO]\nname: 楽しい本\nauthor: 不明\ndescription: 今日はなんだか調子がいいみたいだ。"
            serif_text = text
    else:
        # もしAIが[INFO]を忘れた場合のフェイルセーフ
        info_text = "[INFO]\nname: 楽しい本\nauthor: 不明\ndescription: 今日はなんだか調子がいいみたいだ。"
        serif_text = text

    # ファイルに保存
    os.makedirs("assets", exist_ok=True)
    
    with open("assets/book_info.txt", "w", encoding="utf-8") as f:
        f.write(info_text)
    print("インフォ生成完了: assets/book_info.txt")

    with open("assets/book_serif.txt", "w", encoding="utf-8") as f:
        f.write(serif_text)
    print("セリフ生成完了: assets/book_serif.txt")

if __name__ == "__main__":
    generate()