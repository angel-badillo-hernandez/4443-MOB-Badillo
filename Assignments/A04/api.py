from typing import Optional
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from rich import print

import json
import sys
import random
import math

quizApp = FastAPI(
    title="Quizzler API for CMPS-4443-101 Platform Based App Deveplopment",
    description="""Quizzler API 🚀
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


class QuizBrain:

    def __init__(self):
        """ Setup the quiz brain class which opens a json file of questions and 
            loads them into our class. cd
        """
        with open(".\questions.json") as f:
            self.questions = json.load(f)

        print(self.questions)

        self.numQuestions = len(self.questions)

        self.id = 0

    def setCurrent(self, n) -> None:
        """ Sets the current question id
        Params:
           (int) id : value from 0 to max question item
        """
        self.id = n

    def getCurrentId(self) -> int:
        return self.id

    def nextQuestion(self) -> int:
        self.id += 1
        return self.id

    def numQuestions(self) -> int:
        return self.numQuestions

    def getQuestionText(self) -> str:
        return self.questions[self.id]['question']

    def getCorrectAnswer(self) -> bool:
        return self.questions[self.id]['answer']

    def isFinished(self) -> bool:
        return self.id < len(self.questions)

    def reset(self) -> None:
        self.id = 0

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


Q = QuizBrain()


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
async def getQuestion():
    """
    ### Description:
        Get a quiz question
    ### Params:
        None
    ### Returns:
        str: question text
    """
    question = None
    id = Q.getCurrentId()

    if id < Q.numQuestions:  # Prevent out of bounds
        question = Q.getQuestionText()

    if not question is None:  # If question exists
        return {"success": True, "id": id, "question": question}

    return {"success": False}


@quizApp.get("/question_at/")
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
    id = id

    if id < Q.numQuestions:  # Prevent out of bounds
        question = Q.questions[id]["question"]

    if not question is None:  # If question exists
        return {"success": True, "id": id, "question": question}

    return {"success": False}


@quizApp.get("/answer/")
async def getAnswer():
    """
    ### Description:
        Get a question's answer
    ### Params:
        None
    ### Returns:
        bool: answer value
    """
    answer = None
    id = Q.getCurrentId()

    if id < Q.numQuestions:  # Prevent out of bounds
        answer = Q.getCorrectAnswer()

    if not answer is None:  # If answer exists
        return {"success": True, "id": id, "answer": answer}

    return {"success": False}


@quizApp.get("/answer_at/")
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
    id = id

    if id < Q.numQuestions:  # Prevent out of bounds
        answer = Q.questions[id]["answer"]

    if not answer is None:  # If answer exists
        return {"success": True, "id": id, "answer": answer}

    return {"success": False}


@quizApp.get("/next/")
async def next():
    """
    ### Description:
        Increment current question id
    ### Params:
        None
    ### Returns:
        int: question id
    """
    id = None
    id = Q.nextQuestion()

    if id < Q.numQuestions:  # Prevent going out of bounds
        return {"success": True, "id": id}, 200

    return {"success": False}


@quizApp.get("/reset/")
async def reset():
    """
    ### Description:
        Reset id to 0 
    ### Params:
        None
    ### Returns:
        bool
    """
    id = None

    Q.reset()

    id = Q.getCurrentId()

    if id == 0:
        return {"success": True, "id": id}, 200

    return {"success": False}


if __name__ == "__main__":
    # host="0.0.0.0" for running on server with domain name
    # or
    # host="ip.add.ress" for server ip
    uvicorn.run("api:quizApp",
                host="127.0.0.1",  # localhost
                port=8888,
                log_level="info",
                reload=True)
