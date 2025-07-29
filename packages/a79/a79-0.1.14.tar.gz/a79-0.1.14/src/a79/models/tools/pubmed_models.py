from pydantic import BaseModel

from common_py.connector.tap_pubmed.models import ArticleRecord
from external.a79.src.models.tools import ToolOutput


class GetArticlesInput(BaseModel):
    feed_url: str
    limit: int = 15


class GetArticlesOutput(ToolOutput):
    articles: list[ArticleRecord]
