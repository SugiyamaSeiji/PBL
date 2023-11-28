
import streamlit as st


import openai

import sys



from docx import Document

import concurrent.futures




class GPT3:
    def __init__(self):
        openai.api_key = "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"
    
    def generate_text(self, prompt):
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=[
             {"role": "system", "content": "あなたは要約者です"},
             {"role": "user", "content": f"「{prompt}」この文章を３００字程度に要約してください"}
            ]
        )
        return response['choices'][0]['message']['content']



# ページのタイトルを設定
st.set_page_config(page_title="chatgpt3.5 API Demo", page_icon=":smiley:")

# アプリのタイトルを設定
st.title("平易化")

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

def process_chunk(chunk):
    gpt3 = GPT3()
    return gpt3.generate_text(chunk)

with st.form(key='profile_form'):
    user_input = st.text_input("平易化したい文章を入力してください")
    uploaded_file = st.file_uploader("または、テキストファイルをアップロードしてください", type=["txt"])
    uploaded_word_file = st.file_uploader("Wordファイルをアップロードしてください", type=["docx"])

    send_btn = st.form_submit_button('送信')
    delete_btn = st.form_submit_button('削除')
    
    

    if send_btn:
        result = ""
        
       
        
        

        if user_input:
          
            chunks = split_text(user_input)
            
        elif uploaded_file:
            file_contents = uploaded_file.read().decode('utf-8')
            chunks = split_text(file_contents)
            
        elif uploaded_word_file:
            column_data = extract_table_column(uploaded_word_file, column_index=3) 
            chunks = split_text(column_data)
            
            
           
                
          
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Process each chunk in parallel while preserving order
            chunk_results = list(executor.map(process_chunk, chunks))

        result = ''.join(chunk_results)
            
        gpt3 = GPT3()
        result = gpt3.generate_text(result)

            
            
            
            
        st.write(result)
            

        
        
    if delete_btn:
        result = ""