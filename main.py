from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse
from tools.perplexity import call_perplexity

app = FastAPI()

@app.get("/")
def ping():
    return {"status": "ok"}

@app.post("/sse")
async def handle_tool(request: Request):
    body = await request.json()
    tool = body.get("tool", {})
    name = tool.get("name")
    input_data = tool.get("input", {})

    if name == "get_perplexity_answer":
        prompt = input_data.get("prompt", "")
        result = call_perplexity(prompt)

        def event_stream():
            yield f"data: {result}\n\n"

        return EventSourceResponse(event_stream())
    
    return JSONResponse(content={"error": "Tool not found"}, status_code=404)
