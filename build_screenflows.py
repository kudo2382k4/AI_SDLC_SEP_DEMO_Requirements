import os

folder = r"d:\AISDLC\Document\02_Requirements\Use Cases\Activities Flows"

# Delete old HTML files
for f in os.listdir(folder):
    if f.endswith(".html"):
        os.remove(os.path.join(folder, f))
        print(f"Deleted: {f}")

# ─── Node types: (fill, stroke, fontColor, borderRadius, fontWeight)
STYLES = {
    "entry": ("background:#0f172a;color:#fff;border:2px solid #0f172a;border-radius:999px;font-weight:700;", "#0f172a"),
    "hub":   ("background:var(--hub-fill);color:var(--hub-text);border:2.5px solid var(--hub-stroke);font-weight:700;", "var(--hub-stroke)"),
    "normal":("background:#fff;color:#1e293b;border:1.5px solid #94a3b8;", "#94a3b8"),
    "auth":  ("background:#fef9c3;color:#713f12;border:1.5px solid #ca8a04;", "#ca8a04"),
    "ok":    ("background:#f0fdf4;color:#14532d;border:1.5px solid #16a34a;font-weight:600;", "#16a34a"),
    "err":   ("background:#ffe4e6;color:#881337;border:1.5px solid #be123c;", "#be123c"),
    "warn":  ("background:#fffbeb;color:#713f12;border:1.5px solid #ca8a04;", "#b45309"),
}

ARROW_COLORS = {
    "default": "#94a3b8",
    "ok":      "#16a34a",
    "err":     "#be123c",
    "accent":  "var(--hub-stroke)",
    "warn":    "#ca8a04",
}

NODE_W, NODE_H = 148, 36

def node_html(nid, nx, ny, label, ntype="normal", w=NODE_W, h=NODE_H):
    style, _ = STYLES.get(ntype, STYLES["normal"])
    return (f'<div id="n-{nid}" class="sf-node" style="left:{nx}px;top:{ny}px;width:{w}px;min-height:{h}px;'
            f'{style}">{label}</div>')

def edges_svg(nodes_map, edges):
    lines = []
    for e in edges:
        src = nodes_map.get(e["from"])
        tgt = nodes_map.get(e["to"])
        if not src or not tgt: continue
        sw, sh = src.get("w", NODE_W), src.get("h", NODE_H)
        tw, th = tgt.get("w", NODE_W), tgt.get("h", NODE_H)
        sx = src["x"] + sw // 2
        sy = src["y"] + sh // 2
        tx = tgt["x"] + tw // 2
        ty = tgt["y"] + th // 2

        # Trim to border of nodes
        dx, dy = tx - sx, ty - sy
        dl = max((dx**2 + dy**2)**0.5, 1)
        # Start: move out from src border
        if abs(dx) > abs(dy):
            ox = (sw//2 + 4) * (1 if dx > 0 else -1)
            oy = ox * dy / dx if dx else 0
        else:
            oy = (sh//2 + 4) * (1 if dy > 0 else -1)
            ox = oy * dx / dy if dy else 0
        # End: move back from tgt border
        if abs(dx) > abs(dy):
            ex = (tw//2 + 8) * (1 if dx < 0 else -1)
            ey = ex * dy / dx if dx else 0
        else:
            ey = (th//2 + 8) * (1 if dy < 0 else -1)
            ex = ey * dx / dy if dy else 0

        x1, y1 = sx + ox, sy + oy
        x2, y2 = tx + ex, ty + ey

        color = e.get("color", "#64748b")
        dashed = ' stroke-dasharray="5,3"' if e.get("dashed") else ""
        label = e.get("label", "")
        label_html = ""
        if label:
            mx = (x1+x2)/2
            my = (y1+y2)/2 - 8
            label_html = f'<text x="{mx:.0f}" y="{my:.0f}" text-anchor="middle" font-size="9" fill="{color}" font-style="italic">{label}</text>'
        lines.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{color}" stroke-width="1.5" marker-end="url(#arr-{color.replace("#","").replace("(","").replace(")","").replace(",","").replace(" ","")})" {dashed}/>'
            + label_html
        )
    return lines

def build_html(title, subtitle, sfid, accent, hub_fill, hub_stroke, hub_text,
               badge, badge_bg, badge_txt,
               nodes_list, edges_list, note, canvas_w, canvas_h):

    nodes_map = {n["id"]: n for n in nodes_list}

    # Build unique arrow marker colors
    used_colors = set(["#64748b", "#16a34a", "#be123c", "#ca8a04", hub_stroke])
    for e in edges_list:
        c = e.get("color", "#64748b")
        used_colors.add(c)

    markers = ""
    for c in used_colors:
        cid = c.replace("#","").replace("(","").replace(")","").replace(",","").replace(" ","").replace("var--hub-stroke","accent")
        markers += f'''<marker id="arr-{cid}" markerWidth="8" markerHeight="8" refX="4" refY="3" orient="auto">
          <path d="M0,0 L0,6 L8,3 z" fill="{c}"/>
        </marker>\n'''

    svg_lines = edges_svg(nodes_map, edges_list)
    nodes_html = ""
    for n in nodes_list:
        nodes_html += node_html(n["id"], n["x"], n["y"], n["label"], n.get("type","normal"), n.get("w",NODE_W), n.get("h",NODE_H))

    note_bar = f'<div class="note-bar">⚠ {note}</div>' if note else ""

    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title} | HSA Platform</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"/>
<style>
  :root{{--hub-fill:{hub_fill};--hub-stroke:{hub_stroke};--hub-text:{hub_text};}}
  *{{box-sizing:border-box;margin:0;padding:0;}}
  body{{font-family:'Inter',sans-serif;background:#f1f5f9;color:#0f172a;}}
  .hdr{{background:#0f172a;padding:0 28px;display:flex;align-items:center;justify-content:space-between;height:56px;position:sticky;top:0;z-index:50;box-shadow:0 2px 10px #0004;}}
  .hdr-l{{display:flex;align-items:center;gap:14px;}}
  .badge{{padding:3px 12px;border-radius:999px;font-size:10px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;background:{badge_bg};color:{badge_txt};}}
  .hdr-title{{color:#f1f5f9;font-size:15px;font-weight:700;}}
  .hdr-sub{{color:#94a3b8;font-size:11px;}}
  .hdr-meta{{color:#475569;font-size:11px;}}
  .legend{{background:#fff;border-bottom:1px solid #e2e8f0;padding:8px 28px;display:flex;align-items:center;gap:18px;flex-wrap:wrap;}}
  .li{{display:flex;align-items:center;gap:6px;font-size:11px;color:#475569;}}
  .ld{{width:28px;height:14px;border-radius:3px;border:1.5px solid;flex-shrink:0;}}
  .lbl{{font-size:10px;font-weight:700;color:#94a3b8;text-transform:uppercase;letter-spacing:.06em;}}
  .canvas-wrap{{overflow:auto;padding:24px 28px;background:#f8fafc;}}
  .sf-canvas{{position:relative;background:#fff;border:1px solid #e2e8f0;border-radius:12px;box-shadow:0 4px 20px #0001;overflow:visible;}}
  .sf-node{{position:absolute;display:flex;align-items:center;justify-content:center;text-align:center;border-radius:5px;font-size:10.5px;line-height:1.3;padding:6px 8px;cursor:default;transition:box-shadow .15s;}}
  .sf-node:hover{{box-shadow:0 4px 16px #0003;z-index:20;}}
  .sf-arrows{{position:absolute;top:0;left:0;pointer-events:none;overflow:visible;}}
  .note-bar{{background:#fffbeb;border-top:2px solid #fbbf24;padding:10px 28px;font-size:11.5px;color:#78350f;font-style:italic;}}
  footer{{background:#0f172a;color:#475569;text-align:center;font-size:11px;padding:10px;}}
  .section-label{{position:absolute;font-size:10px;font-weight:700;color:#94a3b8;letter-spacing:.06em;text-transform:uppercase;}}
</style>
</head>
<body>

<header class="hdr">
  <div class="hdr-l">
    <span class="badge">{badge}</span>
    <div>
      <div class="hdr-title">{title}</div>
      <div class="hdr-sub">{subtitle}</div>
    </div>
  </div>
  <div class="hdr-meta">Phase 1 &nbsp;|&nbsp; BA v1.0 &nbsp;|&nbsp; Smart HSA Platform</div>
</header>

<div class="legend">
  <span class="lbl">Legend:</span>
  <div class="li"><div class="ld" style="background:{hub_fill};border-color:{hub_stroke};"></div>Hub/Dashboard</div>
  <div class="li"><div class="ld" style="background:#fff;border-color:#94a3b8;"></div>Screen</div>
  <div class="li"><div class="ld" style="background:#fef9c3;border-color:#ca8a04;"></div>Auth/Action</div>
  <div class="li"><div class="ld" style="background:#f0fdf4;border-color:#16a34a;"></div>Success</div>
  <div class="li"><div class="ld" style="background:#ffe4e6;border-color:#be123c;"></div>Error/Rejected</div>
  <div class="li"><div class="ld" style="background:#fffbeb;border-color:#ca8a04;"></div>Pending/Warning</div>
  <div class="li"><div class="ld" style="background:#0f172a;border-color:#0f172a;border-radius:999px;"></div>Entry Point</div>
</div>

<div class="canvas-wrap">
<div class="sf-canvas" style="width:{canvas_w}px;height:{canvas_h}px;">

  <svg class="sf-arrows" width="{canvas_w}" height="{canvas_h}">
    <defs>{markers}</defs>
    {"".join(svg_lines)}
  </svg>

  {nodes_html}

</div>
</div>

{note_bar}

<footer>{title}&nbsp;|&nbsp;{subtitle}&nbsp;|&nbsp;Generated 2026-04-15</footer>
</body>
</html>"""


# ══════════════════════════════════════════════════════════════════════════════
#  SF01 — STUDENT SCREEN FLOW
# ══════════════════════════════════════════════════════════════════════════════
NW, NH = 152, 36

sf01_nodes = [
    # ── Section: PUBLIC
    {"id":"home",        "x":30,   "y":380, "label":"🏠 Home Page",               "type":"entry", "w":140,"h":40},
    {"id":"catalog",     "x":30,   "y":270, "label":"DS Khóa học công khai",       "type":"normal"},
    {"id":"course_detail","x":30,  "y":200, "label":"Chi tiết Khóa học",           "type":"normal"},
    {"id":"enroll_form", "x":30,   "y":130, "label":"Form Đăng ký KH",            "type":"normal"},
    # ── Section: AUTH
    {"id":"login",       "x":225,  "y":380, "label":"Trang Đăng nhập",            "type":"auth"},
    {"id":"register",    "x":225,  "y":460, "label":"Đăng ký Tài khoản mới",      "type":"normal"},
    {"id":"forgot_pw",   "x":225,  "y":540, "label":"Quên Mật khẩu",             "type":"normal"},
    {"id":"otp",         "x":225,  "y":620, "label":"Xác thực OTP Email",         "type":"normal"},
    {"id":"new_pw",      "x":225,  "y":700, "label":"Đặt Mật khẩu mới",          "type":"normal"},
    # ── Section: DASHBOARD
    {"id":"dashboard",   "x":430,  "y":380, "label":"📊 Dashboard Học viên",      "type":"hub", "w":170,"h":42},
    {"id":"enroll_status","x":430, "y":260, "label":"Trạng thái Đăng ký",         "type":"normal"},
    {"id":"pending",     "x":430,  "y":190, "label":"⏳ PENDING",                 "type":"warn"},
    {"id":"confirmed",   "x":430,  "y":120, "label":"✅ CONFIRMED",               "type":"ok"},
    {"id":"my_courses",  "x":430,  "y":470, "label":"Khóa học của tôi",           "type":"normal"},
    {"id":"notifs",      "x":430,  "y":540, "label":"Thông báo & Alerts",         "type":"normal"},
    {"id":"profile",     "x":430,  "y":620, "label":"Hồ sơ Học viên",            "type":"normal"},
    # ── Section: FEATURES
    {"id":"notif_detail","x":635,  "y":540, "label":"Chi tiết Thông báo",         "type":"normal"},
    {"id":"change_pw",   "x":635,  "y":620, "label":"Đổi Mật khẩu",             "type":"normal"},
    {"id":"edit_profile","x":635,  "y":700, "label":"Chỉnh sửa Hồ sơ",           "type":"normal"},
    # ── Section: COURSE
    {"id":"course_home", "x":635,  "y":380, "label":"Trang KH (Home)",            "type":"normal"},
    {"id":"lectures",    "x":635,  "y":280, "label":"Bài giảng / Tài liệu",       "type":"normal"},
    {"id":"exam_list",   "x":635,  "y":200, "label":"DS Bài Thi Thử",             "type":"normal"},
    {"id":"exam_history","x":635,  "y":120, "label":"Lịch sử Bài thi",            "type":"normal"},
    # ── Section: EXAM FLOW
    {"id":"exam_intro",  "x":840,  "y":200, "label":"Giới thiệu Bài thi",         "type":"normal"},
    {"id":"exam_ui",     "x":840,  "y":290, "label":"🖊 Giao diện Làm bài",      "type":"hub", "w":165,"h":42},
    {"id":"confirm_sub", "x":1060, "y":240, "label":"Xác nhận Nộp bài (Dialog)",  "type":"normal"},
    {"id":"force_sub",   "x":1060, "y":360, "label":"⏰ Force-Submit (Hết giờ)",  "type":"err"},
    # ── Section: RESULTS
    {"id":"result",      "x":1270, "y":180, "label":"🏆 Kết quả & Điểm số",      "type":"ok"},
    {"id":"answer_rev",  "x":1270, "y":260, "label":"Xem Lời giải Đáp án",        "type":"normal"},
    {"id":"radar",       "x":1270, "y":340, "label":"Radar Chart Năng lực",        "type":"normal"},
    {"id":"ai",          "x":1270, "y":420, "label":"Gợi ý AI Adaptive",           "type":"normal"},
    {"id":"timeline",    "x":1270, "y":500, "label":"So sánh Tiến độ",             "type":"normal"},
]

sf01_edges = [
    {"from":"home","to":"catalog"},
    {"from":"home","to":"login"},
    {"from":"catalog","to":"course_detail"},
    {"from":"course_detail","to":"enroll_form"},
    {"from":"enroll_form","to":"pending","label":"Submit"},
    {"from":"login","to":"register"},
    {"from":"login","to":"forgot_pw"},
    {"from":"login","to":"dashboard","label":"Login success","color":"#4338ca"},
    {"from":"forgot_pw","to":"otp"},
    {"from":"otp","to":"new_pw"},
    {"from":"new_pw","to":"login","label":"→ Re-login","dashed":True,"color":"#94a3b8"},
    {"from":"dashboard","to":"enroll_status"},
    {"from":"dashboard","to":"my_courses"},
    {"from":"dashboard","to":"notifs"},
    {"from":"dashboard","to":"profile"},
    {"from":"enroll_status","to":"pending"},
    {"from":"enroll_status","to":"confirmed"},
    {"from":"confirmed","to":"my_courses","color":"#16a34a"},
    {"from":"my_courses","to":"course_home"},
    {"from":"notifs","to":"notif_detail"},
    {"from":"profile","to":"change_pw"},
    {"from":"profile","to":"edit_profile"},
    {"from":"course_home","to":"lectures"},
    {"from":"course_home","to":"exam_list"},
    {"from":"course_home","to":"exam_history"},
    {"from":"exam_list","to":"exam_intro"},
    {"from":"exam_intro","to":"exam_ui"},
    {"from":"exam_ui","to":"confirm_sub","label":"Nộp bài"},
    {"from":"exam_ui","to":"force_sub","label":"Hết giờ","color":"#be123c"},
    {"from":"confirm_sub","to":"result","color":"#16a34a"},
    {"from":"force_sub","to":"result","color":"#16a34a"},
    {"from":"exam_history","to":"result","label":"view past","dashed":True,"color":"#94a3b8"},
    {"from":"result","to":"answer_rev"},
    {"from":"result","to":"radar"},
    {"from":"result","to":"ai"},
    {"from":"result","to":"timeline"},
]

# ══════════════════════════════════════════════════════════════════════════════
#  SF02 — LECTURER SCREEN FLOW
# ══════════════════════════════════════════════════════════════════════════════
sf02_nodes = [
    {"id":"login",       "x":30,   "y":340, "label":"Trang Đăng nhập",            "type":"entry","w":145,"h":40},
    # Dashboard
    {"id":"dashboard",   "x":230,  "y":340, "label":"👨‍🏫 Dashboard GV",          "type":"hub","w":165,"h":42},
    {"id":"notifs",      "x":230,  "y":430, "label":"DS Thông báo",               "type":"normal"},
    {"id":"profile",     "x":230,  "y":500, "label":"Hồ sơ Giảng viên",          "type":"normal"},
    {"id":"change_pw",   "x":230,  "y":570, "label":"Đổi Mật khẩu",             "type":"normal"},
    # Course Mgmt
    {"id":"course_list", "x":450,  "y":200, "label":"DS KH được phân công",       "type":"normal"},
    {"id":"course_dash", "x":450,  "y":280, "label":"Dashboard KH cụ thể",        "type":"hub","w":165,"h":38},
    {"id":"upload",      "x":450,  "y":360, "label":"Upload Bài giảng / Tài liệu","type":"normal"},
    {"id":"histogram",   "x":450,  "y":440, "label":"Phổ điểm KH (Histogram)",    "type":"normal"},
    {"id":"radar_class", "x":450,  "y":520, "label":"Radar Chart tập thể KH",     "type":"normal"},
    {"id":"export_rpt",  "x":450,  "y":600, "label":"Export Báo cáo KH",         "type":"normal"},
    # Student Monitoring
    {"id":"student_list","x":670,  "y":200, "label":"DS Học viên trong KH",       "type":"normal"},
    {"id":"comp_profile","x":670,  "y":280, "label":"Competency Profile HV",       "type":"hub","w":165,"h":38},
    {"id":"radar_ind",   "x":670,  "y":360, "label":"Radar Chart cá nhân HV",     "type":"normal"},
    {"id":"exam_hist",   "x":670,  "y":440, "label":"Lịch sử bài thi của HV",     "type":"normal"},
    {"id":"assign_mat",  "x":670,  "y":540, "label":"Giao tài liệu bổ trợ",       "type":"warn"},
    {"id":"assign_ok",   "x":670,  "y":620, "label":"✅ Xác nhận giao TL",        "type":"ok"},
    # Question Bank
    {"id":"qb_search",   "x":890,  "y":100, "label":"Tìm kiếm CQ trong QB",       "type":"normal"},
    {"id":"qb_mgmt",     "x":890,  "y":200, "label":"Quản lý Câu hỏi (QB)",       "type":"warn"},
    {"id":"compose",     "x":890,  "y":290, "label":"Soạn Câu hỏi đơn lẻ",        "type":"normal"},
    {"id":"import_q",    "x":890,  "y":380, "label":"Import Câu hỏi từ File",      "type":"normal"},
    {"id":"preview_q",   "x":890,  "y":460, "label":"Preview (MathJax)",           "type":"normal"},
    {"id":"tag_q",       "x":890,  "y":540, "label":"Gắn Tag Topic/Bloom/Môn",    "type":"normal"},
    {"id":"submit_q",    "x":890,  "y":620, "label":"Submit để Phê duyệt",         "type":"warn"},
    {"id":"pending_q",   "x":890,  "y":700, "label":"DS CQ đang chờ duyệt",       "type":"normal"},
    {"id":"reject_edit", "x":890,  "y":770, "label":"Hiệu chỉnh CQ Rejected",     "type":"err"},
    # Exam Creation
    {"id":"create_exam", "x":1110, "y":100, "label":"Tạo Đề thi từ QB",           "type":"warn"},
    {"id":"matrix_cfg",  "x":1110, "y":190, "label":"Cấu hình Ma trận Đề thi",    "type":"normal"},
    {"id":"preview_exam","x":1110, "y":280, "label":"Preview Đề thi",              "type":"normal"},
    {"id":"publish_exam","x":1110, "y":370, "label":"✅ Publish Đề thi vào KH",   "type":"ok"},
]

sf02_edges = [
    {"from":"login","to":"dashboard","color":"#047857"},
    {"from":"dashboard","to":"course_list"},
    {"from":"dashboard","to":"qb_mgmt"},
    {"from":"dashboard","to":"notifs"},
    {"from":"dashboard","to":"profile"},
    {"from":"profile","to":"change_pw"},
    {"from":"course_list","to":"course_dash"},
    {"from":"course_dash","to":"upload"},
    {"from":"course_dash","to":"histogram"},
    {"from":"course_dash","to":"radar_class"},
    {"from":"course_dash","to":"export_rpt"},
    {"from":"course_dash","to":"student_list"},
    {"from":"student_list","to":"comp_profile"},
    {"from":"comp_profile","to":"radar_ind"},
    {"from":"comp_profile","to":"exam_hist"},
    {"from":"comp_profile","to":"assign_mat"},
    {"from":"assign_mat","to":"assign_ok","color":"#16a34a"},
    {"from":"qb_search","to":"create_exam"},
    {"from":"qb_mgmt","to":"qb_search"},
    {"from":"qb_mgmt","to":"compose"},
    {"from":"qb_mgmt","to":"import_q"},
    {"from":"compose","to":"preview_q"},
    {"from":"import_q","to":"preview_q"},
    {"from":"compose","to":"tag_q"},
    {"from":"tag_q","to":"submit_q"},
    {"from":"submit_q","to":"pending_q"},
    {"from":"pending_q","to":"reject_edit","label":"Rejected","color":"#be123c"},
    {"from":"reject_edit","to":"submit_q","label":"Re-submit","dashed":True},
    {"from":"create_exam","to":"matrix_cfg"},
    {"from":"matrix_cfg","to":"preview_exam"},
    {"from":"preview_exam","to":"publish_exam","color":"#16a34a"},
]

# ══════════════════════════════════════════════════════════════════════════════
#  SF03 — OPS STAFF SCREEN FLOW
# ══════════════════════════════════════════════════════════════════════════════
sf03_nodes = [
    {"id":"login",      "x":30,  "y":380, "label":"Trang Đăng nhập",           "type":"entry","w":145,"h":40},
    {"id":"dashboard",  "x":230, "y":380, "label":"🧑‍💼 Dashboard Vận hành",    "type":"hub","w":170,"h":42},
    {"id":"notifs",     "x":230, "y":470, "label":"Thông báo / Alerts",         "type":"normal"},
    {"id":"staff_prof", "x":230, "y":540, "label":"Hồ sơ Nhân viên",           "type":"normal"},
    # Enrollment
    {"id":"enr_list",   "x":460, "y":180, "label":"DS Enrollment (PENDING)",    "type":"hub","w":170,"h":38},
    {"id":"enr_detail", "x":460, "y":270, "label":"Chi tiết Enrollment",        "type":"normal"},
    {"id":"payment_ck", "x":460, "y":360, "label":"Xác nhận Thanh toán",        "type":"normal"},
    {"id":"confirm",    "x":460, "y":450, "label":"✅ CONFIRM Enrollment",      "type":"ok"},
    {"id":"reject",     "x":460, "y":540, "label":"❌ REJECT + Lý do",         "type":"err"},
    {"id":"active_stu", "x":460, "y":630, "label":"DS Học viên hoạt động",     "type":"normal"},
    {"id":"broadcast",  "x":460, "y":710, "label":"Gửi Thông báo hàng loạt",   "type":"normal"},
    # Course Mgmt
    {"id":"course_list","x":690, "y":180, "label":"DS Khóa học Trung tâm",     "type":"hub","w":170,"h":38},
    {"id":"create_c",   "x":690, "y":270, "label":"Tạo Khóa học Mới",          "type":"normal"},
    {"id":"config_c",   "x":690, "y":360, "label":"Cấu hình KH (lịch,phí,sl)","type":"normal"},
    {"id":"publish_c",  "x":690, "y":450, "label":"Publish KH (Mở ĐK)",        "type":"ok"},
    {"id":"lect_list",  "x":690, "y":540, "label":"DS Giảng viên Hợp lệ",     "type":"normal"},
    {"id":"assign",     "x":690, "y":630, "label":"Phân công GV vào KH",       "type":"normal"},
    {"id":"activate",   "x":690, "y":710, "label":"✅ Xác nhận Khai giảng",    "type":"warn"},
    {"id":"cancel_c",   "x":690, "y":790, "label":"Đóng / Hủy Khóa học",      "type":"err"},
    # QB Approval
    {"id":"qb_pending", "x":920, "y":180, "label":"DS CQ chờ Phê duyệt",      "type":"warn"},
    {"id":"qb_preview", "x":920, "y":270, "label":"Xem chi tiết + Preview",    "type":"normal"},
    {"id":"qb_approve", "x":920, "y":360, "label":"✅ APPROVE → Publish QB",   "type":"ok"},
    {"id":"qb_reject",  "x":920, "y":460, "label":"❌ REJECT + Ghi chú",      "type":"err"},
    {"id":"qb_stats",   "x":920, "y":560, "label":"Kiểm tra Phân phối QB",     "type":"normal"},
    {"id":"qb_disable", "x":920, "y":650, "label":"Vô hiệu hóa CQ lỗi thời",  "type":"normal"},
    # Reporting
    {"id":"rpt_enroll", "x":1150,"y":180, "label":"Báo cáo Tuyển sinh",        "type":"normal"},
    {"id":"rpt_chart",  "x":1150,"y":270, "label":"Xem Thống kê & Biểu đồ",   "type":"normal"},
    {"id":"rpt_export", "x":1150,"y":360, "label":"Xuất File (PDF / Excel)",   "type":"ok"},
]

sf03_edges = [
    {"from":"login","to":"dashboard","color":"#6d28d9"},
    {"from":"dashboard","to":"enr_list"},
    {"from":"dashboard","to":"course_list"},
    {"from":"dashboard","to":"qb_pending"},
    {"from":"dashboard","to":"rpt_enroll"},
    {"from":"dashboard","to":"notifs"},
    {"from":"dashboard","to":"staff_prof"},
    {"from":"enr_list","to":"enr_detail"},
    {"from":"enr_detail","to":"payment_ck"},
    {"from":"payment_ck","to":"confirm","label":"OK","color":"#16a34a"},
    {"from":"payment_ck","to":"reject","label":"Không HV","color":"#be123c"},
    {"from":"enr_list","to":"active_stu"},
    {"from":"active_stu","to":"broadcast"},
    {"from":"course_list","to":"create_c"},
    {"from":"create_c","to":"config_c"},
    {"from":"config_c","to":"publish_c"},
    {"from":"course_list","to":"lect_list"},
    {"from":"lect_list","to":"assign"},
    {"from":"assign","to":"activate"},
    {"from":"publish_c","to":"activate","label":"Đủ HV"},
    {"from":"course_list","to":"cancel_c","label":"Hủy","color":"#be123c"},
    {"from":"qb_pending","to":"qb_preview"},
    {"from":"qb_preview","to":"qb_approve","label":"Approved","color":"#16a34a"},
    {"from":"qb_preview","to":"qb_reject","label":"Rejected","color":"#be123c"},
    {"from":"qb_pending","to":"qb_stats"},
    {"from":"qb_pending","to":"qb_disable"},
    {"from":"rpt_enroll","to":"rpt_chart"},
    {"from":"rpt_chart","to":"rpt_export"},
]

# ══════════════════════════════════════════════════════════════════════════════
#  SF04 — DIRECTOR SCREEN FLOW
# ══════════════════════════════════════════════════════════════════════════════
sf04_nodes = [
    {"id":"login",      "x":30,  "y":300, "label":"Trang Đăng nhập",           "type":"entry","w":145,"h":40},
    {"id":"dashboard",  "x":230, "y":300, "label":"👔 Dashboard KPI TT",        "type":"hub","w":170,"h":42},
    {"id":"dir_prof",   "x":230, "y":400, "label":"Hồ sơ Giám đốc",            "type":"normal"},
    {"id":"sys_notif",  "x":230, "y":470, "label":"Thông báo Hệ thống",         "type":"normal"},
    # Analytics
    {"id":"revenue",    "x":460, "y":120, "label":"Doanh thu & Tuyển sinh",     "type":"warn"},
    {"id":"enroll_chart","x":460,"y":200, "label":"Biểu đồ Tuyển sinh/tháng",  "type":"normal"},
    {"id":"completion", "x":460, "y":280, "label":"Tỷ lệ Hoàn thành KH",       "type":"warn"},
    {"id":"alert_kh",   "x":460, "y":360, "label":"⚠ Cảnh báo KH chưa đủ HV", "type":"err"},
    {"id":"score_dist", "x":460, "y":440, "label":"Phổ điểm thi Toàn TT",      "type":"warn"},
    {"id":"exam_total", "x":460, "y":520, "label":"Tổng lượt thi & Điểm TB",   "type":"normal"},
    # Operational
    {"id":"all_courses","x":690, "y":120, "label":"DS Khóa học (All Statuses)", "type":"normal"},
    {"id":"course_cmp", "x":690, "y":200, "label":"Thống kê theo KH (Compare)","type":"normal"},
    {"id":"lect_list",  "x":690, "y":300, "label":"DS Giảng viên & Phân công", "type":"normal"},
    {"id":"lect_perf",  "x":690, "y":390, "label":"Thống kê Hiệu suất GV",     "type":"normal"},
    # Reporting & Approval
    {"id":"proposals",  "x":920, "y":120, "label":"DS Đề xuất mở KH Mới",      "type":"warn"},
    {"id":"prop_detail","x":920, "y":210, "label":"Chi tiết đề xuất KH",        "type":"normal"},
    {"id":"approve_kh", "x":920, "y":300, "label":"✅ Phê duyệt mở KH",        "type":"ok"},
    {"id":"rpt_page",   "x":920, "y":400, "label":"Trang Xuất Báo cáo Tổng hợp","type":"normal"},
    {"id":"download",   "x":920, "y":490, "label":"Download PDF / Excel",       "type":"ok"},
]

sf04_edges = [
    {"from":"login","to":"dashboard","color":"#b45309"},
    {"from":"dashboard","to":"revenue"},
    {"from":"dashboard","to":"completion"},
    {"from":"dashboard","to":"score_dist"},
    {"from":"dashboard","to":"all_courses"},
    {"from":"dashboard","to":"proposals"},
    {"from":"dashboard","to":"dir_prof"},
    {"from":"dashboard","to":"sys_notif"},
    {"from":"dashboard","to":"rpt_page"},
    {"from":"revenue","to":"enroll_chart"},
    {"from":"score_dist","to":"exam_total"},
    {"from":"completion","to":"alert_kh","label":"Alert","color":"#be123c"},
    {"from":"all_courses","to":"course_cmp"},
    {"from":"all_courses","to":"lect_list"},
    {"from":"lect_list","to":"lect_perf"},
    {"from":"proposals","to":"prop_detail"},
    {"from":"prop_detail","to":"approve_kh","label":"Approved","color":"#16a34a"},
    {"from":"rpt_page","to":"download"},
]

# ══════════════════════════════════════════════════════════════════════════════
#  SF00 — SYSTEM MASTER SCREEN FLOW
# ══════════════════════════════════════════════════════════════════════════════
sf00_nodes = [
    {"id":"home",      "x":30,  "y":380, "label":"🏠 Home Page / Landing",     "type":"entry","w":165,"h":42},
    {"id":"catalog",   "x":30,  "y":250, "label":"DS Khóa học & GV (Public)",  "type":"normal"},
    {"id":"detail",    "x":30,  "y":180, "label":"Chi tiết Khóa học",          "type":"normal"},
    {"id":"login",     "x":250, "y":380, "label":"Trang Đăng nhập",            "type":"auth"},
    # Student
    {"id":"s_dash",    "x":470, "y":140, "label":"Dashboard Học viên",         "type":"hub","w":158,"h":38},
    {"id":"s_courses", "x":680, "y":90,  "label":"Khóa học của tôi",           "type":"normal"},
    {"id":"s_enroll",  "x":680, "y":160, "label":"Trạng thái ĐK",             "type":"normal"},
    {"id":"s_exam",    "x":880, "y":90,  "label":"Giao diện Thi Thử",          "type":"normal"},
    {"id":"s_result",  "x":1080,"y":90,  "label":"Kết quả & Radar Chart",      "type":"ok"},
    {"id":"s_ai",      "x":1080,"y":160, "label":"Gợi ý AI Adaptive",          "type":"normal"},
    # Lecturer
    {"id":"l_dash",    "x":470, "y":300, "label":"Dashboard Giảng viên",       "type":"hub","w":158,"h":38},
    {"id":"l_qb",      "x":680, "y":260, "label":"Quản lý Câu hỏi (QB)",       "type":"normal"},
    {"id":"l_khdash",  "x":680, "y":330, "label":"Dashboard Khóa học",         "type":"normal"},
    {"id":"l_student", "x":880, "y":295, "label":"Profile Học viên",           "type":"normal"},
    # Ops
    {"id":"o_dash",    "x":470, "y":460, "label":"Dashboard Vận hành",         "type":"hub","w":158,"h":38},
    {"id":"o_enroll",  "x":680, "y":440, "label":"DS Enrollment Mới",          "type":"normal"},
    {"id":"o_confirm", "x":880, "y":440, "label":"Confirm / Reject",           "type":"normal"},
    {"id":"o_course",  "x":680, "y":510, "label":"Quản lý Khóa học",           "type":"normal"},
    {"id":"o_qb",      "x":880, "y":510, "label":"Phê duyệt Câu hỏi",         "type":"normal"},
    # Director
    {"id":"d_dash",    "x":470, "y":620, "label":"Dashboard KPI TT",           "type":"hub","w":158,"h":38},
    {"id":"d_kpi",     "x":680, "y":600, "label":"Doanh thu & Tuyển sinh",     "type":"normal"},
    {"id":"d_perf",    "x":680, "y":670, "label":"Hiệu suất KH & GV",         "type":"normal"},
    {"id":"d_report",  "x":880, "y":635, "label":"Xuất Báo cáo Tổng hợp",     "type":"normal"},
    # Parent
    {"id":"p_report",  "x":470, "y":750, "label":"📧 Báo cáo HT con (Email)", "type":"err","w":170,"h":36},
    {"id":"p_radar",   "x":690, "y":750, "label":"Radar Chart con",            "type":"normal"},
]

sf00_edges = [
    {"from":"home","to":"catalog"},
    {"from":"home","to":"login"},
    {"from":"catalog","to":"detail"},
    {"from":"login","to":"s_dash","label":"Học viên","color":"#4338ca"},
    {"from":"login","to":"l_dash","label":"Giảng viên","color":"#047857"},
    {"from":"login","to":"o_dash","label":"Quản lý/NV","color":"#6d28d9"},
    {"from":"login","to":"d_dash","label":"Giám đốc","color":"#b45309"},
    {"from":"s_dash","to":"s_courses"},
    {"from":"s_dash","to":"s_enroll"},
    {"from":"s_courses","to":"s_exam"},
    {"from":"s_exam","to":"s_result"},
    {"from":"s_result","to":"s_ai"},
    {"from":"l_dash","to":"l_qb"},
    {"from":"l_dash","to":"l_khdash"},
    {"from":"l_khdash","to":"l_student"},
    {"from":"o_dash","to":"o_enroll"},
    {"from":"o_enroll","to":"o_confirm"},
    {"from":"o_dash","to":"o_course"},
    {"from":"o_course","to":"o_qb"},
    {"from":"d_dash","to":"d_kpi"},
    {"from":"d_dash","to":"d_perf"},
    {"from":"d_dash","to":"d_report"},
    {"from":"p_report","to":"p_radar","dashed":True,"color":"#be123c"},
]


# ── Generate all files ──────────────────────────────────────────────────────
configs = [
    ("SF00_System_ScreenFlow.html",
     "SF00 — System Master Screen Flow",
     "Tổng quan Luồng Màn hình toàn Hệ thống | Smart HSA Platform",
     "SF00", "#1e293b", "#e2e8f0", "#1e293b", "#0f172a",
     "System", "#e2e8f0", "#1e293b",
     sf00_nodes, sf00_edges, "", 1300, 860),

    ("SF01_Student_ScreenFlow.html",
     "SF01 — Student Screen Flow",
     "Luồng màn hình Học viên | 32 màn hình | Smart HSA Platform",
     "SF01", "#4338ca", "#eef2ff", "#4338ca", "#1e1b4b",
     "Student", "#e0e7ff", "#3730a3",
     sf01_nodes, sf01_edges,
     "Học viên chỉ truy cập Course sau khi Enrollment = CONFIRMED. Không có nút Pause trong giờ thi. Force-Submit khi hết giờ.",
     1500, 800),

    ("SF02_Lecturer_ScreenFlow.html",
     "SF02 — Lecturer Screen Flow",
     "Luồng màn hình Giảng viên | 29 màn hình | Smart HSA Platform",
     "SF02", "#047857", "#d1fae5", "#047857", "#022c22",
     "Lecturer", "#d1fae5", "#065f46",
     sf02_nodes, sf02_edges,
     "Giảng viên chỉ xem dữ liệu KH được phân công. QB Search chỉ trả câu hỏi của chính GV đó.",
     1380, 860),

    ("SF03_OpsStaff_ScreenFlow.html",
     "SF03 — Operations Staff Screen Flow",
     "Luồng màn hình Quản lý / NV Vận hành | 27 màn hình | Smart HSA Platform",
     "SF03", "#6d28d9", "#ede9fe", "#6d28d9", "#2e1065",
     "Ops Staff", "#ede9fe", "#4c1d95",
     sf03_nodes, sf03_edges,
     "Confirm Enrollment chỉ thực hiện ĐƯỢC sau khi Xác nhận Thanh toán hợp lệ.",
     1400, 880),

    ("SF04_Director_ScreenFlow.html",
     "SF04 — Director Screen Flow",
     "Luồng màn hình Giám đốc Trung tâm | 18 màn hình | Smart HSA Platform",
     "SF04", "#b45309", "#fef3c7", "#b45309", "#78350f",
     "Director", "#fef3c7", "#78350f",
     sf04_nodes, sf04_edges,
     "Giám đốc = Read-only toàn bộ hệ thống. Write permission chỉ tại: Phê duyệt mở Khóa học (UC-GD-01).",
     1200, 640),
]

for (fname, title, subtitle, sfid, accent, hub_fill, hub_stroke, hub_text,
     badge, badge_bg, badge_txt, nodes, edges, note, cw, ch) in configs:
    html = build_html(title, subtitle, sfid, accent, hub_fill, hub_stroke, hub_text,
                      badge, badge_bg, badge_txt, nodes, edges, note, cw, ch)
    path = os.path.join(folder, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Created: {fname}")

print("\nAll done!")
