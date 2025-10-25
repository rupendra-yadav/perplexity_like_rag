from fastapi import FastAPI

from pydantic_models.chat_body import ChatBody
from services.source_sorting_service import SourceSorting
from services.web_search_service import SearchService

app = FastAPI()

search_service = SearchService()
sort_service = SourceSorting()

@app.get("/")
def splash():
    return "Chal chutiye"

@app.post("/chat")
def chat_endpoint(body: ChatBody):
    webres = search_service.web_search(body.query)
    sortres = sort_service.sort_source(webres) 
    return {
        "status":"kanda",
        "request-data":body.query,
        'response-data':sortres}