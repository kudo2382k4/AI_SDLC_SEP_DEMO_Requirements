import os
import xml.etree.ElementTree as ET
import base64
import re

src_folder = r"d:\AISDLC\Document\02_Requirements\Use Cases\Activities Flows"
files = [f for f in os.listdir(src_folder) if f.endswith(".drawio")]

meta = {
    "SF00_System_ScreenFlow.drawio": {
        "title": "SF00 — System Overview Screen Flow",
        "subtitle": "Tổng quan màn hình toàn hệ thống | Smart HSA Platform",
        "color": "#4338ca",
        "badge": "System",
        "badge_color": "#e0e7ff",
        "badge_text": "#3730a3"
    },
    "SF01_HocVien_ScreenFlow.drawio": {
        "title": "SF01 — Student Screen Flow",
        "subtitle": "Luồng màn hình Học viên | Smart HSA Platform",
        "color": "#0284c7",
        "badge": "Student",
        "badge_color": "#e0f2fe",
        "badge_text": "#0c4a6e"
    },
    "SF02_GiangVien_ScreenFlow.drawio": {
        "title": "SF02 — Lecturer Screen Flow",
        "subtitle": "Luồng màn hình Giảng viên | Smart HSA Platform",
        "color": "#047857",
        "badge": "Lecturer",
        "badge_color": "#d1fae5",
        "badge_text": "#065f46"
    },
    "SF03_QuanLy_NV_ScreenFlow.drawio": {
        "title": "SF03 — Operations Staff Screen Flow",
        "subtitle": "Luồng màn hình Quản lý / NV Vận hành | Smart HSA Platform",
        "color": "#6d28d9",
        "badge": "Ops Staff",
        "badge_color": "#ede9fe",
        "badge_text": "#4c1d95"
    },
    "SF04_GiamDoc_ScreenFlow.drawio": {
        "title": "SF04 — Center Director Screen Flow",
        "subtitle": "Luồng màn hình Giám đốc Trung tâm | Smart HSA Platform",
        "color": "#b45309",
        "badge": "Director",
        "badge_color": "#fef3c7",
        "badge_text": "#78350f"
    }
}

for fname in files:
    fpath = os.path.join(src_folder, fname)
    m = meta.get(fname, {
        "title": fname.replace(".drawio", ""),
        "subtitle": "Screen Flow | Smart HSA Platform",
        "color": "#1e293b",
        "badge": "Screen Flow",
        "badge_color": "#f1f5f9",
        "badge_text": "#475569"
    })

    with open(fpath, "r", encoding="utf-8") as f:
        drawio_xml = f.read()

    # Encode the drawio content as base64 for embedding
    encoded = base64.b64encode(drawio_xml.encode("utf-8")).decode("utf-8")
    out_name = fname.replace(".drawio", ".html")
    out_path = os.path.join(src_folder, out_name)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{m['title']} | HSA Platform Documentation</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'Inter', sans-serif; background: #f8fafc; color: #0f172a; }}

    /* ─── HEADER ─── */
    .header {{
      background: #0f172a;
      border-bottom: 3px solid {m['color']};
      padding: 0 32px;
      display: flex; align-items: center; justify-content: space-between;
      height: 60px; position: sticky; top: 0; z-index: 100;
    }}
    .header-left {{ display: flex; align-items: center; gap: 14px; }}
    .header-badge {{
      background: {m['badge_color']}; color: {m['badge_text']};
      padding: 4px 12px; border-radius: 999px; font-size: 11px; font-weight: 600; letter-spacing: 0.04em;
    }}
    .header-title {{ color: #f1f5f9; font-size: 15px; font-weight: 600; }}
    .header-subtitle {{ color: #94a3b8; font-size: 12px; margin-top: 2px; }}
    .header-meta {{ color: #64748b; font-size: 11px; }}

    /* ─── TOOLBAR ─── */
    .toolbar {{
      background: #ffffff; border-bottom: 1px solid #e2e8f0;
      padding: 10px 32px; display: flex; align-items: center; gap: 12px;
    }}
    .btn {{
      display: inline-flex; align-items: center; gap: 6px;
      padding: 7px 16px; border-radius: 7px; font-size: 13px; font-weight: 500;
      cursor: pointer; border: 1px solid #e2e8f0; background: #f8fafc; color: #374151;
      text-decoration: none; transition: all 0.15s;
    }}
    .btn:hover {{ background: #f1f5f9; border-color: #cbd5e1; }}
    .btn-primary {{ background: {m['color']}; color: #ffffff; border-color: {m['color']}; }}
    .btn-primary:hover {{ opacity: 0.9; }}
    .toolbar-sep {{ width: 1px; height: 24px; background: #e2e8f0; }}
    .zoom-info {{ font-size: 12px; color: #6b7280; margin-left: 4px; }}

    /* ─── LEGEND ─── */
    .legend {{
      background: #ffffff; border-bottom: 1px solid #e2e8f0;
      padding: 8px 32px; display: flex; align-items: center; gap: 24px; flex-wrap: wrap;
    }}
    .legend-label {{ font-size: 11px; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 0.05em; }}
    .legend-item {{ display: flex; align-items: center; gap: 6px; font-size: 11px; color: #374151; }}
    .legend-dot {{ width: 12px; height: 12px; border-radius: 2px; border: 1.5px solid; }}

    /* ─── VIEWER ─── */
    .viewer-wrap {{
      width: 100%; height: calc(100vh - 140px);
      position: relative; overflow: hidden;
    }}
    .viewer-wrap iframe {{
      width: 100%; height: 100%; border: none; display: block;
    }}

    /* ─── INFO FOOTER ─── */
    .info-footer {{
      background: #0f172a; color: #64748b; font-size: 11px;
      padding: 8px 32px; display: flex; justify-content: space-between; align-items: center;
    }}
  </style>
</head>
<body>

<!-- HEADER -->
<header class="header">
  <div class="header-left">
    <span class="header-badge">{m['badge']}</span>
    <div>
      <div class="header-title">{m['title']}</div>
      <div class="header-subtitle">{m['subtitle']}</div>
    </div>
  </div>
  <div class="header-meta">Phase 1 &nbsp;|&nbsp; BA v1.0 &nbsp;|&nbsp; Smart HSA Platform</div>
</header>

<!-- TOOLBAR -->
<nav class="toolbar">
  <a class="btn btn-primary" href="#" onclick="document.getElementById('dv').src=document.getElementById('dv').src; return false;">
    ↺ Reload
  </a>
  <div class="toolbar-sep"></div>
  <a class="btn" href="{fname}" download>⬇ Download .drawio</a>
  <a class="btn" onclick="window.print(); return false;" href="#">🖨 Print</a>
  <div class="toolbar-sep"></div>
  <span class="zoom-info">💡 Dùng Ctrl+Scroll để zoom diagram bên dưới</span>
</nav>

<!-- LEGEND -->
<div class="legend">
  <span class="legend-label">Legend:</span>
  <div class="legend-item"><div class="legend-dot" style="background:#e0e7ff;border-color:#4338ca;"></div> Hub / Dashboard Screen</div>
  <div class="legend-item"><div class="legend-dot" style="background:#fff;border-color:#374151;"></div> Regular Screen</div>
  <div class="legend-item"><div class="legend-dot" style="background:#fef9c3;border-color:#ca8a04;"></div> Auth Screen</div>
  <div class="legend-item"><div class="legend-dot" style="background:#ffedd5;border-color:#ea580c;"></div> Exam Screen</div>
  <div class="legend-item"><div class="legend-dot" style="background:#dcfce7;border-color:#16a34a;"></div> Result Screen</div>
  <div class="legend-item"><div class="legend-dot" style="background:#ffe4e6;border-color:#be123c;"></div> Error / Force Action</div>
</div>

<!-- DIAGRAM VIEWER -->
<div class="viewer-wrap">
  <iframe
    id="dv"
    src="https://viewer.diagrams.net/?tags=%7B%7D&lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&page=0#data:image/svg+xml;base64,{encoded}"
    allowfullscreen
    title="{m['title']}"
  ></iframe>
</div>

<!-- FOOTER -->
<footer class="info-footer">
  <span>{m['title']} — Smart HSA Platform Documentation</span>
  <span>Generated: 2026-04-15 &nbsp;|&nbsp; Phase 1</span>
</footer>

</body>
</html>
"""

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"OK: {out_name}")

print("All done.")
