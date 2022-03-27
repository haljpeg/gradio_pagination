import gradio as gr
from gradio.inputs import Textbox
import pickle as pkl
import json
from pagination import create_html

def end_to_end(test_input_str):
    doodles_dict = pkl.load(open("doodles_very_small_info.pkl", "rb"))
    for d in doodles_dict:
        d["rarity_percent"] = min(max(1, int((d["rarity_index"] / len(doodles_dict)) * 100)), 99)

    num_items = 25

    doodles_dict_chunked = [doodles_dict[i:i + num_items] for i in range(0, len(doodles_dict), num_items)]

    doodles_json = json.dumps(doodles_dict_chunked)
    html = create_html(doodles_json, style=True)

    return html

iface = gr.Interface(fn=end_to_end, \
                     inputs=[Textbox(lines=1, placeholder="[TEST] enter anything random", default="", \
                                    label="Search Query")],\
                     outputs="html",\
                     layout="vertical",\
                     examples=["TEST"])
iface.launch()
