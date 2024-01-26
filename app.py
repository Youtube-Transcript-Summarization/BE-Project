
from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
import mysql.connector
from datetime import datetime
from waitress import serve
import nltk
from nltk.corpus import stopwords
import spacy
from spacy.lang.en import English
from langdetect import detect
from gtts import gTTS
from googletrans import Translator
# import langdetect
from langdetect import detect
# from gtts import gTTS
import os

from transformers import MarianMTModel, MarianTokenizer
import sentencepiece

app = Flask(__name__)

# Configure your MySQL database connection details
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'sneha',
    'database': 'be-project'
}

# Establish a connection to the MySQL server
conn = mysql.connector.connect(**db_config)

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create a 'videos' table if it does not exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS videos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        video_id VARCHAR(50) NOT NULL,
        summary TEXT NOT NULL,
        keywords TEXT NOT NULL,
        date_created DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

@app.route('/summary', methods=["GET"])
def summary_api():
    url = request.args.get('url', '')
    video_id = url.split('=')[1]
    
    # Check if the video ID is already present in the database
    query = '''
        SELECT summary, keywords FROM videos WHERE video_id = %s
    '''
    cursor.execute(query, (video_id,))
    existing_summary = cursor.fetchone()


    summary = ""
    # keywords = []
    if existing_summary:
        # If the summary exists in the database, return it directly
        summary = existing_summary[0]
        keywords = existing_summary[1]
        # translate_and_save_audio(summary, "en")
        # translate_and_save_audio(summary, "es")
        # translate_and_save_audio(summary, "fr")
        
    else:
        # If the summary does not exist, fetch transcript and generate summary
        transcript = get_transcript(video_id)
        summary = get_summary(transcript)
        kw = list(get_keywords(summary))
        keywords = ""
        for words in kw:
            keywords =keywords +  words + ', '
        # Save the video ID and summary to the database
        query = '''
            INSERT INTO videos (video_id, summary, keywords)
            VALUES (%s, %s, %s)
        '''
        cursor.execute(query, (video_id, summary, keywords))
        conn.commit()
        
        # return summary,200
        # translate_and_save_audio(summary, "en")
        # translate_and_save_audio(summary, "es")
        # translate_and_save_audio(summary, "fr")
    en_translate = translate_and_save_audio(summary, "en")
    es_translate = translate_and_save_audio(summary, "es")
    fr_translate = translate_and_save_audio(summary, "fr")
    return jsonify({'summary': summary, "keywords": keywords, "en_translate":en_translate, "es_translate":es_translate, "fr_translate":fr_translate}), 200


def get_transcript(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    transcript = ' '.join([d['text'] for d in transcript_list])
    return transcript

def get_summary(transcript):
    summariser = pipeline('summarization')
    summary = ''
    for i in range(0, (len(transcript)//1000)+1):
        summary_text = summariser(transcript[i*1000:(i+1)*1000])[0]['summary_text']
        summary = summary + summary_text + ' '
    return summary


# Download NLTK resources
nltk.download('stopwords')

# Load spaCy models
nlp_en = spacy.load('en_core_web_sm')
nlp_fr = spacy.load('fr_core_news_sm')
nlp_es = spacy.load('es_core_news_sm')


def preprocess_text(text, lang):
    # Tokenize the text using spaCy based on language
    if lang == 'en':
        doc = nlp_en(text)
    elif lang == 'fr':
        doc = nlp_fr(text)
    elif lang == 'es':
        doc = nlp_es(text)
    else:
        raise ValueError(f"Unsupported language: {lang}")

    # Lemmatize the tokens while ignoring punctuation
    lemmatized_tokens = {token.lemma_ for token in doc if not token.is_punct}

    return lemmatized_tokens

def get_keywords(text):
    # Detect language
    lang = detect(text)

    # Preprocess text
    tokens = preprocess_text(text, lang)

    # Filter tokens to include only nouns and adjectives
    pos_tags_to_include = {"NOUN", "PROPN", "ADJ"}
    keywords = {word for word in tokens if nlp_en(word)[0].pos_ in pos_tags_to_include}

    return keywords

def detect_language(text):
    try:
        # Detect the language of the text
        detected_lang = detect(text)
        return detected_lang

    except Exception as e:
        print(f"Language detection failed: {e}")
        return None



# def translate_text_to_audio(input_text, target_lang, output_file):
#     try:
#         # Detect the language of the input text
#         detected_lang = detect_language(input_text)

#         if detected_lang and detected_lang != target_lang:
#             print(f"Detected language ({detected_lang}) does not match the target language ({target_lang}). Translating...")

#             # Translate text to the target language
#             translated_text = translate_text(input_text, detected_lang, target_lang)

#             if translated_text:
#                 # Create a gTTS object for the translated text
#                 tts = gTTS(text=translated_text, lang=target_lang, slow=False)

#                 # Save the audio file
#                 tts.save(output_file)

#                 print(f"Translation to {target_lang} successful. Audio saved to {output_file}")

#                 return translated_text
#         else:
#             print("Detected language matches the target language. Skipping translation.")

#             # Create a gTTS object for the input text
#             tts = gTTS(text=input_text, lang=target_lang, slow=False)

#             # Save the audio file
#             tts.save(output_file)

#             print(f"Audio saved to {output_file}")

#             return input_text

#     except Exception as e:
#         print(f"Translation failed: {e}")
#         return None
# def translate_text(input_text, source_lang, target_lang):
#     try:
#         model_name = f'Helsinki-NLP/opus-mt-{source_lang}-{target_lang}'
#         model = MarianMTModel.from_pretrained(model_name)
#         tokenizer = MarianTokenizer.from_pretrained(model_name)

#         # Tokenize input text
#         tokens = tokenizer(input_text, return_tensors="pt")

#         # Translate tokens
#         translated_tokens = model.generate(**tokens)

#         # Decode translated tokens
#         translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
#         print("translated_text :- " , translated_text)
#         return translated_text

#     except Exception as e:
#         print(e)
#         return None
def translate_and_save_audio(summary, target_language='en'):
    translator = Translator()

    # Detect the language of the summary
    source_language = translator.detect(summary).lang

    # Translate the summary to the target language
    translated_summary = translator.translate(summary, src=source_language, dest=target_language).text

    # Generate a unique file name based on timestamp
    # timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    # audio_file = "D:\\be-project\\frontend\\audio\\translated_summary_{target_language}.mp3"
    audio_file = f"frontend\\audio\\translated_summary_{target_language}.mp3"

    # Create a gTTS object for the translated summary
    tts = gTTS(text=translated_summary, lang=target_language, slow=False)

    # Save the audio file
    tts.save(audio_file)

    print(f"Translation to {target_language} successful. Audio saved to {audio_file}")

    return translated_summary

if __name__ == '__main__':
    # app.run(debug=True)
    serve(app, host='0.0.0.0', port=5000)

# Close the cursor and connection when the application is terminated
@app.teardown_appcontext
def close_connection(exception):
    cursor.close()
    conn.close()
