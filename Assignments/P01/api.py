# Angel Badillo Hernandez
# CMPS-4443-101
# P01 - Quizzical w/FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from rich import print

import json
import sys
import random
import math

host: str = "localhost"
port: int = 8080

quizApp = FastAPI(
    title="Quizzical API for CMPS-4443-101 Platform Based App Deveplopment",
    description="""Quizzical API 🚀
## Provides quiz questions for high IQ people.
""",
    version="0.0.1",
    terms_of_service="",
    contact={
        "name": "Angel Badillo Hernandez",
        "url": "https://it-is-legend27.repl.co",
        "email": "badilloa022402@gmail.com"
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

quizApp.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuizControl:
    def __init__(self):
        """ Setup the quiz control class which opens a json file of questions and 
            loads them into our class.
        """
        with open("C:\\Users\\badil\\4443-MOB-Badillo\\Assignments\P01\questions.json") as f:
            self.questions = json.load(f)

        print(self.questions)

        self.numQuestions = len(self.questions)

    def numQuestions(self) -> int:
        return self.numQuestions

    def getQuestionText(self, id:int) -> str:
        return self.questions[id]['question']

    def getCorrectAnswer(self, id:int) -> bool:
        return self.questions[id]['answer']

    def addQuestion(self, question):
        self.questions.append(question)
        self.numQuestions += 1

#   ___  ___  _   _ _____ ___ ___
#  | _ \/ _ \| | | |_   _| __/ __|
#  |   / (_) | |_| | | | | _|\__ \
#  |_|_\\___/ \___/  |_| |___|___/


class Question(BaseModel):
    question: str
    answer: bool


Q = QuizControl()


@quizApp.get("/")
async def docs_redirect():
    return RedirectResponse(url="/docs")


@quizApp.post("/question/")
async def addQuestion(question: Question):
    """
    ### Description:
        Get a quiz question
    ### Params:
        None
    ### Returns:
        str: question text
    """
    Q.addQuestion(question.dict())
    print(Q.questions)
    return Q.questions

@quizApp.get("/question/")
async def getQuestionAt(id: int):
    """
    ### Description:
        Get a quiz question at a specific index
    ### Params:
        int: id
    ### Returns:
        str: question text
    """
    question = None

    if id < Q.numQuestions:  # Prevent out of bounds
        question = Q.getQuestionText(id)

    if question is None:  # Raise error
        raise HTTPException(status_code=404, detail="Item not found")

    return {"id": id, "question": question}

@quizApp.get("/answer/")
async def getAnswerAt(id: int):
    """
    ### Description:
        Get a question's answer at an index
    ### Params:
        int: id
    ### Returns:
        bool: answer value
    """
    answer = None

    if id < Q.numQuestions:  # Prevent out of bounds
        answer = Q.getCorrectAnswer(id)

    if answer is None:  # Raise error
        raise HTTPException(status_code=404, detail="Item not found")

    return {"success": True, "id": id, "answer": answer}

@quizApp.get("/num_question/")
async def numQuestions():
    """
    ### Description:
        Return the amount of questions.
    ### Params:
        None
    ### Returns:
        int: amount of questions
    """
    numQuestions = None
    numQuestions = Q.numQuestions

    if numQuestions is None:  # Raise error (this should never happen)
        raise HTTPException(status_code=404, detail="Item not found")
    return {"amount": numQuestions}

if __name__ == "__main__":
    # host="0.0.0.0" for running on server with domain name
    # or
    # host="ip.add.ress" for server ip
    uvicorn.run("api:quizApp",
                host=host,
                port=port,
                log_level="info",
                reload=True)
