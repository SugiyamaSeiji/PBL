
import streamlit as st


import openai





class GPT3:
    def __init__(self):
        openai.api_key = ""
    
    def generate_text(self, prompt):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
             {"role": "system", "content": "You are a helpful assistant ."},
             {"role": "user", "content": f"次の文章を子供でも分かるように簡単な言葉で分かりやすく言い換えてください「{prompt}」"}
            ]
        )
        return response['choices'][0]['message']['content']

# ページのタイトルを設定
st.set_page_config(page_title="chatgpt3.5 API Demo", page_icon=":smiley:")

# アプリのタイトルを設定
st.title("平易化")

# フォームを作成
with st.form(key = 'profile_form'):

    # ユーザーの入力を受け取るためのテキストボックスを作成
    user_input = st.text_input("平易化したい文章を入力してください")

    # テキスト送信用のボタンを作成
    send_btn = st.form_submit_button('送信')

    # ユーザーが送信ボタンをクリックした場合にのみ、APIを呼び出して結果を表示する
    if send_btn == True:
        if user_input:
            # APIを呼び出し、結果を取得する
            gpt3 = GPT3()
            result = gpt3.generate_text(user_input)

            # 結果を表示する
            st.write(result)

