
import streamlit as st
import functions as fn

if "show_questions" not in st.session_state:
    st.session_state.show_questions = False

st.sidebar.title("Navigation")



if st.session_state.show_questions:
    page = st.sidebar.radio("Go to", ["Home", "Questions"])
else:
    page = "Home"

# Text input field
if page == "Home":
    user_input = st.text_input("Enter the concept to learn:")

    if st.button("Submit"):
        if user_input:
            st.success(f"You entered: {user_input}")
            st.session_state.query = user_input
            print("Query:", st.session_state.get('query'))
        else:
            st.warning("Please enter something before submitting.")


    uploaded_file3 = st.file_uploader("Upload files", type=["png", "jpg"], accept_multiple_files=True) 
    # if we remove accept_multiple_files=True parm we can select only one file
    # Supports: ["csv", "pdf", "png", "jpg", "txt", "docx", "zip", ...]

    if uploaded_file3:
        if st.button("submit images"):
            for file in uploaded_file3: 
                st.image(file)


    if st.button("Generate Plan"):
        
        query_class=fn.find_class(st.session_state.query)
        st.session_state.query_class=query_class
        if query_class!="direct_explanation": 
            
            response=fn.plan_creater_llm(st.session_state.query,query_class)
            st.session_state.plan=response
            st.write(response)
    if st.button("Generate Explanation"): 
        breif_explanation,detailed_explanation= fn.plan_executer_llm(st.session_state.query,st.session_state.query_class,st.session_state.plan)

        st.header("Breif Explanation")
        st.write(breif_explanation) 
        st.header("Detailed Explanation")
        st.write(detailed_explanation)
        st.session_state.explainations=[breif_explanation,detailed_explanation]

    if st.button("Exam"):
        if 'questions' not in st.session_state:
            Questions = fn.exam_generator(st.session_state.explainations)
            st.session_state.questions=Questions
        else :
            Questions=st.session_state.get('questions')
        # print(Questions)

        score, weak_areas_summary = fn.evaluate_answers(Questions)
    if st.button("START EXAM"):
        st.session_state.show_questions = True
        if 'questions' not in st.session_state:
            Questions = fn.exam_generator(st.session_state.explainations)
            st.session_state.questions=Questions
        else :
            Questions=st.session_state.get('questions')
    if st.button("Reset Session State"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]

    st.write("Click 'Reset Session State' to clear all session data.")

elif page == "Questions":
    st.title("Questions Page")
    


    
    quiz_data=st.session_state.get('questions')
    st.header("Quiz Application")

# Loop through questions
    for index, item in enumerate(quiz_data):
        st.subheader(f"Question {index + 1}: {item['question']}")
        
        # Get user's answer
        selected_option = st.radio(f"Select an option:", item["options"], key=f"q{index}")
        
        # Check answer
        if st.button(f"Check Answer {index + 1}"):
            if selected_option == item["correct_answer"]:
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Incorrect! The correct answer is: {item['correct_answer']}")
    # print(Questions)

    
