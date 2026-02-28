import json 
from pathlib import Path

ACTION_STORAGE = Path(__file__).resolve().parent.parent / "data" / "actions_storage.json"


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

def save_new_action(action_step: str) -> dict:
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

def save_new_hazard(action_step: str, single_hazard: str) -> dict:
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

def save_new_controls(action_step: str, single_hazard: str, control_list: list[str]) -> dict:
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