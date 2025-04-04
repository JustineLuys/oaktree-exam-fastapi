from fastapi import FastAPI
from database import Base, engine
from routers import api, signup, signin
app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}

app.include_router(signin.router)
app.include_router(signup.router)
app.include_router(api.router)