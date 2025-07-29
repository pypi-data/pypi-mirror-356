import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
from audiovisually.preprocess import video_to_mp3, mp3_to_text, translate_data
from audiovisually.predict import classify_emotions, classify_emotions_huggingface
import pytest
import pandas as pd
from dotenv import load_dotenv
load_dotenv

def test_full_pipeline():
    video_path = os.path.join(project_root, '60secondes.mp4')

    ## (1) Video to MP3
    audio_path = video_to_mp3(video_path)

    ## (2) AssemblyAI Transcription
    transcription_df = mp3_to_text(audio_path, os.getenv('ASSEMBLYAI_API_KEY'))

    ## (3) Translation to English
    translation_df = translate_data(transcription_df)

    ## (4) Classify emotions using custom model
    model_path = os.path.join(project_root, 'best_model')
    final_custom_df = classify_emotions(model_path, translation_df, text_column='Translation', output_column='Predicted Emotion')
    print(final_custom_df.head())
    print(final_custom_df['Predicted Emotion'].value_counts())

    ## (5) Classify emotions using Hugging Face pipeline
    final_huggingface_df = classify_emotions_huggingface(translation_df, text_column='Translation', output_column='Predicted Emotion')
    print(final_huggingface_df.head())
    print(final_huggingface_df['Predicted Emotion'].value_counts())

if __name__ == "__main__":
    test_full_pipeline()
