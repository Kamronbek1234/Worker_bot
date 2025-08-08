from pydantic import BaseModel, HttpUrl

class TestRequest(BaseModel):
    user_id: int
    chat_id: int
    bot_id: str
    topic: str
    question_count: int
    callback_url: HttpUrl