from fastapi import FastAPI, BackgroundTasks, HTTPException
from .schemas import TestRequest
from .tasks import generate_test_task

app = FastAPI(
    title="Worker Bot API",
    description="Sun'iy intellektga asoslangan vazifalarni bajaruvchi markaziy servis."
)

@app.get("/")
def read_root():
    return {"message": "Worker Bot ishlamoqda!"}


@app.post("/generate/test", status_code=202)
def create_test_generation_task(request: TestRequest, background_tasks: BackgroundTasks):
    """
    Bu endpoint test yaratish uchun yangi vazifa yaratadi.
    U darhol javob qaytaradi va vazifani fonda bajarishga qo'yadi.
    """
    try:
        # Vazifani Celery'ga yuborish
        generate_test_task.delay(request.dict())
        
        return {"message": "Test yaratish so'rovi qabul qilindi va navbatga qo'yildi."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
