import streamlit as st
import openai
import json
import pandas as pd

user_api_key = st.sidebar.text_input("OpenAI API key", type="password")

openai.api_key = user_api_key
prompt = "Translate the following English text to Italian:\n"

def translate_to_italian(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}, {"role": "user", "content": text}],
    )
    return response['choices'][0]['message']['content']

# Collect interesting words and create a table
def collect_interesting_words(translations):
    words_data = []
    for eng_text, ita_text in translations.items():
        # You may need to process eng_text and ita_text further based on your needs
        words_data.append({'word': eng_text, 'translation': ita_text, 'example': ''})
    return pd.DataFrame(words_data)

# Web app
st.title('Italian Translator and Word Collector')
st.sidebar.markdown('### English to Italian Translation')

# User input
user_input = st.text_area("Enter English text to translate:", "Your text here")

st.title('Italian translator')
st.markdown('Input the writing that you want to improve. \n\
            The AI will provide English translation for you.')

user_input = st.text_area("Enter some text to translate:", "Your text here")


# Translate button
if st.button('Translate'):
    # Add user input to conversation prompt
    prompt += f'User: {user_input}\n'

    # Perform translation
    italian_translation = translate_to_italian(prompt)

    # Display translation
    st.markdown('**Italian Translation:**')
    st.write(italian_translation)

    # Collect interesting words
    translations = json.loads(italian_translation)
    words_df = collect_interesting_words(translations)

    # Display words in a table
    st.markdown('**Interesting Words:**')
    st.table(words_df)

    # Download as CSV button
    csv_button = st.button('Download as CSV')
    if csv_button:
        st.download_button(
            label="Download CSV",
            data=words_df.to_csv(index=False, encoding='utf-8'),
            file_name="interesting_words.csv",
            key="csv_download",
        )
