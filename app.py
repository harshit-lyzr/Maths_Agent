import streamlit as st
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent,Task
from lyzr_automata.pipelines.linear_sync_pipeline import LinearSyncPipeline
from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()
api = os.getenv("OPENAI_API_KEY")

st.set_page_config(
    page_title="Lyzr Maths Application",
    layout="centered",  # or "wide"
    initial_sidebar_state="auto",
    page_icon="lyzr-logo-cut.png",
)

st.markdown(
    """
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# image = Image.open("lyzr-logo.png")
# st.image(image, width=150)

# App title and introduction
st.title("Lyzr Maths Application")
st.markdown("### Welcome to the Lyzr Maths Application!")

query=st.text_input("Enter your Maths Problem: ")

open_ai_text_completion_model = OpenAIModel(
    api_key=api,
    parameters={
        "model": "gpt-4-turbo-preview",
        "temperature": 0.2,
        "max_tokens": 1500,
    },
)

def math_problem_solver(query):

    math_agent = Agent(
            role="maths expert",
            prompt_persona="You are an Expert MATHEMATICIAN. Your task is to ASSIST in solving complex mathematical problems and to PROVIDE detailed explanations for mathematical concepts."
        )

    prompt=f"""You are a reasoning agent tasked with solving 
    the user's logic-based questions. Logically arrive at the solution, and be 
    factual. In your answers, clearly detail the steps involved and give the 
    final answer. Provide the response in bullet points. 
    Question  {query} Answer"""

    math_task  =  Task(
        name="Maths Problem Solver",
        model=open_ai_text_completion_model,
        agent=math_agent,
        instructions=prompt,
    )

    output = LinearSyncPipeline(
        name="Maths Pipline",
        completion_message="pipeline completed",
        tasks=[
              math_task
        ],
    ).run()

    answer = output[0]['task_output']

    return answer

if st.button("Solve"):
    solution = math_problem_solver(query)
    st.markdown(solution)

