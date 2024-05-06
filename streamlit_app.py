# Import python packages
import streamlit as st
import pandas as pd
import requests

# Write directly to the app
st.title("Customer Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie")
# Here will place some input and labels ##
#title = st.text_input('Name of your Smoothie', )
#st.write('The current movie title is', title)
name_on_order = ''
name_on_order = st.text_input("Name of your Smoothie: ")
st.write("The name on your order Smoothie will be : ", name_on_order)
from snowflake.snowpark.functions import col
cnx=st.connection("snowflake")
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
pd_df=my_dataframe.to_pandas()
st.dataframe (pd_df)
#st.stop()
ingredients_list = st.multiselect(
    'Choose Upto 5 Ingredients:'
    ,my_dataframe
    ,max_selections=5)

if ingredients_list:
    sqlstatement = ''
    ingredients_string=''
    for  fruit_chosen in ingredients_list:
        ingredients_string +=   fruit_chosen + ' ';
        
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')


    sqlstatement = """ insert into smoothies.public.orders(ingredients,name_on_order)
                values ('""" + ingredients_string + """','""" + name_on_order +"""' )""";


    
    time_to_insert = st.button("Submit Order")
    
    if time_to_insert:


        session.sql(sqlstatement).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
