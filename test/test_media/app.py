# Step 1: Install Gradio
# Run this command in your terminal if you haven't installed Gradio yet
# pip install gradio
# Step 2: Import Gradio
import gradio as gr
from googleapiclient.discovery import build
from pytube import YouTube
from pytubefix import YouTube
from pytubefix.cli import on_progress
import os
import shutil
import random
import string
import sys

sys.path.append('/Users/vladc/Desktop/solo/face2face')
from face2face import Face2Face
import cv2
from media_toolkit import VideoFile

f2f = Face2Face(device_id=0)


def test_single_face_swap():
    source_img = "test_face_1.jpg"
    target_img = "test_face_2.jpg"
    swapped = f2f.swap_img_to_img(source_img, target_img, enhance_face_model=None)
    cv2.imwrite("test_swap.jpg", swapped)


def generate_random_word(length=5):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def download_youtube_videov1(url, output_path='.'):
    try:
        yt = YouTube(url)
        # Get the highest resolution stream available

        # Download the video
        yt.streams.download(output_path)
        print(f"Downloaded: {yt.title}")
    except Exception as e:
        print(f"An error occurred: {e}")


def download_youtube_video(url, output_path='.'):
    try:
        yt = YouTube(url, on_progress_callback=on_progress, use_po_token=True)
        # Get the highest resolution stream available
        yt = yt.streams.get_highest_resolution()
        # Download the video
        yt.download(output_path, filename='video.mp4')
        print(f"Downloaded: {yt.title}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Set up the API key and service
api_key = 'AIzaSyDcL_cz9Sc2uhrMFHT7PNc8xzLw3iSoY2s'
youtube = build('youtube', 'v3', developerKey=api_key)


def search_youtube(query, max_results=1):
    # Perform the search
    request = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=max_results
    )
    response = request.execute()

    # Extract video information
    videos = []
    for item in response['items']:
        video_data = {
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'videoId': item['id']['videoId'],
            'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        }
        videos.append(video_data)

    return videos


import hashlib


def generate_md5_short_hash(input_string, length=8):
    # Generate the MD5 hash
    md5_hash = hashlib.md5(input_string.encode()).hexdigest()
    # Truncate the hash to the desired length
    short_hash = md5_hash[:length]
    return short_hash


# Step 4: Create the Interface
with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            prompt = gr.Text(label="Prompt", show_label=False, max_lines=1, placeholder="Enter your prompt")
            submit = gr.Button("Submit", scale=0)
        with gr.Column():
            output = gr.Video(label="Your Generated Video")
    with gr.Row():
        with gr.Column():
            with gr.Row():
                image_input = gr.Image(label="upload swap image")
            with gr.Row():
                image_swap = gr.Image(label="upload swap image")
            with gr.Row():
                swap = gr.Button("Swap", scale=0)
        with gr.Column():
            image_output = gr.Image(label="Your Generated Image")


    def process_video(prompt):
        print("Processing Video....", prompt)
        results = search_youtube(prompt)
        prompt_hash = generate_md5_short_hash(prompt)
        downloaded_youtube_video = os.getcwd() + '/downloads/' + prompt_hash + '/video' + '.mp4'
        final_video = os.getcwd() + '/downloads/' + prompt_hash + '/finalvideo' + '.mp4'
        for video in results:
            print(f"Title: {video['title']}")
            print(f"Description: {video['description']}")
            print(f"URL: {video['url']}")
            download_youtube_video(video['url'], output_path='./downloads/' + prompt_hash)
            print()
        # return os.getcwd() +'./downloads/98522486/How\ To\ Become\ a\ Millionaire\ in\ 5\ Years.mp4'
        return final_video


    # def swapface(file):
    #     filename  = generate_random_word() + ".jpg"
    #     shutil.copy(file, os.getcwd()+"/downloads/"+ filename)
    #     filename = os.getcwd()+"/downloads/"+filename
    #     print("downloaded to ",filename)
    #     ## do your work here
    #     return  filename
    from PIL import Image


    def swapface(source_image, swap_image):
        filename = generate_random_word() + ".jpg"
        source_file = 'source' + filename
        swap_file = 'swap' + filename
        final_file = 'final' + filename
        sif = Image.fromarray(source_image)
        swf = Image.fromarray(swap_image)
        sif.save(os.getcwd() + "/downloads/" + source_file)
        swf.save(os.getcwd() + "/downloads/" + swap_file)
        print("downloaded to ", filename)
        ## do your work here
        source_img = os.getcwd() + "/downloads/" + source_file
        target_img = os.getcwd() + "/downloads/" + swap_file
        swapped = f2f.swap_img_to_img(source_img, target_img, enhance_face_model=None)
        cv2.imwrite("test_swap.jpg", swapped)
        final_file_path = os.getcwd() + "/test_swap.jpg"
        print(final_file_path)
        return final_file_path


    submit.click(
        process_video,
        inputs=[prompt],
        outputs=output
    )
    swap.click(swapface, inputs=[image_input, image_swap], outputs=image_output)
# Step 5: Launch the App
demo.launch()