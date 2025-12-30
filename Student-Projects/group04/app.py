import uvicorn
import json
import os
import base64
from datetime import datetime
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from utils.ai_logic import generate_plan, generate_smart_title_from_history
from chat_storage import (load_all_chats, save_chat, update_chat, delete_chat, 
                         delete_all_chats, init_db)

init_db()
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

def log(msg: str):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/template.html", encoding="utf-8") as f:
        return f.read()

@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    log("اتصال WebSocket جدید برقرار شد")
    
    all_chats = load_all_chats()
    current_chat = all_chats[0] if all_chats else None

    async def broadcast_chats_list():
        chats_list = load_all_chats()
        await websocket.send_json({
            "type": "chats",
            "data": [
                {
                    "title": c.get("smart_title") or c["title"],
                    "index": i
                }
                for i, c in enumerate(chats_list)
            ]
        })

    await broadcast_chats_list()

    try:
        while True:
            data = json.loads(await websocket.receive_text())
            action = data.get("action")

            if action == "get_chats":
                log("درخواست دریافت لیست چت‌ها")
                await broadcast_chats_list()

            elif action == "get_chat":
                if not current_chat:
                    save_chat([], "چت جدید")
                    all_chats = load_all_chats()
                    current_chat = all_chats[0] if all_chats else None
                if current_chat:
                    await websocket.send_json({
                        "type": "chat",
                        "title": current_chat.get("smart_title") or current_chat["title"],
                        "messages": current_chat["messages"]
                    })

            elif action == "new_chat":
                save_chat([], "چت جدید")
                all_chats = load_all_chats()
                current_chat = all_chats[0] if all_chats else None
                log("چت جدید ایجاد شد")
                await broadcast_chats_list()

            elif action == "switch_chat":
                idx = data.get("index", 0)
                chats = load_all_chats()
                if 0 <= idx < len(chats):
                    current_chat = chats[idx]
                    title = current_chat.get("smart_title") or current_chat["title"]
                    log(f"تغییر به چت: {title}")
                    await websocket.send_json({
                        "type": "chat_switched",
                        "title": title,
                        "messages": current_chat["messages"],
                        "smart_title": current_chat.get("smart_title")
                    })

            elif action == "delete_chat":
                idx = data.get("index", 0)
                chats = load_all_chats()
                if 0 <= idx < len(chats):
                    chat_to_delete = chats[idx]
                    title = chat_to_delete.get("smart_title") or chat_to_delete["title"]
                    delete_chat(chat_to_delete["id"])
                    log(f"چت حذف شد: {title}")
                    if current_chat and current_chat["id"] == chat_to_delete["id"]:
                        save_chat([], "چت جدید")
                        all_chats = load_all_chats()
                        current_chat = all_chats[0] if all_chats else None
                        log("چت حذف شده جایگزین شد با چت جدید")
                    await broadcast_chats_list()

            elif action == "clear_all":
                delete_all_chats()
                save_chat([], "چت جدید")
                all_chats = load_all_chats()
                current_chat = all_chats[0] if all_chats else None
                log("همه چت‌ها پاک شدند")
                await broadcast_chats_list()

            elif action == "send_message":
                text = data.get("text", "").strip()
                if not text or not current_chat:
                    continue
                log(f"پیام کاربر: {text}")

                current_chat["messages"].append({"role": "user", "content": text})
                log("در حال تولید پاسخ هوش مصنوعی...")
                response = generate_plan(current_chat["messages"])
                current_chat["messages"].append({"role": "bot", "content": response})

                if not current_chat.get("smart_title") and len(current_chat["messages"]) >= 2:
                    smart_title = generate_smart_title_from_history(current_chat["messages"])
                    if smart_title:
                        current_chat["smart_title"] = smart_title
                        log(f"عنوان هوشمند تولید شد: {smart_title}")

                update_chat(current_chat["id"], current_chat["messages"], current_chat.get("smart_title"))

                await websocket.send_json({
                    "type": "new_message",
                    "role": "bot",
                    "content": response
                })
                await broadcast_chats_list()

            elif action == "send_file":
                filename = data.get("filename")
                mime_type = data.get("mimeType")
                base64_data = data.get("data")
                text = data.get("text", "").strip() or "عکس ارسال شد"

                try:
                    file_bytes = base64.b64decode(base64_data)
                    file_path = os.path.join(UPLOAD_DIR, filename)
                    with open(file_path, "wb") as f:
                        f.write(file_bytes)
                    log(f"فایل آپلود شد: {filename} ({len(file_bytes)//1024} KB)")

                    file_info = {
                        "filename": filename,
                        "mimeType": mime_type,
                        "tempUrl": f"/uploads/{filename}"
                    }

                    current_chat["messages"].append({
                        "role": "user",
                        "content": text,
                        "file": file_info
                    })

                    log("در حال تحلیل فایل توسط هوش مصنوعی...")
                    response = generate_plan(current_chat["messages"])
                    current_chat["messages"].append({"role": "bot", "content": response})

                    update_chat(current_chat["id"], current_chat["messages"], current_chat.get("smart_title"))

                    await websocket.send_json({
                        "type": "message_sent",
                        "role": "user",
                        "content": text,
                        "file": file_info
                    })
                    await websocket.send_json({
                        "type": "new_message",
                        "role": "bot",
                        "content": response
                    })
                    await broadcast_chats_list()

                except Exception as e:
                    log(f"خطا در آپلود فایل: {e}")
                    await websocket.send_json({
                        "type": "error",
                        "message": "آپلود فایل ناموفق بود. دوباره تلاش کنید."
                    })

    except Exception as e:
        log(f"خطا در وب‌سوکت: {e}")

@app.get("/view/{filename:path}")
async def view_image(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}


HOST = os.getenv("APP_HOST", "127.0.0.1")
PORT = int(os.getenv("APP_PORT", "8000"))

if __name__ == "__main__":
    log("مربی هوشمند بدنسازی در حال اجرا...")
    log(f"آدرس: http://{HOST}:{PORT}")
    uvicorn.run(app, host=HOST, port=PORT)
