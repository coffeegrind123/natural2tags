import unicodedata
import gradio as gr
from text2tags import TaggerLlama

model = TaggerLlama()

SPACE_COMMAS = True
BRACKET2WEIGHT = True
SPACE2UNDERSCORE = False
IGNOREUNDERSCORES = True

ui_prompts = []

def normalize_characters(data: str):
    return unicodedata.normalize("NFKC", data)

def format_prompt(*prompts: list):
    ret = []

    for prompt in prompts:
        if not prompt or prompt.strip() == "":
            ret.append("")
            continue

        prompt = normalize_characters(prompt)

        # Use TaggerLlama to predict tags
        tags = model.predict_tags(prompt)
        ret.append(', '.join(tags))

    return ret

def on_before_component(component: gr.component, **kwargs: dict):
    if "elem_id" in kwargs and kwargs["elem_id"] == "paste":
        with gr.Blocks(analytics_enabled=False) as ui_component:
            button = gr.Button(value="🪄", elem_classes="tool", elem_id="format")
            button.click(fn=format_prompt, inputs=ui_prompts, outputs=ui_prompts)
            return ui_component
    return None

script_callbacks.on_before_component(on_before_component)
