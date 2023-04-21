import streamlit as st
from langchain import PromptTemplate
from langchain import OpenAI

template ="""
    Below is an query that may be poorly worded.
    Your goal is to:
    - Point out any errors or inappropriate usage of vocabulary or grammar in the input query.
    - Correct the spelling and grammar mistakes and convert the input text to a specified tone
    - Convert the input text to a specified writing style. Emoji is permitted.
    - Format the output text in appropriate format based on the style and tone.

    Below is the query, tone, and target writing style:
    - TONE: {tone}
    - STYLE: {style}
    - query: {query}

    - The good and bad aspects of the original input in terms of writing:
    - MODIFIED QUERY:
"""
prompt = PromptTemplate(input_variables=["tone", "style", "query"],template=template)


def load_LLM():
    llm=OpenAI(temperature=0.5)
    return llm

llm=load_LLM()

st.set_page_config(page_title="LinguaShine",page_icon=":robot:")
st.header("LinguaShine")

col1, col2 =st.columns(2)

with col1:
    st.markdown("LinguaShine is the ultimate tool for anyone looking to polish their English language skills. Whether you're a non-native speaker looking to improve your fluency or a native speaker looking to refine your grammar and vocabulary, LinguaShine has got you covered. With a range of fun and engaging exercises, quizzes, and lessons, LinguaShine makes it easy to hone your English language skills at your own pace. Whether you're preparing for an exam, a job interview, or just looking to boost your confidence when speaking English, LinguaShine is the perfect app for you. Try it out today and see the difference for yourself!")

with col2:
    st.image(image="DALL·E 2023-04-21 11.03.08.png")

st.markdown("## Enter Your Query ")
col1, col2 =st.columns(2)
with col1:
    option_tone = st.selectbox("Which tone would you like your query to have?",
        ("Formal","Informal"))
with col2:
    option_writing_style = st.selectbox("Which kind of writing style you want to choose?",
        ("Business style","Social media style","Email style","Poetic style"))
def get_text():
    input_text = st.text_area(label="",placeholder="Input your query here...",key="query_input")
    return input_text

query=get_text()
st.markdown("### Your Converted Query")

if query:
    prompt_with_query = prompt.format(tone=option_tone,style=option_writing_style,query=query)
    modified_query = llm(prompt_with_query)
    st.write(modified_query)