from fastapi import APIRouter
from tools.backend_route_tools import add_hazards, add_controls, get_user_topic, add_action

router = APIRouter()

@router.post("/api/add-hazard")
def new_hazards(topic: str, action: str):
    hazard_list = add_hazards(topic=topic, action=action)
    return {"hazard_list": hazard_list}


@router.post("/api/add-control")
def new_controls(topic: str, action: str, hazard: str):
    controls_list = add_controls(topic=topic, action=action, hazard=hazard)
    return {"controls_list": controls_list}

@router.post("/api/set-user-topic")
def user_topic(topic: str):
    topic = get_user_topic(topic)
    return {"topic": topic}

@router.post("/api/add-action-step")
def new_step(action: str):
    action = add_action(action)
    return {"action": action}