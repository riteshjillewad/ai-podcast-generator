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


def add_intro_music(voice_audio, music_file, final_output):
    """
    Add intro music before podcast starts
    """

    speech = AudioSegment.from_wav(voice_audio)

    music = AudioSegment.from_wav(music_file)

    # lower music volume
    music = music - 12

    # keep first 5 sec only
    intro = music[:5000]

    final_audio = intro + speech

    final_audio.export(final_output, format="wav")


def generate_podcast(script, host_wav, guest_wav, final_output, music_file=None):

    os.makedirs("temp", exist_ok=True)

    temp_voice_output = "temp/temp_voice.wav"

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

    # save voice-only podcast first
    combined.export(temp_voice_output, format="wav")

    # if music selected, add intro music
    if music_file and os.path.exists(music_file):
        add_intro_music(
            voice_audio=temp_voice_output,
            music_file=music_file,
            final_output=final_output
        )
    else:
        combined.export(final_output, format="wav")

    return final_output
