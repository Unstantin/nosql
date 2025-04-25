from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import datetime
import redis
import json
import uuid
import logging
from fastapi.logger import logger as fastapi_logger

# Настройка базового логгера
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

fastapi_logger = logging.getLogger("fastapi")
fastapi_logger.setLevel(logging.INFO)

app = FastAPI()

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)


class UserRegister(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    user_id: str
    email: str


class ChatCreate(BaseModel):
    name: str
    creator_id: str


class MessageSend(BaseModel):
    chat_id: str
    sender_id: str
    text: str


class MessageResponse(BaseModel):
    message_id: str
    sender_id: str
    text: str
    timestamp: str


class ChatResponse(BaseModel):
    chat_id: str
    name: str
    creator_id: str
    created_at: str

@app.get("/test-log")
def test_log():
    fastapi_logger.debug("Это DEBUG сообщение")
    fastapi_logger.info("Это INFO сообщение")
    fastapi_logger.warning("Это WARNING сообщение")
    fastapi_logger.error("Это ERROR сообщение")
    return {"status": "Логи протестированы"}


@app.post("/register/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegister):
    if redis_client.hexists("user_emails", user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    user_id = str(uuid.uuid4())

    redis_client.hset(f"user:{user_id}", mapping={
        "email": user.email,
        "password_hash": user.password
    })

    redis_client.hset("user_emails", user.email, user_id)

    return {"user_id": user_id, "email": user.email}


@app.post("/chats/", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
def create_chat(chat_data: ChatCreate):
    chat_id = str(uuid.uuid4())
    chat_key = f"chat:{chat_id}"
    created_at = datetime.now().isoformat()

    redis_client.hset(chat_key, mapping={
        "name": chat_data.name,
        "creator_id": chat_data.creator_id,
        "created_at": created_at
    })

    return {
        "chat_id": chat_id,
        "name": chat_data.name,
        "creator_id": chat_data.creator_id,
        "created_at": created_at
    }


@app.post("/messages/", status_code=status.HTTP_201_CREATED)
def send_message(message: MessageSend):
    chat_key = f"chat:{message.chat_id}"
    exists = redis_client.exists(chat_key)
    fastapi_logger.info(f"Checking chat: {chat_key}, exists: {exists}")  # Логируем

    if not exists:
        fastapi_logger.info(message.chat_id)
        raise HTTPException(status_code=404, detail="Chat not found")

    message_id = str(uuid.uuid4())
    message_data = {
        "message_id": message_id,
        "chat_id": message.chat_id,
        "sender_id": message.sender_id,
        "text": message.text,
        "timestamp": datetime.now().isoformat()
    }
    redis_client.lpush(f"chat:{message.chat_id}:messages", json.dumps(message_data))
    return {"message_id": message_id, "status": "Message sent"}


@app.get("/chats/{chat_id}/messages/", response_model=list[MessageResponse])
def get_messages(chat_id: str, limit: int = 100):
    message_key = f"chat:{chat_id}:messages"

    messages = redis_client.lrange(message_key, 0, limit - 1)

    return [MessageResponse(**json.loads(msg)) for msg in messages]