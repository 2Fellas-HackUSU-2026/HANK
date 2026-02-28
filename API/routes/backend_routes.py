from fastapi import APIRouter
from tools.backend_route_tools import add_hazards, add_controls, get_user_topic, add_action, suggest_actions

router = APIRouter()

@router.post("/api/add-hazard")
def new_hazards(topic: str, action: str, num_hazards: int = 5):
    hazard_list = add_hazards(topic=topic, action=action, num_hazards=num_hazards)
    return {"hazard_list": hazard_list}


@router.post("/api/add-control")
def new_controls(topic: str, action: str, hazard: str, num_controls: int = 3):
    controls_list = add_controls(topic=topic, action=action, hazard=hazard, num_controls=num_controls)
    return {"controls_list": controls_list}

@router.post("/api/set-user-topic")
def user_topic(topic: str):
    topic = get_user_topic(topic)
    return {"topic": topic}

@router.post("/api/add-action-step")
def new_step(action: str):
    action = add_action(action)
    return {"action": action}

@router.post("/api/suggest-actions")
def get_suggested_actions(topic: str):
    actions_list = suggest_actions(topic=topic)
    return {"actions_list": actions_list}