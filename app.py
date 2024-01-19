from flask import Flask, request
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

app = Flask(__name__)

@app.route('/summary', methods=["GET"])
def summary_api():
    # GET /summary?url=https://www.youtube.com/watch?v=m-Feuh_zIfk&ab_channel=IncognitoCEO HTTP/1.1
    url = request.args.get('url', '')
    video_id = url.split('=')[1]
    print("video_id is :- ", video_id)
    summary = get_summary(get_transcript(video_id))
    
    return summary, 200

def get_transcript(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    transcript = ' '.join([d['text'] for d in transcript_list])
    print("transcript is :- ", transcript)
    return transcript

def get_summary(transcript):
    summariser = pipeline('summarization')
    summary = ''
    for i in range(0, (len(transcript)//1000)+1):
        summary_text = summariser(transcript[i*1000:(i+1)*1000])[0]['summary_text']
        summary = summary + summary_text + ' '
    print("summary is :- ", summary)
    return summary
    

if __name__ == '__main__':
    app.run()