from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
import uuid
import time

def router() -> APIRouter:
    app = APIRouter()

    class Message:
        def __init__(self, sender:str, content:str) -> None:
            self.id = str(uuid.uuid4())
            self.epoch = time.time()
            self.sender = sender
            self.content = content

    class RequestMessage:
        def __init__(self, method:str, path:str, headers:dict[str, str], body:str) -> None:
            self.id = str(uuid.uuid4())
            self.epoch = time.time()
            self.method = method
            self.path = path
            self.headers = headers
            self.body = body

    messages:list[Message] = []
    requests:list[RequestMessage] = [] 

    @app.post("/messages/{sender:str}/send")
    async def print_content(sender:str, request:Request):
        text = (await request.body()).decode()
        message = Message(sender, text)
        messages.append(message)
        return message.id

    @app.get("/messages/")
    async def get_messages(sender:str = None, page_number:int = 1, page_size:int = 10):
        begin = ((page_number-1) * page_size)
        end = begin + page_size
        items = [i for i in reversed([f"{i.id} @at {i.epoch}: {i.sender} -> {i.content}" for i in messages if i.sender == sender or sender is None])]
        return items[begin:end]
    
    @app.get("/messages/{id:str}")
    async def get_message(id:str):
        candidates = [i for i in messages if i.id == id]
        if candidates:
            return candidates[0]
        else:
            raise HTTPException(404, f"message: {id} not found")
        
    @app.get("/requests/")
    async def get_requests(page_number:int = 1, page_size:int = 10):
        begin = ((page_number-1) * page_size)
        end = begin + page_size
        return requests[begin:end]
        
    @app.get("/requests/{id:str}")
    async def get_request(id:str):
        candidates = [i for i in requests if i.id == id]
        if candidates:
            return candidates[0]
        else:
            raise HTTPException(404, f"request: {id} not found")

    all_path = "/requests/{path:path}"

    @app.get(all_path)
    @app.post(all_path)
    @app.put(all_path)
    @app.patch(all_path)
    @app.delete(all_path)
    async def send_request(path:str, request:Request):
        body = (await request.body()).decode()
        headers = {i:request.headers.get(i) for i in request.headers.keys()}
        message = RequestMessage(request.method, path, headers, body)
        requests.append(message)
        return message.id

    return app