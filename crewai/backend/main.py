from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq
import os

app = FastAPI()

# -------- CORS FIX --------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
api_key = os.getenv("GROQ_API_KEY")


# -------- LLM --------
llm = ChatGroq(
    api_key=api_key,
    model="llama-3.3-70b-versatile"
)

# -------- AGENTS --------
researcher = Agent(
    role="Research Agent",
    goal="Understand topic deeply",
    backstory="Expert researcher who gathers structured insights",
    llm=llm,
    verbose=True
)

writer = Agent(
    role="Writer Agent",
    goal="Write structured blog",
    backstory="Professional content writer",
    llm=llm,
    verbose=True
)

# -------- STATE --------
state = {
    "step": 0,
    "task": "",
    "tone": "",
    "length": ""
}

# -------- REQUEST MODEL --------
class Message(BaseModel):
    message: str


# -------- MAIN API --------
@app.post("/crewai-agent")
def agent(msg: Message):

    # STEP 1 → Ask topic
    if state["step"] == 0:
        state["task"] = msg.message
        state["step"] = 1
        return {"reply": "Frontend Agent: What tone? (formal/casual)"}

    # STEP 2 → Ask tone
    elif state["step"] == 1:
        state["tone"] = msg.message
        state["step"] = 2
        return {"reply": "Frontend Agent: What length? (short/medium/long)"}

    # STEP 3 → Generate blog
    elif state["step"] == 2:
        state["length"] = msg.message

        # -------- TASK 1 --------
        task1 = Task(
            description=f"Research about {state['task']}",
            expected_output="Detailed research notes about the topic",
            agent=researcher
        )

        # -------- TASK 2 --------
        task2 = Task(
            description=f"""
            Write a {state['length']} blog in {state['tone']} tone on {state['task']}.
            Include title, intro, body, conclusion.
            """,
            expected_output="A complete well-structured blog",
            agent=writer
        )

        # -------- CREW --------
        crew = Crew(
            agents=[researcher, writer],
            tasks=[task1, task2],
            verbose=True
        )

        result = crew.kickoff()

        state["step"] = 0

        # ✅ SAFE EXTRACTION OF FINAL BLOG
        final_blog = None

        try:
            final_blog = result.raw
        except:
            try:
                final_blog = result.tasks_output[-1].raw
            except:
                final_blog = str(result)

        return {"reply": final_blog}