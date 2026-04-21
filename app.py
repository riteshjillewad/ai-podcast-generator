import gradio as gr
import os
import time

from services.script_service import generate_script
from models.xtts_model import clone_voice

os.makedirs("outputs", exist_ok=True)


def process_request(audio_file, topic, tone, duration):

    if audio_file is None:
        raise gr.Error("Please upload a voice sample.")

    yield "⏳ Generating AI script...", None

    script = generate_script(topic, tone, duration)

    yield "🎤 Cloning your voice...", None

    output_audio = "outputs/final_podcast.wav"

    clone_voice(
        text=script,
        speaker_wav=audio_file,
        output_path=output_audio
    )

    yield script, output_audio


with gr.Blocks(theme=gr.themes.Soft(), title="VoxCast AI") as app:

    gr.Markdown("""
    # 🎙️ VoxCast AI
    ### Generate Podcasts in Your Own Voice
    Upload a voice sample, choose topic & tone, and create AI podcasts instantly.
    """)

    with gr.Tab("🎧 Generate Podcast"):

        with gr.Row():

            with gr.Column(scale=1):
                audio_input = gr.Audio(
                    type="filepath",
                    label="Upload Voice Sample"
                )

                topic = gr.Textbox(
                    label="Podcast Topic",
                    placeholder="Future of Artificial Intelligence"
                )

                tone = gr.Dropdown(
                    ["Professional", "Casual", "Funny", "Motivational"],
                    value="Professional",
                    label="Tone"
                )

                duration = gr.Dropdown(
                    ["30 Seconds", "1 Minute"],
                    value="30 Seconds",
                    label="Duration"
                )

                btn = gr.Button("🚀 Generate Podcast", variant="primary")

            with gr.Column(scale=1):
                script_output = gr.Textbox(
                    label="Generated Script",
                    lines=12
                )

                audio_output = gr.Audio(
                    label="Podcast Output"
                )

                file_output = gr.File(
                    label="Download Audio"
                )

    with gr.Tab("ℹ️ About"):
        gr.Markdown("""
        ## VoxCast AI

        Features:
        - AI podcast script generation
        - Personal voice cloning
        - Topic-based narration
        - Fast local processing

        Built using:
        - Gradio
        - Ollama
        - XTTS-v2
        """)

    btn.click(
        fn=process_request,
        inputs=[audio_input, topic, tone, duration],
        outputs=[script_output, audio_output]
    )

app.launch()
