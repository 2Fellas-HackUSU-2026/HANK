from fastapi import APIRouter

router = APIRouter()

@router.post("/api/add-hazard")
def add_hazard(topic: str, action: str):
    pass 

@router.post("/api/add-control")
def add_control(topic: str, action: str, hazard: str):
    pass
