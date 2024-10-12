import streamlit as st
import yaml
from yaml.loader import SafeLoader
from streamlit_cookies_controller import CookieController

controller = CookieController()


with open('auth_config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)


def check_credentials(username, password):
    if username in config['credentials']['usernames']:
        if config['credentials']['usernames'][username]["password"] == password:
            return True
    return False

def authentication_ui():
    placeholder = st.empty()
    with placeholder.form("login"):
        st.markdown("#### Enter your credentials")
        username = st.text_input("User")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
    
    if submit and check_credentials(username, password):
        st.session_state["login_status"] = True
        st.session_state["username"] = username
        controller.set('login_status', True)
        controller.set('logged_in_user', username)
        placeholder.empty()
        st.success(f"Login successful. Welcome, {username}!")
    elif submit:
        st.error("Either username or password is incorrect")

def i_am_in():
    logged_in_user = st.session_state.get("username", controller.get('logged_in_user'))
    if logged_in_user:
        st.write(f"Welcome, {logged_in_user}!")
    if st.button("Log out"):
        st.session_state.clear()
        controller.remove('login_status')
        controller.remove('logged_in_user')

def check_password():
    if 'login_status' not in st.session_state:
        if controller.get('login_status'):
            st.session_state['login_status'] = True
            st.session_state['username'] = controller.get('logged_in_user')
        else:
            authentication_ui()
    if st.session_state.get("login_status"):
        return True

