import streamlit as st
import openai
import json
import pandas as pd

user_api_key = st.sidebar.text_input("OpenAI API key", type="password")

openai.api_key = user_api_key

def translate_to_italian(text):
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a helpful translator."},
        {"role": "user", "content": f"Translate the following English text to Italian: {text}"}
      ]
    )
    return response['choices'][0]['message']['content']

# Collect interesting words and create a table
def collect_interesting_words(translation):
    words_data = []
    words = translation.split()
    for word in words:
        word_translation = translate_to_italian(word)
        example_sentence = translate_to_italian(f"Use the word '{word}' in a sentence.")
        words_data.append({'word': word, 'translation': word_translation, 'example': example_sentence})
    return pd.DataFrame(words_data)

# Web app
st.title('English-Italian Translator')
st.sidebar.markdown('### Enter your API key here')

# User input
user_input = st.text_area("Enter English text to translate:", "Your text here")

# Translate button
if st.button('Translate'):
    italian_translation = translate_to_italian(user_input)

    # Display translation
    st.markdown('**Italian Translation:**')
    st.write(italian_translation)

    # Collect interesting words
    words_df = collect_interesting_words(user_input)

    # Display words in a table
    st.markdown('**Interesting Words:**')
    st.table(words_df)

    # Download as CSV button
    csv_button = st.button('Download as CSV')
    if csv_button:
        st.download_button(
            label= "Download CSV",
            data= words_df.to_csv(index=False, encoding='utf-8'),
            file_name= "interesting_words.csv",
            key= "csv_download",
        )
