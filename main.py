from telegram.ext import ApplicationBuilder, CommandHandler
import datetime
import pytz
import sys
import os
import asyncio

# Khắc phục lỗi in tiếng Việt trên console của Windows
sys.stdout.reconfigure(encoding='utf-8')

from config import TELEGRAM_BOT_TOKEN, TIMEZONE
import bot_handlers as handlers
import scheduler_tasks as tasks

def main():
    """Hàm khởi chạy Bot."""
    if not TELEGRAM_BOT_TOKEN:
        print("LỖI: Chưa có TELEGRAM_BOT_TOKEN trong file .env")
        return

    print("Đang khởi động World Cup 2026 Bot (Kiến trúc Webhook)...")
    
    # Khởi tạo Application (tự động bao gồm JobQueue)
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Đăng ký lệnh cơ bản
    app.add_handler(CommandHandler("start", handlers.start))
    app.add_handler(CommandHandler("bxh", handlers.bang_xep_hang))
    app.add_handler(CommandHandler("lich", handlers.lich_thi_dau))
    app.add_handler(CommandHandler("lichtong", handlers.lichtong))
    app.add_handler(CommandHandler("tyso", handlers.tyso))
    app.add_handler(CommandHandler("huy", handlers.stop))
    
    # Cài đặt vòng lặp "Đi tuần tra" (Polling) cứ 5 phút (300 giây) chạy 1 lần. 
    job_queue = app.job_queue
    job_queue.run_repeating(tasks.poll_events, interval=300, first=10)
    
    # Kích hoạt tính năng WEBHOOK thay vì POLLING
    # Webhook là giải pháp tuyệt đối chính xác và hiệu quả nhất cho Server Render,
    # giải quyết vĩnh viễn lỗi Conflict khi Zero-Downtime Deployment.
    
    port = int(os.environ.get("PORT", 10000))
    render_url = os.environ.get("RENDER_EXTERNAL_URL")
    
    if render_url:
        print(f"Đã phát hiện Server Render. Khởi chạy Webhook tại cổng {port}...")
        webhook_url = f"{render_url}/webhook"
        app.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path="webhook",
            webhook_url=webhook_url,
            drop_pending_updates=True
        )
    else:
        print("Khởi chạy ở chế độ Polling (Dành cho máy tính cá nhân)...")
        app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    asyncio.set_event_loop(asyncio.new_event_loop())
    main()
