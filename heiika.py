
import streamlit as st


import openai

import sys





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

with st.form(key='profile_form'):
    user_input = st.text_input("平易化したい文章を入力してください")
    uploaded_file = st.file_uploader("または、テキストファイルをアップロードしてください", type=["txt"])

    send_btn = st.form_submit_button('送信')
    delete_btn = st.form_submit_button('削除')
    
    

    if send_btn:
        result = ""
        
        if (user_input and uploaded_file) or (not user_input and not uploaded_file):
            st.warning("テキストまたはファイルのどちらかを入力してください。")
            sys.exit(1)
        
        

        if user_input:
            gpt3 = GPT3()
            result = gpt3.generate_text(user_input)
        elif uploaded_file:
            file_contents = uploaded_file.read().decode('utf-8')
            gpt3 = GPT3()
            result = gpt3.generate_text(file_contents)
            

        st.write(result)
        
    if delete_btn:
        result = ""