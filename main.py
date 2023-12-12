import streamlit as st
import pandas as pd
import openai
import os
import random

# Set up the OpenAI API key
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Function to generate lyrics
def generate_lyrics(artist_name, genre, subject=None, rhyme=None, temperature=0.7, use_slang=False, include_non_lexical=False, specific_non_lexical=None):
    prompt = f"Imagine you are a songwriter. Write the lyrics to a song based on this {genre} that the author wants: {subject}, in similarity to this artist: {artist_name}, and if available create rhymes with this phrase {rhyme}. Try your best to match the style of the artist. Unless specified, do not use slang or casual language in the lyrics generated."

    # Modify the prompt based on the use_slang parameter
    if use_slang:
        prompt += " You are allowed to use slang and casual language in the lyrics in this case."

    # Include non-lexical vocals in the prompt if the toggle button is enabled
    if include_non_lexical:
        prompt += " Include some non-lexical vocals (e.g., lalalaaa) in the lyrics."

        # Include a specific non-lexical vocal if provided
        if specific_non_lexical:
            prompt += f" Use '{specific_non_lexical}' as a non-lexical vocal."

    # Generate lyrics using OpenAI GPT-3
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        temperature=temperature,
    )

    generated_lyric = response['choices'][0]['text']

    return generated_lyric

# Streamlit app
st.title("Lyric Generator Chatbot")

# Get user inputs
artist_name = st.text_input("Enter the artist's name:")
genre = st.text_input("Enter the genre:")
subject = st.text_input("Subject (Optional):", "Enter the subject for this particular song")
rhyme = st.text_input("Rhyme (Optional):", "Enter a particular word or phrase that you would like used")
temperature = st.slider("Select temperature", 0.1, 1.0, 0.7, 0.1)
use_slang = st.checkbox("Allow Slang in Lyrics", value=False, key='slang_checkbox', help='Use slang and casual language in the lyrics.')
include_non_lexical = st.checkbox("Include Non-Lexical Vocals", value=False, key='non_lexical_checkbox', help='Include some non-lexical vocals in the lyrics.')
specific_non_lexical = st.text_input("Specific Non-Lexical Vocal (Optional):", "Enter a specific non-lexical vocal")

# Generate lyrics when the user clicks the button
if st.button("Generate Lyrics"):
    if artist_name and genre:
        # Call the generate_lyrics function
        generated_lyric = generate_lyrics(artist_name, genre, subject, rhyme, temperature, use_slang, include_non_lexical, specific_non_lexical)

        # Display the generated lyric
        st.success(f"Generated Lyric:\n{generated_lyric}")

        # Ask for user feedback
        user_feedback = st.selectbox("How satisfied are you with the generated lyric?", ["Satisfied", "Neutral", "Dissatisfied"])

        # Use user feedback to refine the model if dissatisfied
        if user_feedback == "Dissatisfied":
            st.info("Thank you for your feedback! We will use this to improve our lyric generation.")
            # You can include logic here
