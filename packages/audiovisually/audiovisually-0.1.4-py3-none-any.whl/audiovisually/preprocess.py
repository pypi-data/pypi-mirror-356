# This file is part of the Audiovisually project.
# Here we can find some preprocessing functions for the video/audio files.
# The current functions are:

# 1. video_to_mp3: Converts a video file to MP3 format.
# 2. mp3_to_text_assemblyai: Transcribes MP3 audio to text using AssemblyAI.
# 3. translate_df: Translates text in a DataFrame from one language to another using a pre-trained translation model.

# Feel free to add any functions you find useful.

import pandas as pd
from moviepy.video.io.VideoFileClip import VideoFileClip
from googletrans import Translator
import tempfile
import whisper
import torch
import os
import sys
import nltk
import asyncio
from googletrans import Translator
from .utils import build_assemblyai_model

#nltk.download('punkt', quiet=True) # Download only if not already present
#nltk.download('punkt_tab', quiet=True) # Download only if not already present

## (1) Video to MP3
def video_to_mp3(video_path, output_path=None):
    """
    Convert a video file to MP3 audio.

    Args:
        video_path (str): Path to the input video file.
        output_path (str, optional): Path to save the output MP3 file. If None, saves in the same folder as input.

    Returns:
        str: Path to the generated MP3 file, or error message if conversion fails.
    
    Example:
        >>> from audiovisually.preprocess import video_to_mp3
        >>> mp3_path = video_to_mp3("input.mp4")
    """
    try:
        sys.stdout = open(os.devnull, 'w') # Suppress output
        video = VideoFileClip(video_path)
        sys.stdout = sys.__stdout__ # Restore output
        if video.audio is None:
            return f"!(1)! No audio in video file: {video_path}"

        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            audio_path = output_path
        else:
            base, ext = os.path.splitext(os.path.basename(video_path))
            audio_path = os.path.join(os.path.dirname(video_path), f"{base}.mp3")

        video.audio.write_audiofile(audio_path, codec='mp3')
        video.audio.close()
        video.close()
        return audio_path
    except Exception as e:
        return f"!(1)! Video to MP3 error: {e}"

## (2) AssemblyAI Transcription
def mp3_to_text(
    audio_path,
    api_key=None,
    engine='assemblyai',
    whisper_model='base',
    timestamps=False
):
    """
    Transcribe an audio file to text using AssemblyAI or OpenAI Whisper.

    Args:
        audio_path (str): Path to the audio file.
        api_key (str, optional): AssemblyAI API key (required if engine='assemblyai').
        engine (str): 'assemblyai' or 'whisper' (default 'assemblyai').
        whisper_model (str): Whisper model size (default 'base').
        timestamps (bool): If True and engine='whisper', return timestamps.

    Returns:
        pd.DataFrame or str: DataFrame with sentences (and optionally timestamps) or error message if transcription fails.

    Example:
        >>> from audiovisually.preprocess import mp3_to_text
        >>> df = mp3_to_text("audio.mp3", api_key="your_api_key", engine="assemblyai")
        >>> df = mp3_to_text("audio.mp3", engine="whisper", timestamps=True)
    """
    try:
        if engine == "assemblyai":
            if timestamps:
                print("Warning: Timestamps are only supported with Whisper. Set engine='whisper' for timestamps output.")
            if not api_key:
                return "!(2)! AssemblyAI API key required."
            assemblyai_model, config = build_assemblyai_model(api_key)
            transcript = assemblyai_model.transcribe(audio_path, config=config)
            sentences = nltk.tokenize.sent_tokenize(transcript.text)
            df = pd.DataFrame(sentences, columns=["Sentence"])
            return df
        elif engine == "whisper":
            model = whisper.load_model(whisper_model)
            result = model.transcribe(audio_path, verbose=False, word_timestamps=timestamps)
            if timestamps:
                # Return DataFrame with text and timestamps
                segments = result.get("segments", [])
                data = []
                for seg in segments:
                    data.append({
                        "Sentence": seg["text"].strip(),
                        "Start": seg["start"],
                        "End": seg["end"]
                    })
                df = pd.DataFrame(data)
                return df
            else:
                sentences = nltk.tokenize.sent_tokenize(result["text"])
                df = pd.DataFrame(sentences, columns=["Sentence"])
                return df
        else:
            return "!(2)! Unknown engine. Use 'assemblyai' or 'whisper'."
    except Exception as e:
        return f"!(2)! Transcription error: {e}"

## (3) Translation to English
def translate_data(
    data, 
    source_lang='auto', 
    dest_lang='en', 
    text_column='Sentence', 
    translated_column='Translation'
):
    """
    Translate text in a DataFrame column, a list of strings, or a single string to a target language.

    Args:
        data (pd.DataFrame, list, or str): DataFrame, list of strings, or single string to translate.
        source_lang (str): Source language code (default 'auto').
        dest_lang (str): Destination language code (default 'en').
        text_column (str): Name of the column with text to translate (used if data is DataFrame).
        translated_column (str): Name of the column to store translations (used if data is DataFrame).

    Returns:
        pd.DataFrame, str, or list: DataFrame with translations, translated string, or list of translations.
    
    Example:
        >>> from audiovisually.preprocess import translate_data
        >>> df = pd.DataFrame({"Sentence": ["Hola", "Bonjour"]})
        >>> translated_df = translate_data(df, dest_lang='en')
        >>> translated_str = translate_data("Guten Morgen", dest_lang='en')
        >>> translated_list = translate_data(["Ciao", "Hallo"], dest_lang='en')
    """
    try:
        async def translate_single_text(text, translator_instance):
            if pd.isna(text) or str(text).strip() == "":
                return ""
            try:
                result = await translator_instance.translate(text, src=source_lang, dest=dest_lang)
                return result.text
            except Exception as inner_e:
                return f"Translation error: {inner_e}"

        async def process_dataframe(dataframe):
            async with Translator() as translator:
                translations = []
                for text in dataframe[text_column]:
                    translations.append(await translate_single_text(text, translator))
                return translations

        async def process_list(texts):
            async with Translator() as translator:
                return [await translate_single_text(text, translator) for text in texts]

        async def process_string(text):
            async with Translator() as translator:
                return await translate_single_text(text, translator)

        if isinstance(data, pd.DataFrame):
            data[translated_column] = asyncio.run(process_dataframe(data))
            return data
        elif isinstance(data, str):
            return asyncio.run(process_string(data))
        elif isinstance(data, list):
            return asyncio.run(process_list(data))
        else:
            return "!(3)! Input must be a DataFrame, string, or list of strings."
    except Exception as e:
        return f"!(3) Translation error: {e}"
