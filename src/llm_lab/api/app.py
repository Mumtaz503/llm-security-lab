import logging
from fastapi import FastAPI, HTTPException
from llm_lab.models import QueryRequest
from llm_lab.logging_setup import config_logging
from llm_lab.providers import get_provider
from llm_lab.providers.base import ProviderError

config_logging()
logger = logging.getLogger("llm_lab.api.app")


app = FastAPI()


def build_msg(question: str):
    return [
        {"role": "system", "content": "You are a helpful assistant. Answer Briefly."},
        {"role": "user", "content": question},
    ]


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/v1/query")
async def query(request: QueryRequest):
    provider = (
        request.provider or ""
    ).strip() or "mock"  # missing or blank provider defaults to mock
    try:
        provider = get_provider(provider)
    except ProviderError as e:
        raise HTTPException(status_code=400, detail=str(e))

    logger.info(
        "request.start provider=%s question_len=%d",
        provider.name,
        len(request.question),
    )

    try:
        completion = provider.complete(
            build_msg(request.question), timeout=request.timeout or 30 # placeholder timeout
        )
    except ProviderError as e:
        raise HTTPException(status_code=500, detail=str(e))

    logger.info(
        "request.complete provider=%s answer_len=%d",
        provider.name,
        len(completion.content),
    )

    return {"content": completion.content, "provider": completion.provider}
