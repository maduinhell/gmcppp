from fastapi import HTTPException,APIRouter

from backend.app.routers.conversation import CURRENT_USER
from backend.app.services import db
from .models import QuizzResponse,QuizzRequest
from backend.app.services.ai import AIServiceError
from backend.app.services.errors import ai_error_http
from backend.app.services.quizz import generate_quizz
from backend.app.services.db.crud import add_quizz
router = APIRouter(prefix="/quizz",tags=["quizz"])
@router.post('/')
def quizz(request:QuizzRequest):
    quizz_id,conversation_id = add_quizz(db,CURRENT_USER,request.subject,request.number_quizzes,request.number_options)
    print(conversation_id)
    try:
        subject = request.subject.strip()
        number_questions = request.number_quizzes
        number_options = request.number_options
        response = generate_quizz(subject, number_questions, number_options)
    except AIServiceError as error:
        raise ai_error_http(error)
    return QuizzResponse(
        answer = response["answer"],
        model = response["model"],
        tokens_used = response["tokens_used"]
    )