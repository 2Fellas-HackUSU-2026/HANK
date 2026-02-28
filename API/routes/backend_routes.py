from fastapi import APIRouter
from tools.backend_route_tools import add_hazards, add_controls, get_user_topic
from tools.save_data import save_new_action, save_new_hazard, save_new_controls

router = APIRouter()

@router.post("/api/add-hazard")
def new_hazards(topic: str, action: str):
    hazard_list = add_hazards(topic=topic, action=action)

    for hazard in hazard_list:
        save_new_hazard(action_step= action, single_hazard=hazard )

    return {"hazard_list": hazard_list}


@router.post("/api/add-control")
def new_controls(topic: str, action: str, hazard: str):
    controls_list = add_controls(topic=topic, action=action, hazard=hazard)
    save_new_controls(action_step=action, single_hazard= hazard, control_list= controls_list)

    return {"controls_list": controls_list}

@router.post("/api/set-user-topic")
def user_topic(topic: str):
    topic = get_user_topic(topic)
    return {"topic": topic}

@router.post("/api/add-action-step")
def new_step(action: str):
    action_entry = save_new_action(action)
    return {"action": action_entry}
