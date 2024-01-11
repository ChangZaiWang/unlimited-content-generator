import asyncio
import websockets

import os
import re
import requests

import openai
from openai import OpenAI
import yt_dlp
from pydub import AudioSegment

from moviepy.editor import *
from moviepy.video.io.VideoFileClip import VideoFileClip
import moviepy.video.fx.crop as crop_vid


def check_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"{path} created successfully")

client = OpenAI()
VIDEO_PATH = "./video/"
AUDIO_PATH = "./audio/"
SERMON_PATH = "./sermon/"
SOCIAL_POST_PATH = "./socialpost/"
SUBTITLE_PATH = "./subtitle/"
SHORTS_PATH = "./shorts/"
IMAGE_PATH = "./image/"

check_directory(VIDEO_PATH)
check_directory(AUDIO_PATH)
check_directory(SERMON_PATH)
check_directory(SOCIAL_POST_PATH)
check_directory(SUBTITLE_PATH)
check_directory(SHORTS_PATH)
check_directory(IMAGE_PATH)


def download_video(URL):
    try:
        # get video title
        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(URL, download=False)

        title = info["title"]
        duration = info.get("duration", 0)  # 使用 get() 避免當無法獲取 duration 時的 KeyError

        if duration > 7200:
            return "Sorry! Your video is too long to be processed."

        # set download options
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": f"{VIDEO_PATH}/{title}.%(ext)s"
        }

        # download video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([URL])  # 將 URL 放入一個列表中

        # rename ext. to mp4
        for f in os.listdir(VIDEO_PATH):
            if f.startswith(title):
                os.rename(f"{VIDEO_PATH}/{f}", f"{VIDEO_PATH}/{title}.mp4")
                break

        return title + ".mp4"

    except yt_dlp.DownloadError as e:
        return f"Error downloading video: {e}"

    except Exception as e:
        return f"An unexpected error occurred: {e}"

def extract_audio(video_file):
    try:
        if not os.path.exists(VIDEO_PATH + video_file):
            return f"Error: Video file {video_file} not found."
        
        video = VideoFileClip(VIDEO_PATH + video_file)
        audio = video.audio
        audio_file = AUDIO_PATH + video_file.replace("mp4", "mp3")
        audio.write_audiofile(audio_file)
    
        return video_file.replace("mp4", "mp3")
    
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def compress_audio(audio_file):
    try: 
        if not os.path.exists(AUDIO_PATH + audio_file):
            return f"Error: Audio file {audio_file} not found."
        
        file_size = os.path.getsize(AUDIO_PATH + audio_file)
        if file_size <= 25000000:
            return audio_file
        
        audio = AudioSegment.from_file(AUDIO_PATH + audio_file)

        # Set output parameters
        channels = 1  # mono
        frame_rate = 16000  # sample rate
        bit_rate = "24k"  # 位元率

        # Audio transcode and save
        output_audio = audio.set_channels(channels).set_frame_rate(frame_rate)
        output_file = "compressed_" + audio_file
        output_audio.export(AUDIO_PATH + output_file, format="mp3", bitrate=bit_rate)

        # Check the size of the compressed 
        compressed_file_size = os.path.getsize(AUDIO_PATH + output_file)
        if compressed_file_size > 25000000:
            print("File too big..., compress again...")
            bit_rate = "16k"  # Lower bitrate for a second compression
            output_audio.export(os.path.join(AUDIO_PATH, output_file), format="mp3", bitrate=bit_rate)

        return output_file
    
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def get_transcript(audio_file):
    try:
        if not os.path.exists(AUDIO_PATH + audio_file):
            return f"Audio file {audio_file} not found."
        
        audio = open(AUDIO_PATH + audio_file, "rb")
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio, 
            language="zh",
            response_format="srt"
        )
        transcript = transcript.replace(" ", "，")
            
        return transcript
    
    except openai.OpenAIError as e:
        return f"OpenAI API error: {e}"
    
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def save_file(input, path, filename):
    with open(path + filename, "w") as file:
        file.write(input)

def extract_text_from_srt(srt_string):
    ## re.findall() -> re.sub() ##
    ## regex ^

    pattern = re.compile(r'\d+\n\d{2}:\d{2}:\d{2},\d{3}，-->，\d{2}:\d{2}:\d{2},\d{3}\n(.*?)\n\n', re.DOTALL)
    matches = pattern.findall(srt_string)

    cleaned_matches = [match.strip() for match in matches]

    result = ' '.join(cleaned_matches)

    return result

def generate_sermon(text):
    try:
        response = client.chat.completions.create(
            model = "gpt-4-1106-preview",
            messages = [
            {"role": "system", "content": "你是一位牧師，下面將提供逐字稿，請加上適當的標點符號，整理成有結構且易讀的內容，並且為產出的內容適當的命名，同時為每一段下一個小標題。"},
            {"role": "user", "content": text}
            ]
        )

        return response.choices[0].message.content
    
    except openai.OpenAIError as e:
        return f"OpenAI API error: {e}"
    
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def generate_social_post(text, style):
    try:
        response = client.chat.completions.create(
            model = "gpt-4-1106-preview",
            messages = [
            {"role": "system", "content": f"你是一個厲害的社群媒體經營者，下面將提供牧師的講章，請產生五篇社群貼文，並加上主題標籤。風格：{style}"},
            {"role": "user", "content": text}
            ]
        )

        return response.choices[0].message.content
    
    except openai.OpenAIError as e:
        return f"OpenAI API error: {e}"
    
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def generate_clip(text):
    try:
        response = client.chat.completions.create(
            model = "gpt-4-1106-preview",
            messages = [
            {"role": "system", "content": "你是一個厲害的短影音剪輯師，下面將提供一份字幕檔，請根據字幕檔的內容，給予五個你認為可以剪輯成長度為60秒的短影音段落。時間段落指示請依照SRT字幕檔的格式：時間 --> 時間"},
            {"role": "user", "content": text}
            ]
        )
        clips = response.choices[0].message.content

        matches = re.findall(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', clips)
        if not matches:
            print("Clips not found, trying again")
            return generate_clip(text)

        return matches
    
    except openai.OpenAIError as e:
        return f"OpenAI API error: {e}"
    
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def generate_shorts(matches, video_file):
    file_num = 1
    for match in matches:
        time = match.split(" --> ")
        start_time = time[0]
        end_time = time[1]

        sixteen_by_nine_video = VideoFileClip(VIDEO_PATH + video_file).subclip((start_time), (end_time))
        
        nine_by_sixteen_video = VideoFileClip(VIDEO_PATH + video_file).subclip((start_time), (end_time))
        w, h = nine_by_sixteen_video.size
        target_ratio = 1080 / 1920
        current_ratio = w / h

        if current_ratio > target_ratio:
            # The video is wider than the desired aspect ratio, crop the width
            new_width = int(h * target_ratio)
            x_center = w / 2
            y_center = h / 2
            nine_by_sixteen_video = crop_vid.crop(nine_by_sixteen_video, width=new_width, height=h, x_center=x_center, y_center=y_center)
        else:
            # The video is taller than the desired aspect ratio, crop the height
            new_height = int(w / target_ratio)
            x_center = w / 2
            y_center = h / 2
            nine_by_sixteen_video = crop_vid.crop(nine_by_sixteen_video, width=w, height=new_height, x_center=x_center, y_center=y_center)

        
        sixteen_by_nine_video.write_videofile(
            SHORTS_PATH + f"original_clip_{file_num}.mp4", 
            codec='libx264', 
            audio_codec='aac', 
            temp_audiofile='temp-audio.m4a', 
            remove_temp=True
        )
        print(f"Saved file original_clip_{file_num}")

        nine_by_sixteen_video.write_videofile(
            SHORTS_PATH + f"shorts_{file_num}.mp4", 
            codec='libx264', 
            audio_codec='aac', 
            temp_audiofile='temp-audio.m4a', 
            remove_temp=True
        )
        print(f"Saved file shorts_{file_num}")
        file_num += 1

def generate_social_post_image(prompt, style):
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=f"請針對以下內容，設計適合的社群貼文圖，但不要出現文字。\n 風格：{style}。\n" + prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        image_url = response.data[0].url
        print(image_url)

        image = requests.get(image_url)
        if image.status_code == 200:
            with open(IMAGE_PATH + "image.png", "wb") as f:
                f.write(image.content)
            print("Image downloaded successfully.")
        else:
            raise Exception(f"Failed to download image. Status code: {image.status_code}")

    except openai.OpenAIError as e:
        return f"OpenAI API error: {e}"

    except Exception as e:
        return f"An unexpected error occurred: {e}"

async def handler(websocket, path):
    async for message in websocket:
        try:
            data = eval(message)
            yt_url = data["yt_url"]
            social_post_style = data["social_post_style"]
            image_style = data["image_style"]

            video_file = download_video(yt_url)
            audio_file = extract_audio(video_file)
            compressed_audio_file = compress_audio(audio_file)
            transcript = get_transcript(compressed_audio_file)
            save_file(transcript, SUBTITLE_PATH, "subtitle.srt")
            srt_text = extract_text_from_srt(transcript)
            sermon = generate_sermon(srt_text)
            save_file(sermon, SERMON_PATH, "sermon.txt")
            social_post = generate_social_post(sermon, social_post_style)
            save_file(social_post, SOCIAL_POST_PATH, "social_post.txt")
            times = generate_clip(transcript)
            generate_shorts(times, video_file)
            image_prompt = social_post
            generate_social_post_image(image_prompt, image_style)

            responce = f"Processing completed for {yt_url}"
        except Exception as e:
            responce = f"Error processing {yt_url}: {str(e)}"

        await websocket.send(responce)

start_server = websockets.serve(handler, "localhost", 8765, ping_interval=None)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()