import google.generativeai as genai
import os
import streamlit as st
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
import geopy.distance as dis
from geopy.extra.rate_limiter import RateLimiter

#Hàm tìm tên các món có trong prompt
def find_fast_food(description: str, location: bool = False):
    """
    Identify fast food type based on a description provided by the user.

    Args:
        description: Any kind of description including specific food types, cravings, or attributes.

    Returns:
        A list of fast food types that match the description.
    """
    if location == False:
        fast_food_types = {
            "burger": ["Burger", "burger phô mai"],
            "pizza": ["Pizza", "Pizza Pepperoni"],
            "sushi": ["Sushi"],
            "khoai tây chiên": ["khoai tây chiên phô mai", "khoai tây lốc xoáy"],
            "tacos": ["Tacos", "Burrito"],
            "gà": ["gà rán", "gà viên"]
        }

        for keyword, foods in fast_food_types.items():
            if keyword.lower() in description.lower(): #Tìm trong input của user
                return foods

        return ["Unknown fast food"] #Nếu không có trong danh sách thì trả về

#Hàm để embedding prompt
def embed_fn(title, text): 
  return genai.embed_content(model=finder,
                             content=text,
                             task_type="retrieval_document",
                             title=title)["embedding"]

#Hàm tìm ra quán ăn hợp với yêu cầu nhất
def find_best_loc(query, dataframe,user_cord):
  distance = []
  query_embedding = genai.embed_content(model=finder,
                                        content=query,
                                        task_type="retrieval_query")
  dot_products = np.dot(np.stack(dataframe['C_Embeddings']), query_embedding["embedding"])
  dot_products_after_sort = np.sort(dot_products)[::-1][:3] #Lấy ra 3 shop có dp cao nhất
  for i in dot_products_after_sort: 
    address = dataframe.iloc[np.where(dot_products == i)]['Địa chỉ'].values[0] #Tìm quán có địa chỉ tương ứng
    print(dataframe.iloc[np.where(dot_products == i)]['Tên quán'].values[0])
    location = loc.geocode(address, namedetails=True)
    cord = (location.latitude, location.longitude)
    distance.append(dis.geodesic(cord, user_cord).km) #Tính khoảng cách tới user
  if 0 in distance: distance.remove(0)
  min_dis = np.argmin(distance)
  idx = np.where(dot_products == dot_products_after_sort[min_dis]) #Trả về index của quán
  print(idx)
  return dataframe.iloc[idx]['Tên quán'].values[0],dataframe.iloc[idx]['Link'].values[0], min_dis

#Hàm điều chỉnh tên các role để phù hợp với streamlit
def role_to_streamlit(role):
  if role == "model":
    return "assistant"
  else:
    return role

finder = 'models/embedding-001'
loc = Nominatim(user_agent="vuanhkhoinee@gmail.com")
geolocator = RateLimiter(loc.geocode, min_delay_seconds=1) 