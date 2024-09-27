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
                           menu_icon='robot', icons=['chat-dots-fill'],
                           default_index=0)

# Progress tracking system
if "student_progress" not in st.session_state:
    st.session_state.student_progress = {
        "questions_asked": 0,
        "hints_given": 0,
        "answer_requested": False,
        "confirmation_requested": False  # Track whether confirmation is requested before final answer
    }

# Function to dynamically generate Socratic questions based on the student's input
def generate_socratic_question(user_prompt):
    query = f"As a Socratic teaching assistant, ask a probing question to guide the student based on the student's input: '{user_prompt}'. The questions should be framed in such a way that they guide the student to the answer they asked"
    model_response = st.session_state.chat_session.send_message(query)
    return model_response.text.strip()

# Function to dynamically generate a hint based on the student's input
def generate_hint(user_prompt):
    query = f"As a teaching assistant, provide a helpful hint that addresses the student's input: '{user_prompt}'."
    model_response = st.session_state.chat_session.send_message(query)
    return model_response.text.strip()

# Function to ask if the student wants the answer
def ask_for_answer():
    return "Would you like to know the answer now? Please confirm by typing 'confirm'."

# Function to dynamically generate the final answer based on the user's prompt
def generate_final_answer(user_prompt):
    query = f"Provide a detailed but concise explanation to answer the student's question: '{user_prompt}'."
    model_response = st.session_state.chat_session.send_message(query)
    return model_response.text.strip()

# Function to detect dynamic user requests for the final answer
def is_requesting_final_answer(user_prompt):
    keywords = ["final answer", "solution", "can you tell me", "please provide", "I want the answer"]
    return any(keyword in user_prompt.lower() for keyword in keywords)

# Function to detect when student has reached sufficient understanding or the correct answer
def check_understanding(user_prompt):
    # Define keywords or phrases indicating the student has reached a good understanding
    understanding_keywords = ["got it", "understood", "makes sense", "thank you", "I get it", "that helps"]
    return any(keyword in user_prompt.lower() for keyword in understanding_keywords)

# Function to handle the end of the conversation
def conclude_conversation():
    conclusion_message = "Great! It seems like you've got a solid understanding of the concept. 😊 Would you like to end the conversation now? If so, just type 'end'."
    st.session_state.student_progress["answer_requested"] = True  # Mark conversation as ending
    return conclusion_message

# Function to handle the conversation flow
def handle_student_response(user_prompt):
    if is_requesting_final_answer(user_prompt):
        st.session_state.student_progress["confirmation_requested"] = True
        return ask_for_answer()

    # Asking if the student wants the answer after a few hints
    if st.session_state.student_progress["hints_given"] >= 3 and not st.session_state.student_progress["answer_requested"]:
        st.session_state.student_progress["confirmation_requested"] = True
        return ask_for_answer()

    # Generate the next probing question
    next_question = generate_socratic_question(user_prompt)
    st.session_state.student_progress["questions_asked"] += 1
    return next_question

# Function to save conversation history and generate a downloadable file
def save_conversation():
    conversation_text = "Conversation History:\n\n"
    for message in st.session_state.chat_session.history:
        role = "User" if message.role == "user" else "Assistant"
        conversation_text += f"{role}: {message.parts[0].text}\n\n"

    file_path = "conversation_history.txt"
    with open(file_path, "w") as file:
        file.write(conversation_text)
    return file_path

if selected == "SortifyAI":
    model = load_gemini_pro_model()

    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    # Initialize chat history if not already done
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.title("🤖 SortifyAI!! How can I help?")

    # Display only the sequential conversation (user prompt and assistant response)
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["text"])

    # Input field for user's message
    user_prompt = st.chat_input("Ask your query about Sorting Algorithms....")
    if user_prompt:
        # Append user's message to the chat history
        st.session_state.chat_history.append({"role": "user", "text": user_prompt})
        st.chat_message("user").markdown(user_prompt)

        # Check if the student is requesting to end the conversation
        if st.session_state.student_progress["answer_requested"] and user_prompt.lower() == "end":
            st.chat_message("assistant").markdown("Thanks for using SortifyAI! Have a great day ahead! 🌟")
            st.stop()

        # Check if the student has gained understanding
        elif check_understanding(user_prompt):
            conclusion = conclude_conversation()
            st.session_state.chat_history.append({"role": "assistant", "text": conclusion})
            st.chat_message("assistant").markdown(conclusion)

        else:
            # Generate the next step: either a hint or Socratic question
            if st.session_state.student_progress["confirmation_requested"] and user_prompt.lower() == "confirm":
                answer = generate_final_answer(user_prompt)
                st.session_state.chat_history.append({"role": "assistant", "text": answer})
                st.chat_message("assistant").markdown(answer)

                # Reset the progress counters after providing the final answer
                st.session_state.student_progress["questions_asked"] = 0
                st.session_state.student_progress["hints_given"] = 0
                st.session_state.student_progress["answer_requested"] = False
                st.session_state.student_progress["confirmation_requested"] = False

            else:
                # Generate the next probing question or hint
                next_step = handle_student_response(user_prompt)

                # Display the Socratic question or hint
                st.session_state.chat_history.append({"role": "assistant", "text": next_step})
                st.chat_message("assistant").markdown(next_step)

                # Increment hint count if the response is a hint
                if "hint" in next_step.lower():
                    st.session_state.student_progress["hints_given"] += 1

    # Show student progress
    st.sidebar.write(f"Questions Asked: {st.session_state.student_progress['questions_asked']}")
    st.sidebar.write(f"Hints Given: {st.session_state.student_progress['hints_given']}")

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
