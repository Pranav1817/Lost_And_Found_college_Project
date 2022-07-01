import pickle
from pathlib import Path
from tkinter import Button, OptionMenu, image_names
from turtle import width, window_width
from webbrowser import BackgroundBrowser
from sqlalchemy import null
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import streamlit_authenticator as sa

df = pd.read_csv("post.csv")
df.index = df.index + 1
st.set_page_config(page_title="RCOEM: Lost and Found", layout="wide",page_icon="lostandfound.png")


#--- USER AUTHENTICATION.

names = ["Pranav", "Rajat","Prajwal"]
username = ["Pranav123","Rajat123","Prajwal123"]

file_path = Path(__file__).parent / "hashed_passwords.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = sa.Authenticate(names, username,hashed_passwords,"sales_dashboard","abcdef",cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login","main")

if authentication_status == False:
    st.error("Username/password is not correct")

if authentication_status == None:
    st.warning("Please enter your user name and Password.")

if authentication_status == True:

    st.title("RCOEM: Lost and Found web application")
    st.sidebar.header("Menu")
    st.sidebar.title(f"Welcome {name}")
    selected = option_menu("Main Menu", ['Refresh','Create or Delete Report','Contact','About'],orientation="horizontal")
    authenticator.logout("Logout","sidebar")

    if selected == 'Refresh':
        st.title("Current Lost or Found Post: ")
        st.write(df)

    if selected == 'About' :
        st.write("This web application helps you to find your lost object. Main objective of our project is to increase the connectivity of the people in our workpalce.")

        st.markdown("1. What to do if you found any stray object ?")
        st.write("Answer: If you found any object and you found nobody who confem that it belong to him/her then you can login to our web application and create a found report. Then go to lost and found department. Submit that object.")

        st.markdown("2. What to do if you lost your any thing ?")
        st.write("Answer: If you lost your object then just quickly login to our website and check if some has written a found report. if yes contact to Admin and tell him that this object belong to you He/She will ask you about some of the dispription of your lost your object if the discription matches with the object then you can collect the object form the lost and found department.")

        st.markdown("3. You might thinking: 'What will I get by helping others to find there lost object ?' ")
        st.write("Answer: Lets be honest we all can relate how bad and abscent minded it feels when we loose any object. So by your simple effort if you can help someone to reduce there tension. Then why not do it.")
        st.write("But yes to promote you to help in these good cause we have decided to give you (refering to the person who found any object) some credit points. Based on the number of credit you will recieve some incentive.")


    if selected == 'Contact':
        from PIL import Image
        img = Image.open("Admin_of_lost_and_found_web_application.jpg")
        st.image(img)
        st.markdown("Admin: Mr. XYZ (This pic does not belong to us all right reserve to respective creators) ")
        st.markdown("To contact our lost and found admin you can email Mr. XYZ at xyz@rknec.edu or call at Phone no: +91 9527240965 ")
        st.markdown("you can call during college hours i.e. form 8:00 AM to 5:00 PM ")
        st.markdown("If in case you call and no body pick up the call then feel free to leave a voice note. Our abmin will contact you as soon as possible.")

    if selected == 'Create or Delete Report':
#------- Display the post----------------------------
        st.title("Current Lost or Found Post: ")
        st.write(df)


#------- Delete the existing post--------------------
        st.markdown("Want to delete a post ? ")
        option_form3 = st.form("options_form3")
        Id2 = st.number_input("Enter post id which you want to delete")
        delete = st.button("Delete")
        if delete:
            df = df.drop(df[df.Id  ==  Id2].index)
            df.to_csv('post.csv',index=False)

#------ Creation of a post-------
        st.write("Create a post: ")
        option_form2 = st.form("options_form2")
        name = option_form2.text_input("Enter your Name")
        Id = option_form2.number_input("Enter your ID")
        type = option_form2.text_input("Mention is it a lost report or found report: ")
        depertment = option_form2.text_input("Enter name of your department")
        description = option_form2.text_area("Write in detail explaining your position.")
        update = option_form2.form_submit_button('Create post')
        if update:
            new_data = {"Id": Id,"Name of Creator": name,"Name of department":depertment,"Type of Report": type,"Description": description}
            df = df.append(new_data,ignore_index=True)
            df.to_csv("post.csv",index=False)
        

        


