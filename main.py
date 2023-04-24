import configparser

import requests
import streamlit as st
from langchain import OpenAI
from langchain.callbacks import get_openai_callback

LANGUAGE_INSTRUCTIONS_DICT = {
    "Chinese": "- 请使用中文输出\n",
    "English": "- Please output English.\n"
}

STYLE_INSTRUCTIONS_DICT = {
    "小红书": "- Using many emojis, hashtags, and exaggerated language.\n",
    "豆瓣": "- Speaking poetically and affectedly, without expressing oneself directly.\n",
    "微博": "- Speaking in a sarcastic or ambiguous way, often with the intention of mocking or arguing.\n",
    "工作日报": "- Please modify the text to a style appropriate for a work report, it should be clear and professional and use a lot of jargons.\n",
    "Instagram": "- Please make the text suitable for an Instagram post, which may include emojis, hashtags, and short, catchy phrases.\n",
    "Email": "- Please make the text suitable for an email, which should be polite, professional, and well-organized. And use email format.\n",
    "Work Report": "- Please make the text suitable for a work progress report, which should be clear, concise, and informative.\n"
}


def get_user_ip():
    try:
        ip = requests.get("https://api64.ipify.org?format=json").json()['ip']
    except Exception as e:
        ip = "unknown"
    return ip

def get_text(user_inputs):
    # Read the whitelist from the config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    whitelist = set(config['whitelist']['ip_addresses'].split(', '))
    # Get the user's IP address
    user_ip = get_user_ip()

    if user_ip in whitelist:
        # If the user is in the whitelist, don't limit their inputs
        input_text = st.text_area(label="", placeholder="Input your text here...", key="text_input")

        # Add the input to the session_state if it doesn't already exist
        if "user_input_list" not in st.session_state:
            st.session_state.user_input_list = []

        # Append the input to the user_input_list
        if input_text:
            st.session_state.user_input_list.append(input_text)

    else:
        # If the user is not in the whitelist, limit their inputs to 10
        if user_ip not in user_inputs:
            user_inputs[user_ip] = 1
        else:
            user_inputs[user_ip] += 1

        if user_inputs[user_ip] <= 10:
            input_text = st.text_area(label="", placeholder="Input your text here...", key="text_input")

            # Add the input to the session_state if it doesn't already exist
            if "user_input_list" not in st.session_state:
                st.session_state.user_input_list = []

            # Append the input to the user_input_list
            if input_text:
                st.session_state.user_input_list.append(input_text)

        else:
            input_text = ""
            st.warning("You have exceeded the maximum number of inputs (10).")

    return input_text



def get_language_instructions(language):
    return LANGUAGE_INSTRUCTIONS_DICT.get(language, "")


def get_style_instructions(style):
    return STYLE_INSTRUCTIONS_DICT.get(style, "")


@st.cache_data()
def load_LLM():
    llm = OpenAI(temperature=0.5)
    return llm

def display_interface():
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("LinguaShine is the ultimate tool for anyone looking to polish their language. Try it out today and see the difference for yourself!")

        st.markdown("[Please Give Me a 🌟Star🌟 on Github](https://github.com/chenhuiyu/LinguaShine)")

    with col2:
        st.image(image="DALL·E 2023-04-21 11.03.08.png", width=250)

    st.markdown("## Enter Your Text")

    col1, col2 = st.columns(2)

    with col1:
        option_language = st.selectbox("Please select the language you want to input.", ("Chinese", "English"))

    with col2:
        if option_language == 'Chinese':
            option_writing_style = st.selectbox("请选择你需要生成的文本格式.", ("小红书", "豆瓣", "微博", "工作日报"))
        elif option_language == 'English':
            option_writing_style = st.selectbox("Please select the writing style you want to generate.", ("Instagram", "Email", "Work Report"))

    return option_language, option_writing_style


def handle_conversion(llm, input_text, language, style):
    # Create the PromptTemplate object with the input variables and the template
    template = """
    Below is the target output language and style:
    - Language: {language}
    - Style: {style}
    Below is a sentence or some keyword.
    - Text: {text}

    Your goal is to generate output in the corresponding language and style based on the input text:
    - Output Text:
    """

    # Combine the template, the input variables, and the instructions
    prompt_with_query = template.format(language=language, style=style, text=input_text)

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
    option_language, option_writing_style = display_interface()
    language = get_language_instructions(option_language)
    style = get_style_instructions(option_writing_style)

    input_text = get_text(user_inputs)

    llm = load_LLM()
    if input_text and st.button("Convert!"):
        handle_conversion(llm, input_text, language, style)

if __name__ == '__main__':
    if "user_inputs" not in st.session_state:
        st.session_state.user_inputs = {}
    main(st.session_state.user_inputs)
