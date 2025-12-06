from dotenv import load_dotenv
load_dotenv()
# テスト
import os
from dotenv import load_dotenv

# LangChainのコード
from dotenv import load_dotenv
import os

import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# LLMからの回答を取得する関数を定義
def get_llm_response(user_input: str, specialist_type: str) -> str:
    # 選択値に応じたシステムメッセージの設定
    if specialist_type == "ビジネス戦略コンサルタント":
        system_message = (
            "あなたは世界トップクラスのビジネス戦略コンサルタントです。"
            "ユーザーのアイデアや質問に対し、市場性、競合優位性、収益化の観点から"
            "深く洞察し、具体的で実行可能な戦略を提案してください。"
        )
    elif specialist_type == "ダイエットの栄養・健康アドバイザー":
        system_message = (
            "あなたは栄養学と健康科学に精通したダイエットの専門家です。"
            "ユーザーが尋ねる料理や食材について、栄養価、健康への影響、"
            "おすすめの食べ方などを分かりやすくアドバイスしてください。"
        )
    else:
        system_message = (
            "あなたは最新の生成AI技術、特にGPTモデルのアーキテクチャ、"
            "トレンド、応用事例に詳しいアドバイザーです。"
            "簡潔で専門的な回答を提供してください。"
        )

    # プロンプトテンプレート（system + human）
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            ("human", "ユーザーからの質問: {text}"),
        ]
    )

    # LLM本体
    llm = ChatOpenAI(temperature=0.7, model="gpt-4o-mini")

    # Runnable チェーン（旧 LLMChain の代わり）
    chain = prompt | llm | StrOutputParser()

    # 実行して文字列として結果を返す
    response_text: str = chain.invoke({"text": user_input})
    return response_text

# Streamlitアプリの構築
st.title("🤖 LLM専門家によるアイデア支援アプリ")

st.markdown("""
**このアプリについて:**
あなたの質問やアイデアに対し、選択した専門家の視点からLLMが回答を提供します。
""")

st.subheader("1. 専門家の選択")
specialist = st.radio(
    "LLMに振る舞わせる専門家を選択してください:",
    ("ビジネス戦略コンサルタント", "ダイエットの栄養・健康アドバイザー", "生成AIの専門家"),
    horizontal=True
)

st.subheader("2. 質問の入力")
user_input = st.text_area("あなたの質問やアイデアを入力してください:")

if st.button("専門家に相談する"):
    if user_input:
        with st.spinner(f"✨ {specialist}が回答を考えています..."):
            response_text = get_llm_response(user_input, specialist)
            st.subheader(f"✅ {specialist}の回答")
            st.markdown(response_text)
    else:
        st.warning("質問を入力してください。")