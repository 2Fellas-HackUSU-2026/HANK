from openai import OpenAI
from pydantic import BaseModel, Field
from agent.agent import agent

class HazardResponse(BaseModel):
    hazards: list[str]

class ControlReponse(BaseModel):
    controls: list[str]

class ActionResponse(BaseModel):
    actions: list[str]
    

def add_hazards(topic: str, action: str, num_hazards: int = 5):
    """
    Prompts the agent to come up with hazards associated with the action param. Use topic param as context to decide with what lens to view the problem at hand. 

    :param topic: User's topic/job description.
    :type topic: str
    :param action: The action for which hazards are to be found.
    :type action: str
    :param num_hazards: The number of hazards to generate.
    :type num_hazards: int

    :return hazards: returns a list of hazards associated with the `action`
    :return type: list
    """

    prompt = f"As an expert with {topic}, your job is to come up with a well thought out list of exactly {num_hazards} hazards that might be associated with {action}. Your hazards should be writen in 2-4 words."
    query = f"What is a list of exactly {num_hazards} hazards when performing {action}"

    hazards = agent(system_prompt= prompt, query= query, return_format= HazardResponse)
    
    return hazards.hazards


def add_controls(topic: str, action: str, hazard: str, num_controls: int = 3):
    """
    Prompts the agent to come up with controls associated with the hazrad. it should use the `topic` as context to decide with what lens to view the problem at hand, and it should use the `action` to make sure the controls are reasonable.  

    :param topic: User's topic/job description.
    :type topic: str
    :param action: The action, provides increased context when finding controls.
    :type action: str
    :param hazard: The hazard for which controls should be created.
    :type hazard: str
    :param num_controls: The number of controls to generate.
    :type num_controls: int

    :return controls: returns a list of controls associated with the `hazard`
    :return type: list
    """

    prompt = f"""
    As an expert with {topic}, your job is to come up with a well thought out list of exactly {num_controls} controls (engineering, adminstrative, etc.) to mitigate the risks that might be associated with {hazard}. The controls you come up with should be relavent to the {action} while mitigating the risks of the {hazard}. The control should be written in less than 12 words.
    """
    query = f"What is a list of exactly {num_controls} controls to mitgate the {hazard}"

    controls = agent(system_prompt= prompt, query= query, return_format= ControlReponse)

    return controls.controls
    
def get_user_topic(topic: str):
    topic = topic
    return topic

def suggest_actions(topic: str):
    """
    Prompts the agent to come up with suggested actions associated with the topic param.

    :param topic: User's topic/job description.
    :type topic: str

    :return actions: returns a list of actions associated with the `topic`
    :return type: list
    """

    prompt = f"As an expert with {topic}, your job is to come up with a well thought out list of common actions or tasks that might be performed in this role. Your actions should be concise."
    query = f"What is a list of 3 to 6 common actions when working as/with {topic}?"

    actions = agent(system_prompt= prompt, query= query, return_format= ActionResponse)

    return actions.actions

def add_action(action_step: str):
    action = action_step
    return action

def add_to_json(action: str, single_hazard: str, control_list: list[str]):
    template = {"action_step": action, "hazards": {single_hazard: {"controls": [control]}} }

    new_template = {"action": action, "hazards": [{"hazard": single_hazard, "controls": control_list}]}