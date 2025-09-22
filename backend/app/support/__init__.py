from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_support_dashboard():
    return {"message": "Support Dashboard"}
