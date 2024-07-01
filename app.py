from flask import Flask, request, jsonify
import mysql.connector
from waitress import serve
import os
from utilities.summary import get_summary
from utilities.transcript import get_transcript
from utilities.keywords import get_keywords
from utilities.text_to_audio import translate_text_to_audio
from utilities.highlights import get_highlights

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
        video_id VARCHAR(255) PRIMARY KEY,
        summary LONGTEXT NOT NULL,
        keywords TEXT NOT NULL,
        date_created DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

summary = ""
keywords = ""

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

    highlights = get_highlights(url)
    if existing_summary:
        # If the summary exists in the database, return it directly
        summary = existing_summary[0]
        keywords = existing_summary[1]
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
        
    en = translate_text_to_audio(summary, "en", keywords)
    es = translate_text_to_audio(summary, "es", keywords)
    fr = translate_text_to_audio(summary, "fr", keywords)
    return jsonify({'summary': summary,"keywords": keywords,"en_keywords":en[1], "es_keywords":es[1], "fr_keywords":fr[1], "en_translate":en[0], "es_translate":es[0], "fr_translate":fr[0], "highlights_ts" : highlights}),200

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)

# Close the cursor and connection when the application is terminated
@app.teardown_appcontext
def close_connection(exception):
    cursor.close()
    conn.close()
