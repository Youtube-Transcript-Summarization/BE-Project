# Import required libraries
from yt_dlp import YoutubeDL
import os
os.environ["PAFY_BACKEND"] = "internal"
import cv2
import pytesseract
from pytube import YouTube
import pafy
# from google.colab.patches import cv2_imshow

def get_highlights(url):

    text_data = []
    timestamps = []

    i = 0
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


     # Use yt-dlp to get a direct video URL
    ydl_opts = {
        'format': 'best',
        'quiet': True
    }

    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_url = info_dict.get('url')

    # Open the video stream from the URL
    cap = cv2.VideoCapture(video_url)

    # Read video frames and perform OCR
    while i < 21:
        frame = cap.read()[1]
        if frame is None:
            # print("Breaking...")
            break

        # Perform OCR on the frame
        text = pytesseract.image_to_string(frame)
        timestamp_ms = cap.get(cv2.CAP_PROP_POS_MSEC)

        # Display the text
        if len(text) > 3:
            text_data.append(text)
            timestamps.append(timestamp_ms)
            i+=1

    cap.release()


    for text, timestamp in zip(text_data, timestamps):
        print(f"Timestamp: {timestamp} ms, Text: {text}")

    import re
    new_text_data = []

    for text in text_data:
        formatted_text = text.strip().replace('\n', ' ').replace('\x0c', '')
        formatted_text = re.sub(r'[^a-zA-Z0-9\s]', '', formatted_text)
        new_text_data.append(formatted_text.lower())

    new_text_data = list(filter(lambda x: x.strip(), new_text_data))
    print(new_text_data)

    def levenshtein_distance(s1, s2):
        """Calculate the Levenshtein distance between two strings."""
        s1 = s1.lower()
        s2 = s2.lower()
        if len(s1) < len(s2):
            return levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def similarity_percentage(s1, s2):
        """Calculate the percentage similarity between two strings."""
        distance = levenshtein_distance(s1, s2)
        max_length = max(len(s1), len(s2))
        return 100 * (1 - distance / max_length)

    # Example usage:

    sim_percentages = []
    for i in range(0,len(new_text_data) - 1):
        percentage_similarity = similarity_percentage(new_text_data[i], new_text_data[i + 1])
        sim_percentages.append(percentage_similarity)

    print(sim_percentages)

    important_frames_text = []
    important_frames_ts = []

    for i in range(1,len(sim_percentages)):
        if sim_percentages[i] < sim_percentages[i - 1]:
            if sim_percentages[i + 1] > sim_percentages[i]:
            # Capture that frame as important
                important_frames_text.append(new_text_data[i-1])
                important_frames_ts.append(timestamps[i-1])

    print(important_frames_text)
    print(important_frames_ts)
    return  important_frames_ts