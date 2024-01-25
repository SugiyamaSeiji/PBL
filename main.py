import streamlit as st
from PIL import Image
from generate import run_app

st.markdown('<link rel="stylesheet" href="styles.css">', unsafe_allow_html=True)

image = Image.open("static/nankai.png")

original_width, original_height = image.size
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

if __name__ == "__main__":
    run_app()