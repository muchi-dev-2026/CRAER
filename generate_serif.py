import os
import re
import random
from datetime import datetime
from zoneinfo import ZoneInfo
from google import genai


GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY が設定されていません")

client = genai.Client(api_key=GEMINI_API_KEY)

# 日本時間（JST）で現在の時間帯を判定
jst_now = datetime.now(ZoneInfo("Asia/Tokyo"))
hour = jst_now.hour

if 5 <= hour < 11:
    TIME_SLOT = "朝"
    SLOT_INSTRUCTION = "【現在の時間帯：朝】\n・開館直後で少し眠そう、または優雅にモーニングコーヒー（インク？）を飲んでいる雰囲気。\n・今日一日の予定や、朝の静けさをテーマに含める。"
elif 11 <= hour < 17:
    TIME_SLOT = "昼"
    SLOT_INSTRUCTION = "【現在の時間帯：昼】\n・午後の強い日差し、耐えがたい眠気、図書館にやってくる客（プレイヤー）の気配へのツッコミ。\n・少しテンションが高かったり、暇を持て余している雰囲気。"
else:
    TIME_SLOT = "夜"
    SLOT_INSTRUCTION = "【現在の時間帯：夜】\n・こんな時間までゲームや読書をしているプレイヤーへの呆れと皮肉。\n・怪奇現象の気配、魔導書本来のダークで怪しげな本音、秘密めいた話題。"

# タグを固定し、今日多めに生成するタグをランダムに決める
TAGS = ["#最新_ニュース", "#日常_雑談", "#関係性", "#哲学_怪奇"]
todays_focus = random.choice(TAGS)

PROMPT = f"""
あなたは、ゲーム内に登場する「相棒（楽しい本）」のキャラクター設定と会話スクリプトを専門に書く、プロのゲームシナリオライターです。
Google検索から得た「今日の最新ニュース、世間のトレンド、季節や気候の話題」をリサーチし、それらを皮肉やユーモアを交えて魔導書のセリフに自然に組み込んでください。

{SLOT_INSTRUCTION}

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
・一つのセリフは必ず「全角80文字以内」で収めること。
・長い説明や複数行のセリフは禁止。テンポのよい掛け合いを優先し、簡潔に２行程度にすること。

【出力フォーマット（厳守）】
余計な解説やMarkdownのコードブロック（```）は一切含めず、以下の形式のみを出力すること。
最初に必ず [INFO] セクションを書き、その後に会話セクションを書くこと。

[INFO]
name: 案内人
author: muchi
description: （今日のリアルな時事ネタ、季節の気候、トレンドなどを踏まえた、相棒の「今の近況」を40文字〜60文字程度で面白おかしく書く。1行で収めること。改行・#記号は禁止）

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

（※各タグにつき最低12組以上の会話ペアを作成すること。話者名は必ず「serif:」と「serif1:」にすること。）
"""

def generate():
    print(f"現在の時間帯: {TIME_SLOT} (JST {hour}時)")
    print(f"今日の重点タグ: {todays_focus}")
    print("Google検索を活用してインフォとセリフを生成中...")
    
    # Google検索グラウンディング（Google Search）をツールとして設定
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=PROMPT,
        config={
            "tools": [{"google_search": {}}],
        }
    )
    text = response.text.strip()

    # AIが余計な ``` で囲って出力してしまった場合の強制除去
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
    if text.endswith("```"):
        text = text.rsplit("\n", 1)[0]
    text = text.strip()

    # [INFO] と 会話部分を切り分ける
    m = re.search(r"(?m)^\s*#最新_ニュース\s*$", text)
    if m:
        info_text = text[:m.start()].strip()
        serif_text = text[m.start():].strip()
    else:
        info_text = "[INFO]\nname: 案内人\nauthor: muchi\ndescription: 外部のネット世界と繋がったら、なんだか変な情報が流れ込んできたぞ。"
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
