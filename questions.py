
import streamlit as st
import json

# Sample quiz data
quiz_data = [
    {
        "question": "What is OOP?",
        "options": ["A. Object-Oriented Programming", "B. Only One Program", "C. Other Operating Process", "D. None"],
        "correct_answer": "A. Object-Oriented Programming"
    },
    {
        "question": "Which keyword is used to define a function in Python?",
        "options": ["A. func", "B. def", "C. function", "D. define"],
        "correct_answer": "B. def"
    }
]

# Streamlit app
st.header("Quiz Application")
st.session_state.questions = quiz_data
if 'questions' not in st.session_state:
    st.write("false")
if st.button("strart"):
    questions=st.session_state.get('questions')
    if questions:
        st.write("got questions")
    else:
        st.write("no questions")
    
# Loop through questions
for index, item in enumerate(quiz_data):
    st.subheader(f"Question {index + 1}: {item['question']}")
    
    # Get user's answer
    selected_option = st.radio(f"Select an option:", item["options"], key=f"q{index}")
    
    # Check answer
    if st.button(f"Check Answer {index + 1}"):
        if selected_option == item["correct_answer"]:
            st.text("✅ Correct!")
            
            
        else:
            st.text(f"❌ Incorrect! The correct answer is: {item['correct_answer']}")
