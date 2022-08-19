import streamlit as st

Mylist = [1,2,3]
if(l := len(Mylist) > 2):
    st.print(len(Mylist))
    st.print(l)