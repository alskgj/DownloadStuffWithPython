from fastapi import FastAPI
import uvicorn
import random
import time
import asyncio

app = FastAPI()


@app.get("/random/{identifier}")
async def root(identifier: int):
    """ This simulates a webservice that takes some time to respond
    """
    await asyncio.sleep(random.randint(0, 3))
    return {"message": f"Hello! You sent me {identifier}", "value": identifier}


@app.get("/{identifier}")
async def root(identifier: int):
    """ This simulates a webservice that takes exactly 1s to respond
    """
    await asyncio.sleep(1)
    return {"message": f"Hello! You sent me {identifier}", "value": identifier}


if __name__ == "__main__":
    uvicorn.run(app)
