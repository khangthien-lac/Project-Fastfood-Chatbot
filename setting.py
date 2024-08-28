import streamlit as st
import pandas as pd
from model_command import embed_fn

df = pd.read_excel(r'F:\Study\AI\2nd Project\Doc\Dat2.xlsx',index_col=0)  #Đọc dataset
df['Comments'] = df['Đánh giá trung bình'] + df['Giới thiệu về quán']
df['C_Embeddings'] = df.apply(lambda row: embed_fn(row['Tên quán'], row['Comments']), axis=1) #Embedding các đánh giá về quán
st.session_state.df = df
st.header("Cài đặt")
st.write(f"Địa chỉ hiện tại của bạn: ")
st.write(f'{st.session_state.user_address}')