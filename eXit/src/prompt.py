import warnings
import logging
logging.basicConfig(level=logging.ERROR)
warnings.filterwarnings("ignore")
from dataclasses import dataclass
from typing import Any, Callable, List, Type
import questionary
from sentence_transformers import SentenceTransformer, util
import os

model = SentenceTransformer('all-MiniLM-L6-v2')

@dataclass
class IPromptImage:
    src: str
    width: int = 72
    reduce_colorset: int = 8

@dataclass
class IPromptText:
    message: str
    color: str = None
    attrs: List[str] = None

@dataclass
class IPrompt:
    text: IPromptText
    image: IPromptImage = None
    options: List[str] = None
    hidden: bool = False
    dtype: Type = str
    can_skip: bool = False

@dataclass
class IScenarioOutcome:
    examples: List[str]
    scenario: 'IScenario' = None
    message: str = None
    exec: Callable = None

@dataclass
class IScenario:
    prompt: IPrompt
    outcomes: List[IScenarioOutcome]
    model: Any = None

def prompt(prompt: IPrompt, premessage: str = None):
    if prompt.image:
        os.system(f"timg {prompt.image.src} -m a24h -s {prompt.image.width} -r {prompt.image.reduce_colorset}")
    if premessage is not None:
        print(premessage)
    if prompt.options:
        return prompt.dtype(questionary.select(
            prompt.text.message,
            choices=prompt.options
        ).ask())
    elif prompt.hidden:
        return prompt.dtype(questionary.password(
            prompt.text.message
        ).ask())
    else:
        return prompt.dtype(questionary.text(
            prompt.text.message
        ).ask())

def run(scenario: IScenario, premessage: str = None) -> IScenario:
    answer = prompt(scenario.prompt, premessage)
    outcomes = scenario.outcomes
    next, max_score = None, float('-inf')
    answer_embedding = model.encode(answer, convert_to_tensor=True)
    for outcome in outcomes:
        score = max([ util.cos_sim(model.encode(example, convert_to_tensor=True), answer_embedding)[0][0] for example in outcome.examples ])
        if score > max(0.5, max_score):
            next = outcome
            max_score = score
    os.system('cls' if os.name == 'nt' else 'clear')
    if next is None:
        run(scenario, "You are unable to do that.")
    else:
        if next.exec is not None:
            next.exec()
        if next.scenario:
            run(next.scenario, next.message)
        elif next.message:
            print(next.message)
