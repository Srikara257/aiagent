from langchain.chat_models import init_chat_model
import streamlit as st
import json
GROQ_API_KEY="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"

def llm_call(prompt):
    print("in llm.py")
    model = init_chat_model("llama3-8b-8192", model_provider="groq", groq_api_key=GROQ_API_KEY)
    

    response = model.invoke(prompt)
    return response.content if response else ""

def find_class(query):
    prompt=f""" you are an expert at classifying the concept given. You have been asked to classify the following query: {query} as direct_explanation, process, concept
    use the following suggestion to classify the query given

    direct_explanation: if the query is  relates to small concept or a definition(explain about the concept of inheritance in oops as inheritance is a small concpet of oops, explain about photosynthesis as photosynthesis is a small concept)
    process: if the query is a process or a step by step guide like (explain about analog image to digital image conversion, explain about photosynthesis here photosynthesis is a process)
    concept: if the query is a concept or a theory like (explain about oops concepts, explain about laws of physics )

    return only the class name nothing else only one word should be in resposne
    expected output : any one class from direct_explanation, process, concept
    """
    response = llm_call(prompt)
    return response



def plan_creater_llm(query,query_class):
    print("Query:",query)

    



    if(query_class=="process"):
        prompt=f"""
    You are an expert at creating a plan to learn a concept given. You have been asked to create a plan of phases to acheive the process: 
    
    PROCESS = {query}
    
    Generate only key points of the concept, no explaination of the key points will be generated 
        Do not generate any extra words even like ```python and ```
        
        expected output :
        json list of phases of the process
    """
        

    if(query_class=="concept"):
        prompt=f"""
    You are an expert at dividing the concept given into different subtopics. You have been asked to create a list of subtopics(which will be helpful in understaing the concept) involved in concept given 
     
      CONCEPT = {query}
    
    Generate only key points of the concept, no explaination of the key points will be generated 
        Do not generate any extra words even like ```python and ```
        
        expected output :
        json list of top 10 keypoints of the concept
    """
    response = llm_call(prompt)
    print(response)
    converted_list = []
    try:
        converted_list = json.loads(response)

        print(converted_list) 

    except:
        print("Error in converting response to json")
    return converted_list



def plan_executer_llm(query,query_class="direct_explanation",plan=None):
    breif_prompt=f"""Explain the following query briefly and provide real-world applications where it is commonly used. Make sure the explanation is concise yet informative. Also, give examples of how it is applied in real-world scenarios.

    Query: {query}

"""
    breif_explanation = llm_call(breif_prompt)
    if not plan or query_class=="direct_explanation":
        depth_prompt=f"""Please provide a comprehensive and in-depth explanation of the following query. Break down the core concepts, underlying principles, and any relevant contextual information. Explore multiple perspectives, discuss theoretical foundations, and include practical examples or analogies where appropriate. Your response should offer deep insights and thorough analysis that help the reader fully understand the topic.
        Also, give examples of how it is applied 
        explain where it is used in real world scenarios
        Query:{query}
         """

    else:
        depth_prompt=f"""You are an expert at explaining the concept given. You have been asked to explain the concept given in detail using the plan given below. 
        
        Also, give examples of how it is applied 
        explain where it is used in real world scenarios
        Query: {query}
        
        Plan: {plan}
        
        Generate only key points of the concept, no explaination of the key points will be generated 
        Do not generate any extra words even like ```python and ```
        
        expected output :
        below mention things must be in the response for every keypoint in the plan
        detailed explanation of the concept
        Explaination of all the keypoints in the plan is must and should be in order
        Explaination of all the keypoints in the plan is must and should be in order
        Also, give examples of how it is applied 
        explain where it is used in real world scenarios
        """
    breif_explanation = llm_call(breif_prompt)
    detailed_explanation = llm_call(depth_prompt)
    return breif_explanation,detailed_explanation

    
def exam_generator(explainations):
    prompt = f"""
    Based only on the following learning material, generate exactly 20 multiple-choice questions (MCQs).
    
    Learning Material:
    Breif Explanation: {explainations[0]}
    Detailed Explanation: {explainations[1]}
    
    Return a JSON array where each element is an object with:
    - "question" (string)
    - "options" (list of 4 strings: A, B, C, D)
    - "correct_answer" (one of "A", "B", "C", "D").
    
    Example format:
    [
        {{"question": "What is OOP?", "options": ["A. Object-Oriented Programming", "B. Only One Program", "C. Other Operating Process", "D. None"],
        "correct_answer": "A"}}
    ]
    
    Return **only** the JSON array, with no extra text.
    Return **only** the JSON array, with no extra text.
    dont give any extra information in the response like : Here are the 20 multiple-choice questions (MCQs) based on the provided learning material:
    """

    response = llm_call(prompt)
    print(response)
    
    try:
        questions = json.loads(response)  # Parse JSON response
        if isinstance(questions, list):
            return questions
        else:
            print("Error: Response is not a list.")
            return []
    except json.JSONDecodeError:
        print("Error: Response could not be parsed as JSON.")
        return []
    
import json

# Define the string values
def create_json_file(explainations):
    data = {
    "breif_explaination": "Hello, this is string A",
    "detail explaination": "And this is string B"
    }
# Write to a JSON file
    with open("output.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

    print("JSON file created successfully!")




# def evaluate_answers(questions):
#     score = 0
#     score_st = 0
#     total_questions = len(questions)
#     weak_areas = []
#     weak_areas_st = []

#     for q in questions:
#         print("\n" + q["question"])
#         st.write("\n" + q["question"])
#         for option in q["options"]:
#             print(option)
#             st.write(option)

#         user_answer = input("Enter your answer (A/B/C/D): ").strip().upper()
#         user_answer_st = st.text_input("Enter your answer (A/B/C/D): ").strip().upper()

#         if user_answer == q["correct_answer"]:
#             score += 1
#         else:
#             weak_areas.append(q["question"])  # Store questions where the user got it wrong
#         if user_answer_st == q["correct_answer"]:
#             score_st += 1
#         else:
#             weak_areas_st.append(q["question"])

    # print(f"\nYour Score: {score}/{total_questions}")
    # st.write(f"\nYour Score: {score_st}/{total_questions}")

    # weak_areas_summary = " ".join(weak_areas_st[:3])  # Limit to top 3 weak topics
    # return score, weak_areas_summary 
    

    
def evaluate_answers(quiz_data):
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


    



# import requests

# TAVILY_API_KEY = "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"  # Replace with your key

# def search_tavily(query):
#     url = "https://api.tavily.com/search"
#     headers = {
#         "Authorization": f"Bearer {TAVILY_API_KEY}",
#         "Content-Type": "application/json"
#     }
#     data = {
#         "query": query,
#         "search_depth": "advanced",  # "basic" or "advanced"
#         "max_results": 5  # How many links/snippets you want
#     }

#     response = requests.post(url, headers=headers, json=data)
#     results = response.json()
#     return results["results"]  # List of results with title, snippet, url

# for res in search_tavily("Python OOP concepts"):
#     title = res.get("title", "No Title")
#     url = res.get("url", "No URL")
#     snippet = res.get("snippet", "No Snippet Available")
    
#     print(f"{title} - {url}\n{snippet}\n")

# search_tavily("Python OOP concepts")