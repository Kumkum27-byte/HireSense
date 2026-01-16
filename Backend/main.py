from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from uuid import uuid4


#Create app instance
app = FastAPI()

#interview questions
interviews = {}

QUESTION_BANK = {
    "ML Engineer":[
        "Introduce yourself",
        "What is overfitting?",
        "Explain bias vs variance.",
        "What is a confusion matrix"
    ]
}

#Routes
@app.get("/")
def home():
    return{"message": "Welcome to AI-Interview Evaluator application!"}

@app.post("/interview")
def start_interview(role:str, level:str):
    interview_id = str(uuid4())

    questions = QUESTION_BANK.get(role, [])

    interviews[interview_id] = {
        "interview_id":interview_id,
        "role":role,
        "questions":questions,
        "current_question":0,
        "answers":[],
        "status":"IN_PROGRESS"
    }

    return{
        "interview_id":interview_id,
        "questions":questions[0]
    }

@app.get("/interview/{interview_id}/question")
def next_question(interview_id:str):
    if interview_id not in interviews:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    interview = interviews[interview_id]

    if interview["status"]!="IN PROGRESS":
        return{"message":"Interview completed", status:interview["status"]}
    
    interview["current_question"]+=1
    idx = interview["current_question"]
    questions = interview["questions"]

    if idx<len(questions):
        return{"question":question[idx], "question_number":idx+1}
    else:
        interview["status"] = "COMPLETED"
        return{"message":"No more questions", "status":"COMPLETED"}
    