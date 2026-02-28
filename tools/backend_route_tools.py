from openai import OpenAI
from pydantic import BaseModel, Field

def add_hazard(topic: str, action: str):
    """
    Prompts the agent to come up with hazards associated with the action param. Use topic param as context to decide with what lens to view the problem at hand. 

    :param topic: User's topic/job description.
    :type topic: str
    :param action: The action for which hazards are to be found.
    :type action: str

    :return hazards: returns a list of hazards associated with the `action`
    :return type: list
    """

    prompt = f"as an expert with {topic}, your job is to come up with a well thought out list of hazards that might be associated with {action}. The hazards you come up with should be relavent to the {action}. You should give the hazards as a list."

    #agent.invoke()
    hazards = []
    return hazards

def add_control(topic: str, action: str, hazard):
    """
    Prompts the agent to come up with controls associated with the hazrad. it should use the `topic` as context to decide with what lens to view the problem at hand, and it should use the `action` to make sure the controls are reasonable.  

    :param topic: User's topic/job description.
    :type topic: str
    :param action: The action for which hazards are to be found.
    :type action: str

    :return hazards: returns a list of hazards associated with the `action`
    :return type: list
    """

    prompt = f"""
    as an expert with {topic}, your job is to come up with a well thought out list of both engineering, adminstrative controls to mitigate the risks that might be associated with {hazard}. The controls you come up with should be relavent to the {action} while mitigating the risks of the {hazard}. 

    You should provide your findings as a list.
    """

    #agent.invoke()
    controls = []
    return controls
    
