import asyncio

import asyncpg
import os
import uvicorn
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.routing import Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from starlette.responses import JSONResponse

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'])
]

routes = [
    Mount('/static', StaticFiles(directory='app/static'), name='static')
]

templates = Jinja2Templates(directory='app/templates')


async def startup():
    global conn
    print("connect")
    conn = await asyncpg.connect(
        "postgres://mxqkomkc:w2w1BetfK154mVvEMfJpuNGAYyqlzVyo@john.db.elephantsql.com:5432/mxqkomkc")

app = Starlette(middleware=middleware, on_startup=[startup], routes=routes, debug=True)



@app.route("/")
async def proc_hom(request: Request):
    return templates.TemplateResponse('index.html',
                                      {'request': request})

@app.route("/villa", methods=['GET'])
async def proc_sen(request: Request):
    sentence: str = request.query_params['id']
    if not sentence:
        return JSONResponse({"error": "no id provided"}, status_code=400)
    else:
        try:
            id = int(sentence)
        except ValueError:
            return JSONResponse({"error": "id is not a number"},
                                status_code=400)
        out = await conn.fetch("SELECT * FROM villas WHERE villa_number=$1", id)
        base = []
        for val in out:
            sd = dict()
            for key, v in val.items():
                sd[key] = v
            base.append(sd)
        return templates.TemplateResponse('answer.html',{'request': request, 'data': base, 'results': len(base), 'id': id})
@app.route("/name", methods=['GET'])
async def proc_sen(request: Request):
    sentence: str = request.query_params['id']
    if not sentence:
        return JSONResponse({"error": "no id provided"}, status_code=400)
    else:
        try:
            id = str(sentence)
        except ValueError:
            return JSONResponse({"error": "id is not a name"},
                                status_code=400)
        out = await conn.fetch("SELECT * FROM villas WHERE member_name=$1", id)
        base = []
        for val in out:
            sd = dict()
            for key, v in val.items():
                sd[key] = v
            base.append(sd)
        return templates.TemplateResponse('answer.html',{'request': request, 'data': base, 'results': len(base), 'id': id})



if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=os.getenv("PORT", 5000))
