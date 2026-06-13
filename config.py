import os
from dotenv import load_dotenv

# Nạp các biến môi trường từ file .env
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TIMEZONE = os.getenv("TIMEZONE", "Asia/Ho_Chi_Minh")

# Sử dụng ESPN Public API (Miễn phí 100%)
API_URL = "http://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard"

