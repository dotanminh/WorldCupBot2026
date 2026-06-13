import feedparser
import datetime
import pytz
from config import TIMEZONE

# VnExpress RSS feeds theo chuyên mục
VNEXPRESS_FEEDS = {
    "Tin mới nhất": "https://vnexpress.net/rss/tin-moi-nhat.rss",
    "Thời sự":      "https://vnexpress.net/rss/thoi-su.rss",
    "Kinh doanh":   "https://vnexpress.net/rss/kinh-doanh.rss",
    "Thế giới":     "https://vnexpress.net/rss/the-gioi.rss",
    "Công nghệ":    "https://vnexpress.net/rss/so-hoa.rss",
    "Sức khỏe":     "https://vnexpress.net/rss/suc-khoe.rss",
    "Thể thao":     "https://vnexpress.net/rss/the-thao.rss",
    "Giải trí":     "https://vnexpress.net/rss/giai-tri.rss",
}

# Feed mặc định cho broadcast tự động (top news)
DEFAULT_FEED_URL = "https://vnexpress.net/rss/tin-moi-nhat.rss"

def get_latest_news(feed_url=DEFAULT_FEED_URL, limit=5):
    """Lấy danh sách bài viết mới nhất từ RSS feed."""
    try:
        feed = feedparser.parse(feed_url)
        articles = []
        vn_tz = pytz.timezone(TIMEZONE)
        
        for entry in feed.entries[:limit]:
            # Xử lý thời gian publish
            try:
                pub_time = datetime.datetime(*entry.published_parsed[:6], tzinfo=pytz.utc)
                pub_vn = pub_time.astimezone(vn_tz)
                time_str = pub_vn.strftime("%H:%M %d/%m")
            except Exception:
                time_str = "N/A"
            
            # Lấy mô tả ngắn (tóm tắt) - strip HTML tags cơ bản
            description = entry.get("summary", "")
            description = description.replace("<p>", "").replace("</p>", "")
            # Cắt mô tả nếu quá dài
            if len(description) > 200:
                description = description[:200] + "..."
            
            articles.append({
                "title":       entry.title,
                "link":        entry.link,
                "description": description,
                "time":        time_str,
            })
        
        return articles
    except Exception as e:
        print(f"Lỗi khi fetch RSS VnExpress: {e}")
        return []


def get_news_by_category(category_name):
    """Lấy tin theo chuyên mục cụ thể."""
    url = VNEXPRESS_FEEDS.get(category_name, DEFAULT_FEED_URL)
    return get_latest_news(feed_url=url, limit=5)


def get_all_categories():
    """Trả về danh sách tên chuyên mục."""
    return list(VNEXPRESS_FEEDS.keys())


def format_articles_message(articles, header="📰 TIN TỨC MỚI NHẤT"):
    """Định dạng danh sách bài viết thành tin nhắn Telegram."""
    if not articles:
        return "❌ Không lấy được tin tức. Vui lòng thử lại sau."
    
    msg = f"📰 *{header}* 📰\n"
    msg += f"_(VnExpress - Cập nhật lúc {datetime.datetime.now(pytz.timezone(TIMEZONE)).strftime('%H:%M %d/%m/%Y')})_\n\n"
    
    for i, article in enumerate(articles, 1):
        msg += f"*{i}. {article['title']}*\n"
        if article['description']:
            msg += f"_{article['description']}_\n"
        msg += f"🕒 {article['time']} | [Đọc tiếp]({article['link']})\n\n"
    
    return msg.strip()
