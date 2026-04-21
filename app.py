import gradio as gr
import os
from datetime import datetime

from services.script_service import generate_dialogue
from models.xtts_model import generate_podcast

os.makedirs("outputs", exist_ok=True)


def get_timestamp_filename():
    now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    return f"outputs/podcast_{now}.wav"


def get_history():
    files = os.listdir("outputs")
    files = [f for f in files if f.endswith(".wav")]
    files.sort(reverse=True)

    return [os.path.join("outputs", f) for f in files]


def process(host_audio, guest_audio, topic):

    if host_audio is None or guest_audio is None:
        return "Upload both voices.", None, get_history()

    script = generate_dialogue(topic)

    output_file = get_timestamp_filename()

    generate_podcast(
        script=script,
        host_wav=host_audio,
        guest_wav=guest_audio,
        final_output=output_file
    )

    return script, output_file, get_history()


with gr.Blocks(title="CloneCast AI") as app:

    gr.Markdown("# 🎙️ CloneCast AI")
    gr.Markdown("Multi-Speaker Agentic Podcast Generator")

    with gr.Tab("🎧 Generate"):

        with gr.Row():

            with gr.Column():
                host_audio = gr.Audio(type="filepath", label="Host Voice")
                guest_audio = gr.Audio(type="filepath", label="Guest Voice")
                topic = gr.Textbox(label="Podcast Topic")

                btn = gr.Button("🚀 Generate Podcast")

            with gr.Column():
                script_box = gr.Textbox(
                    label="Generated Script",
                    lines=18
                )

                audio_box = gr.Audio(
                    label="Latest Podcast"
                )

    with gr.Tab("📁 History"):

        history_files = gr.Files(
            label="Generated Podcasts",
            value=get_history()
        )

    btn.click(
        fn=process,
        inputs=[host_audio, guest_audio, topic],
        outputs=[script_box, audio_box, history_files]
    )

app.launch()
