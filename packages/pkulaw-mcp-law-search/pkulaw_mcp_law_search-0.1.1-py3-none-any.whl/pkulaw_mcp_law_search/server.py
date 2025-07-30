import os
from typing import Annotated, List

from pydantic import Field, BaseModel

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

import requests


API_KEY = os.getenv('PKULAW_API_KEY') or os.getenv('API_KEY')

API_URL = os.getenv('API_URL', 'https://test-apim-gateway.pkulaw.com/fabao-ai-open-search')
API_TIMEOUT = int(os.getenv('API_TIMEOUT', '20'))

API_HEADERS = {}
if API_KEY:
    API_HEADERS["Authorization"] = f"Bearer {API_KEY}"

SIZE = int(os.getenv('SIZE', '3'))
PORT = int(os.getenv('PORT', '3000'))


mcp = FastMCP(name="pkulaw-law-search")


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse("OK")


class SearchResult(BaseModel):
    title: str = Field(description="title of law")
    content: str = Field(description="content of law, the matched part")
    url: str = Field(description="url of law in pkulaw.com, for details")


@mcp.tool()
def search(
    query: Annotated[
        str,
        Field(
            description=f"query for law search, can be keywords or text for semantic search using embeddings"
        ),
    ],
) -> List[SearchResult]:
    """Semantic search of law content, using embeddings."""
    req = {
        "query": query,
        "page_size": SIZE,
        "kg_base": "law",
        "rerank": True,
    }

    resp = requests.post(
        url=API_URL,
        json=req,
        headers=API_HEADERS,
        timeout=API_TIMEOUT,
    )

    if resp.status_code != 200:
        result = resp.json()
        msg = result.get('message') or ''
        raise ValueError(f'fail to search: {msg}')

    search_results = []
    results = resp.json()
    
    for result in results:
        meta = result.get('metadata') or {}
        r = SearchResult(
            title=meta.get('title'),
            content=result['page_content'],
            url=meta.get('source')
        )
        search_results.append(r)

    return search_results


def serve_stdio():
    mcp.run()


def serve_streamable_http():
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=PORT,
    )


