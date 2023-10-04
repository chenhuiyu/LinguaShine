import configparser

import requests
import streamlit as st
from langchain import OpenAI
from langchain.callbacks import get_openai_callback
import os


LANGUAGE_INSTRUCTIONS_DICT = {
    # "Chinese": "- 请使用中文输出\n",
    "English": "- Please output English.\n",
}

# New: Dictionary for academic paper section prompts
PAPER_SECTION_PROMPTS = {
    "General": "Review for any grammatical or syntactical errors. Ensure the sentences in the paragraph flow logically. Replace any vague or ambiguous words with clearer terms. Avoid jargon unless it's standard in the field and necessary for understanding. Ensure variety in sentence structures. Break up long sentences if they are hard to understand. Ensure the tone is consistent and appropriate for an academic paper.",
    "Title": "Ensure the title captures the essence of the research succinctly.",
    "Abstract": "Ensure it provides a concise summary of the research.",
    "Introduction": "Establish context and background of the study.",
    "Methodology": "Streamline the methods description, ensuring clarity for replication.",
    "Results": "Emphasize significant findings using clear language.",
    "Discussion": "Interpret results and link them back to existing literature.",
    "Conclusion": "Summarize main research points.",
}


def get_user_ip():
    try:
        ip = requests.get("https://api64.ipify.org?format=json").json()["ip"]
    except Exception as e:
        ip = "unknown"
    return ip


def get_text(user_inputs):
    # Read the whitelist from the config file
    # config = configparser.ConfigParser()
    # config.read("config.ini")
    # whitelist = set(config["whitelist"]["ip_addresses"].split(", "))
    # Get the user's IP address
    # user_ip = get_user_ip()

    # if user_ip in whitelist:
    # If the user is in the whitelist, don't limit their inputs
    input_text = st.text_area(
        label="", placeholder="Input your text here...", key="text_input"
    )

    # Add the input to the session_state if it doesn't already exist
    if "user_input_list" not in st.session_state:
        st.session_state.user_input_list = []

    # Append the input to the user_input_list
    if input_text:
        st.session_state.user_input_list.append(input_text)

    # else:
    #     # If the user is not in the whitelist, limit their inputs to 10
    #     if user_ip not in user_inputs:
    #         user_inputs[user_ip] = 1
    #     else:
    #         user_inputs[user_ip] += 1

    #     if user_inputs[user_ip] <= 10:
    #         input_text = st.text_area(
    #             label="", placeholder="Input your text here...", key="text_input"
    #         )

    #         # Add the input to the session_state if it doesn't already exist
    #         if "user_input_list" not in st.session_state:
    #             st.session_state.user_input_list = []

    #         # Append the input to the user_input_list
    #         if input_text:
    #             st.session_state.user_input_list.append(input_text)

    #     else:
    #         input_text = ""
    #         st.warning("You have exceeded the maximum number of inputs (10).")

    return input_text


def get_language_instructions(language):
    return LANGUAGE_INSTRUCTIONS_DICT.get(language, "")


@st.cache_data()
def load_LLM():
    llm = OpenAI(
        # model_name="gpt-4",
        temperature=0.1,
        max_tokens=2048,
    )
    return llm


def display_interface():
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            "LinguaShine is the ultimate tool for anyone looking to polish their language. Try it out today and see the difference for yourself!"
        )

        st.markdown(
            "[Please Give Me a 🌟Star🌟 on Github](https://github.com/chenhuiyu/LinguaShine)"
        )

    with col2:
        st.image(image="DALL·E 2023-04-21 11.03.08.png", width=250)

    st.markdown("## Enter Your Text")

    col1, col2 = st.columns(2)

    with col1:
        option_language = st.selectbox(
            "Please select the language you want to input.", ("English", "English")
        )

    with col2:  # New column for selecting the section of the academic paper
        option_paper_section = st.selectbox(
            "Select the section of the academic paper you want to optimize.",
            list(PAPER_SECTION_PROMPTS.keys()),
        )

    return option_language, option_paper_section


def handle_conversion(llm, input_text, language, section):
    # Create the PromptTemplate object with the input variables and the template
    template = """**Task**:
You have been presented with a section from an English academic paper in the field of Civil Engineering. Your role is to refine this section, ensuring its clarity and accessibility without compromising its technical integrity. Afterward, detail the improvements you made and their significance.

**Objective**:
A well-optimized paper isn't just technically accurate; it's also accessible and easy to follow. Your refinements should make the content resonate more effectively with its primary audience—Civil Engineering professionals—while also being comprehensible to a wider academic readership.

**Areas of Focus**:
1. **Content Clarity**: 
   - **Issue**: A cluttered text often hides the main point, causing confusion.
   - **Optimize**: Distill the content to spotlight the primary idea. Excise any redundant or tangential sentences.
   - **Benefit**: Enhanced focus and reduced reader effort.

2. **Logical Flow**:
   - **Issue**: Disjointed sentences can disrupt the narrative flow.
   - **Optimize**: Sequence sentences for a coherent progression of ideas.
   - **Benefit**: A smoother reading experience.

3. **Word Choice**:
   - **Issue**: Ambiguous or complex words can alienate readers.
   - **Optimize**: Use clear and precise terminology. Retain field-specific jargon only when indispensable.
   - **Benefit**: Improved comprehension.

4. **Grammar & Syntax**:
   - **Issue**: Grammatical errors undermine credibility.
   - **Optimize**: Ensure linguistic correctness, from verb tenses to sentence structures.
   - **Benefit**: A polished and professional presentation.

5. **Sentence Structure**:
   - **Issue**: Overly lengthy or abrupt sentences can be off-putting.
   - **Optimize**: Aim for a mix of sentence lengths, prioritizing clarity.
   - **Benefit**: Enhanced readability.

6. **Tone & Formality**:
   - **Issue**: Inconsistent or casual tone can diminish the paper's gravitas.
   - **Optimize**: Maintain a consistent, scholarly tone. Steer clear of colloquial expressions.
   - **Benefit**: Ensures the work is taken seriously.

**Presented Section**:
- {section}

---
**Input Text**: Here's a section from a Civil Engineering academic paper:
- {text}
---

**Expected Output**:
Your submission should comprise two segments: the refined text and a specific analysis of your refinements.
- Refined Text:(In English)
- Analysis:(In Chinese)

"""

    # Combine the template, the input variables, and the instructions
    prompt_with_query = template.format(
        language=language, section=PAPER_SECTION_PROMPTS[section], text=input_text
    )
    # prompt_with_query += PAPER_SECTION_PROMPTS[section]

    # Display the modified query
    if input_text:
        with get_openai_callback() as cb:
            output = llm(prompt_with_query)
            st.markdown("### Your Converted Text")
            st.success(output)
            st.write(cb)


def main(user_inputs):
    st.set_page_config(page_title="LinguaShine", page_icon=":robot:")
    st.header("LinguaShine")
    (
        option_language,
        option_paper_section,
    ) = display_interface()  # Updated function return
    language = get_language_instructions(option_language)

    input_text = get_text(user_inputs)

    llm = load_LLM()
    # st.button("Convert!")
    if input_text and st.button("Convert!"):
        handle_conversion(llm, input_text, language, option_paper_section)


if __name__ == "__main__":
    if "user_inputs" not in st.session_state:
        st.session_state.user_inputs = {}
    main(st.session_state.user_inputs)
