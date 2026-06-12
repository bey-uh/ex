import streamlit as st
import json
import os
from datetime import datetime, date, timedelta
import calendar

# ── 페이지 설정 ───────────────────────────────────────────────
st.set_page_config(
    page_title="일정 관리",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 커스텀 CSS ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

/* 배경 */
.stApp { background-color: #F7F8FC; }

/* 사이드바 */
section[data-testid="stSidebar"] {
    background-color: #1E1F2E;
}
section[data-testid="stSidebar"] * {
    color: #E8E9F3 !important;
}
/* 입력 필드 안의 텍스트는 검은색 */
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea,
section[data-testid="stSidebar"] .stTextInput input,
section[data-testid="stSidebar"] .stTextArea textarea,
section[data-testid="stSidebar"] [data-baseweb="select"] [data-testid="stMarkdownContainer"] p,
section[data-testid="stSidebar"] [data-baseweb="input"] input,
section[data-testid="stSidebar"] [data-baseweb="textarea"] textarea,
section[data-testid="stSidebar"] div[data-baseweb="select"] div,
section[data-testid="stSidebar"] [role="listbox"] li,
section[data-testid="stSidebar"] [data-baseweb="select"] span {
    color: #111111 !important;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stTextInput label,
section[data-testid="stSidebar"] .stDateInput label,
section[data-testid="stSidebar"] .stTextArea label,
section[data-testid="stSidebar"] .stTimeInput label,
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stMultiSelect label {
    color: #A0A3B1 !important;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* 카테고리 배지 */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.03em;
}
.badge-work    { background:#E8F0FE; color:#1967D2; }
.badge-personal{ background:#FCE8F3; color:#B5245F; }
.badge-health  { background:#E6F4EA; color:#1E8E3E; }
.badge-study   { background:#FFF3E0; color:#E65100; }
.badge-other   { background:#F3E8FF; color:#6B2FA0; }

/* 일정 카드 */
.schedule-card {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 10px;
    border-left: 4px solid #4F46E5;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    transition: box-shadow .2s;
}
.schedule-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.10); }
.card-work     { border-left-color: #1967D2; }
.card-personal { border-left-color: #B5245F; }
.card-health   { border-left-color: #1E8E3E; }
.card-study    { border-left-color: #E65100; }
.card-other    { border-left-color: #6B2FA0; }

.card-title {
    font-size: 1rem;
    font-weight: 700;
    color: #1A1B2E;
    margin-bottom: 4px;
}
.card-meta {
    font-size: 0.8rem;
    color: #6B7280;
    margin-bottom: 6px;
}
.card-desc {
    font-size: 0.85rem;
    color: #4B5563;
    line-height: 1.5;
}

/* 캘린더 그리드 */
.cal-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 4px;
    margin-top: 12px;
}
.cal-header {
    text-align: center;
    font-size: 0.72rem;
    font-weight: 700;
    color: #6B7280;
    padding: 6px 0;
    letter-spacing: 0.06em;
}
.cal-day {
    background: #FFFFFF;
    border-radius: 8px;
    padding: 8px 6px;
    min-height: 72px;
    font-size: 0.8rem;
    color: #374151;
    cursor: default;
    border: 1px solid #E9EAF0;
}
.cal-day-today {
    background: #4F46E5;
    color: #FFFFFF !important;
    border-color: #4F46E5;
}
.cal-day-other { opacity: 0.35; }
.cal-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    display: inline-block;
    margin: 1px;
}

/* 통계 박스 */
.stat-box {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 18px 22px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    text-align: center;
}
.stat-num { font-size: 2rem; font-weight: 700; color: #1A1B2E; }
.stat-lbl { font-size: 0.78rem; color: #6B7280; margin-top: 2px; }

/* 버튼 */
.stButton > button {
    background: #4F46E5;
    color: #FFFFFF !important;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 0.45rem 1.2rem;
    transition: background .2s;
}
.stButton > button:hover { background: #4338CA; }

/* 헤더 타이틀 */
.page-title {
    font-size: 1.6rem;
    font-weight: 700;
    color: #1A1B2E;
    margin-bottom: 0;
}
.page-sub {
    font-size: 0.85rem;
    color: #9CA3AF;
    margin-bottom: 20px;
}

/* 탭 */
.stTabs [data-baseweb="tab-list"] {
    background: #EEEEF6;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px;
    font-weight: 500;
    color: #6B7280;
}
.stTabs [aria-selected="true"] {
    background: #FFFFFF !important;
    color: #4F46E5 !important;
    font-weight: 700;
}

hr { border-color: #E9EAF0; margin: 16px 0; }
</style>
""", unsafe_allow_html=True)

# ── 데이터 저장/불러오기 ──────────────────────────────────────
DATA_FILE = "schedules.json"

def load_schedules():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_schedules(schedules):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(schedules, f, ensure_ascii=False, indent=2)

if "schedules" not in st.session_state:
    st.session_state.schedules = load_schedules()
if "edit_idx" not in st.session_state:
    st.session_state.edit_idx = None

# ── 헬퍼 ─────────────────────────────────────────────────────
CATEGORY_MAP = {
    "업무":   ("work",     "💼"),
    "개인":   ("personal", "🏠"),
    "건강":   ("health",   "💪"),
    "학습":   ("study",    "📚"),
    "기타":   ("other",    "✨"),
}
PRIORITY_EMOJI = {"높음": "🔴", "보통": "🟡", "낮음": "🟢"}

def cat_key(label):
    return CATEGORY_MAP.get(label, ("other", ""))[0]

def render_badge(cat_label):
    key = cat_key(cat_label)
    emoji = CATEGORY_MAP.get(cat_label, ("", ""))[1]
    return f'<span class="badge badge-{key}">{emoji} {cat_label}</span>'

def schedules_on(d: date):
    ds = str(d)
    return [s for s in st.session_state.schedules if s["date"] == ds]

def color_for(cat_label):
    colors = {
        "업무": "#1967D2", "개인": "#B5245F",
        "건강": "#1E8E3E", "학습": "#E65100", "기타": "#6B2FA0",
    }
    return colors.get(cat_label, "#4F46E5")

# ── 사이드바: 일정 추가 / 수정 ────────────────────────────────
with st.sidebar:
    st.markdown("## 📅 일정 관리")
    st.markdown("---")

    editing = st.session_state.edit_idx is not None
    if editing:
        st.markdown("### ✏️ 일정 수정")
        s = st.session_state.schedules[st.session_state.edit_idx]
        default_title    = s["title"]
        default_date     = date.fromisoformat(s["date"])
        _s = s.get("start_time", "09:00")
        _e = s.get("end_time",   "10:00")
        default_start    = datetime.strptime(_s, "%H:%M").time()
        default_end      = datetime.strptime(_e, "%H:%M").time()
        default_cat      = s.get("category",   "업무")
        default_priority = s.get("priority",   "보통")
        default_desc     = s.get("description","")
    else:
        st.markdown("### ➕ 새 일정 추가")
        default_title    = ""
        default_date     = date.today()
        default_start    = datetime.strptime("09:00", "%H:%M").time()
        default_end      = datetime.strptime("10:00", "%H:%M").time()
        default_cat      = "업무"
        default_priority = "보통"
        default_desc     = ""

    title    = st.text_input("제목",        value=default_title,    placeholder="일정 제목을 입력하세요")
    sel_date = st.date_input("날짜",        value=default_date)
    c1, c2   = st.columns(2)
    start_t  = c1.time_input("시작 시간", value=default_start)
    end_t    = c2.time_input("종료 시간", value=default_end)
    category = st.selectbox("카테고리",     list(CATEGORY_MAP.keys()),
                            index=list(CATEGORY_MAP.keys()).index(default_cat))
    priority = st.selectbox("우선순위",     ["높음", "보통", "낮음"],
                            index=["높음", "보통", "낮음"].index(default_priority))
    desc     = st.text_area("메모",         value=default_desc,     placeholder="추가 메모 (선택)", height=90)

    st.markdown("")
    btn_label = "💾 수정 저장" if editing else "➕ 일정 추가"
    if st.button(btn_label, use_container_width=True):
        if title.strip():
            entry = {
                "title":       title.strip(),
                "date":        str(sel_date),
                "start_time":  start_t.strftime("%H:%M"),
                "end_time":    end_t.strftime("%H:%M"),
                "category":    category,
                "priority":    priority,
                "description": desc,
                "created_at":  datetime.now().isoformat(),
            }
            if editing:
                st.session_state.schedules[st.session_state.edit_idx] = entry
                st.session_state.edit_idx = None
                st.success("일정이 수정되었습니다!")
            else:
                st.session_state.schedules.append(entry)
                st.success("일정이 추가되었습니다!")
            save_schedules(st.session_state.schedules)
            st.rerun()
        else:
            st.warning("제목을 입력해 주세요.")

    if editing:
        if st.button("❌ 취소", use_container_width=True):
            st.session_state.edit_idx = None
            st.rerun()

    st.markdown("---")
    # 필터
    st.markdown("#### 🔍 필터")
    filter_cat  = st.multiselect("카테고리", list(CATEGORY_MAP.keys()), default=list(CATEGORY_MAP.keys()))
    filter_prio = st.multiselect("우선순위", ["높음", "보통", "낮음"], default=["높음", "보통", "낮음"])

# ── 메인 영역 ─────────────────────────────────────────────────
today = date.today()
filtered = [
    s for s in st.session_state.schedules
    if s.get("category", "기타") in filter_cat
    and s.get("priority", "보통") in filter_prio
]
filtered_sorted = sorted(filtered, key=lambda x: (x["date"], x.get("start_time", "")))

st.markdown(f'<p class="page-title">📅 내 일정</p>', unsafe_allow_html=True)
st.markdown(f'<p class="page-sub">오늘은 {today.strftime("%Y년 %m월 %d일")} 입니다</p>', unsafe_allow_html=True)

# 통계
total   = len(st.session_state.schedules)
today_n = len(schedules_on(today))
week_n  = len([s for s in st.session_state.schedules
               if today <= date.fromisoformat(s["date"]) <= today + timedelta(days=6)])
high_n  = len([s for s in st.session_state.schedules if s.get("priority") == "높음"])

sc1, sc2, sc3, sc4 = st.columns(4)
for col, num, lbl in [
    (sc1, total,   "전체 일정"),
    (sc2, today_n, "오늘 일정"),
    (sc3, week_n,  "이번 주 일정"),
    (sc4, high_n,  "높은 우선순위"),
]:
    col.markdown(f"""
    <div class="stat-box">
        <div class="stat-num">{num}</div>
        <div class="stat-lbl">{lbl}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("")
tab_list, tab_cal, tab_all = st.tabs(["📋 목록", "📆 캘린더", "🗂 전체 보기"])

# ── 탭 1: 목록 ───────────────────────────────────────────────
with tab_list:
    view_date = st.date_input("날짜 선택", value=today, key="view_date")
    day_scheds = [s for s in filtered_sorted if s["date"] == str(view_date)]

    st.markdown(f"**{view_date.strftime('%Y년 %m월 %d일')}** — {len(day_scheds)}개 일정")
    if not day_scheds:
        st.info("이 날에 등록된 일정이 없습니다.")
    else:
        for i, s in enumerate(day_scheds):
            idx = st.session_state.schedules.index(s)
            key = cat_key(s.get("category", "기타"))
            prio_e = PRIORITY_EMOJI.get(s.get("priority","보통"),"")
            st.markdown(f"""
            <div class="schedule-card card-{key}">
                <div class="card-title">{prio_e} {s['title']}</div>
                <div class="card-meta">
                    🕐 {s.get('start_time','')} – {s.get('end_time','')} &nbsp;|&nbsp;
                    {render_badge(s.get('category','기타'))}
                </div>
                {"<div class='card-desc'>" + s['description'] + "</div>" if s.get('description') else ""}
            </div>""", unsafe_allow_html=True)
            col_e, col_d, _ = st.columns([1, 1, 5])
            if col_e.button("✏️ 수정", key=f"edit_{idx}"):
                st.session_state.edit_idx = idx
                st.rerun()
            if col_d.button("🗑️ 삭제", key=f"del_{idx}"):
                st.session_state.schedules.pop(idx)
                save_schedules(st.session_state.schedules)
                st.rerun()

# ── 탭 2: 캘린더 ─────────────────────────────────────────────
with tab_cal:
    cy, cm = st.columns([1, 3])
    yr  = cy.number_input("년",  value=today.year,  min_value=2000, max_value=2100, step=1)
    mon = cm.selectbox("월", range(1, 13),
                       index=today.month - 1,
                       format_func=lambda x: f"{x}월")
    yr, mon = int(yr), int(mon)

    days_ko  = ["월", "화", "수", "목", "금", "토", "일"]
    cal_days = calendar.monthcalendar(yr, mon)
    cat_colors = {k: color_for(k) for k in CATEGORY_MAP}

    header_html = '<div class="cal-grid">'
    for d in days_ko:
        header_html += f'<div class="cal-header">{d}</div>'
    header_html += '</div>'
    st.markdown(header_html, unsafe_allow_html=True)

    grid_html = '<div class="cal-grid">'
    for week in cal_days:
        for day in week:
            if day == 0:
                grid_html += '<div class="cal-day cal-day-other"></div>'
                continue
            d = date(yr, mon, day)
            is_today = (d == today)
            day_class = "cal-day-today" if is_today else "cal-day"
            dots = "".join(
                f'<span class="cal-dot" style="background:{color_for(s.get("category","기타"))}"></span>'
                for s in schedules_on(d)[:4]
            )
            grid_html += f'<div class="cal-day {day_class}"><strong>{day}</strong><br>{dots}</div>'
    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)

    st.markdown("---")
    month_scheds = [s for s in filtered_sorted
                    if s["date"].startswith(f"{yr:04d}-{mon:02d}")]
    st.markdown(f"**{yr}년 {mon}월** 전체 일정 — {len(month_scheds)}개")
    if not month_scheds:
        st.info("이 달에 등록된 일정이 없습니다.")
    else:
        for s in month_scheds:
            idx = st.session_state.schedules.index(s)
            key = cat_key(s.get("category", "기타"))
            prio_e = PRIORITY_EMOJI.get(s.get("priority","보통"),"")
            dt = date.fromisoformat(s["date"])
            st.markdown(f"""
            <div class="schedule-card card-{key}">
                <div class="card-title">{prio_e} {s['title']}</div>
                <div class="card-meta">
                    📅 {dt.strftime('%m월 %d일')} &nbsp;
                    🕐 {s.get('start_time','')} – {s.get('end_time','')} &nbsp;|&nbsp;
                    {render_badge(s.get('category','기타'))}
                </div>
                {"<div class='card-desc'>" + s['description'] + "</div>" if s.get('description') else ""}
            </div>""", unsafe_allow_html=True)
            col_e, col_d, _ = st.columns([1, 1, 5])
            if col_e.button("✏️", key=f"cal_edit_{idx}"):
                st.session_state.edit_idx = idx
                st.rerun()
            if col_d.button("🗑️", key=f"cal_del_{idx}"):
                st.session_state.schedules.pop(idx)
                save_schedules(st.session_state.schedules)
                st.rerun()

# ── 탭 3: 전체 보기 ───────────────────────────────────────────
with tab_all:
    st.markdown(f"전체 **{len(filtered_sorted)}**개 일정")
    if not filtered_sorted:
        st.info("등록된 일정이 없습니다. 사이드바에서 일정을 추가해 보세요!")
    else:
        for s in filtered_sorted:
            idx = st.session_state.schedules.index(s)
            key = cat_key(s.get("category", "기타"))
            prio_e = PRIORITY_EMOJI.get(s.get("priority","보통"),"")
            dt = date.fromisoformat(s["date"])
            st.markdown(f"""
            <div class="schedule-card card-{key}">
                <div class="card-title">{prio_e} {s['title']}</div>
                <div class="card-meta">
                    📅 {dt.strftime('%Y년 %m월 %d일')} &nbsp;
                    🕐 {s.get('start_time','')} – {s.get('end_time','')} &nbsp;|&nbsp;
                    {render_badge(s.get('category','기타'))}
                </div>
                {"<div class='card-desc'>" + s['description'] + "</div>" if s.get('description') else ""}
            </div>""", unsafe_allow_html=True)
            col_e, col_d, _ = st.columns([1, 1, 5])
            if col_e.button("✏️ 수정", key=f"all_edit_{idx}"):
                st.session_state.edit_idx = idx
                st.rerun()
            if col_d.button("🗑️ 삭제", key=f"all_del_{idx}"):
                st.session_state.schedules.pop(idx)
                save_schedules(st.session_state.schedules)
                st.rerun()