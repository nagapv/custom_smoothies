# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
# from snowflake.snowpark.context import get_active_session

# Connection to snowflake.
cnx = st.connection("snowflake")
session = cnx.session()
# Below line is for Streamlit in Snowflake.
# session = get_active_session()

# Write directly to the app
st.markdown("<h1 style='text-align: center; color: red;'>🥤🥤🥤</h1>", unsafe_allow_html=True)
st.title("Customize Your Smoothie!")
st.write(
    """
    Choose the fruits you want in your custom Smoothie, by Naga :smiley:
    """
)

name_on_order = st.text_input("**Name on Smoothie:**")
if name_on_order:
    st.write("The name on your Smoothie will be:", name_on_order)

# Reading choices from Snowflake table.
# my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

# For doing the same in Streamlit in Snowflake.
# my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# # st.dataframe(data=my_dataframe, use_container_width=True)

# ingredients_list = st.multiselect(
#      '**Choose up to 5 ingredients:**',
#     my_dataframe, max_selections=5
# )

# Offering only limited choices internally.
ingredients_list = st.multiselect(
    "**Choose up to 3 ingredients:**",
    ["Apple 🍎", "Banana 🍌", "Mango 🥭", "Peaches 🍑", "Pineapple 🍍", "Strawberries 🍓"],
    max_selections=3
)
# st.write("Your favourite fruit is:", ingredients_list)
# https://docs.streamlit.io/develop/api-reference/widgets/st.selectbox
# https://docs.streamlit.io/develop/api-reference/widgets/st.multiselect

st.write("**Add some milk 🥛?**")
include_milk = st.checkbox("Yes please!")

sweet_type = st.radio("**Choose your sweetener:**",
                      ["Sugar","Sugarfree","Honey","No sweetener!"])

if sweet_type != "No sweetener!":
    st.write("Your sweetener:", sweet_type)
    sweet_level = st.slider("**How much of sweetner?**",
                                0, 150, value=100, step=25)
else:
    st.write("Your sweetener: None, healthy choise!")
    sweet_level = 0

if (ingredients_list and sweet_type):
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredients_string = ", ".join(ingredients_list)

    # st.write(ingredients_string)

    my_insert_stmt = """insert into smoothies.public.orders(
                name_on_order, ingredients, include_milk, sweet_type, sweet_level
                )
            values (
            '""" + name_on_order + """', '""" + ingredients_string + """',
            '""" + str(include_milk).capitalize() + """', '""" + sweet_type + """',
            '""" + str(sweet_level) + """'
            )"""

    # st.write(my_insert_stmt)
    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered!', icon="✅")
