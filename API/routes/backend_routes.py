from fastapi import APIRouter
from tools.backend_route_tools import add_hazards, add_controls, get_user_topic
from tools.save_data import save_new_action, save_new_hazard, save_new_controls

router = APIRouter()

@router.post("/api/add-hazard")
def new_hazards(topic: str, action: str):
    """
    Generate hazards for an action and persist each hazard under that action.

    This endpoint uses the AI hazard-generation helper to produce a list of
    hazards relevant to the provided job context (`topic`) and action step
    (`action`). Every generated hazard is then saved to `actions_storage.json`
    via `save_new_hazard`, creating the action entry first if it does not exist.

    Args:
        topic: The user-provided job/topic context used to frame hazard generation.
        action: The action step for which hazards should be generated.

    Returns:
        dict: JSON payload with key `hazard_list`, containing the generated list
        of hazard strings.
    """
    hazard_list = add_hazards(topic=topic, action=action)

    for hazard in hazard_list:
        save_new_hazard(action_step= action, single_hazard=hazard )

    return {"hazard_list": hazard_list}


@router.post("/api/add-control")
def new_controls(topic: str, action: str, hazard: str):
    """
    Generate controls for a hazard and persist them under the action/hazard pair.

    This endpoint uses the AI controls-generation helper to create control
    recommendations for the specified hazard in the context of the given topic
    and action. The generated controls are then merged into storage with
    `save_new_controls`, avoiding duplicate control strings.

    Args:
        topic: The user-provided job/topic context for control generation.
        action: The action step associated with the hazard.
        hazard: The specific hazard to mitigate with controls.

    Returns:
        dict: JSON payload with key `controls_list`, containing the generated
        list of control strings.
    """
    controls_list = add_controls(topic=topic, action=action, hazard=hazard)
    save_new_controls(action_step=action, single_hazard= hazard, control_list= controls_list)

    return {"controls_list": controls_list}

@router.post("/api/set-user-topic")
def user_topic(topic: str):
    """
    Echo and validate the user's selected topic context.

    This route currently passes the topic through `get_user_topic` and returns
    it directly. It is primarily used by the frontend to set or confirm the
    active topic context before requesting hazards/controls.

    Args:
        topic: The job/topic description supplied by the user.

    Returns:
        dict: JSON payload with key `topic` containing the resolved topic string.
    """
    topic = get_user_topic(topic)
    return {"topic": topic}

@router.post("/api/add-action-step")
def new_step(action: str):
    """
    Persist a new action step in storage if it does not already exist.

    The action is written to `actions_storage.json` through `save_new_action`.
    If the action already exists, the existing action entry is returned without
    creating duplicates.

    Args:
        action: The action step text to create or look up.

    Returns:
        dict: JSON payload with key `action`, containing the stored action entry
        in the format `{"action": <str>, "hazards": <list>}`.
    """
    action_entry = save_new_action(action)
    return {"action": action_entry}
