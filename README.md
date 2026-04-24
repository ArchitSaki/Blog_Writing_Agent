# Blog_Writing_Agent

This is the project for building a agentic system for writing the blogs on the user input. There are multiple ways to do this project as we can use simple logic or we can use multiple frameworks for it, but i decided to go with this appraches as i thought it would bring all the ways into it. 
In this project I have thought of 2 approaches to tackle the problem. 
-I first used a fully logic based system i.e state based system where I manually shown the interaction between the backend and frontend agent for generating the Blog and 
-In the second approach i have buuild the agents using CrewAi, with using crewai i got to implement the multi agent system and in this the whole logic was automated so that the Agents will handle everything.

## Approach 1: State Machine Based System

In the first approach, I built a fully controlled system using a **state-based logic**.

Here, the backend manually controls the flow of conversation step by step.

### How it works:
- User first gives the **blog topic**
- Then system asks for **tone (formal/casual)**
- Then system asks for **length (short/medium/long)**
- Finally, based on all inputs, the blog is generated using an LLM (Groq API)

## Approach 2: CrewAI Multi-Agent System

In the second approach, I used **CrewAI** to build a multi-agent system.

Here, instead of manually controlling the flow, different agents handle different tasks automatically.

### How it works:
- One agent understands the user request
- Another agent plans the blog structure
- Another agent generates the final blog
- All agents work together like a team (crew)

##how to run:-
- for that first create a virtual environment and install all the dependencies i.e requirements.txt file in it.
- then after that open the approach you want to test
- if you selected the state based then go in backend folder on your terminal and execute it 
- once the backend has started then open the html page and you are good to go...

## 📌 Conclusion

This project helped me understand how AI agents can be built using both **traditional logic-based approaches** and **modern autonomous multi-agent systems**. It gave me a clear idea of how real-world AI applications evolve from simple rule-based systems to intelligent agent-based architectures.
