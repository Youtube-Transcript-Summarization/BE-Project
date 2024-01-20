# from flask import Flask, request, jsonify
# from youtube_transcript_api import YouTubeTranscriptApi
# from transformers import pipeline
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:sonu@2002@localhost/db_name'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# class Summary(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     video_id = db.Column(db.String(50), nullable=False)
#     # transcript = db.Column(db.Text, nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     date_generated = db.Column(db.DateTime, default=datetime.utcnow)

#     def __repr__(self):
#         return f"Summary('{self.video_id}', '{self.transcript}', '{self.content}', '{self.date_generated}')"


# @app.route('/summary', methods=["GET"])
# def summary_api():
#     # GET /summary?url=https://www.youtube.com/watch?v=m-Feuh_zIfk&ab_channel=IncognitoCEO HTTP/1.1
#     # url = request.args.get('url', '')
#     # video_id = url.split('=')[1]
#     # print("video_id is :- ", video_id)
#     # summary = get_summary(get_transcript(video_id))
    
#     # return summary, 200

#     url = request.args.get('url', '')
#     video_id = url.split('=')[1]
#     transcript = get_transcript(video_id)
#     summary = get_summary(transcript)

#     # Save the video ID, transcript, and summary to the database
#     new_summary = Summary(video_id=video_id, transcript=transcript, content=summary)
#     db.session.add(new_summary)
#     db.session.commit()

#     return jsonify({'video_id': video_id, 'transcript': transcript, 'summary': summary}), 200

# def get_transcript(video_id):
#     transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
#     transcript = ' '.join([d['text'] for d in transcript_list])
#     print("transcript is :- ", transcript)
#     return transcript

# def get_summary(transcript):
#     summariser = pipeline('summarization')
#     summary = ''
#     for i in range(0, (len(transcript)//1000)+1):
#         summary_text = summariser(transcript[i*1000:(i+1)*1000])[0]['summary_text']
#         summary = summary + summary_text + ' '
#     print("summary is :- ", summary)
#     return summary
    

# if __name__ == '__main__':
#     app.run()


from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
import mysql.connector
from datetime import datetime
from waitress import serve

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
        SELECT summary FROM videos WHERE video_id = %s
    '''
    cursor.execute(query, (video_id,))
    existing_summary = cursor.fetchone()

    if existing_summary:
        # If the summary exists in the database, return it directly
        return existing_summary[0], 200
    else:
        # If the summary does not exist, fetch transcript and generate summary
        transcript = get_transcript(video_id)
        summary = get_summary(transcript)

        # Save the video ID and summary to the database
        query = '''
            INSERT INTO videos (video_id, summary)
            VALUES (%s, %s)
        '''
        cursor.execute(query, (video_id, summary))
        conn.commit()

        return summary,200

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

if __name__ == '__main__':
    # app.run(debug=True)
    serve(app, host='0.0.0.0', port=5000)

# Close the cursor and connection when the application is terminated
@app.teardown_appcontext
def close_connection(exception):
    cursor.close()
    conn.close()
