# main.py
import os
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
from gemini_util import (load_gemini_pro_model, gemini_pro_vision_response)

# Setting up page configuration
st.set_page_config(
    page_title="SortifyAI",
    page_icon="🧠",
    layout="centered"
)

# Sidebar navigation
with st.sidebar:
    selected = option_menu("SortifyAI",
                           ["SortifyAI"],
                           icons=['chat-dots-fill'],
                           default_index=0)

# Progress tracking system
if "student_progress" not in st.session_state:
    st.session_state.student_progress = {
        "questions_asked": 0,
        "hints_given": 0,
        "answer_requested": False
    }

# Function to identify which sorting algorithm the user is asking about
def detect_sorting_algorithm(user_prompt):
    algorithms = ["quicksort", "mergesort", "bubblesort", "insertionsort", "heapsort", "selectionsort"]
    for algo in algorithms:
        if algo in user_prompt.lower():
            return algo
    return None

# Function to dynamically generate Socratic questions based on the student's input and detected algorithm
def generate_socratic_question(user_prompt, detected_algorithm):
    # Sending prompt to model to generate a Socratic question
    query = f"As a Socratic teaching assistant, ask a probing question to guide the student about {detected_algorithm} based on the student's input: '{user_prompt}'."
    with st.spinner("Response generating..."):
        model_response = st.session_state.chat_session.send_message(query)
    #model_response = st.session_state.chat_session.send_message(query)
    return model_response.text.strip()

# Function to dynamically generate a hint based on the student's input and detected algorithm
def generate_hint(user_prompt, detected_algorithm):
    # Sending prompt to model to generate a context-specific hint
    query = f"As a teaching assistant, provide a helpful hint for {detected_algorithm} that addresses the student's input: '{user_prompt}'."
    model_response = st.session_state.chat_session.send_message(query)
    return model_response.text.strip()

# Function to ask if the student wants the answer
def ask_for_answer():
    return "Would you like to know the answer now? Type 'yes' if you'd like to see it, or continue exploring with more questions and hints."

# Function to dynamically generate the final answer based on the algorithm
def generate_final_answer(detected_algorithm):
    # Generating a final, concise answer about the detected algorithm
    query = f"Provide a detailed but concise explanation of the key points and time complexity of {detected_algorithm}."
    model_response = st.session_state.chat_session.send_message(query)
    return model_response.text.strip()

# Function to handle the conversation flow
def handle_student_response(user_prompt, detected_algorithm):
    # Asking if the student wants the answer after a few hints
    if st.session_state.student_progress["hints_given"] >= 3 and not st.session_state.student_progress["answer_requested"]:
        return ask_for_answer()

    # Otherwise, generate the next probing question
    next_question = generate_socratic_question(user_prompt, detected_algorithm)
    st.session_state.student_progress["questions_asked"] += 1
    return next_question

# Function to save conversation history and generate a downloadable file
def save_conversation():
    # Prepare the conversation history as a string
    conversation_text = "Conversation History:\n\n"
    for message in st.session_state.chat_session.history:
        role = "User" if message.role == "user" else "Assistant"
        conversation_text += f"{role}: {message.parts[0].text}\n\n"

    # Save the conversation to a text file
    file_path = "conversation_history.txt"
    with open(file_path, "w") as file:
        file.write(conversation_text)
    return file_path

if selected == "SortifyAI":
    model = load_gemini_pro_model()

    # Initialize chat session if not already present
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    # Streamlit page title
    st.title("🤖 SortifyAI!! How can I help?")

    # Display the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(message.role):
            st.markdown(message.parts[0].text)

    # Input field for user's message
    user_prompt = st.chat_input("Ask your query about Sorting Algorithms....")
    if user_prompt:
        st.chat_message("user").markdown(user_prompt)

        # Detect which sorting algorithm is being discussed
        detected_algorithm = detect_sorting_algorithm(user_prompt)

        # Check if the student has already requested the answer
        if st.session_state.student_progress["answer_requested"] or user_prompt.lower() == "yes":
            answer = generate_final_answer(detected_algorithm)
            with st.chat_message("assistant"):
                st.markdown(answer)
            st.session_state.student_progress["answer_requested"] = True
        else:
            # Generate the next step: either a hint or Socratic question
            next_step = handle_student_response(user_prompt, detected_algorithm)

            # Display the Socratic question or hint
            with st.chat_message("assistant"):
                st.markdown(next_step)

            # Increment hint count if the response is a hint
            if "hint" in next_step.lower():
                st.session_state.student_progress["hints_given"] += 1

    # Show student progress
    st.sidebar.write(f"Questions Asked: {st.session_state.student_progress['questions_asked']}")
    st.sidebar.write(f"Hints Given: {st.session_state.student_progress['hints_given']}")
    st.sidebar.write(f"Answer Requested: {st.session_state.student_progress['answer_requested']}")

    # Button to save and download the conversation
    if st.sidebar.button("Save and Download Conversation"):
        file_path = save_conversation()
        with open(file_path, "rb") as file:
            st.sidebar.download_button(
                label="Download Conversation",
                data=file,
                file_name="conversation_history.txt",
                mime="text/plain"
            )








