import time
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class safeRequest(BaseModel):
    input_data: str

class safeResponse(BaseModel):
    result: str
    attempts: int
    time_taken: float


@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/crack-safe", response_model=safeResponse)
def crack_safe(request: safeRequest):
    start_time = time.perf_counter()  
    numGuess = 0

    guess = ""

    def backtrack(guess):
        nonlocal numGuess
        if len(guess) == 10 and guess == request.input_data:
            return guess  
        
        for i in range(10):
            add_digit = guess + str(i)
            numGuess += 1  
            if request.input_data.startswith(add_digit):
                result = backtrack(add_digit)
                if result is not None:
                    return result

    result = backtrack(guess)
    end_time = time.perf_counter()  
    execution_time = (end_time - start_time) * 1000

    return {"result": result, "attempts": numGuess, "time_taken": round(execution_time, 4)}
