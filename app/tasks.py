import time
import requests
import json
from celery import Celery
from .config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

celery = Celery(
    __name__,
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND
)

@celery.task(name="generate_test_task")
def generate_test_task(request_data: dict):
    """
    Bu vazifa fonda test yaratish mantig'ini bajaradi.
    """
    try:
        print(f"Vazifa qabul qilindi: {request_data['topic']} mavzusida test yaratish.")
        
        # --- SUN'IY INTELLEKTGA MUROJAAT QILINADIGAN JOY ---
        # TODO: Bu yerga OpenAI GPT-4o API'siga murojaat kodi yoziladi.
        # Hozircha biz sun'iy javob generatsiya qilamiz.
        time.sleep(10) # AI o'ylanayotganini simulyatsiya qilish uchun

        mock_questions = [
            {
                "question": f"{request_data['topic']} haqida 1-savol?",
                "options": ["A) Variant", "B) Variant", "C) Variant", "D) Variant"],
                "answer": "A"
            },
            {
                "question": f"{request_data['topic']} haqida 2-savol?",
                "options": ["A) Javob", "B) Javob", "C) Javob", "D) Javob"],
                "answer": "C"
            }
        ]
        
        result = {
            "status": "success",
            "user_id": request_data["user_id"],
            "chat_id": request_data["chat_id"],
            "bot_id": request_data["bot_id"],
            "data": mock_questions
        }
        
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
        result = {
            "status": "error",
            "user_id": request_data["user_id"],
            "chat_id": request_data["chat_id"],
            "bot_id": request_data["bot_id"],
            "message": "Test yaratishda kutilmagan xatolik yuz berdi."
        }

    # Natijani asosiy botga callback_url orqali qaytaramiz
    try:
        requests.post(request_data["callback_url"], data=json.dumps(result), headers={'Content-Type': 'application/json'})
        print(f"Callback muvaffaqiyatli yuborildi: {request_data['callback_url']}")
    except requests.exceptions.RequestException as e:
        print(f"Callback yuborishda xatolik: {e}")
        
    return result
