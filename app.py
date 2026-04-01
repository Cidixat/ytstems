import gradio as gr
import threading
from ytstems import process, MODELS

log_lines = []
log_lock = threading.Lock()


def run_process(url, stem_option):
    if not url.strip():
        yield "Please enter a YouTube URL."
        return

    yield "Downloading audio..."
    try:
        mp3_path, stems_dir = process(url.strip(), stem_option)
    except Exception as e:
        yield f"Error: {e}"
        return

    yield (
        f"Done!\n\n"
        f"MP3 saved to: {mp3_path}\n"
        f"Stems saved to: {stems_dir}"
    )


with gr.Blocks(title="YTStems") as demo:
    gr.Markdown("# YTStems\nDownload a YouTube video's audio and split it into stems.")

    url_input = gr.Textbox(label="YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
    stem_option = gr.Radio(choices=list(MODELS.keys()), value=list(MODELS.keys())[0], label="Stem count")
    run_btn = gr.Button("Process", variant="primary")
    output = gr.Textbox(label="Status", lines=6, interactive=False)

    run_btn.click(fn=run_process, inputs=[url_input, stem_option], outputs=output)

if __name__ == "__main__":
    demo.launch()
