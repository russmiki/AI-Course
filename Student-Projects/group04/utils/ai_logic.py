import requests
import os
import base64
from PIL import Image
import hashlib
import tempfile
from dotenv import load_dotenv

load_dotenv(override=True)


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY را در فایل .env تنظیم کن")

image_analysis_cache = {}

def get_image_hash(filepath):
    """محاسبه هش عکس برای استفاده به عنوان کلید کش"""
    try:
        with open(filepath, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def compress_image(filepath, max_size=512, quality=30):
    """فشرده‌سازی پیشرفته عکس برای حداقل کردن حجم"""
    try:
        img = Image.open(filepath)
        
        if img.mode in ("RGBA", "P", "LA"):
            img = img.convert("RGB")
        
        img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        fd, output_path = tempfile.mkstemp(suffix='.jpg')
        os.close(fd)
        
        img.save(output_path, "JPEG", quality=quality, optimize=True)
        
        file_size = os.path.getsize(output_path) / 1024
        print(f"حجم عکس فشرده: {file_size:.1f} KB")
        
        if file_size > 20:
            img.save(output_path, "JPEG", quality=20, optimize=True)
            file_size = os.path.getsize(output_path) / 1024
            print(f"حجم پس از فشرده‌سازی اضافی: {file_size:.1f} KB")
        
        return output_path
    except Exception as e:
        print(f"[خطا در فشرده‌سازی عکس] {e}")
        return filepath


def generate_smart_title_from_history(chat_history) -> str:
    """
    با توجه به کل تاریخچه چت، یک عنوان کوتاه و جذاب می‌سازه
    فقط پیام‌های کاربر رو می‌فرسته به مدل
    """
    user_messages = []
    has_image = False

    for msg in chat_history:
        if msg["role"] == "user":
            text = msg.get("content", "").strip()
            if "file" in msg and msg["file"]["mimeType"].startswith("image/"):
                has_image = True
                if text:
                    user_messages.append(f"عکس آپلود کرد + متن: {text}")
                else:
                    user_messages.append("عکس بدن یا تمرین آپلود کرد")
            elif text:
                user_messages.append(text)

    if not user_messages:
        return "چت جدید"

    context = "".join(user_messages[-8:])  

    prompt = f"""
این پیام‌های کاربر در یک چت بدنسازی و تغذیه هست:

{context}

یک عنوان کوتاه، جذاب و حرفه‌ای (حداکثر ۴۰ کاراکتر فارسی) برای این مکالمه بساز.
اگر عکس آپلود شده → حتماً به تحلیل بدن یا فرم اشاره کن.
فقط خود عنوان را بنویس، بدون نقل قول و توضیح.

عنوان:""".strip()

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "http://127.0.0.1:8000",
                "X-Title": "Smart Fitness Coach",
                "Content-Type": "application/json"
            },
            json={
                "model": "google/gemma-2-9b-it:free",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.4,
                "max_tokens": 30
            },
            timeout=25
        )
        response.raise_for_status()
        title = response.json()["choices"][0]["message"]["content"].strip()
        
        title = title.split("")[0].strip()
        if title.lower().startswith(("عنوان", "title", "اسم")):
            title = title.split(":", 1)[-1].strip()
        title = title.strip('\'"“”`')
        
        return title[:40] if len(title) > 40 else title

    except Exception as e:
        print(f"[خطا در تولید عنوان هوشمند] {e}")
        if has_image:
            return "تحلیل عکس بدن"
        return "برنامه تمرینی و تغذیه"


def generate_plan(chat_history):
    url = "https://openrouter.ai/api/v1/chat/completions"

    has_image = any(
        "file" in msg and msg["file"]["mimeType"].startswith("image/")
        for msg in chat_history
    )

    last_user_text = ""
    last_user_has_image = False
    last_user_message = None 

    for msg in reversed(chat_history):
        if msg["role"] == "user":
            last_user_message = msg
            if msg.get("content", "").strip():
                last_user_text = msg["content"].strip()
            if "file" in msg and msg["file"]["mimeType"].startswith("image/"):
                last_user_has_image = True
            break

    no_photo_keywords = [
        "عکس ندارم", "عکسی ندارم", "بدون عکس", "بدون تصویر", "no photo", "without photo",
        "don't have photo", "عکس نمیتونم", "فقط برنامه", "just program", "برنامه بدون عکس"
    ]
    user_said_no_photo = any(kw in last_user_text.lower() for kw in no_photo_keywords) if last_user_text else False

    force_vision = last_user_has_image and not user_said_no_photo

    cached_analysis = None
    image_filepath = None

    if has_image and not force_vision:
        for msg in reversed(chat_history):
            if (msg["role"] == "user" and "file" in msg and 
                msg["file"]["mimeType"].startswith("image/")):
                image_filepath = os.path.join("static", "uploads", msg["file"]["filename"])
                if os.path.exists(image_filepath):
                    image_hash = get_image_hash(image_filepath)
                    if image_hash in image_analysis_cache:
                        cached_analysis = image_analysis_cache[image_hash]
                        print("استفاده از تحلیل کش شده عکس (چون عکس جدید نیست)")
                    break

    if force_vision:
        system_prompt = (
            "تو مربی حرفه‌ای بدنسازی و تغذیه با بیش از ۱۵ سال تجربه جهانی هستی.\n"
            "تخصصت تحلیل دقیق بدن از روی عکس و ساخت برنامه‌های ۱۰۰٪ شخصی‌سازی‌شده است.\n\n"
            "رفتار تو:\n"
            "۱. عکس کاربر را دقیق تحلیل کن (فقط بدن، بدون توصیف محیط یا لباس):\n"
            "   - درصد چربی بدن تقریبی\n"
            "   - وضعیت پوسچر و تعادل بدن\n"
            "   - نقاط قوت و ضعف عضلانی\n\n"
            "۲. با توجه به متن درخواست کاربر (اگر نوشته)، دقیقاً همان چیزی را بده که خواسته:\n"
            "   - فقط برنامه غذایی خواست → فقط تغذیه\n"
            "   - فقط برنامه تمرینی خواست → فقط تمرین + ریکاوری\n"
            "   - هدف کلی یا برنامه کامل خواست → برنامه کامل تمرینی + تغذیه + ریکاوری\n"
            "   - هدف مشخصی نگفت → تحلیل بدن را بده و بپرس هدفش چیه\n\n"
            "همیشه فارسی، حرفه‌ای، انگیزشی و ساختارمند (با سرتیتر و لیست) جواب بده."
        )
        model = "nvidia/nemotron-nano-12b-v2-vl:free"
        temperature = 0.35
        use_vision = True

    elif has_image and cached_analysis:  
        system_prompt = (
            "تو مربی حرفه‌ای بدنسازی و تغذیه هستی.\n"
            "تحلیل قبلی بدن کاربر (از عکس قبلی):\n"
            f"{cached_analysis}\n\n"
            "حالا بر اساس این تحلیل و درخواست جدید کاربر، دقیقاً همان چیزی را بده که خواسته:\n"
            "- فقط برنامه غذایی خواست → فقط تغذیه\n"
            "- فقط برنامه تمرینی خواست → فقط تمرین + ریکاوری\n"
            "- هدف کلی یا برنامه کامل خواست → برنامه کامل بده\n"
            "- هدف مشخصی نگفت → راهنمایی کن و بپرس\n\n"
            "همیشه فارسی، حرفه‌ای و ساختارمند جواب بده."
        )
        model = "nex-agi/deepseek-v3.1-nex-n1:free"
        temperature = 0.4
        use_vision = False

    else:
        system_prompt = (
            "تو مربی حرفه‌ای بدنسازی و تغذیه هستی.\n\n"
            "رفتار دقیق تو:\n"
            "اطلاعاتی که نیاز داری رو از کاربر بگیر"
            "- فقط وقتی برنامه کامل می‌دهی که کاربر هدف واضحی گفته باشه.\n"
            "- اگر فقط برنامه غذایی خواست → فقط تغذیه بده\n"
            "- اگر فقط برنامه تمرینی خواست → فقط تمرین + ریکاوری بده\n"
            "- اگر درخواست واضحی نداد → مشاوره بده و بپرس چی می‌خواد\n\n"
            "همیشه فارسی، حرفه‌ای، انگیزشی و ساختارمند جواب بده."
        )
        model = "nex-agi/deepseek-v3.1-nex-n1:free"
        temperature = 0.4
        use_vision = False

    messages = [{"role": "system", "content": system_prompt}]

    for msg in chat_history:
        role = "user" if msg["role"] == "user" else "assistant"
        content_list = []

        if msg.get("content", "").strip():
            content_list.append({"type": "text", "text": msg["content"]})

        if (force_vision and role == "user" and 
            "file" in msg and msg["file"]["mimeType"].startswith("image/") and
            msg is last_user_message):

            filepath = os.path.join("static", "uploads", msg["file"]["filename"])
            if os.path.exists(filepath):
                print("شروع فشرده‌سازی و پردازش عکس جدید...")
                compressed_path = compress_image(filepath)
                try:
                    with open(compressed_path, "rb") as f:
                        image_data = f.read()

                    img_b64 = base64.b64encode(image_data).decode("ascii")

                    content_list.append({
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}
                    })
                    print("عکس جدید با موفقیت به مدل ارسال شد")

                    if compressed_path != filepath:
                        os.remove(compressed_path)

                except Exception as e:
                    content_list.append({"type": "text", "text": "عکس قابل پردازش نبود."})
                    print(f"[خطا در پردازش عکس] {e}")

        if content_list:
            messages.append({"role": role, "content": content_list})
        elif msg.get("content", "").strip():
            messages.append({"role": role, "content": msg["content"]})

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 2000,
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://127.0.0.1:8000",
        "X-Title": "Smart Fitness Coach",
        "Content-Type": "application/json"
    }

    try:
        print(f"ارسال درخواست به {model}...")
        response = requests.post(url, json=payload, headers=headers, timeout=180)
        response.raise_for_status()
        
        result = response.json()["choices"][0]["message"]["content"].strip()
        
        if force_vision and image_filepath and os.path.exists(image_filepath):
            image_hash = get_image_hash(image_filepath)
            if image_hash:
                image_analysis_cache[image_hash] = result
                print("تحلیل جدید عکس در کش ذخیره شد")
        
        return result

    except requests.exceptions.RequestException as e:
        error = str(e).lower()
        if "rate limit" in error:
            return "سرور شلوغه، چند لحظه دیگه دوباره امتحان کن."
        return "خطای اتصال به سرور."
    except Exception as e:
        print(f"[خطای غیرمنتظره] {e}")
        return "خطای غیرمنتظره‌ای رخ داد. دوباره امتحان کن."