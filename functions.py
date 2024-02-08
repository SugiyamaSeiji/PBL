import sys
import openai
import streamlit as st
import concurrent.futures
import os
from docx import Document

class GPT3:
    def __init__(self):
        openai.api_key = ""
    
    def generate_text(self, prompt, max_tokens):
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=[
             {"role": "system", "content": "あなたは要約者です"},
             {"role": "user", "content": f"「{prompt}」この文章を{max_tokens + 80}字程度に要約してください"}
            ]
        )
        return response['choices'][0]['message']['content']


    def generate_text_keyword(self, prompt, keyword, max_tokens):
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=[
             {"role": "system", "content": "あなたは要約者です"},
             {"role": "user", "content": f"「{prompt}」この文章を{max_tokens}字程度に要約してください。また 「{keyword}」というキーワードを要約結果に含めるようにしてください"}
            ]
        )
        return response['choices'][0]['message']['content']
    
    def generate_text_phrase(self, prompt, phrase, max_tokens):
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=[
             {"role": "system", "content": "あなたは要約者です"},
             {"role": "user", "content": f"「{phrase}」という内容を要約の中で強く伝えるようにして、「{prompt}」この文章を{max_tokens}字程度に要約してください。"}
            ]
        )
        return response['choices'][0]['message']['content']

def extract_table_column(docx_file, column_index):
    doc = Document(docx_file)
    text = ""
    
    for table in doc.tables:
        for row in table.rows:
            if len(row.cells) > column_index:
                text += row.cells[column_index].text + "\n"
                
    return text

def split_text(text, max_tokens=4000):
    chunks = [text[i:i + max_tokens] for i in range(0, len(text), max_tokens)]
    return chunks

def remove_newlines(text):
    return text.replace('\n', '')

def process_chunk(chunk, max_tokens=4000):
    gpt3 = GPT3()
    return gpt3.generate_text(chunk, max_tokens)

def input_rireki(keyword_input, phrase_input, filename, final_result_without_keyword, final_result_with_keyword, final_result_with_phrase):
    final_result_without_keyword = final_result_without_keyword.replace('\n', '')
    final_result_with_keyword = final_result_with_keyword.replace('\n', '')
    final_result_with_phrase = final_result_with_phrase.replace('\n', '')
        
    if not os.path.exists("rireki.txt"):
        with open("rireki.txt", "w", encoding="utf-8") as file:
            file.write("<end>\n")

    with open("rireki.txt", "r", encoding="utf-8") as file:
        now_content = file.read()
    
    new_content = f"{filename}\n{final_result_without_keyword}\n{keyword_input}\n{final_result_with_keyword}\n{phrase_input}\n{final_result_with_phrase}\n<end>\n"
    combined_content = new_content + now_content

    with open("rireki.txt", "w", encoding="utf-8") as file:
        file.write(combined_content)

def display_rireki():
    with open('rireki.txt', 'r', encoding='utf-8') as file:
            file_contents = file.read()

    items = file_contents.split("\n<end>\n")


    if len(items) >= 3:
        block = items[1].strip().split("\n")
        prev_filename = block[0]
        prev_final_result_without_keyword = block[1]
        prev_keyword_input = block[2]
        prev_final_result_with_keyword = block[3]
        prev_phrase_input = block[4]
        prev_final_result_with_phrase = block[5]
        st.markdown('\n\n')
        st.markdown(f'<div class="center"><h6>一つ前の履歴内容</h6></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="center"><h6>ファイル名：</h6></div>', unsafe_allow_html=True)
        st.markdown(f'<div style="background-color:#CBFFD3; padding:10px; border-radius:5px;">{prev_filename}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="center"><h6>最終要約結果：</h6></div>', unsafe_allow_html=True)
        st.markdown(f'<div style="background-color:#CBFFD3; padding:10px; border-radius:5px;">{prev_final_result_without_keyword}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="center"><h6>最終要約結果（キーワード：{prev_keyword_input}）：</h6></div>', unsafe_allow_html=True)
        st.markdown(f'<div style="background-color:#CBFFD3; padding:10px; border-radius:5px;">{prev_final_result_with_keyword}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="center"><h6>最終要約結果（フレーズ：{prev_phrase_input}）：</h6></div>', unsafe_allow_html=True)
        st.markdown(f'<div style="background-color:#CBFFD3; padding:10px; border-radius:5px;">{prev_final_result_with_phrase}</div>', unsafe_allow_html=True)
    
def write_result(result, option, file=None):   
    if file is None:
        with open("history.txt", "a", encoding="utf-8") as file:
            file.write(f"最終要約結果{option}\n")
            file.write(result + "\n")
    else:
        file.write(f"最終要約結果{option}\n")
        file.write(result + "\n")

def check_output():
    with open('rireki.txt', 'r', encoding='utf-8') as file:
            file_contents = file.read()

    items = file_contents.split("\n<end>\n")
    block = items[0].strip().split("\n")
    filename = block[0]
    final_result_without_keyword = block[1]
    final_result_with_keyword = block[3]
    final_result_with_phrase = block[5]
    
    return filename, final_result_without_keyword, final_result_with_keyword, final_result_with_phrase

def count_characters(text):
    count_fullwidth = sum(1 for char in text if 0xFF01 <= ord(char) <= 0xFF5E or ord(char) == 0x3000)
    count_halfwidth = len(text) - count_fullwidth
    count_word = count_fullwidth + count_halfwidth
    return count_word
