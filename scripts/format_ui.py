import unicodedata
from text2tags import TaggerLlama
import gradio as gr
from modules import script_callbacks, scripts, shared
from modules.processing import StableDiffusionProcessingTxt2Img, StableDiffusionProcessingImg2Img

model = TaggerLlama()

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

        tags = model.predict_tags(prompt)
        formatted_tags = ', '.join(tags)
        print(formatted_tags)

        ret.append(formatted_tags)

    return ret

def process_prompt(prompt):
    if not prompt or prompt.strip() == "":
        return ""
    tags = model.predict_tags(prompt)
    formatted_tags = ', '.join(tags)
    return formatted_tags

def hijack_processing():
    original_txt2img_init = StableDiffusionProcessingTxt2Img.__init__
    original_img2img_init = StableDiffusionProcessingImg2Img.__init__

    def new_txt2img_init(self, *args, **kwargs):
        if 'prompt' in kwargs:
            kwargs['prompt'] = process_prompt(kwargs['prompt'])
        original_txt2img_init(self, *args, **kwargs)

    def new_img2img_init(self, *args, **kwargs):
        if 'prompt' in kwargs:
            kwargs['prompt'] = process_prompt(kwargs['prompt'])
        original_img2img_init(self, *args, **kwargs)

    StableDiffusionProcessingTxt2Img.__init__ = new_txt2img_init
    StableDiffusionProcessingImg2Img.__init__ = new_img2img_init

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

"""
Register Callbacks
"""
script_callbacks.on_before_component(on_before_component)
script_callbacks.on_app_started(hijack_processing)
