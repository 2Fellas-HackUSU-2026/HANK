import json 
from pathlib import Path

ACTION_STORAGE = Path(__file__).resolve().parent.parent / "data" / "actions_storage.json"


###This is for saving data to json

def _normalize_hazard_entry(hazard_entry: dict) -> dict | None:
    hazard = hazard_entry.get("hazard")
    controls = hazard_entry.get("controls", [])

    if not isinstance(hazard, str) or not hazard.strip():
        return None

    if not isinstance(controls, list):
        controls = []

    normalized_controls = [control for control in controls if isinstance(control, str) and control.strip()]
    return {"hazard": hazard, "controls": normalized_controls}


def _normalize_action_entry(action_entry: dict) -> dict | None:
    action = action_entry.get("action")
    hazards = action_entry.get("hazards", [])

    # Backward compatibility: repair accidentally nested action objects.
    if isinstance(action, dict):
        action = action.get("action")

    if not isinstance(action, str) or not action.strip():
        return None

    if not isinstance(hazards, list):
        hazards = []

    normalized_hazards: list[dict] = []
    for hazard_entry in hazards:
        if not isinstance(hazard_entry, dict):
            continue
        normalized = _normalize_hazard_entry(hazard_entry)
        if normalized is None:
            continue
        normalized_hazards.append(normalized)

    return {"action": action, "hazards": normalized_hazards}

def load_actions() -> list[dict]:
    if not ACTION_STORAGE.exists() or ACTION_STORAGE.stat().st_size == 0:
        return []

    try:
        with open(ACTION_STORAGE, "r", encoding="utf-8") as f:
            data = json.load(f)

            if not isinstance(data, list):
                return []

            merged_by_action: dict[str, dict] = {}
            normalized_data: list[dict] = []

            for action_entry in data:
                if not isinstance(action_entry, dict):
                    continue

                normalized_action = _normalize_action_entry(action_entry)
                if normalized_action is None:
                    continue

                action_key = normalized_action["action"]
                existing_action = merged_by_action.get(action_key)
                if existing_action is None:
                    merged_by_action[action_key] = normalized_action
                    normalized_data.append(normalized_action)
                    continue

                existing_hazards = existing_action.setdefault("hazards", [])
                for hazard_entry in normalized_action["hazards"]:
                    existing_hazard = next(
                        (h for h in existing_hazards if h.get("hazard") == hazard_entry["hazard"]),
                        None,
                    )
                    if existing_hazard is None:
                        existing_hazards.append(hazard_entry)
                        continue

                    controls = existing_hazard.setdefault("controls", [])
                    for control in hazard_entry.get("controls", []):
                        if control not in controls:
                            controls.append(control)

            return normalized_data
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
