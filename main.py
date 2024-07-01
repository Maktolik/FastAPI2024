import uvicorn

from fastapi import FastAPI

from items_views import router as items_router
from users.views import router as users_router


app = FastAPI()
app.include_router(items_router, tags=["Items"])
app.include_router(users_router, tags=["Users"])


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/hello/")
def say_hello(name: str = "world"):
    name = name.title()
    return {"message": f"Hello {name}"}


@app.post("/calc/add/")
def add(a: int, b: int):
    return {
        "a": a,
        "b": b,
        "result": a + b,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
