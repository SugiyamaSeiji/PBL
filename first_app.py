import streamlit as st
import plotly.express as px
from PIL import Image
image = Image.open("南海放送ロゴ.png")

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
            height: 90px;
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

import streamlit as st

st.markdown(
    '<div class="title-bg">'
    '<h4>南海放送 特別番組！！～台本要約～</h4>'
    '<h6>台本のセリフからあらすじを出力！！<br></h6>'
    '</div>',
    unsafe_allow_html=True
)

b = " "
st.text(b)

st.markdown('<div class="center"><h5>ファイルのアップロード</h5></div>', unsafe_allow_html=True)
st.file_uploader("言い換えをしたいファイルをアップロードしてね！",type=["docx"])

a = " "

output_text = "chatGPTで生成したあらすじ"

st.text(output_text)



# これは調節用の空白です
# 改善策求ム
# b = " "
# st.text(b)
# # ここからcolum1
# # col1, _, col2 = st.columns([2, 0.1, 2])
# #columごとやstreamlitごとにCSSを分けないと反映されなかったためコードが嵩んでいます
# #余裕があるときにCSSファイルにまとめておきます
# col1.markdown("""
#     <style>
#         .center {
#             display: flex;
#             align-items: center;
#             padding: 0;
#             margin: 0;
#             text-align: center;
#             border-bottom: 1px solid #ccc; /* タイトルとコンテンツの境界線を追加 */
#             background-color: #f0f0f0;
#         }
#         .button_center {
#             display: flex;
#             justify-content: center;
#         }
#     </style>
# """, unsafe_allow_html=True)
# button_label = "変換する"
# col1.markdown('<div class="center"><h3>ファイルのアップロード</h3></div>', unsafe_allow_html=True)
# col1.file_uploader("台本をアップロードしてください",type=["docx"])# ここの文章を直したい
# if col1.button("変換する"):
#     #chatGPTの処理を記述
#     #a = chatGPT文章
#     pass
# # ここからcolum2
# col1.markdown("""
#     <style>
#         .center {
#             display: flex;
#             align-items: center;
#             padding: 0;
#             margin: 0;
#             text-align: center;
#             border-bottom: 1px solid #ccc; /* タイトルとコンテンツの境界線を追加 */
#             background-color: #f0f0f0;
#         }
#     </style>
# """, unsafe_allow_html=True)
# a = "実験レポート助けて"
# output_text = a+"aaaaaaaaaaa\naaaaaaaaaaaaaaaaaaaa"
# # これも調節用の空白です　直し方を考えている途中です　出来てなくてすみません
# col2.text(b)
#
# # 列2に要素を追加
# col2.markdown('<div class="center"><h3>変換後のテキスト</h3></div>', unsafe_allow_html=True)
# col2.text("出力専用のテキストボックス")
# col2.text(output_text)
