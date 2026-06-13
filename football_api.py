import requests
from datetime import datetime, timezone
import pytz
from config import API_URL, TIMEZONE

# Dữ liệu dự phòng tĩnh cho World Cup 2026 (Kết quả bốc thăm thực tế)
FALLBACK_WC_2026_GROUPS = [
    [
        {"rank": 1, "group": "BẢNG A", "team": {"name": "Mexico"}, "points": 0, "goalsDiff": 0},
        {"rank": 2, "group": "BẢNG A", "team": {"name": "South Africa"}, "points": 0, "goalsDiff": 0},
        {"rank": 3, "group": "BẢNG A", "team": {"name": "South Korea"}, "points": 0, "goalsDiff": 0},
        {"rank": 4, "group": "BẢNG A", "team": {"name": "Czechia"}, "points": 0, "goalsDiff": 0},
    ],
    [
        {"rank": 1, "group": "BẢNG B", "team": {"name": "Canada"}, "points": 0, "goalsDiff": 0},
        {"rank": 2, "group": "BẢNG B", "team": {"name": "Bosnia"}, "points": 0, "goalsDiff": 0},
        {"rank": 3, "group": "BẢNG B", "team": {"name": "Qatar"}, "points": 0, "goalsDiff": 0},
        {"rank": 4, "group": "BẢNG B", "team": {"name": "Switzerland"}, "points": 0, "goalsDiff": 0},
    ],
    [
        {"rank": 1, "group": "BẢNG C", "team": {"name": "Brazil"}, "points": 0, "goalsDiff": 0},
        {"rank": 2, "group": "BẢNG C", "team": {"name": "Morocco"}, "points": 0, "goalsDiff": 0},
        {"rank": 3, "group": "BẢNG C", "team": {"name": "Haiti"}, "points": 0, "goalsDiff": 0},
        {"rank": 4, "group": "BẢNG C", "team": {"name": "Scotland"}, "points": 0, "goalsDiff": 0},
    ],
    [
        {"rank": 1, "group": "BẢNG D", "team": {"name": "USA"}, "points": 0, "goalsDiff": 0},
        {"rank": 2, "group": "BẢNG D", "team": {"name": "Paraguay"}, "points": 0, "goalsDiff": 0},
        {"rank": 3, "group": "BẢNG D", "team": {"name": "Australia"}, "points": 0, "goalsDiff": 0},
        {"rank": 4, "group": "BẢNG D", "team": {"name": "Türkiye"}, "points": 0, "goalsDiff": 0},
    ],
    [
        {"rank": 1, "group": "BẢNG E", "team": {"name": "Curaçao"}, "points": 0, "goalsDiff": 0},
        {"rank": 2, "group": "BẢNG E", "team": {"name": "Ecuador"}, "points": 0, "goalsDiff": 0},
        {"rank": 3, "group": "BẢNG E", "team": {"name": "Germany"}, "points": 0, "goalsDiff": 0},
        {"rank": 4, "group": "BẢNG E", "team": {"name": "Côte d'Ivoire"}, "points": 0, "goalsDiff": 0},
    ],
    [
        {"rank": 1, "group": "BẢNG F", "team": {"name": "France"}, "points": 0, "goalsDiff": 0},
        {"rank": 2, "group": "BẢNG F", "team": {"name": "Japan"}, "points": 0, "goalsDiff": 0},
        {"rank": 3, "group": "BẢNG F", "team": {"name": "Egypt"}, "points": 0, "goalsDiff": 0},
        {"rank": 4, "group": "BẢNG F", "team": {"name": "Peru"}, "points": 0, "goalsDiff": 0},
    ],
    [
        {"rank": 1, "group": "BẢNG G", "team": {"name": "Argentina"}, "points": 0, "goalsDiff": 0},
        {"rank": 2, "group": "BẢNG G", "team": {"name": "Nigeria"}, "points": 0, "goalsDiff": 0},
        {"rank": 3, "group": "BẢNG G", "team": {"name": "Sweden"}, "points": 0, "goalsDiff": 0},
        {"rank": 4, "group": "BẢNG G", "team": {"name": "Iran"}, "points": 0, "goalsDiff": 0},
    ],
    [
        {"rank": 1, "group": "BẢNG H", "team": {"name": "England"}, "points": 0, "goalsDiff": 0},
        {"rank": 2, "group": "BẢNG H", "team": {"name": "Senegal"}, "points": 0, "goalsDiff": 0},
        {"rank": 3, "group": "BẢNG H", "team": {"name": "Saudi Arabia"}, "points": 0, "goalsDiff": 0},
        {"rank": 4, "group": "BẢNG H", "team": {"name": "Colombia"}, "points": 0, "goalsDiff": 0},
    ],
    [
        {"rank": 1, "group": "BẢNG I", "team": {"name": "Spain"}, "points": 0, "goalsDiff": 0},
        {"rank": 2, "group": "BẢNG I", "team": {"name": "Mali"}, "points": 0, "goalsDiff": 0},
        {"rank": 3, "group": "BẢNG I", "team": {"name": "Costa Rica"}, "points": 0, "goalsDiff": 0},
        {"rank": 4, "group": "BẢNG I", "team": {"name": "Wales"}, "points": 0, "goalsDiff": 0},
    ],
    [
        {"rank": 1, "group": "BẢNG J", "team": {"name": "Portugal"}, "points": 0, "goalsDiff": 0},
        {"rank": 2, "group": "BẢNG J", "team": {"name": "Cameroon"}, "points": 0, "goalsDiff": 0},
        {"rank": 3, "group": "BẢNG J", "team": {"name": "Panama"}, "points": 0, "goalsDiff": 0},
        {"rank": 4, "group": "BẢNG J", "team": {"name": "Serbia"}, "points": 0, "goalsDiff": 0},
    ],
    [
        {"rank": 1, "group": "BẢNG K", "team": {"name": "Italy"}, "points": 0, "goalsDiff": 0},
        {"rank": 2, "group": "BẢNG K", "team": {"name": "Algeria"}, "points": 0, "goalsDiff": 0},
        {"rank": 3, "group": "BẢNG K", "team": {"name": "Jamaica"}, "points": 0, "goalsDiff": 0},
        {"rank": 4, "group": "BẢNG K", "team": {"name": "New Zealand"}, "points": 0, "goalsDiff": 0},
    ],
    [
        {"rank": 1, "group": "BẢNG L", "team": {"name": "Netherlands"}, "points": 0, "goalsDiff": 0},
        {"rank": 2, "group": "BẢNG L", "team": {"name": "Ghana"}, "points": 0, "goalsDiff": 0},
        {"rank": 3, "group": "BẢNG L", "team": {"name": "Honduras"}, "points": 0, "goalsDiff": 0},
        {"rank": 4, "group": "BẢNG L", "team": {"name": "Poland"}, "points": 0, "goalsDiff": 0},
    ]
]

import requests
import datetime
import pytz

from config import API_URL, TIMEZONE

def get_today_fixtures():
    """Lấy danh sách các trận đấu từ ESPN API cho ngày hôm nay và ngày mai (giờ VN)."""
    try:
        vn_tz = pytz.timezone(TIMEZONE)
        today = datetime.datetime.now(vn_tz)
        tomorrow = today + datetime.timedelta(days=1)
        
        dates_str = f"{today.strftime('%Y%m%d')}-{tomorrow.strftime('%Y%m%d')}"
        url = f"{API_URL}?dates={dates_str}"
        
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("events", [])
    except Exception as e:
        print(f"Lỗi khi gọi API ESPN Fixtures: {e}")
        return []

def get_all_fixtures():
    """Lấy TOÀN BỘ lịch thi đấu của giải từ ESPN."""
    try:
        url = f"{API_URL}?dates=20260611-20260720"
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("events", [])
    except Exception as e:
        print(f"Lỗi khi gọi ESPN All Fixtures: {e}")
        return []

def get_completed_matches():
    """Lọc các trận đã kết thúc để xem tỉ số."""
    events = get_all_fixtures()
    completed = []
    for e in events:
        try:
            state = e["competitions"][0]["status"]["type"]["state"]
            if state == "post":  # Đã đá xong
                completed.append(e)
        except:
            pass
    return completed

def get_upcoming_matches():
    """Lọc các trận chưa đá hoặc đang đá để xem lịch tổng."""
    events = get_all_fixtures()
    upcoming = []
    for e in events:
        try:
            state = e["competitions"][0]["status"]["type"]["state"]
            if state in ["pre", "in"]:  # Chưa đá hoặc đang đá
                upcoming.append(e)
        except:
            pass
    return upcoming

def get_standings():
    """Lấy danh sách các bảng đấu và tự động tính điểm từ các trận đã đá."""
    # Bắt đầu với bảng điểm 0
    groups = list(FALLBACK_WC_2026_GROUPS)
    # Tạo một từ điển để map tên đội với đối tượng đội trong bảng để dễ cập nhật
    team_dict = {}
    for group in groups:
        for team in group:
            team["points"] = 0
            team["goalsDiff"] = 0
            team["goalsFor"] = 0  # Tiêu chí 3 của FIFA: Số bàn thắng ghi được
            team["played"] = 0
            team_dict[team["team"]["name"]] = team
            
    completed = get_completed_matches()
    for e in completed:
        try:
            comp = e["competitions"][0]
            competitors = comp["competitors"]
            t1_name = competitors[0]["team"]["displayName"]
            t2_name = competitors[1]["team"]["displayName"]
            
            # Kiểm tra xem đội có trong danh sách bảng (nếu là vòng loại trực tiếp có thể xử lý khác, nhưng WC thường tên đội cố định)
            if t1_name not in team_dict or t2_name not in team_dict:
                continue
                
            s1 = int(competitors[0].get("score", 0))
            s2 = int(competitors[1].get("score", 0))
            
            # Cập nhật số trận đã đá
            team_dict[t1_name]["played"] += 1
            team_dict[t2_name]["played"] += 1
            
            # Cập nhật hiệu số và số bàn thắng
            team_dict[t1_name]["goalsDiff"] += (s1 - s2)
            team_dict[t2_name]["goalsDiff"] += (s2 - s1)
            team_dict[t1_name]["goalsFor"] += s1
            team_dict[t2_name]["goalsFor"] += s2
            
            # Cập nhật điểm
            if s1 > s2:
                team_dict[t1_name]["points"] += 3
            elif s1 < s2:
                team_dict[t2_name]["points"] += 3
            else:
                team_dict[t1_name]["points"] += 1
                team_dict[t2_name]["points"] += 1
        except Exception:
            pass

    # Sau khi tính điểm, sắp xếp lại từng bảng theo chuẩn FIFA
    for group in groups:
        # Tiêu chí FIFA: 1. Điểm, 2. Hiệu số bàn thắng, 3. Tổng số bàn thắng ghi được
        group.sort(key=lambda x: (x["points"], x["goalsDiff"], x["goalsFor"]), reverse=True)
        # Cập nhật lại rank
        for idx, team in enumerate(group):
            team["rank"] = idx + 1
            
    return groups

def get_match_lineups(event_id):
    """Lấy danh sách đội hình ra sân từ ESPN Summary API."""
    try:
        url = f"http://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/summary?event={event_id}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        rosters = data.get("rosters", [])
        if not rosters or len(rosters) < 2:
            return None
            
        msg = f"📋 **ĐỘI HÌNH RA SÂN CHÍNH THỨC** 📋\n\n"
        for team_roster in rosters:
            team_name = team_roster["team"]["displayName"]
            formation = team_roster.get("formation", "Chưa rõ sơ đồ")
            msg += f"🛡 **{team_name}** (Sơ đồ: {formation})\n"
            
            starters = [p for p in team_roster.get("roster", []) if p.get("starter", False)]
            for player in starters:
                jersey = player.get("jersey", "?")
                p_name = player["athlete"]["displayName"]
                pos = player["position"].get("abbreviation", "")
                msg += f"👤 #{jersey} {p_name} ({pos})\n"
            msg += "\n"
        return msg.strip()
    except Exception as e:
        print(f"Lỗi khi lấy lineups event {event_id}: {e}")
        return None

def format_fixture_message(events):
    """Định dạng dữ liệu từ ESPN thành tin nhắn văn bản."""
    if not events:
        return "📅 Hiện tại hệ thống không ghi nhận trận đấu World Cup nào."
        
    msg = "📅 **LỊCH THI ĐẤU & TỈ SỐ TRỰC TIẾP (ESPN)** 📅\n\n"
    for event in events:
        try:
            comp = event["competitions"][0]
            competitors = comp["competitors"]
            
            # Tên 2 đội
            team1 = competitors[0]["team"]["displayName"]
            team2 = competitors[1]["team"]["displayName"]
            
            # Tỉ số (nếu có)
            score1 = competitors[0].get("score", "")
            score2 = competitors[1].get("score", "")
            
            # Trạng thái (Ví dụ: Scheduled, Halftime, Full Time)
            status = comp["status"]["type"]["shortDetail"]
            state = comp["status"]["type"]["state"]
            
            # Xử lý giờ (ESPN trả về dạng 2026-06-12T02:00Z)
            date_str = event["date"]
            dt_obj = datetime.datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            vn_tz = pytz.timezone(TIMEZONE)
            dt_vn = dt_obj.astimezone(vn_tz)
            time_str = dt_vn.strftime("%d/%m lúc %H:%M")
            
            # Hiển thị khoảng trắng nếu chưa đá, ngược lại hiển thị tỉ số
            if state == "pre":
                msg += f"⚽ {team1} **  -  ** {team2}\n"
            else:
                # Dù đang đá hay đã đá xong thì đều cập nhật tỉ số
                msg += f"⚽ {team1} **{score1} - {score2}** {team2}\n"
                
            msg += f"🕒 {time_str} | 📌 {status}\n\n"
        except Exception as e:
            print(f"Lỗi format 1 trận ESPN: {e}")
            continue
            
    return msg
