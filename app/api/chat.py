from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.agents.orchestrator import process_query
from app.database.client import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.security.authentication import get_current_user

router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Natural language SOC investigation endpoint.
    """

    return process_query(
        request.query,
        db,
    )