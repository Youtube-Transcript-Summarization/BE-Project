from langdetect import detect
import nltk
from nltk.corpus import stopwords
import spacy


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