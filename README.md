# 🏆 World Cup 2026 Telegram Bot - Skill Package

Chào mừng bạn đến với gói mã nguồn (Skill) siêu Bot cập nhật kết quả và lịch thi đấu FIFA World Cup 2026 tự động trên nền tảng Telegram! 

Dự án này được thiết kế theo kiến trúc **Webhook** kết hợp nền tảng Serverless (Render) và API của ESPN, đảm bảo hoạt động mượt mà 24/7, tỷ lệ "chết" gần như bằng 0.

## ✨ Tính năng nổi bật
1. **Lấy Lịch thi đấu & Tỉ số:** Tự động quét API ESPN để lấy dữ liệu thi đấu nhanh và chính xác nhất.
2. **Bảng xếp hạng (Live Standings):** Tự động tính điểm, hiệu số bàn thắng và tổng bàn thắng theo tiêu chuẩn FIFA ngay khi trận đấu kết thúc.
3. **Báo thức thông minh (1h trước trận):** Gửi nhắc nhở chính xác đến từng người dùng.
4. **Đội hình ra sân (30p trước trận):** Tự động cào đội hình xuất phát chính thức từ ESPN.
5. **Bản tin 14h00:** Tổng kết tỉ số rạng sáng và lịch thi đấu đêm nay.
6. **Đăng ký người dùng tự động:** Bất kỳ ai sử dụng lệnh của Bot đều được tự động lưu vào danh sách VIP để nhận thông báo.

## 📁 Cấu trúc Mã nguồn
- `main.py`: Trái tim của Bot, khởi chạy máy chủ Webhook.
- `bot_handlers.py`: Chứa các lệnh giao tiếp người dùng (`/start`, `/lich`, `/lichtong`, `/tyso`, `/bxh`).
- `football_api.py`: Modul gọi API ESPN và xử lý logic tính điểm.
- `scheduler_tasks.py`: Các kịch bản chạy ngầm tự động theo giờ (JobQueue).
- `config.py`: Cấu hình múi giờ và đường dẫn.
- `database.py`: Lưu trữ người dùng bằng SQLite.
- `requirements.txt`, `runtime.txt`, `Procfile`: Các tệp dùng để cấu hình máy chủ Render.

---

## 🚀 Hướng dẫn cài đặt từ con số 0

### Bước 1: Tạo Bot Telegram của riêng bạn
1. Mở ứng dụng Telegram, tìm kiếm **@BotFather**.
2. Gõ lệnh `/newbot` và làm theo hướng dẫn để đặt Tên và Username cho Bot.
3. BotFather sẽ cấp cho bạn một đoạn mã dài gọi là **Bot Token** (Ví dụ: `123456789:ABCDefgh...`). Hãy copy và cất kỹ đoạn mã này.

### Bước 2: Tải Code lên GitHub
1. Tạo một tài khoản GitHub (nếu chưa có) và tạo một Repository (Kho lưu trữ) mới.
2. Giải nén gói mã nguồn này và tải **TẤT CẢ** các tệp lên Repository vừa tạo.
3. Bấm **Commit changes** để lưu lại.

### Bước 3: Triển khai lên máy chủ miễn phí Render
1. Truy cập [Render.com](https://render.com) và đăng nhập bằng tài khoản GitHub của bạn.
2. Bấm **New+** góc phải trên cùng, chọn **Web Service**.
3. Chọn Repository chứa mã nguồn bạn vừa tải lên ở Bước 2.
4. Cấu hình Server:
   - **Name:** Đặt tên tùy ý (Ví dụ: `wc2026-bot-vip`).
   - **Runtime:** `Python 3`.
   - **Build Command:** `pip install -r requirements.txt`.
   - **Start Command:** `python main.py`.
5. Cuộn xuống phần **Environment Variables** (Biến môi trường), thêm 1 biến sau:
   - Key: `TELEGRAM_BOT_TOKEN`
   - Value: Dán đoạn mã Token bạn lấy từ BotFather ở Bước 1 vào đây.
6. Bấm **Create Web Service**.

### Bước 4: Tận hưởng thành quả
- Chờ Render chạy lệnh Build (khoảng 2-3 phút). 
- Khi thấy chữ `Your service is live 🎉` trên màn hình Logs, hãy mở Telegram và chat `/start` với con Bot của bạn!
- Tặng link Bot cho bạn bè và tận hưởng mùa World Cup nhé!
