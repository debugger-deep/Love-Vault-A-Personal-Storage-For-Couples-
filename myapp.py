import streamlit as st
from os import listdir
from datetime import datetime
st.set_page_config(page_icon="❤️",page_title="Love Vault")

# Basic credentials
credentials = {"arghyadeep": "togetherforever", "aaeshi": "togetherforever"}

# Memory storage directory
memory_dir = "memories/"

# Initialize session state for login persistence
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = ""

def login():
    st.title("❤️Welcome to Our Virtual Memory Box Babe!!❤️")
    st.caption("Developed by your love❤️")
    st.write("A space filled with love and memories - created just for us.")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in credentials and password == credentials[username]:
            st.session_state['logged_in'] = True
            st.session_state['current_user'] = username
            st.success(f"Login successful! Welcome, {username.capitalize()}! 🌸")
        else:
            st.error("Incorrect credentials. Love is the key! 😉")

def memory_box():
    st.title("Upload Our Cherished Memories Babyy!!❤️")
    st.caption("Developed by Arghyadeep")
    st.write(f"Hello, {st.session_state['current_user'].capitalize()}! 💕")
    st.write("Let's create some beautiful memories together. Share a special moment with me below:")

    # Text memories
    text_message = st.text_area("Write a message or memory", "")
    if st.button("Save Message"):
        if text_message:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(memory_dir + "messages.txt", "a") as f:
                f.write(f"[{timestamp}] {st.session_state['current_user'].capitalize()} wrote: {text_message}\n")
            st.success("Your sweet message has been saved with all my love! 💌")
        else:
            st.warning("Don’t forget to share something special! 😘")

    # Upload files (photos, voice notes, etc.)
    uploaded_files = st.file_uploader("Upload photos or voice notes that remind us of each other", type=["jpg", "jpeg", "png", "mp3", "wav"], accept_multiple_files=True)
    for file in uploaded_files:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_path = memory_dir + file.name
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        # Save file details in a log
        with open(memory_dir + "file_log.txt", "a") as log:
            log.write(f"[{timestamp}] {st.session_state['current_user'].capitalize()} uploaded: {file.name}\n")
        st.success(f"{file.name} has been lovingly added to our collection! 🥰")

def display_memories():
    st.title("💖 Our Precious Memories 💖")
    st.write("Here’s a collection of the moments we've shared:")

    # Display text messages
    try:
        st.write("**Messages of Love:**")
        with open(memory_dir + "messages.txt", "r") as f:
            for line in f.readlines():
                st.write(line.strip())
    except FileNotFoundError:
        st.info("No messages yet. Start adding some loving words for us!")

    # Display uploaded files with timestamps and names
    st.write("**Photos and Voice Notes:**")
    try:
        with open(memory_dir + "file_log.txt", "r") as log:
            for entry in log.readlines():
                st.write(entry.strip())
                file_name = entry.split(": ")[1].strip()
                if file_name.endswith((".jpg", ".jpeg", ".png")):
                    st.image(memory_dir + file_name)
                elif file_name.endswith((".mp3", ".wav")):
                    st.audio(memory_dir + file_name)
    except FileNotFoundError:
        st.info("No photos or voice notes uploaded yet. Let’s capture some beautiful moments!")

def add_footer():
    st.write("")
    st.write("")
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='text-align: center;'>
            <p style='color: grey; font-size: 14px;'>Made with 💖 by <strong>Arghyadeep</strong> for <strong>Aaeshi</strong></p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    if not st.session_state['logged_in']:
        login()  # Show the login page only if not logged in
    else:
        st.sidebar.title("Our Memory Box 💖")
        
        option = st.sidebar.radio("Choose an option", ["Upload Memories", "View Memories"])

        if option == "Upload Memories":
            memory_box()
        elif option == "View Memories":
            display_memories()

        add_footer()
