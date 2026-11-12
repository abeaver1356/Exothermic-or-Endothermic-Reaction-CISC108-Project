from dataclasses import dataclass
from drafter import *

@dataclass
class Multi_Choice_Question:
    prompt: str
    options: list[str]
    
@dataclass
class Text_Question:
    prompt: str
    
@dataclass
class State:
    questions: list[Multi_Choice_Question]
    text_questions: list[Text_Question]
    position: int
    
QUESTIONS = [
    Multi_Choice_Question("What was the enthalpy of the reaction?",
             ["Positive", "Negative", "Unknown"]),
    Multi_Choice_Question("Are the surroundings hotter or cooler after the reaction took place?",
             ["Hotter", "Cooler", "No Change"])]

TEXT_QUESTIONS = [
    Text_Question("What was the recorded temperature BEFORE the reaction took place?"),
    Text_Question("What was the recorded temperature AFTER the reaction took place?")]

@route
def index(state:State)->Page:
    return Page(state, [
        Header("Exothermic or Endothermic"),
        Button ("Start the questions", "ask")
    ])

@route
def ask(state: State) -> Page:
    question = state.text_questions[state.position]
    content = [
        Header("Question" + str(state.position + 1)),
        question.prompt + "\n"
    ]
    return Page(state, [
        Button("Submit", "ask_multi")
    ])

@route
def ask_multi(state: State) -> Page:
    question = state.questions[state.position]
    content = [
        Header("Question" + str(state.position + 1)),
        question.prompt + "\n"
    ]
    return Page(state, [
        Header("Results"),
        Button("Play again", "restart")
    ])
        
@route
def restart(state: State) -> Page:
    state.position = 0
    return index(state)

start_server(State(QUESTIONS, TEXT_QUESTIONS, 0))
