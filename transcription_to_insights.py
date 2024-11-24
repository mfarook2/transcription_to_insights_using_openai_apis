import streamlit as st
from openai import OpenAI
import os

# Sidebar options for LLM selection
llm_option = st.sidebar.selectbox(
    "LLM",
    options=["chatgpt-4o-latest", "gpt-4o-mini",  "gpt-4", "gpt-3.5-turbo"]
)

# Sidebar slider for temperature setting
temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0, 
    max_value=1.0,
    step=0.1,
    key="temperature",help="0.0 -> Factuail  1.0 -> Creative"
)

# Sidebar slider for max tokens setting
max_tokens= st.sidebar.slider(
    "Max Tokens",
    min_value=10, 
    max_value=1000,
    step=10,
    key="max_tokens"
)


# Sidebar multiselect for analysis options
options = st.sidebar.multiselect(
    "Content Analysis Options",
    ["Summary", "Key points", "Sentiment Analysis"],
    placeholder="Choose one or more options"
)

# Function to transcribe audio to text
def transcribe(audio_file):
    """
    Transcribes the provided audio file using OpenAI's Whisper model.
    Returns the transcription text.
    """
    #audio_file = open('/Users/mohammadfarook/Desktop/Personal/Projects/openai-speech-to-text/project-2/new-zealand-tourism.mp3', "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file, 
    response_format="text",
    language='en'
    )
    return (transcription)

# Function to process text through chat completion
def process_audio_and_generate_response(messages):
    """
    Generates a response using the OpenAI chat completion API.
    Uses the selected LLM, temperature, and max tokens to customize output.
    """
    response = client.chat.completions.create(
        model=llm_option,
        temperature=temperature,
        messages=messages,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content

# Initialize OpenAI client with API key
client = OpenAI(api_key=os.environ.get('OPEN_API_KEY'))

uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])
transcription=""
if uploaded_file is not None:

    tab1, tab2, tab3, tab4 = st.tabs(["📖 Transcript", "📃  Summary", "🔑 Key Points", "😂 Sentiment Analysis"])
    transcription = transcribe(uploaded_file)
    #st.text_area("Transcript", transcription)
    tab1.write(transcription)

    # Display results based on user's selected options
    for option in options:
        if (option == 'Summary'):
            # create a summary of the transcribed text
            messages = [
                {"role": "system", "content": "You are a helpful assitant"},
                {"role": "user", "content": f"Summarize the content labeled trnscription, and create logical paragraphs: {transcription}"}
            ]
            summary = process_audio_and_generate_response(messages)
            #st.text_area('Summary', summary)
            tab2.write(summary)

        if (option == 'Key points'):
            # create a summary of the transcribed text
            messages = [
                {"role": "system", "content": "You are a helpful assitant"},
                {"role": "user", "content": f"Create a bullet point list of key points: {transcription}"}
            ]
            key_points = process_audio_and_generate_response(messages)
            #st.text_area('Key points', key_points)
            tab3.write(key_points)

        if (option == 'Sentiment Analysis'):
            # create a summary of the transcribed text
            messages = [
                {"role": "system", "content": "You are a helpful assitant,"},
                {"role": "user", "content": f"Analyze and derive the common sentiments of this text: {transcription}"}
            ]
            sentiment_analysis = process_audio_and_generate_response(messages)
            #st.text_area('Sentiment Analysis', sentiment_analysis)
            tab4.write(sentiment_analysis)    
else:
    st.info("Please upload an audio file to start transcription.")
