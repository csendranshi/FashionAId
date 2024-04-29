import streamlit as st
import google.generativeai as genai
import pymongo
from config import streamlit_api_key, weather_api_key
import requests

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["FashionAId-DB"]
my_profiles = db["Profiles"]

lat = "40.7209"
lon = "74.0007"

url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_key}&cnt=1"

response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Print the response content (usually in JSON format)
    data = response.json()
else:
    # Print an error message if the request was not successful
    print("Error:", response.status_code)



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
Weather info: {data['list']}
If either of the instruction is not present use the best of your judgement to assume it, 
use as many fashion blogs as you want to make a decision and 
give the top 10 results bulletted in seperate lines
    Outfit :<name of the outfit>

'''

genai.configure(api_key=streamlit_api_key)
model = genai.GenerativeModel(model_name = "gemini-pro")


# Show stuff to the screen if there's a prompt
try:
    if prompt_enter:
        response = model.generate_content(prompt)
        st.write(response.text)
except Exception as error:
    st.write("An error has occurred", SystemExit(error))


st.write("Enjoy your event")