import sys
import time
import openai
import streamlit as st
from docx import Document
import concurrent.futures
from functions import GPT3
from functions import extract_table_column, split_text, remove_newlines, process_chunk, input_rireki, display_rireki, write_result, check_output, count_characters

def display_result(final_result, title):
    st.markdown(f'<div class="center"><h5>{title}</h5></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="background-color:#cfe2f3; padding:10px; border-radius:5px;">{final_result}</div>', unsafe_allow_html=True)

def sending_data(user_input, uploaded_file, uploaded_word_file, keyword_input, phrase_input, max_tokens, filename):
    if user_input:
        chunks = split_text(user_input)
    elif uploaded_file:
        file_contents = uploaded_file.read().decode('utf-8')
        chunks = split_text(file_contents)
    elif uploaded_word_file:
        column_data = extract_table_column(uploaded_word_file, column_index=3)
        chunks = split_text(column_data)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        chunk_results = list(executor.map(process_chunk, chunks))

    combined_result = '\n'.join(chunk_results)
    final_result_without_keyword = GPT3().generate_text(combined_result, max_tokens)

    display_result(final_result_without_keyword, "最終要約結果")
    # 出力文字数を表示
    st.text(f"出力文字数: {count_characters(final_result_without_keyword)}文字")

    if keyword_input:
        final_result_with_keyword = GPT3().generate_text_keyword(combined_result, keyword_input, max_tokens)
        display_result(final_result_with_keyword, "最終要約結果 (キーワードあり)")
        # 出力文字数を表示
        st.text(f"出力文字数: {count_characters(final_result_with_keyword)}文字")
    
    else:
        keyword_input = "なし"
        final_result_with_keyword = "なし"

    if phrase_input:
        final_result_with_phrase = GPT3().generate_text_phrase(combined_result, phrase_input, max_tokens)
        display_result(final_result_with_phrase, "最終要約結果 (フレーズあり)")
        # 出力文字数を表示
        st.text(f"出力文字数: {count_characters(final_result_with_phrase)}文字")
    
    else:
        phrase_input = "なし"
        final_result_with_phrase = "なし"
    
    input_rireki(keyword_input, phrase_input, filename, final_result_without_keyword, final_result_with_keyword, final_result_with_phrase)
    
    display_rireki()

def input_history(keyword_input, phrase_input, filename, final_result_without_keyword, final_result_with_keyword, final_result_with_phrase):
    with open("history.txt", "w", encoding="utf-8") as file:
        file.write(f"{filename}\n")
    
    write_result(final_result_without_keyword, "（キーワード、フレーズなし）")
    
    if keyword_input:
        write_result(final_result_with_keyword, "（キーワード：" + keyword_input + "）")
    
    if phrase_input:
        write_result(final_result_with_phrase, "（フレーズ：" + phrase_input + "）")

def run_app():
    result = ""
    with st.form(key='profile_form'):
        user_input = st.text_input("平易化したい文章を入力してください")
        uploaded_file = st.file_uploader("または、テキストファイルをアップロードしてください", type=["txt"])
        uploaded_word_file = st.file_uploader("Wordファイルをアップロードしてください", type=["docx"])
        
        keyword_input = st.text_input("キーワードを入力してください ")
        phrase_input = st.text_input("要約に含めたい内容をフレーズで入力してください ")

        # 出力文字数の範囲を指定するためのラジオボタン
        selected_range = st.radio('出力文字数の範囲を選択してください', ['300~400 文字', '400~500 文字', '500~600 文字'])

        # 選択された範囲に基づいて max_tokens を設定
        if selected_range == '300~400 文字':
            max_tokens = 450
        elif selected_range == '400~500 文字':
            max_tokens = 600
        elif selected_range == '500~600 文字':
            max_tokens = 800
        else:
            # デフォルト値
            max_tokens = 450

        send_btn = st.form_submit_button('送信')
        delete_btn = st.form_submit_button('削除')
        input_history_btn = st.form_submit_button('テキストファイルに保存')

        col1, col2 = st.columns(2)
        button_style = """
            <style>
                div.stButton {
                    display: flex;
                    justify-content: center;
                }
            </style>
        """
        with col1:
            st.markdown(button_style, unsafe_allow_html=True)

        with col2:
            st.markdown(button_style, unsafe_allow_html=True)

        if send_btn:
            filename = uploaded_word_file.name  if uploaded_word_file else "no_filename"
            message = st.success('送信ボタンがクリックされました。')
            time.sleep(3)
            message.empty()

            # 空の入力をチェック
            if not user_input and not uploaded_file and not uploaded_word_file:
                st.error("エラー: 要約する文章がありません。")
                return

            sending_data(user_input, uploaded_file, uploaded_word_file, keyword_input, phrase_input, max_tokens, filename)

        if delete_btn:
            message = st.warning('削除ボタンがクリックされました。')
            time.sleep(3)
            message.empty()
            st.write(result)
        
        if input_history_btn:
            
            message = st.warning('テキストファイルに保存ボタンがクリックされました。')
            time.sleep(3)
            message.empty()
            
            with open('rireki.txt', 'r', encoding='utf-8') as file:
                file_contents = file.read()

            items = file_contents.split("\n<end>\n")
    
            if len(items) >= 2:
                output =  check_output()
                input_history(keyword_input, phrase_input, output[0], output[1], output[2], output[3])
            else:
                st.warning('テキストファイルに保存する結果がありません')
