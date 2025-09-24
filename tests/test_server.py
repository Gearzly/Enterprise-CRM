from fastapi import FastAPI
from app.core.crud import opportunity as crud_opportunity

app = FastAPI()

@app.get("/test")
def test():
    # Test if the method exists
    has_method = hasattr(crud_opportunity, 'get_multi')
    return {"has_method": has_method}