from typing import Optional, Literal
from pydantic import BaseModel, constr

class SearchParams(BaseModel):
    q: constr(min_length=1)
    type: Optional[Literal["products", "services", "all"]] = "all"
    page: Optional[int] = 1
    limit: Optional[int] = 10

