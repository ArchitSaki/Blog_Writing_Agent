from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq

app = FastAPI()

# Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔑 Add your Groq API key here
client = Groq(api_key="your_groq_api_key")

# -------- STATE MACHINE APPROACH --------
state = {
    "step": 0,
    "task": "",
    "tone": "",
    "length": ""
}

class Message(BaseModel):
    message: str
    mode: str   # "state" or "prompt"


@app.post("/agent")
def agent(msg: Message):
    
    if msg.mode == "state":
        return state_machine(msg.message)
    else:
        return prompt_agent(msg.message)


# -------- APPROACH 1: CONTROLLED AGENT --------
def state_machine(user_input):

    if state["step"] == 0:
        state["task"] = user_input
        state["step"] = 1
        return {"reply": "What tone? (formal/casual)"}

    elif state["step"] == 1:
        state["tone"] = user_input
        state["step"] = 2
        return {"reply": "What length? (short/medium/long)"}

    elif state["step"] == 2:
        state["length"] = user_input

        blog = generate_blog(
            state["task"],
            state["tone"],
            state["length"]
        )

        state["step"] = 0
        return {"reply": blog}


# -------- APPROACH 2: PROMPT AGENT --------
def prompt_agent(user_input):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are an AI agent. Ask questions if needed, then generate a blog."
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    return {"reply": response.choices[0].message.content}


# -------- LLM GENERATION --------
def generate_blog(task, tone, length):

    prompt = f"""
    Write a {length} blog on: {task}
    Tone: {tone}
    Include title, intro, body, conclusion.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a professional writer."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content