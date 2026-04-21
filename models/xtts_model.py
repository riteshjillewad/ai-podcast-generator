from TTS.api import TTS
from pydub import AudioSegment
import os

print("Loading XTTS Model...")

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")


def generate_line(text, speaker_wav, output_path):
    tts.tts_to_file(
        text=text,
        speaker_wav=speaker_wav,
        language="en",
        file_path=output_path
    )


def generate_podcast(script, host_wav, guest_wav, final_output):

    os.makedirs("temp", exist_ok=True)

    combined = AudioSegment.silent(duration=500)

    lines = script.split("\n")
    count = 0

    for line in lines:

        line = line.strip()

        if line.startswith("HOST:"):
            text = line.replace("HOST:", "").strip()
            temp_file = f"temp/host_{count}.wav"

            generate_line(text, host_wav, temp_file)

            combined += AudioSegment.from_wav(temp_file)
            combined += AudioSegment.silent(duration=400)

            count += 1

        elif line.startswith("GUEST:"):
            text = line.replace("GUEST:", "").strip()
            temp_file = f"temp/guest_{count}.wav"

            generate_line(text, guest_wav, temp_file)

            combined += AudioSegment.from_wav(temp_file)
            combined += AudioSegment.silent(duration=400)

            count += 1

    combined.export(final_output, format="wav")

    return final_output
