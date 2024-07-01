# from transformers import MarianMTModel, MarianTokenizer
# from langdetect import detect
# from gtts import gTTS
# from googletrans import Translator
    

# def translate_text_to_audio(summary, target_language, keywords):
#     translator = Translator()

#     # Detect the language of the summary
#     source_language = translator.detect(summary).lang

#     # Translate the summary to the target language
#     translated_summary = translator.translate(summary, src=source_language, dest=target_language).text
#     translated_keywords = translator.translate(keywords, src=source_language, dest=target_language).text
#     # Generate a unique file name based on timestamp
#     # timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#     # audio_file = "D:\\be-project\\frontend\\audio\\translated_summary_{target_language}.mp3"
#     audio_file = f"frontend\\audio\\translated_summary_{target_language}.mp3"

#     # Create a gTTS object for the translated summary
#     tts = gTTS(text=translated_summary, lang=target_language, slow=False)

#     # Save the audio file
#     tts.save(audio_file)

#     print(f"Translation to {target_language} successful. Audio saved to {audio_file}")

#     return [translated_summary, translated_keywords]

from transformers import MarianMTModel, MarianTokenizer
from langdetect import detect
from gtts import gTTS

def detect_language(text):
    try:
        # Detect the language of the text
        detected_lang = detect(text)
        return detected_lang

    except Exception as e:
        print(f"Language detection failed: {e}")
        return None



def translate_text_to_audio(input_text, target_lang, keywords):
    try:
        # Detect the language of the input text
        print("----======*****target_lang :-  ", target_lang)
        detected_lang = detect_language(input_text)

        if detected_lang and detected_lang != target_lang:
            print(f"Detected language ({detected_lang}) does not match the target language ({target_lang}). Translating...")

            # Translate text to the target language
            translated_text = translate_text(input_text, detected_lang, target_lang)
            translated_keywords = translate_text(keywords, detected_lang, target_lang)

            if translated_text:
                # Create a gTTS object for the translated text
                tts = gTTS(text=translated_text, lang=target_lang, slow=False)
                output_file = f"frontend\\audio\\translated_summary_{target_lang}.mp3"
                # Save the audio file
                tts.save(output_file)

                print(f"Translation to {target_lang} successful. Audio saved to {output_file}")

                return [translated_text, translated_keywords]
                
        else:
            print("Detected language matches the target language. Skipping translation.")

            # Create a gTTS object for the input text
            tts = gTTS(text=input_text, lang=target_lang, slow=False)

            output_file = f"frontend\\audio\\translated_summary_{target_lang}.mp3"
            # Save the audio file
            tts.save(output_file)

            print(f"Audio saved to {output_file}")

            return [input_text, keywords]
            
    except Exception as e:
        print(f"Translation failed: {e}")
        return None
    

def translate_text(input_text, source_lang, target_lang):
    try:
        model_name = f'Helsinki-NLP/opus-mt-{source_lang}-{target_lang}'
        model = MarianMTModel.from_pretrained(model_name)
        tokenizer = MarianTokenizer.from_pretrained(model_name)

        # Tokenize input text
        tokens = tokenizer(input_text, return_tensors="pt")

        # Translate tokens
        translated_tokens = model.generate(**tokens)

        # Decode translated tokens
        translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
        print("translated_text :- " , translated_text)
        return translated_text

    except Exception as e:
        print(e)
        return None