from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from tools.perplexity import call_perplexity

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def ping():
    return {"status": "ok"}

@app.get("/sse")
async def handle_tool_get(request: Request):
    try:
        # For GET requests, we'll use query parameters
        tool_name = request.query_params.get("name", "")
        prompt = request.query_params.get("prompt", "")

        if tool_name == "get_perplexity_answer":
            if not prompt:
                return JSONResponse(
                    content={"error": "Prompt is required"},
                    status_code=400
                )
            
            result = call_perplexity(prompt)

            def event_stream():
                yield f"data: {result}\n\n"

            return EventSourceResponse(event_stream())
        
        return JSONResponse(
            content={"error": f"Tool '{tool_name}' not found"},
            status_code=404
        )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

@app.post("/sse")
async def handle_tool_post(request: Request):
    try:
        body = await request.json()
        tool = body.get("tool", {})
        name = tool.get("name")
        input_data = tool.get("input", {})

        if name == "get_perplexity_answer":
            prompt = input_data.get("prompt", "")
            if not prompt:
                return JSONResponse(
                    content={"error": "Prompt is required"},
                    status_code=400
                )
            
            result = call_perplexity(prompt)

            def event_stream():
                yield f"data: {result}\n\n"

            return EventSourceResponse(event_stream())
        
        return JSONResponse(
            content={"error": f"Tool '{name}' not found"},
            status_code=404
        )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )
