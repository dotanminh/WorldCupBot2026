from telegram.ext import ContextTypes
import database as db
import football_api as api
import datetime
import pytz
import asyncio
from config import TIMEZONE

# Lưu trữ các ID trận đấu và ngày đã gửi thông báo để tránh gửi trùng lặp
sent_1h_alerts = set()
sent_lineup_alerts = set()
sent_daily_wrapup_date = ""

async def send_afternoon_wrapup(context: ContextTypes.DEFAULT_TYPE):
    """Tổng kết lúc 2h chiều (14:00): Tỉ số các trận vừa đá hôm nay, và lịch trận tiếp theo."""
    vn_tz = pytz.timezone(TIMEZONE)
    now_vn = datetime.datetime.now(vn_tz)
    
    # 1. Lấy tỉ số các trận trong ngày hôm nay (từ 00:00 đến 14:00)
    completed = api.get_completed_matches()
    today_scores = []
    today_str = now_vn.strftime("%Y-%m-%d")
    for e in completed:
        dt_obj = datetime.datetime.fromisoformat(e["date"].replace("Z", "+00:00")).astimezone(vn_tz)
        if dt_obj.strftime("%Y-%m-%d") == today_str:
            today_scores.append(e)
            
    # 2. Lấy lịch các trận từ 14:00 hôm nay đến 14:00 ngày mai
    upcoming = api.get_upcoming_matches()
    next_matches = []
    tomorrow = now_vn + datetime.timedelta(days=1)
    
    for e in upcoming:
        dt_obj = datetime.datetime.fromisoformat(e["date"].replace("Z", "+00:00")).astimezone(vn_tz)
        if now_vn < dt_obj <= tomorrow:
            next_matches.append(e)
            
    msg = "☀️ **BẢN TIN WORLD CUP CHIỀU NAY** ☀️\n\n"
    
    msg += "✅ **KẾT QUẢ CÁC TRẬN VỪA QUA:**\n"
    if today_scores:
        msg += api.format_fixture_message(today_scores).replace("📅 **LỊCH THI ĐẤU & TỈ SỐ (ESPN)** 📅\n\n", "")
    else:
        msg += "Không có trận nào diễn ra trong sáng nay.\n\n"
        
    msg += "🔜 **LỊCH THI ĐẤU ĐÊM NAY & RẠNG SÁNG MAI:**\n"
    if next_matches:
        msg += api.format_fixture_message(next_matches).replace("📅 **LỊCH THI ĐẤU & TỈ SỐ (ESPN)** 📅\n\n", "")
    else:
        msg += "Chưa có lịch thi đấu tiếp theo.\n"

    users = db.get_all_subscribers()
    for user_id in users:
        try:
            await context.bot.send_message(chat_id=user_id, text=msg, parse_mode='Markdown')
            await asyncio.sleep(0.05) # Tránh bị Telegram phạt Rate Limit
        except Exception as e:
            pass

async def poll_events(context: ContextTypes.DEFAULT_TYPE):
    """Hàm này chạy 5 phút 1 lần để quét toàn bộ sự kiện."""
    global sent_1h_alerts, sent_lineup_alerts, sent_daily_wrapup_date
    
    vn_tz = pytz.timezone(TIMEZONE)
    now_vn = datetime.datetime.now(vn_tz)
    
    # 1. Kiểm tra xem có phải 14:00 chiều để gửi bản tin không
    today_str = now_vn.strftime("%Y-%m-%d")
    if now_vn.hour == 14 and 0 <= now_vn.minute < 10 and sent_daily_wrapup_date != today_str:
        await send_afternoon_wrapup(context)
        sent_daily_wrapup_date = today_str
        
    # 2. Quét các trận đấu sắp diễn ra
    upcoming = api.get_upcoming_matches()
    users = db.get_all_subscribers()
    
    for event in upcoming:
        try:
            event_id = event["id"]
            date_str = event["date"]
            dt_obj = datetime.datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            dt_vn = dt_obj.astimezone(vn_tz)
            
            time_diff = dt_vn - now_vn
            minutes_to_match = time_diff.total_seconds() / 60.0
            
            # Thông tin trận đấu
            comp = event["competitions"][0]
            competitors = comp["competitors"]
            team1 = competitors[0]["team"]["displayName"]
            team2 = competitors[1]["team"]["displayName"]
            time_str = dt_vn.strftime("%d/%m lúc %H:%M")
            round_info = event.get("name", f"{team1} vs {team2}")
            
            # BÁO THỨC TRƯỚC 1 TIẾNG (Cửa sổ 55-65 phút)
            if 55 <= minutes_to_match <= 65 and event_id not in sent_1h_alerts:
                match_msg = f"🔔 **SẮP DIỄN RA (Sau 1 tiếng nữa)** 🔔\n\n⚽ **{team1}** 🆚 **{team2}**\n🕒 Giờ đá: {time_str}\n📌 Trận: {round_info}\n\nĐừng bỏ lỡ nhé!"
                for user_id in users:
                    try:
                        await context.bot.send_message(chat_id=user_id, text=match_msg, parse_mode='Markdown')
                        await asyncio.sleep(0.05)
                    except: pass
                sent_1h_alerts.add(event_id)
                
            # LẤY ĐỘI HÌNH RA SÂN TRƯỚC 30 PHÚT (Cửa sổ 20-35 phút)
            if 20 <= minutes_to_match <= 35 and event_id not in sent_lineup_alerts:
                lineups_msg = api.get_match_lineups(event_id)
                if lineups_msg:
                    header = f"🔥 **CẬP NHẬT TRƯỚC TRẬN ĐẤU (30 phút)** 🔥\n\n⚽ **{team1}** 🆚 **{team2}**\n\n"
                    full_msg = header + lineups_msg
                    for user_id in users:
                        try:
                            await context.bot.send_message(chat_id=user_id, text=full_msg, parse_mode='Markdown')
                            await asyncio.sleep(0.05)
                        except: pass
                    sent_lineup_alerts.add(event_id)
                    
        except Exception as e:
            print(f"Lỗi khi quét sự kiện event_id: {e}")
