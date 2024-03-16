import math
import os

import moviepy.editor as mp
from pydub import AudioSegment


def extract_audio(video_path):
    # extracts audio from a video

    folder_path = os.path.dirname(video_path)
    folder_path = os.path.join(folder_path, "audio")
    os.makedirs(folder_path, exist_ok=True)
    audio_path = os.path.join(folder_path, "audio.wav")

    video_clip = mp.VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_path)

    return audio_path


def split_audio_in_pieces(audio_path):
    # splits large audio file into smaller chunks

    audio = AudioSegment.from_wav(audio_path)
    length_audio = len(audio)
    audio_duration = 60 * 1000  # audio chunks of 60 sec.
    number_of_pieces = math.ceil(length_audio / audio_duration)

    pieces = []

    # create a unique folder for every run
    folder_path = os.path.dirname(audio_path)

    for i in range(number_of_pieces):
        piece_name = os.path.join(folder_path, f"audio_piece_{i}.wav")
        start = i * audio_duration
        end = (
            (i + 1) * audio_duration
            if (i + 1) * audio_duration < length_audio
            else length_audio
        )

        split_audio = audio[start:end]
        split_audio.export(piece_name, format="wav")
        pieces += [piece_name]

    return pieces


def join_audio_pieces(pieces):
    # joins chunks of audio into a complete audio file

    folder_path = os.path.dirname(pieces[0])
    output_path = os.path.join(folder_path, "joined_audio.wav")

    combined_audio = AudioSegment.empty()
    for piece_name in pieces:
        piece = AudioSegment.from_wav(piece_name)
        combined_audio += piece

    combined_audio.export(output_path, format="wav")
    return output_path
