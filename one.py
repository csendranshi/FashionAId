import streamlit as st
import google.generativeai as genai
import pymongo
from config import api_key
import requests

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["FashionAId-DB"]
my_profiles = db["Profiles"]


st.title('Outfit Recommendation App 👗')
st.subheader('Get instant Outfit Recommendations')

# User inputs
name = st.text_input("Enter Your Name please")
occasion = st.text_input('The occasion you want the dress for')
aesthetic = st.text_input('Choose your desired aesthetic')
extra = st.text_input('Additional information/requests')

if name:
    my_profile_details = my_profiles.find({"name" : name})
    if my_profile_details:
        my_profile_details = my_profile_details[0]

prompt_enter = st.button("Outfit") 

# prompt = f''' Can you create 4 outfit ideas (10 lines max) for the particular occasion,
#  based on aesthetic, for the weather, the type of clothes, the colour combinations, the gender, and
#  any extra information but dont give extra info more priority over the other fields:
# particular occasion:{occasion},
# aesthetic:{aesthetic} ,
# weather:{weather} ,
# gender:{gender},
# type of clothes:{type_of_clothes} ,
# colour combinations:{color_combos} ,
# extra iinformation:{extra} ,
# If either of the instruction is not present use the best of your judgement to assume it,
# use as many fashion blogs as you want to make a decision and
# give the top 10 results bulletted in seperate lines
#     Outfit :<name of the outfit>
#
# '''

prompt = f''' Can you create 4 outfit ideas for the particular occasion, and given aesthetic and
using the information enclosed in wardrobe, and 
 any extra information but dont give extra information more priority over the other fields:
particular occasion:{occasion},
aesthetic:{aesthetic} ,
information enclosed in wardrobe: {my_profile_details},
extra information:{extra} ,
If either of the instruction is not present use the best of your judgement to assume it, 
use as many fashion blogs as you want to make a decision and 
give the top 10 results bulletted in seperate lines
    Outfit :<name of the outfit>

'''

genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name = "gemini-pro")


# Show stuff to the screen if there's a prompt
try:
    if prompt_enter:
        response = model.generate_content(prompt)
        st.write(response.text)
except Exception as error:
    st.write("An error has occurred", SystemExit(error))


st.write("Enjoy your event")