import asyncio
from fastapi import FastAPI,WebSocket

from pydantic_models.chat_body import ChatBody
from services.llm_service import LLMService
from services.source_sorting_service import SourceSorting
from services.web_search_service import SearchService

app = FastAPI()

search_service = SearchService()
sort_service = SourceSorting()
llm_service = LLMService()

@app.get("/")
def splash():
    return "Chal chutiye"

@app.get("/category")
def get_category():
    return {
        "status": 200,
        "data":"true",
        "category":{
            "one":"one",
            "one":"one",
            "one":"one",
        }
    }

@app.websocket("/ws/chat")
async def chat_websocket(websocket: WebSocket):
    await websocket.accept()

    try:
         
         await asyncio.sleep(0.1)
         data = await websocket.receive_json()
         query = data.get("query")
         webres = search_service.web_search(query)
         await asyncio.sleep(0.1)
         await websocket.send_json({
             "type":"web result",
             "data": webres
         })
         # sortres = sort_service.sort_source(webres) 
         llmres = llm_service.generate_response(query,webres)
         
         for chunk in llmres:
             await asyncio.sleep(0.1)
             await websocket.send_json({
                 "type":"content",
                 "data":chunk
                 }
                 )
    
    except:
        print("no idea what happened")
    finally:
       await websocket.close()

@app.post("/chat")
def chat_endpoint(body: ChatBody):
    webres = search_service.web_search(body.query)
    # sortres = sort_service.sort_source(webres) 
    llmres = llm_service.generate_response(body.query,webres)
    return {
        "status":"success",
        "request-data":body.query,
        'response-data':llmres}