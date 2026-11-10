import streamlit as st
from snowflake.snowpark.functions import col

st.set_page_config(
    page_title="Custom Smoothie Order Form",
    page_icon="🥤",
)

st.title("🥤 Customize Your Smoothie!")
st.write("Choose the fruits you want in your custom smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table(
    "SMOOTHIES.PUBLIC.FRUIT_OPTIONS"
).select(col("FRUIT_NAME"))

fruit_options = [row["FRUIT_NAME"] for row in my_dataframe.collect()]

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_options,
    max_selections=5,
)

if ingredients_list:
    ingredients_string = ""

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + " "

    my_insert_stmt = f"""
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS
            (INGREDIENTS, NAME_ON_ORDER)
        VALUES
            ('{ingredients_string}', '{name_on_order}')
    """

    if st.button("Submit Order"):
        session.sql(my_insert_stmt).collect()
        st.success(
            f"Your Smoothie is ordered, {name_on_order}!",
            icon="✅",
        )