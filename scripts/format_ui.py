import unicodedata
from text2tags import TaggerLlama
import gradio as gr
from modules import script_callbacks, scripts, shared

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

class ScriptProcessPrompts(scripts.Script):
    def title(self):
        return "Prompt Processor"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def process(self, p, *args):
        p.all_prompts = [process_prompt(x) for x in p.all_prompts]
        p.all_negative_prompts = [process_prompt(x) for x in p.all_negative_prompts]

        p.main_prompt = process_prompt(p.main_prompt)
        p.main_negative_prompt = process_prompt(p.main_negative_prompt)

        if getattr(p, 'enable_hr', False):
            p.all_hr_prompts = [process_prompt(x) for x in p.all_hr_prompts]
            p.all_hr_negative_prompts = [process_prompt(x) for x in p.all_hr_negative_prompts]

            p.hr_prompt = process_prompt(p.hr_prompt)
            p.hr_negative_prompt = process_prompt(p.hr_negative_prompt)

def before_token_counter(params: script_callbacks.BeforeTokenCounterParams):
    params.prompt = process_prompt(params.prompt)

script_callbacks.on_before_token_counter(before_token_counter)
script_callbacks.on_before_component(on_before_component)
