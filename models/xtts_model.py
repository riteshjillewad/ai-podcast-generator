from TTS.api import TTS
import re

print("Loading XTTS model...")

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")


def clean_text(text):
    text = re.sub(r"\[.*?\]", "", text)
    text = re.sub(r"Title:.*", "", text)
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def clone_voice(text, speaker_wav, output_path):
    text = clean_text(text)

    # Keep only first 400 chars for speed
    text = text[:400]

    tts.tts_to_file(
        text=text,
        speaker_wav=speaker_wav,
        language="en",
        file_path=output_path,
        split_sentences=True
    )

    return output_path