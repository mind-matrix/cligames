import os
from src.player import PlayVideo
from src.prompt import IScenario, IScenarioOutcome, IPrompt, IPromptText, IPromptImage, run

def play_ending():
    PlayVideo("eXit (Press Q to quit)", "assets/end.mp4")

ending_1 = IScenario(
    IPrompt(
        IPromptText("Congratulations, you're heading to a new world! Do you want to play again?", color="cyan"),
        image=IPromptImage(
            "assets/6.png",
            reduce_colorset=24
        )
    ),
    [
        IScenarioOutcome(
            ["yes", "play", "okay", "again", "sure", "why not", "do it"],
            None
        ),
        IScenarioOutcome(
            ["no", "not again", "never", "nope", "definitely not"],
            None,
            "Thank you for playing"
        )
    ]
)

scenario_1_1_1_2_1 = IScenario(
    IPrompt(
        IPromptText("In the water you see a boat. What do you do?", color="cyan"),
        image=IPromptImage(
            "assets/5.jpg"
        )
    ),
    [
        IScenarioOutcome(
            ["board it", "get on it", "get on the boat", "go aboard"],
            ending_1
        )
    ]
)

scenario_1_1_1_2 = IScenario(
    IPrompt(
        IPromptText("You crawl through the tunnel and the tunnel leads you to a beach. What do you do?"),
        image=IPromptImage(
            "assets/3.png"
        )
    ),
    [
        IScenarioOutcome(
            ["look around","look","walk into the beach"],
            scenario_1_1_1_2_1
        ),
        IScenarioOutcome(
            ["go back into the tunnel", "turn back", "go back"],
            None,
            "You try going back but the tunnel has collapsed in on itself."
        )
    ]
)
scenario_1_1_1_2.outcomes[1].scenario = scenario_1_1_1_2

scenario_1_1_1 = IScenario(
    IPrompt(
        IPromptText("You start to escape but your friend is too weak to go with you.\nThey hand you a note. What do you do?", color="cyan"),
        image=IPromptImage(
            "assets/4.png"
        )
    ),
    [
        IScenarioOutcome(
            ["read it","read note","read the note"],
            None,
            "It is too dark to read the note."
        ),
        IScenarioOutcome(
            ["light a match","light a fire","hold a lamp","use a flashlight"],
            None,
            "You do not have a matchstick, a lamp or any lighter"
        ),
        IScenarioOutcome(
            ["leave", "exit tunnel", "leave my friend"],
            scenario_1_1_1_2
        )
    ]
)
scenario_1_1_1.outcomes[0].scenario = scenario_1_1_1
scenario_1_1_1.outcomes[1].scenario = scenario_1_1_1

scenario_1_1 = IScenario(
    IPrompt(
        IPromptText("The barrel rolls aside and you find a secret tunnel. What do you do?", color="cyan"),
        image=IPromptImage(
            "assets/2.png"
        )
    ),
    [
        IScenarioOutcome(
            ["enter tunnel","go into tunnel","go inside","enter it"],
            scenario_1_1_1
        ),
        IScenarioOutcome(
            ["sit besides my friend", "sit with him"],
            None
        )
    ]
)

scenario_1_2_1 = IScenario(
    IPrompt(
        IPromptText("The note says, \"Don't leave me here.\" Do you leave your friend or stay?", color="cyan"),
        image=IPromptImage(
            "assets/7.jpg"
        )
    ),
    [
        IScenarioOutcome(
            ["leave him", "leave her", "exit", "move on", "don't stay", "can't stay", "won't stay", "do not stay", "leave my friend"],
            scenario_1_1_1_2
        ),
        IScenarioOutcome(
            ["stay with your friend", "don't leave", "do not leave", "stay", "sit besides my friend"],
            exec=play_ending
        )
    ]
)

scenario_1_2 = IScenario(
    IPrompt(
        IPromptText("Your friend hands you a note. What do you do?", color="cyan"),
        image=IPromptImage(
            "assets/4.png"
        )
    ),
    [
        IScenarioOutcome(
            ["read it","read note","read the note", "light a match","light a fire","hold a lamp","use a flashlight"],
            scenario_1_2_1
        ),
        IScenarioOutcome(
            ["leave", "leave my friend", "throw it away", "enter tunnel"],
            scenario_1_1_1
        )
    ]
)

start = IScenario(
    IPrompt(
        IPromptText("You are trapped in a dungeon with your friend. You see a barrel. What do you do?", color="cyan"),
        image=IPromptImage(
            "assets/1.png"
        )
    ),
    [
        IScenarioOutcome(
            ["move barrel","remove barrel","push barrel","roll barrel"],
            scenario_1_1
        ),
        IScenarioOutcome(
            ["sit besides my friend", "sit with him", "sit down next to my friend"],
            scenario_1_2
        ),
    ]
)

scenario_1_1.outcomes[1].scenario = scenario_1_2
ending_1.outcomes[0].scenario = start

os.system('cls' if os.name == 'nt' else 'clear')
run(start)