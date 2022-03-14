import asyncio

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/{identifier}")
async def root(identifier: int):
    """ This simulates a webservice that takes roughly 0.1s to respond
    """
    # await asyncio.sleep(0.01)
    return {"message": f"Hello! You sent me {identifier}", "value": identifier}

if __name__ == "__main__":
    uvicorn.run(app='webserver:app')
