from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import database as db
import football_api as api
import news_api as news

async def send_long_message(update: Update, text: str):
    """Gửi tin nhắn dài qua Telegram bằng cách cắt chuỗi an toàn (max 4000 ký tự)."""
    max_len = 4000
    if len(text) <= max_len:
        await update.message.reply_text(text, parse_mode='Markdown')
        return
        
    parts = []
    while len(text) > 0:
        if len(text) <= max_len:
            parts.append(text)
            break
        split_pos = text.rfind('\n\n', 0, max_len)
        if split_pos == -1:
            split_pos = text.rfind('\n', 0, max_len)
        if split_pos == -1:
            split_pos = max_len
            
        parts.append(text[:split_pos])
        text = text[split_pos:].lstrip()
        
    for part in parts:
        await update.message.reply_text(part, parse_mode='Markdown')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /start, đăng ký người dùng."""
    chat_id = update.effective_chat.id
    username = update.effective_chat.username or update.effective_chat.first_name
    
    is_new = db.add_subscriber(chat_id, username)
    
    welcome_msg = (
        "🏆 **Chào mừng bạn đến với Siêu Bot FIFA World Cup 2026!** 🏆\n\n"
        "Bạn đã đăng ký tài khoản VIP thành công. Bot sẽ tự động phục vụ bạn các tính năng sau:\n"
        "⏰ **Báo thức trận đấu:** Tự động gửi lịch nhắc nhở bạn đúng 1 tiếng trước khi bóng lăn.\n"
        "📋 **Đội hình ra sân:** Tự động gửi danh sách cầu thủ đá chính 30 phút trước trận đấu.\n"
        "☀️ **Bản tin 14h00:** Tự động tổng kết kết quả rạng sáng và báo lịch đêm nay vào 2h chiều mỗi ngày.\n"
        "📈 **BXH Real-time:** Bảng xếp hạng tự động cộng điểm và nhảy bậc ngay khi trận đấu kết thúc.\n\n"
        "**Các lệnh tra cứu thủ công (Bấm vào để gọi):**\n"
        "/lich - Xem lịch thi đấu hôm nay\n"
        "/lichtong - Xem toàn bộ lịch 104 trận (Từ Vòng bảng đến Chung kết)\n"
        "/tyso - Xem tổng hợp tỉ số các trận đã kết thúc\n"
        "/bxh - Xem bảng xếp hạng 12 bảng đấu (Live Standings)\n"
        "/huy - Hủy nhận thông báo"
    )
    await context.bot.send_message(chat_id=chat_id, text=welcome_msg, parse_mode='Markdown')

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /huy, hủy đăng ký."""
    chat_id = update.effective_chat.id
    db.remove_subscriber(chat_id)
    await context.bot.send_message(
        chat_id=chat_id, 
        text="Đã hủy đăng ký. Bạn sẽ không nhận được thông báo tự động nữa."
    )

async def lich_thi_dau(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /lich, gửi lịch hôm nay."""
    chat_id = update.effective_chat.id
    username = update.effective_chat.username or update.effective_chat.first_name
    db.add_subscriber(chat_id, username) # Tự động đăng ký lại nếu DB bị xoá
    
    # Thông báo cho người dùng bot đang xử lý
    await context.bot.send_chat_action(chat_id=chat_id, action='typing')
    
    fixtures = api.get_today_fixtures()
    msg = api.format_fixture_message(fixtures)
    await send_long_message(update, msg)

async def lichtong(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /lichtong, xem tất cả lịch chưa đá của World Cup."""
    chat_id = update.effective_chat.id
    username = update.effective_chat.username or update.effective_chat.first_name
    db.add_subscriber(chat_id, username)
    
    await update.message.reply_text("🔄 Đang tải toàn bộ lịch thi đấu từ hệ thống... (Vui lòng đợi vài giây)")
    upcoming = api.get_all_fixtures()
    if not upcoming:
        await update.message.reply_text("📅 Hiện tại chưa có lịch thi đấu mới nào.")
        return
        
    msg = "🌍 **LỊCH TỔNG TOÀN GIẢI WORLD CUP (Các trận sắp tới)** 🌍\n\n"
    msg += api.format_fixture_message(upcoming).replace("📅 **LỊCH THI ĐẤU & TỈ SỐ TRỰC TIẾP (ESPN)** 📅\n\n", "")
    
    await send_long_message(update, msg)

async def tyso(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /tyso, xem toàn bộ tỷ số các trận đã đá."""
    chat_id = update.effective_chat.id
    username = update.effective_chat.username or update.effective_chat.first_name
    db.add_subscriber(chat_id, username)
    
    await update.message.reply_text("🔄 Đang tải toàn bộ kết quả tỉ số... (Vui lòng đợi vài giây)")
    completed = api.get_completed_matches()
    if not completed:
        await update.message.reply_text("⚽ Hiện tại giải đấu chưa có trận nào đá xong.")
        return
        
    msg = "🏆 **TỔNG HỢP TỈ SỐ WORLD CUP (Từ đầu giải)** 🏆\n\n"
    msg += api.format_fixture_message(completed).replace("📅 **LỊCH THI ĐẤU & TỈ SỐ TRỰC TIẾP (ESPN)** 📅\n\n", "")
    
    await send_long_message(update, msg)

async def bang_xep_hang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /bxh."""
    chat_id = update.effective_chat.id
    username = update.effective_chat.username or update.effective_chat.first_name
    db.add_subscriber(chat_id, username)
    
    await context.bot.send_chat_action(chat_id=chat_id, action='typing')
    
    standings = api.get_standings()
    if not standings:
        await context.bot.send_message(chat_id=chat_id, text="Chưa có dữ liệu bảng xếp hạng hiện tại.")
        return
        
    # Tạo tin nhắn BXH tóm tắt (Phương án 1)
    msg = "🏆 **BẢNG XẾP HẠNG WORLD Cup 2026** 🏆\n\n"
    for group in standings:
        # group là danh sách các đội trong 1 bảng
        group_name = group[0]["group"]
        # Loại bỏ các từ thừa nếu API trả về (ví dụ "Group A" -> "BẢNG A")
        clean_group_name = str(group_name).replace("Group", "BẢNG").upper().strip()
        
        # Mảng thông tin Quốc gia đăng cai (Host Country)
        # World Cup 2026: Mexico (Bảng A), Canada (Bảng B), Mỹ (Bảng D và phần lớn còn lại)
        group_hosts = {
            "BẢNG A": "🇲🇽 Mexico",
            "BẢNG B": "🇨🇦 Canada",
            "BẢNG C": "🇺🇸 USA",
            "BẢNG D": "🇺🇸 USA",
            "BẢNG E": "🇺🇸 USA",
            "BẢNG F": "🇺🇸 USA",
            "BẢNG G": "🇺🇸 USA",
            "BẢNG H": "🇺🇸 USA",
            "BẢNG I": "🇺🇸 USA",
            "BẢNG J": "🇺🇸 USA",
            "BẢNG K": "🇺🇸 USA",
            "BẢNG L": "🇺🇸 USA"
        }
        host = group_hosts.get(clean_group_name, "🇺🇸 🇨🇦 🇲🇽")
        
        msg += f"🔥 **{clean_group_name}** (📍 {host})\n"
        for team in group:
            rank = team["rank"]
            name = team["team"]["name"]
            points = team["points"]
            gd = team["goalsDiff"]
            
            # Chọn icon số đếm
            number_icons = {1: "1️⃣", 2: "2️⃣", 3: "3️⃣", 4: "4️⃣", 5: "5️⃣", 6: "6️⃣"}
            rank_icon = number_icons.get(rank, f"{rank}.")
            
            # Thêm dấu + cho hiệu số dương
            gd_str = f"+{gd}" if gd > 0 else str(gd)
            
            msg += f"{rank_icon} ⚽ {name} - {points}đ (HS: {gd_str})\n"
        msg += "\n"
        
    # Do Telegram giới hạn độ dài tin nhắn (khoảng 4096 ký tự),
    # ta cắt ra nếu quá dài (1 bảng khoảng 150 ký tự, 12 bảng khoảng 1800 -> dư sức gửi 1 tin)
    if len(msg) > 4000:
        msg = msg[:4000] + "\n... (Còn nữa)"
        
    await context.bot.send_message(chat_id=chat_id, text=msg, parse_mode='Markdown')

async def tintuc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /tintuc - Xem tin tức VnExpress theo chuyên mục."""
    chat_id = update.effective_chat.id
    username = update.effective_chat.username or update.effective_chat.first_name
    db.add_subscriber(chat_id, username)

    # Tạo inline keyboard chọn chuyên mục
    categories = news.get_all_categories()
    keyboard = []
    row = []
    for i, cat in enumerate(categories):
        row.append(InlineKeyboardButton(cat, callback_data=f"news_{cat}"))
        if len(row) == 2:  # 2 nút mỗi hàng
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    # Thêm nút xem tất cả
    keyboard.append([InlineKeyboardButton("📰 Tất cả tin mới nhất", callback_data="news_Tin mới nhất")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "📰 *Chọn chuyên mục tin tức VnExpress:*",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def tintuc_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý khi người dùng bấm chọn chuyên mục tin tức."""
    query = update.callback_query
    await query.answer()

    category = query.data.replace("news_", "")
    await query.edit_message_text(f"🔄 Đang tải tin *{category}*...", parse_mode='Markdown')

    articles = news.get_news_by_category(category)
    msg = news.format_articles_message(articles, header=f"TIN TỨC - {category.upper()}")

    # Telegram giới hạn tin nhắn edit_message_text nên gửi tin mới
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=msg,
        parse_mode='Markdown',
        disable_web_page_preview=False
    )
