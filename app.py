import streamlit as st
from router import route_question

st.title("🌱 Agri Climate Intelligence Assistant")

query = st.text_input("Ask question:")

if st.button("Ask"):
    result = route_question(query)
    st.write(result)