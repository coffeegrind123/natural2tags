import unicodedata

import gradio as gr
from modules import script_callbacks, scripts, shared


"""
References
"""
ui_prompts = []


"""
Functions
"""


def format_prompt(*prompts: list):
    ret = []

    for prompt in prompts:
        if not prompt or prompt.strip() == "":
            ret.append("")
            continue

        prompt = model.predict_tags(prompt)
        print(prompt)

        ret.append(prompt)

    return ret


def on_before_component(component: gr.component, **kwargs: dict):
    if "elem_id" in kwargs:
        if kwargs["elem_id"] in [
            "txt2img_prompt",
            "txt2img_neg_prompt",
            "img2img_prompt",
            "img2img_neg_prompt",
        ]:
            ui_prompts.append(component)
            return None
        elif kwargs["elem_id"] == "paste":
            with gr.Blocks(analytics_enabled=False) as ui_component:
                button = gr.Button(value="🪄", elem_classes="tool", elem_id="format")
                button.click(fn=format_prompt, inputs=ui_prompts, outputs=ui_prompts)
                return ui_component
        return None
    return None



script_callbacks.on_before_component(on_before_component)
