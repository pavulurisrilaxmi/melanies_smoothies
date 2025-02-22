# Import python packages
import streamlit as st

cnx = st.connection('snowflake')
session = cnx.session()
import requests

from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """choose the fruits you want in your custom smoothie! :apple: :pineapple:
    """
)

import streamlit as st

    ##option = st.selectbox("what is your favorite fruit",("Banana", "Strawberries", "peaches"), )
    
    ##st.write("your favorite fruit is:", option)

import streamlit as st

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be:', name_on_order )


my_dataframe = session.table("smoothies.public.fruit_options").select (col('Fruit_Name'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#convert the snowspark dataframe to panda dataframe to use the LOC function

pd_df= my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredients_list = st.multiselect(
    "choose upto 5 ingredients",
    my_dataframe, 
    max_selections=5
)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text (ingredients_list)
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        # st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ search_on)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
        
    #st.write (ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
