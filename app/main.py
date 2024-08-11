from fastapi import FastAPI, Request
from app.routers import category, products, auth, permission, reviews
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import time
from loguru import logger
from uuid import uuid4
from fastapi.responses import JSONResponse

# class TimingMiddleware:
#     def __init__(self, app):
#         self.app = app
#
#     async def __call__(self, scope, receive, send):
#         start_time = time.time()
#         await self.app(scope, receive, send)
#         duration = time.time() - start_time
#         print(f"Request duration: {duration:.10f} seconds")


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="7UzGQS7woBazLUtVQJG39ywOP7J7lkPkB0UmDhMgBR8=")
# app.add_middleware(TimingMiddleware)
logger.add("info.log", format="Log: [{extra[log_id]}:{time} - {level} - {message} ", level="INFO", enqueue = True)


@app.middleware("http")
async def log_middleware(request: Request, call_next):
    log_id = str(uuid4())
    with logger.contextualize(log_id=log_id):
        try:
            response = await call_next(request)
            if response.status_code in [401, 402, 403, 404]:
                logger.warning(f"Request to {request.url.path} failed")
            else:
                logger.info('Successfully accessed ' + request.url.path)
        except Exception as ex:
            logger.error(f"Request to {request.url.path} failed: {ex}")
            response = JSONResponse(content={"success": False}, status_code=500)
        return response


# origins = [
#     "http://localhost:3000",
#     "https://example.com",
#     "null"
# ]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods='*',
#     allow_headers='*'
# )


@app.get("/{name}")
async def main_page(name):
    logger.info("Hello from the root path")
    hello_world()
    return {"message": f"Hello {name}"}

def hello_world():
    logger.info("hello() called!")


# @app.middleware('http')
# async def modify_request_response_middleware(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     duration = time.time() - start_time
#     print(f"Request duration: {duration:.10f} seconds")
#     return response

@app.get("/")
async def welcome() -> dict:
    return {"message": "My e-commerce app"}


@app.get("/create_session")
async def session_set(request: Request):
    request.session["my_session"] = "1234"
    return 'ok'

@app.get("/read_session")
async def session_info(request: Request):
    my_var = request.session.get("my_session")
    return my_var

@app.get("/delete_session")
async def session_delete(request: Request):
    my_var = request.session.pop("my_session")
    return my_var


@app.get("/hello")
async def greeter():
    return {"Hello": "World"}


@app.get("/goodbye")
async def farewell():
    return {"Goodbye": "World"}


app.include_router(category.router)
app.include_router(products.router)
app.include_router(auth.router)
app.include_router(permission.router)
app.include_router(reviews.router)


# uvicorn app.main:app --reload

