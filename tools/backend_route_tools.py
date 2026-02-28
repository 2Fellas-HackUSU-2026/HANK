from openai import OpenAI
from pydantic import BaseModel, Field
from agent.agent import agent
import json 
from pathlib import Path



ACTION_STORAGE = Path(__file__).resolve().parent.parent / "data" / "actions_storage.json"


class HazardResponse(BaseModel):
    hazards: list[str]

class ControlReponse(BaseModel):
    controls: list[str]
    

def add_hazards(topic: str, action: str):
    """
    Prompts the agent to come up with hazards associated with the action param. Use topic param as context to decide with what lens to view the problem at hand. 

    :param topic: User's topic/job description.
    :type topic: str
    :param action: The action for which hazards are to be found.
    :type action: str

    :return hazards: returns a list of hazards associated with the `action`
    :return type: list
    """

    prompt = f"As an expert with {topic}, your job is to come up with a well thought out list of hazards that might be associated with {action}. Your hazards should be writen in 2-4 words."
    query = f"What is a list of 5 to 10 hazards when performing {action}"

    hazards = agent(system_prompt= prompt, query= query, return_format= HazardResponse)
    
    return hazards.hazards

def add_controls(topic: str, action: str, hazard):
    """
    Prompts the agent to come up with controls associated with the hazrad. it should use the `topic` as context to decide with what lens to view the problem at hand, and it should use the `action` to make sure the controls are reasonable.  

    :param topic: User's topic/job description.
    :type topic: str
    :param action: The action, provides increased context when finding controls.
    :type action: str
    :param hazard: The hazard for which controls should be created.
    :type hazard: str

    :return controls: returns a list of controls associated with the `hazard`
    :return type: list
    """

    prompt = f"""
    As an expert with {topic}, your job is to come up with a well thought out list of both engineering, adminstrative controls to mitigate the risks that might be associated with {hazard}. The controls you come up with should be relavent to the {action} while mitigating the risks of the {hazard}. The control should be written in less than 12 words.
    """
    query = f"What is a list of 1 to 8 controls to mitgate the {hazard}"

    controls = agent(system_prompt= prompt, query= query, return_format= ControlReponse)

    return controls.controls
    
def get_user_topic(topic: str):
    topic = topic
    return topic

def add_action(action_step: str):
    action = action_step

    action_dict = {"action": {"action": action}}

    
    return action


###This is for saving data to json

def load_actions() -> list[dict]:
    if not ACTION_STORAGE.exists() or ACTION_STORAGE.stat().st_size == 0:
        return []

    try:
        with open(ACTION_STORAGE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []
    
def save_actions(data: list[dict]) -> None:
    ACTION_STORAGE.parent.mkdir(parents=True, exist_ok=True)
    with open(ACTION_STORAGE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def find_action(data: list[dict], action_step: str) -> dict | None:
    return next((item for item in data if item.get("action") == action_step), None)

def add_action(action_step: str) -> dict:
    """
    Step 1: add action only.
    Creates: {"action": <action_step>, "hazards": []}
    """
    data = load_actions()
    action_entry = find_action(data, action_step)

    if action_entry is None:
        action_entry = {"action": action_step, "hazards": []}
        data.append(action_entry)
        save_actions(data)

    return action_entry

def add_hazard(action_step: str, single_hazard: str) -> dict:
    """
    Step 2: add one hazard under an existing action.
    Creates hazard object: {"hazard": <single_hazard>, "controls": []}
    """
    data = load_actions()
    action_entry = find_action(data, action_step)

    if action_entry is None:
        action_entry = {"action": action_step, "hazards": []}
        data.append(action_entry)

    hazards = action_entry.setdefault("hazards", [])
    hazard_entry = next((h for h in hazards if h.get("hazard") == single_hazard), None)

    if hazard_entry is None:
        hazard_entry = {"hazard": single_hazard, "controls": []}
        hazards.append(hazard_entry)
        save_actions(data)

    return hazard_entry

def add_controls(action_step: str, single_hazard: str, control_list: list[str]) -> dict:
    """
    Step 3: add controls to a specific hazard under an action.
    """
    data = load_actions()
    action_entry = find_action(data, action_step)

    if action_entry is None:
        action_entry = {"action": action_step, "hazards": []}
        data.append(action_entry)

    hazards = action_entry.setdefault("hazards", [])
    hazard_entry = next((h for h in hazards if h.get("hazard") == single_hazard), None)

    if hazard_entry is None:
        hazard_entry = {"hazard": single_hazard, "controls": []}
        hazards.append(hazard_entry)

    existing_controls = hazard_entry.setdefault("controls", [])
    for control in control_list:
        if control not in existing_controls:
            existing_controls.append(control)

    save_actions(data)
    return hazard_entry