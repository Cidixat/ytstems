import gradio as gr
from ytstems import process, process_file, MODELS

stem_choices = list(MODELS.keys())


def run(url, file, stem_option):
    if file is not None:
        yield "Processing file..."
        try:
            audio_path, stems_dir = process_file(file, stem_option)
        except Exception as e:
            yield f"Error: {e}"
            return
        yield f"Done!\n\nAudio: {audio_path}\nStems: {stems_dir}"
    elif url and url.strip():
        yield "Downloading audio..."
        try:
            mp3_path, stems_dir = process(url.strip(), stem_option)
        except Exception as e:
            yield f"Error: {e}"
            return
        yield f"Done!\n\nAudio: {mp3_path}\nStems: {stems_dir}"
    else:
        yield "Please enter a URL or upload a file."


CSS = """
.gradio-container {
    max-width: 900px !important;
    margin: 0 auto;
}
.html-container {
    padding: 0;
}
.step-box {
    border: 1px solid #e0e0e0;
    border-radius: 12px;
}
.step-header {
    font-size: 1.1rem;
    font-weight: 600;
    border-bottom: 1px solid #e0e0e0;
    padding-bottom: 16px;
    margin-bottom: 16px !important;
}
.gr-group {
    padding: 16px;
}
.row {
    gap: 16px;
}

.top-spacing {
    margin-top: 16px;
}

.big-button {
    margin: 0 auto 16px;
    padding: 24px;
    max-width: 50%;
    font-size: 24px;
}

.vertical-radio .wrap {
    flex-direction: column !important;
}
"""

with gr.Blocks(title="YTStems", css=CSS) as demo:
    gr.Markdown("# YTStems\nSplit any song into individual stems using AI-powered source separation.")

    # Step 1
    with gr.Group(elem_classes="step-box"):
        gr.HTML("<p class='step-header'>Step 1 — Choose your source</p>")
        with gr.Column():
            with gr.Row():
                with gr.Column():
                    gr.Markdown("#### From a URL", elem_classes="source-header")
                    gr.Markdown("Paste a URL from YouTube, SoundCloud, Bandcamp, and [many more](https://github.com/yt-dlp/yt-dlp/blob/master/supportedSites.md).")
                    url_input = gr.Textbox(label="URL", placeholder="https://www.youtube.com/watch?v=...", elem_classes="top-spacing")

                with gr.Column():
                    gr.Markdown("#### From a local file", elem_classes="source-header")
                    gr.Markdown("Upload an audio file (MP3, WAV, FLAC, etc.) to split into stems.")
                    file_input = gr.File(label="Audio file", file_types=["audio"], elem_classes="top-spacing")

    # Step 2
    with gr.Group(elem_classes="step-box"):
        gr.HTML("<p class='step-header'>Step 2 — Choose your stem model</p>")
        with gr.Column():
            stem_option = gr.Radio(choices=stem_choices, value=stem_choices[0], label="Available Models", elem_classes="vertical-radio")

    # Step 3
    with gr.Group(elem_classes="step-box"):
        gr.HTML("<p class='step-header'>Step 3 — Process</p>")
        with gr.Column():
            process_btn = gr.Button("Split them stems!", variant="primary", elem_classes="big-button", interactive=False)
            output = gr.Textbox(label="Status", lines=5, interactive=False)

    def toggle_btn(url, file):
        return gr.update(interactive=bool((url and url.strip()) or file is not None))

    url_input.change(fn=toggle_btn, inputs=[url_input, file_input], outputs=process_btn)
    file_input.change(fn=toggle_btn, inputs=[url_input, file_input], outputs=process_btn)
    process_btn.click(fn=run, inputs=[url_input, file_input, stem_option], outputs=output)
if __name__ == "__main__":
    demo.launch()
