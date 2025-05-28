import gradio as gr
import requests

def query_llm(prompt):
    r = requests.post("http://fastapi:8000/chat", json={"prompt": prompt})
    choices = r.json().get("choices", [])
    return choices[0]["message"]["content"] if choices else "Error"

demo = gr.Interface(fn=query_llm, inputs="text", outputs="text")
demo.launch(server_name="0.0.0.0", server_port=8501)
