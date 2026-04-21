import gradio as gr
import os

from services.script_service import generate_script
from models.xtts_model import clone_voice

os.makedirs("outputs", exist_ok=True)


def process_request(audio_file, topic, tone, duration):

    if audio_file is None:
        return "Upload voice sample first.", None

    script = generate_script(topic, tone, duration)

    output_audio = "outputs/final_podcast.wav"

    clone_voice(
        text=script,
        speaker_wav=audio_file,
        output_path=output_audio
    )

    return script, output_audio


with gr.Blocks() as app:

    gr.Markdown("# 🎙️ Fast AI Podcast Generator")

    with gr.Row():

        with gr.Column():
            audio_input = gr.Audio(type="filepath", label="Voice Sample")

            topic = gr.Textbox(label="Topic")

            tone = gr.Dropdown(
                ["Professional", "Casual", "Funny"],
                value="Professional",
                label="Tone"
            )

            duration = gr.Dropdown(
                ["30 Seconds", "1 Minute"],
                value="30 Seconds",
                label="Duration"
            )

            btn = gr.Button("🚀 Generate Fast Podcast")

        with gr.Column():
            script_box = gr.Textbox(label="Generated Script", lines=8)
            audio_box = gr.Audio(label="Podcast Audio")

    btn.click(
        fn=process_request,
        inputs=[audio_input, topic, tone, duration],
        outputs=[script_box, audio_box]
    )

app.launch()
