import google.generativeai as genai
import os
import streamlit as st
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
import geopy.distance as dis
from geopy.extra.rate_limiter import RateLimiter
from model_command import embed_fn, find_best_loc, role_to_streamlit

genai.configure(api_key='AIzaSyBbpsd22RnM0BXGNRSHzuZ1-ju7p7W9hvQ')
if "user_cord" not in st.session_state: #Kiểm tra xem user có nhập địa chỉ không
    st.session_state.user_cord = None
#Khu vực lúc mới vào web
def pre_enter(): 
    st.header('Địa chỉ của bạn')
    user_address = st.text_input("Hãy nhập vào đây địa chỉ của bạn",placeholder='235 Nguyễn Văn Cừ, Phường 4, Quận 5, Hồ Chí Minh , Việt Nam')
    user_location = loc.geocode(user_address, namedetails=True)
    if st.button("Bắt đầu"):
        if user_location != None:
            user_cord = (user_location.latitude, user_location.longitude)
            st.session_state.user_address = user_address
            st.session_state.user_cord = user_cord
            st.rerun()
        else: st.warning('Hãy nhập lại địa chỉ hợp lệ')

#Tắt và quay về ban đầu
def end_chat():
    st.session_state.user_cord = None
    st.session_state.chat.history = None
    st.rerun()

#Các trang phụ
loc = Nominatim(user_agent="vuanhkhoinee@gmail.com")                      #Khởi tạo agent để sử dụng geopy
geolocator = RateLimiter(loc.geocode, min_delay_seconds=1)                #Giới hạn số yêu cầu gửi về server của geopy
user_cord = st.session_state.user_cord
logout_page = st.Page(end_chat, title="Kết thúc chat", icon=":material/logout:")
settings = st.Page("setting.py", title="Cài đặt", icon=":material/settings:")
model_chat = st.Page('All/model.py',title='Model')
introduction = st.Page('All/introduce.py',title='Giới thiệu',default=(user_cord != ''))

alll = [introduction,model_chat]
account_pages = [logout_page, settings]

st.title("Hướng dẫn viên về fast food của riêng bạn")

#Điều chỉnh kích thước logo
st.html("""
  <style>
    [alt=Logo] {
      height: 4rem;
    }
  </style>
        """)
st.logo(r"Image\Fulllogo-removebg-preview.v1.png", icon_image=r"Image\logo-removebg-preview.v1.png")

page_dict = {}
if st.session_state.user_cord != None: #Kiểm tra địa chỉ để cho truy cập vào các trang sâu hơn
    page_dict["All"] = alll
if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict)
else:
    pg = st.navigation([st.Page(pre_enter)])
pg.run()