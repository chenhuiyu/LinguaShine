import streamlit as st
from langchain import PromptTemplate
from langchain import OpenAI

template = """
    Below is a sentence or some keyword. Your goal is to generate text in the corresponding language and style based on the input text.
    Below is the target writing language and style, and input text:
    - Language: {language}
    - Style: {style}
    - Text: {text}

    - Output Text:
"""

language_instructions_dict = {
    "Chinese": "- 请使用中文输出\n",
    "English": "- Please output English.\n"
}

style_instructions_dict = {
    "小红书": "- 请将文本修改为适合小红书的风格，使用很多emoji、话题标签和简短、吸引人的短语。\n",
    "豆瓣": "- 请将文本修改为适合豆瓣的风格，说话富有诗意、矫揉造作，不直抒胸臆。\n",
    "微博": "- 请将文本修改为适合微博的风格，说话阴阳怪气，讽刺或者抬杠。\n",
    "工作日报": "- 请将文本修改为适合工作报告的风格，应清晰、简洁、专业。\n",
    "Instagram": "- Please make the text suitable for an Instagram post, which may include emojis, hashtags, and short, catchy phrases.\n",
    "Email": "- Please make the text suitable for an email, which should be polite, professional, and well-organized.\n",
    "Work Report": "- Please make the text suitable for a work progress report, which should be clear, concise, and informative.\n"
}

def get_language_instructions(language):
    if language in language_instructions_dict:
        return f"{language_instructions_dict[language]}"
    else:
        return ""

def get_style_instructions(style):
    if style in style_instructions_dict:
        return f"{style_instructions_dict[style]}"
    else:
        return ""

def load_LLM():
    llm = OpenAI(temperature=0.5)
    return llm

st.set_page_config(page_title="LinguaShine", page_icon=":robot:")
st.header("LinguaShine")

col1, col2 = st.columns(2)

with col1:
    st.markdown("LinguaShine is the ultimate tool for anyone looking to polish their language. Try it out today and see the difference for yourself!")

with col2:
    st.image(image="DALL·E 2023-04-21 11.03.08.png")

st.markdown("## Enter Your Text")

col1, col2 = st.columns(2)


with col1:
    option_language = st.selectbox("Please select the language you want to input.", ("Chinese", "English"))

with col2:
    if option_language == 'Chinese':
        option_writing_style = st.selectbox("请选择你需要生成的文本格式.",
                                           ("小红书", "豆瓣", "微博", "工作日报"))
    elif option_language == 'English':
        option_writing_style = st.selectbox("Please select the writing style you want to generate.",
                                           ("Instagram", "Email", "Work Report"))
# Get the language-specific instructions and the style-specific instructions
language = get_language_instructions(option_language)
style = get_style_instructions(option_writing_style)
def get_text():
    input_text = st.text_area(label="", placeholder="Input your text here...", key="text_input")
    return input_text

input_text = get_text()
# Define the input variables for the PromptTemplate
input_variables = ["language", "style", "text"]

# Create the PromptTemplate object with the input variables and the template
prompt = PromptTemplate(input_variables=input_variables, template=template)
llm = load_LLM()
# Combine the template, the input variables, and the instructions
prompt_with_query = template.format(language=language, style=style, text=input_text)
modified_query = llm(prompt_with_query)

# Display the modified query
if input_text:
    st.markdown("### Your Converted Text")
    st.write(modified_query)
