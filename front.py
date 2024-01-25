import streamlit as st
import plotly.express as px
from PIL import Image

image = Image.open("static/nankai.png")

st.markdown("""
    <style>
        h4 {
            font-family: "Arial", sans-serif; /* フォントを指定 */
        }
        .title-bg{
            display: flex;
            padding: 0;
            margin: 0;
            background-color: #e0ffff;
            height: 60px;
        }
        .sub-title-bg{
            display: flex;
            padding: 0;
            margin: 0;
            background-color: #e0ffff;
        }
        .css-1l02znn {
            display: flex;
            align-items: center;
            padding: 0;
            margin: 0;
            text-align: center;
            color:white;
            border-radius: 40px;
            height: 50px;
            background-color: #0000cd;
            border-bottom: 1px solid #ccc;
        }
        .full-width-title {
            width: 100%;
            text-align: center;
            padding: 1rem; /* タイトルの上下左右の余白を追加 */
            background-color: #f0f0f0; /* タイトルの背景色を設定 */
        }
        .css-1fom3eu {
            flex: 1;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .streamlit-columns {
            margin-top: 20px; /* columnsの上に20pxの空白を追加 */
        }
        body {
            margin: 0;
            padding: 0;
        }
    </style>
""", unsafe_allow_html=True)

original_width, original_height = image.size
# 幅をオリジナルの10%に設定
target_width = int(original_width * 0.5)
st.image(image, width=target_width, use_column_width=False)

st.markdown(
    '<div class="title-bg">'
    '<h4>南海放送 特別番組！！～台本要約～</h4>'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title-bg">'
    '<h6>台本のセリフからあらすじを出力！！<br></h6>'
    '</div>',
    unsafe_allow_html=True
)
