import gradio as gr
import os
from datetime import datetime

from services.script_service import generate_dialogue
from models.xtts_model import generate_podcast
from agents.music_agent import choose_music
from agents.planner_agent import choose_mode

# create outputs folder
os.makedirs("outputs", exist_ok=True)


# ---------------------------------------------------
# Generate unique timestamp filename
# ---------------------------------------------------
def get_timestamp_filename():
    now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    return f"outputs/podcast_{now}.wav"


# ---------------------------------------------------
# Get generated podcast history
# ---------------------------------------------------
def get_history():
    files = os.listdir("outputs")
    files = [f for f in files if f.endswith(".wav")]
    files.sort(reverse=True)

    return [os.path.join("outputs", f) for f in files]


# ---------------------------------------------------
# Main Generate Function
# ---------------------------------------------------
'''def process(host_audio, guest_audio, topic):

    # validation
    if host_audio is None or guest_audio is None:
        return "Please upload both host and guest voices.", None, get_history()

    if topic.strip() == "":
        return "Please enter a topic.", None, get_history()

    # Step 1 - Generate Host + Guest Dialogue
    script = generate_dialogue(topic)

    # Step 2 - Music Agent decides intro music
    # music_file = choose_music(topic)
    music_file = None

    # Step 3 - Final output filename
    final_output = get_timestamp_filename()

    # Step 4 - Generate podcast with music intro
    generate_podcast(
        script=script,
        host_wav=host_audio,
        guest_wav=guest_audio,
        final_output=final_output,
        music_file=music_file
    )

    # Step 5 - Return outputs
    return script, final_output, get_history()
'''

def process(host_audio, guest_audio, topic):

    if host_audio is None or guest_audio is None:
        return "Upload both voices.", None, get_history()

    if topic.strip() == "":
        return "Enter topic.", None, get_history()

    # Planner Agent decides style
    mode = choose_mode(topic)

    # Generate script using chosen mode
    script = generate_dialogue(topic, mode)

    final_output = get_timestamp_filename()

    generate_podcast(
        script=script,
        host_wav=host_audio,
        guest_wav=guest_audio,
        final_output=final_output,
        music_file=None
    )

    # Show selected mode in script box
    script = f"🎯 Planner Agent Mode: {mode.upper()}\n\n{script}"

    return script, final_output, get_history()

# ---------------------------------------------------
# UI
# ---------------------------------------------------
with gr.Blocks(title="CloneCast AI", theme=gr.themes.Soft()) as app:

    gr.Markdown("""
    # 🎙️ CloneCast AI  
    ### Multi-Speaker Agentic Podcast Generator

    Upload host + guest voices, enter topic, and generate a full AI podcast with music intro.
    """)

    # ---------------------------------------------------
    # Generate Tab
    # ---------------------------------------------------
    with gr.Tab("🎧 Generate Podcast"):

        with gr.Row():

            # Left Panel
            with gr.Column():

                host_audio = gr.Audio(
                    type="filepath",
                    label="🎤 Upload Host Voice"
                )

                guest_audio = gr.Audio(
                    type="filepath",
                    label="🎙 Upload Guest Voice"
                )

                topic = gr.Textbox(
                    label="📝 Podcast Topic",
                    placeholder="Example: Future of Artificial Intelligence"
                )

                btn = gr.Button(
                    "🚀 Generate Podcast",
                    variant="primary"
                )

            # Right Panel
            with gr.Column():

                script_box = gr.Textbox(
                    label="📜 Generated Script",
                    lines=18
                )

                audio_box = gr.Audio(
                    label="🎵 Latest Podcast Output"
                )

    # ---------------------------------------------------
    # History Tab
    # ---------------------------------------------------
    with gr.Tab("📁 Podcast History"):

        history_files = gr.Files(
            label="Generated Podcasts",
            value=get_history()
        )

    # ---------------------------------------------------
    # About Tab
    # ---------------------------------------------------
    with gr.Tab("ℹ️ About"):

        gr.Markdown("""
        ## CloneCast AI Features

        ✅ Host + Guest Voice Cloning  
        ✅ AI Dialogue Generation  
        ✅ Music Agent (Auto Intro Music)  
        ✅ Multi-Speaker Podcast Output  
        ✅ Podcast History Storage  
        ✅ Timestamp Saved Files  

        Built using:

        - Gradio  
        - Ollama  
        - XTTS-v2  
        - Python  
        """)

    # ---------------------------------------------------
    # Button Action
    # ---------------------------------------------------
    btn.click(
        fn=process,
        inputs=[host_audio, guest_audio, topic],
        outputs=[script_box, audio_box, history_files]
    )


# ---------------------------------------------------
# Run App
# ---------------------------------------------------
app.launch()
