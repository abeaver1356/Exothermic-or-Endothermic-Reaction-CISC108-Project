#from bakery import assert_equal
from dataclasses import dataclass
from drafter import *

set_website_title("Exothermic or Endothermic")
set_site_information(
    author="Alex Beaver",
    description= "Helps students determine whether their reaction was exo or endothermic.",
    sources= "Thanks to the Drafter docs",
    planning=["Alex Beaver Plan.pdf, Alex Beaver Design.pdf"],
    links= ["https://github.com/abeaver1356/Exothermic-or-Endothermic-Reaction-CISC108-Project"]
    )
hide_debug_information()


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
    answers: list[str]

QUESTIONS = [
    Multi_Choice_Question("What was the enthalpy of the reaction?",
                         ["Positive", "Negative", "Unknown"]),
    Multi_Choice_Question("Are the surroundings hotter or cooler after the reaction took place?",
                         ["Hotter", "Cooler", "No Change"])
]

TEXT_QUESTIONS = [
    Text_Question("What was the recorded temperature BEFORE the reaction took place?"),
    Text_Question("What was the recorded temperature AFTER the reaction took place?")
]

@route
def index(state: State) -> Page:
    return Page(state, [
        Header("Exothermic or Endothermic"),
        Button("Start the questions", "ask")
    ])

@route
def ask(state: State) -> Page:
    if state.position < len(state.text_questions):
        question = state.text_questions[state.position]

        return Page(state, [
            Header("Question " + str(state.position + 1)),
            question.prompt,
            TextBox("answer"),
            Button("Submit", "submit_text")
        ])

    else:
        return ask_multi(state)

@route
def submit_text(state: State, answer: str) -> Page:
    state.answers.append(answer)
    state.position += 1
    return ask(state)

@route
def ask_multi(state: State) -> Page:
    question_position = state.position - len(state.text_questions)
    question = state.questions[question_position]

    return Page(state, [
        Header("Question " + str(state.position + 1)),
        question.prompt,
        SelectBox("answer", question.options),
        Button("Submit", "submit_multi")
    ])

@route
def submit_multi(state: State, answer: str) -> Page:
    state.answers.append(answer)
    state.position += 1

    if state.position < len(state.text_questions) + len(state.questions):
        return ask(state)

    return Page(state, [
        Header("Results"),
        "Your answers:",
        *[answer for answer in state.answers],
        Button("Play again", "restart")
    ])

@route
def restart(state: State) -> Page:
    state.position = 0
    state.answers = []
    return index(state)



start_server(State(QUESTIONS, TEXT_QUESTIONS, 0, []))
