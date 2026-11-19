from fastapi import APIRouter,HTTPException

from backend.app.routers.chat import CURRENT_USER
from backend.app.services import db
from backend.app.services.db.crud import add_flashcard
from .models import FlashCardsRequest,FlashCardsResponse
from backend.app.services.flashcard import generate_flashcard
from backend.app.services.ai import AIServiceError
from backend.app.services.errors import ai_error_http
router = APIRouter(prefix="/flashcard",tags=["flashcards"])

@router.post("/",response_model=FlashCardsResponse)
def flashcard(request:FlashCardsRequest):
    flashcard_id,conversation_id = add_flashcard(db,CURRENT_USER,request.topic,request.number_flashcards)
    print(conversation_id)
    try:
        clean_topic = request.topic.strip()
        response = generate_flashcard(clean_topic,request.number_flashcards)
    except AIServiceError as error:
        raise ai_error_http(error)
    return FlashCardsResponse(
        answer = response["answer"],
        model = response["model"],
        tokens_used = response["tokens_used"]
    )