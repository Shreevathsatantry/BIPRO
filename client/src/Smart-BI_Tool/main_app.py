import streamlit as st

# Set page config, this should be the first Streamlit command
st.set_page_config(
    page_title="Smart BI Tool",
    layout="wide"
)

# Now import your modules
from modules import Clean, dashboard_self, Overview1, vizzu , Pygwalk, Chat, app
#

# Sidebar for navigation
with st.sidebar:
    st.title("Navigation")
    page = st.selectbox(
        "Choose a page", 
        [
            "Home", 
            "Data Cleaning (AutoClean)", 
            "Dynamic Dashboard", 
            "Data Visualization", 
            "Data Analysis", 
            "Chat with Dataset", 
            "Knowledge graph",
            "Vizzu Animation"
        ]
    )

# Home Page
if page == "Home":
    st.markdown("<h1 style='text-align: center;'>Welcome to Smart BI Tool</h1>", unsafe_allow_html=True)
    image_path = r"C:\Users\shree\Desktop\Final_BI_tool\BIPro-latest\client\src\assets\streamlit_image.png"
    st.image(image_path)


# Page-specific logic
elif page == "Data Cleaning (AutoClean)":
    Clean.show_page()  

elif page == "Dynamic Dashboard":
    dashboard_self.show_page()  

elif page == "Data Visualization":
    Pygwalk.show_page()

elif page == "Data Analysis":
    Overview1.show_page()

elif page == "Chat with Dataset":
    Chat.show_page()

elif page == "Knowledge graph":
    app.show_page()

elif page == "Vizzu Animation":
    vizzu.show_page()
