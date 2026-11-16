"""Sinh tasks/phan-cong-4-tuan.xlsx + tasks/todo.md cho vCraft.

Chạy: python scripts/gen_assignment_xlsx.py
Ghi đè file Excel và file markdown. Muốn sửa kế hoạch thì sửa TASKS dưới đây rồi chạy lại.
"""

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from pathlib import Path
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]

MEN_LAM = "1B3A6B"
DAT_NUNG = "B4552D"
TRANG_NGA = "F7F3EA"
GRID = "D9D3C7"
TEXT = "22201D"

STATUSES = [
    ("Chưa làm", "E5E7EB", "chưa bắt đầu: chưa có nhánh, chưa có commit"),
    ("Đang làm", "FEF3C7", "đang code, tự tiến được: đã có nhánh và ≥1 commit"),
    ("Đang chờ", "FEE2E2", "bị chặn bởi người/task khác — BẮT BUỘC ghi cột “Chờ”"),
    ("Hoàn thành", "D1FAE5", "PR đã merge + test pass + demo được + có link bằng chứng"),
    ("Bỏ (đã cắt)", "D1D5DB", "cắt khỏi V1 theo quy tắc cắt, có ghi lý do"),
]

A = "Phan Anh"
Q = "Quân"
D = "Đông"
ALL = "Cả nhóm"

TASKS = [
    # week 1
    (1, "T1.1", "Repo GitHub, .gitignore, .gitattributes", D, "", "repo + 3 người clone được", "`git push` thành công, 3 người clone được", "Must", "2026-11-18"),
    (1, "T1.2", "Docker Compose (db + api + web)", A, D, "deploy/docker-compose.yml", "`make up` chạy, 3 service healthy", "Must", "2026-11-19"),
    (1, "T1.3", ".env.example + Makefile (up/down/seed/test/logs)", D, "", "Makefile, .env.example", "người mới chạy 1 lệnh là có app", "Must", "2026-11-19"),
    (1, "T1.4", "Schema 19 bảng + Alembic migration đầu", A, "", "backend/app/models/, alembic/", "`alembic upgrade head` sạch trên DB trống", "Must", "2026-11-21"),
    (1, "T1.5", "Auth: JWT cookie httpOnly, argon2, role dependency", A, "", "routers/auth.py, core/security.py", "3 vai trò đăng nhập, sai role bị 403", "Must", "2026-11-21"),
    (1, "T1.6", "docs/api.md → OpenAPI → type TS cho FE", A, Q, "openapi.json + src/lib/api.ts", "FE gọi /api/auth/me bằng type sinh tự động", "Must", "2026-11-23"),
    (1, "T1.7", "Design tokens + layout + trang đăng nhập/đăng ký", Q, "", "design-tokens.ts, tailwind.config.ts, routes/auth/", "2 trang chạy, responsive 320/1440", "Must", "2026-11-23"),
    (1, "T1.8", "Seed data Bát Tràng (5 hộ, 40-60 SP, 4 đơn, 5 ghim, 4 tin)", D, "", "backend/app/seed/", "`make seed` chạy 2 lần không nhân đôi dữ liệu", "Must", "2026-11-23"),
    (1, "T1.9", "Smoke test schema portable (tạo schema + CRUD trên SQLite)", D, "", "tests/test_schema_portable.py", "pytest pass — chứng minh độc lập CSDL", "Must", "2026-11-23"),
    (1, "T1.10", "MỐC TUẦN 1", ALL, "", "—", "`make up` + login 3 vai trò + seed có dữ liệu", "Mốc", "2026-11-23"),
    # week 2
    (2, "T2.1", "Hồ sơ xưởng CRUD + ảnh + chứng nhận", A, "", "routers/workshops.py", "artisan sửa hồ sơ, trang công khai cập nhật", "Must", "2026-11-25"),
    (2, "T2.2", "Sản phẩm CRUD + lọc + tìm + phân trang", A, "", "routers/products.py", "200 SP lọc/tìm < 1 giây", "Must", "2026-11-26"),
    (2, "T2.3", "Pipeline ảnh: Pillow WebP 400/1200 + magic bytes + ≤10MB", A, "", "services/image_pipeline.py", "upload 5 ảnh, 1 ảnh lỗi không chặn ảnh khác", "Must", "2026-11-27"),
    (2, "T2.4", "Nhật ký sản xuất + QR + trang /p/{token}", A, "", "services/qr_service.py, routers/public.py", "quét điện thoại mở đúng trang, không cần login", "Must", "2026-11-28"),
    (2, "T2.5", "Danh mục UI: lọc hộ/phân loại, tìm, skeleton/empty/error", Q, "", "features/catalog/", "đủ 4 trạng thái, không cuộn ngang", "Must", "2026-11-26"),
    (2, "T2.6", "Bản đồ + ghim + popup + lazy-load", Q, "", "features/map/", "5 ghim đúng vị trí, click ra popup", "Should", "2026-11-27"),
    (2, "T2.7", "Upload UI: progress từng ảnh, lỗi riêng từng ảnh", Q, "", "features/upload/", "upload 5 ảnh thấy 5 progress", "Must", "2026-11-28"),
    (2, "T2.8", "F13 nhập liệu: autocomplete, tự điền, format giá/ngày, lỗi theo field", Q, "", "features/forms/", "gõ 2 ký tự ra gợi ý, chọn bằng bàn phím", "Must", "2026-11-29"),
    (2, "T2.9", "Admin duyệt hộ (F2) + tin cộng đồng (F11)", D, A, "routers/admin.py", "duyệt → đăng nhập được; từ chối có lý do", "Must", "2026-11-28"),
    (2, "T2.10", "Test auth + sản phẩm + upload", D, "", "tests/test_auth.py, test_products.py", "pytest pass, coverage dòng mới ≥ 80%", "Must", "2026-11-30"),
    (2, "T2.11", "MỐC TUẦN 2", ALL, "", "—", "§7 dòng 2, 7, 8, 10 xanh", "Mốc", "2026-11-30"),
    # week 3
    (3, "T3.1", "State machine quote + with_for_update()", A, "", "services/quote_machine.py", "đi đủ 6 trạng thái, chuyển sai trả 409", "Must", "2026-12-02"),
    (3, "T3.2", "Bidding (1 hộ 1 lần) + accept 1 bid + tạo order/lot", A, "", "services/order_service.py", "2 người accept cùng lúc → chỉ 1 thắng", "Must", "2026-12-03"),
    (3, "T3.3", "Công đoạn: cập nhật, cấm nhảy cóc, % hoàn thành", A, "", "services/stage_service.py", "không đánh dấu xong bước 3 khi bước 2 chưa xong", "Must", "2026-12-04"),
    (3, "T3.4", "Admin chia đơn + chặn vượt số lượng", A, "", "routers/admin.py (split)", "tổng lot ≤ quantity đơn", "Must", "2026-12-05"),
    (3, "T3.5", "Audit log mọi chuyển trạng thái", A, "", "services/audit.py", "tra được ai đổi, lúc nào, từ đâu sang đâu", "Must", "2026-12-05"),
    (3, "T3.6", "Luồng buyer UI: tạo đơn, xem bid, chấp nhận", Q, "", "features/quotes/", "3 màn hình chạy, không reload", "Must", "2026-12-04"),
    (3, "T3.7", "Timeline công đoạn + % tiến độ", Q, "", "features/orders/StageTimeline.tsx", "buyer thấy cập nhật ngay sau refresh", "Must", "2026-12-05"),
    (3, "T3.8", "F14: slug, 404, 301, SPA fallback", Q, A, "routes/ + slug util", "refresh /san-pham/x vẫn mở đúng", "Must", "2026-12-06"),
    (3, "T3.9", "Test state machine — VIẾT TRƯỚC khi code", D, "", "tests/test_quote_machine.py", "test fail trước khi Anh code, pass sau", "Must", "2026-12-02"),
    (3, "T3.10", "Endpoint analytics + rà lỗi 500 toàn luồng", D, "", "routers/admin.py (stats)", "không còn 500 ở 11 luồng §7", "Should", "2026-12-07"),
    (3, "T3.11", "MỐC TUẦN 3", ALL, "", "—", "§7 dòng 3, 4, 5, 6 xanh", "Mốc", "2026-12-07"),
    # week 4
    (4, "T4.1", "Index + EXPLAIN ANALYZE + ghi lại kế hoạch truy vấn", A, "", "alembic + docs/architecture.md", "danh mục 200 SP < 2.5 giây", "Must", "2026-12-10"),
    (4, "T4.2", "ETL bulk seed (COPY) + view thống kê SQL", A, "", "scripts/seed_bulk.py, views", "seed 60 SP < 5 giây, idempotent", "Should", "2026-12-10"),
    (4, "T4.3", "Polish UI: 4 trạng thái mọi trang, responsive, bản sắc", Q, "", "frontend/src/", "checklist design-system §10 pass", "Must", "2026-12-12"),
    (4, "T4.4", "a11y: axe, keyboard, focus, alt text", Q, "", "tests/a11y.spec.ts", "0 lỗi critical/serious", "Must", "2026-12-12"),
    (4, "T4.5", "Nginx + TLS + domain + rate limit", D, "", "deploy/nginx.conf, certs", "https://domain chạy, login 5 lần/phút bị chặn", "Must", "2026-12-11"),
    (4, "T4.6", "Demo script + video dự phòng + checklist trước thi", D, "", "docs/demo-script.md", "kịch bản A và B chạy được", "Must", "2026-12-13"),
    (4, "T4.7", "Tập demo 2 lần (kịch bản A và B)", ALL, "", "—", "10 phút, không vấp", "Mốc", "2026-12-13"),
    (4, "T4.8", "Rà 10 kiểm tra hướng rubric trong CONSTRAINTS.md", D, "", "—", "tick hết 10 dòng", "Must", "2026-12-14"),
    (4, "T4.9", "MỐC CUỐI", ALL, "", "—", "§7 dòng 9, 11 xanh + demo sẵn sàng", "Mốc", "2026-12-14"),
]

RUBRIC = [
    (1, "Chức năng và các features đã cài đặt", 0.35, "requirements §4 F1-F14 + §7", "Demo 12 bước §4 demo-script"),
    (2, "Thiết kế: logic, dễ sử dụng", 0.10, "architecture §5 (máy trạng thái), design-system §5 (4 trạng thái)", "Chạy luồng báo giá 6 bước"),
    (3, "Giao diện: responsive, đẹp, hiện đại, bản sắc thương hiệu", 0.20, "design-system (11 mục)", "Chỉ đường men lam + serif + ảnh tràn viền"),
    (4, "Hiệu năng: fetch/AJAX, không tải lại, JSON, cập nhật DOM", 0.10, "F14 + api.md JSON + TanStack Query", "DevTools Network: chỉ XHR, document 1 lần"),
    (5, "Phong cách lập trình: pattern, tách UI/nghiệp vụ, tổ chức gói, chú thích", 0.05, "architecture §12 (7 pattern + 9 quy ước)", "Mở cấu trúc thư mục + 1 service có docstring"),
    (6, "Xử lý nhập liệu: kiểm tra, tự động điền, gợi ý, chuyển đổi", 0.05, "F13 + api §10", "Gõ 2 ký tự ra autocomplete, lỗi theo field"),
    (7, "An ninh: xác thực, phiên, truy cập, mã hóa", 0.05, "F1, F2 + security-checklist", "Đăng nhập sai 5 lần bị chặn, sai role bị 403"),
    (8, "Viết lại / định tuyến URL", 0.05, "F14 + architecture §13.2", "Refresh URL slug vẫn mở đúng"),
    (9, "CSDL hướng đối tượng + độc lập CSDL", 0.05, "architecture §13.1 + test SQLite", "Mở models/ + chạy test portable"),
]

MILESTONES = [
    (1, "T1.10", "`make up` + login 3 vai trò + seed có dữ liệu", "Cắt: tin cộng đồng + bản đồ xuống Should", "2026-11-23"),
    (2, "T2.11", "§7 dòng 2, 7, 8, 10 xanh", "Cắt F9 chia đơn + F12 công đoạn xuống Should", "2026-11-30"),
    (3, "T3.11", "§7 dòng 3, 4, 5, 6 xanh", "Giữ upload cơ bản, bỏ resize WebP 2 bản", "2026-12-07"),
    (4, "T4.9", "§7 dòng 9, 11 xanh + demo sẵn sàng", "Bỏ bản đồ, giữ danh mục; dùng video dự phòng", "2026-12-14"),
]

STACK = [
    (A, "Python 3.12, SQL", "FastAPI, Uvicorn, SQLAlchemy (sync), Alembic", "Pydantic v2, PyJWT, argon2-cffi, Pillow, qrcode", "pytest, pytest-cov", "Docker (tuần 1), Git", "React component, Nginx config, Grafana"),
    (Q, "TypeScript", "React 19, Vite", "Tailwind, shadcn/ui, TanStack Query, React Router, Zod, react-hook-form, react-leaflet, openapi-typescript", "Vitest (nhẹ), Playwright (a11y)", "Git", "Python, DB, Docker, state machine"),
    (D, "Bash / PowerShell, Python cơ bản", "Docker Compose, Nginx", "pytest, httpx, certbot", "pytest (integration), Playwright", "Docker, Nginx, Cloudflare DNS, GitHub Actions", "Schema, auth, state machine, React"),
]

BACKLOG = [
    ("B1", "GitHub Actions: lint + test + build image", "CI/CD, DevOps", "Nếu V1 xong sớm"),
    ("B2", "Redis: rate-limit + cache catalog", "DevOps/DE", "Sau V1"),
    ("B3", "Prometheus + Grafana (compose profile ops)", "AIOps, observability", "Sau V1"),
    ("B4", "Locust: 1 script load test + đọc số liệu", "DevOps/AIOps", "Tuần 4 nếu còn thời gian"),
    ("B5", "Tự gắn nhãn ảnh sản phẩm (MobileNet/CLIP offline)", "CV/AI portfolio", "V2 hoặc project cá nhân"),
]

thin = Side(style="thin", color=GRID)
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)


def header_cell(ws, row, col, text, width=None):
    c = ws.cell(row=row, column=col, value=text)
    c.font = Font(bold=True, color="FFFFFF", size=10)
    c.fill = PatternFill("solid", fgColor=MEN_LAM)
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = BORDER
    if width:
        ws.column_dimensions[get_column_letter(col)].width = width
    return c


def body_cell(ws, row, col, value, wrap=True, align="left", size=10, bold=False):
    c = ws.cell(row=row, column=col, value=value)
    c.font = Font(size=size, bold=bold, color=TEXT)
    c.alignment = Alignment(horizontal=align, vertical="top", wrap_text=wrap)
    c.border = BORDER
    return c


def status_legend(ws, row, col, label, color, note, last_col):
    c = ws.cell(row=row, column=col, value=label)
    c.fill = PatternFill("solid", fgColor=color)
    c.font = Font(size=10, bold=True, color=TEXT)
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = BORDER
    ws.merge_cells(start_row=row, start_column=col + 1, end_row=row, end_column=last_col)
    n = ws.cell(row=row, column=col + 1, value=note)
    n.font = Font(size=9, color=TEXT)
    n.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)


def build():
    wb = Workbook()

    # ---------------- Sheet 1: Phân công ----------------
    ws = wb.active
    ws.title = "Phân công"
    widths = {"A": 5, "B": 6, "C": 8, "D": 44, "E": 11, "F": 10, "G": 30, "H": 38,
              "I": 8, "J": 14, "K": 16, "L": 26, "M": 12, "N": 20}
    for k, v in widths.items():
        ws.column_dimensions[k].width = v

    ws.merge_cells("A1:N1")
    t = ws["A1"]
    t.value = "vCraft — Phân công 4 tuần"
    t.font = Font(bold=True, size=16, color="FFFFFF")
    t.fill = PatternFill("solid", fgColor=MEN_LAM)
    t.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[1].height = 32

    ws.merge_cells("A2:N2")
    s = ws["A2"]
    s.value = "Mục tiêu: 2026-12-14 · Nhóm 3 người: Phan Anh (BE/Data) · Quân (FE) · Đông (Infra/QA) · Bản theo dõi chính, cập nhật cuối mỗi buổi làm việc"
    s.font = Font(size=9, italic=True, color=TEXT)
    s.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[2].height = 18

    ws.merge_cells("A4:N4")
    lg = ws["A4"]
    lg.value = "CHÚ THÍCH MÀU TRẠNG THÁI (cột J có dropdown — bấm vào ô để chọn)"
    lg.font = Font(bold=True, size=10, color="FFFFFF")
    lg.fill = PatternFill("solid", fgColor=DAT_NUNG)
    lg.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[4].height = 18

    for i, (label, color, note) in enumerate(STATUSES):
        status_legend(ws, 5 + i, 1, label, color, note, 14)
        ws.row_dimensions[5 + i].height = 17

    ws.row_dimensions[10].height = 6

    # dashboard
    dash = [(1, "Tổng task", "=COUNTA($C$12:$C$60)"),
            (3, "Hoàn thành", '=COUNTIF($J$12:$J$60,"Hoàn thành")'),
            (5, "Đang làm", '=COUNTIF($J$12:$J$60,"Đang làm")'),
            (7, "Đang chờ", '=COUNTIF($J$12:$J$60,"Đang chờ")'),
            (9, "Chưa làm", '=COUNTIF($J$12:$J$60,"Chưa làm")'),
            (11, "% hoàn thành", '=IF($B$11=0,0,$D$11/$B$11)')]
    for col, label, formula in dash:
        c = ws.cell(row=11, column=col, value=label)
        c.font = Font(size=9, bold=True, color=TEXT)
        c.alignment = Alignment(horizontal="right", vertical="center")
        v = ws.cell(row=11, column=col + 1, value=formula)
        v.font = Font(size=12, bold=True, color=MEN_LAM)
        v.alignment = Alignment(horizontal="center", vertical="center")
        v.border = BORDER
        v.fill = PatternFill("solid", fgColor=TRANG_NGA)
    ws.cell(row=11, column=12).number_format = "0%"
    ws.row_dimensions[11].height = 22

    ws.merge_cells("A12:N12")
    w = ws["A12"]
    w.value = '=IF($H$11>3,"⚠ Có "&$H$11&" task bị chặn — họp ngay để gỡ","OK: số task bị chặn trong mức chấp nhận")'
    w.font = Font(size=9, bold=True, color="B3261E")
    w.alignment = Alignment(horizontal="left", vertical="center", indent=1)

    HEAD_ROW = 14
    heads = ["STT", "Tuần", "ID", "Việc", "Phụ trách", "Hỗ trợ", "Output", "Tiêu chí xong",
             "Ưu tiên", "Trạng thái", "Chờ (ID/người)", "Bằng chứng (PR/commit)", "Deadline", "Ghi chú"]
    for i, h in enumerate(heads, start=1):
        header_cell(ws, HEAD_ROW, i, h)
    ws.row_dimensions[HEAD_ROW].height = 30

    first = HEAD_ROW + 1
    for idx, (week, tid, title, owner, support, output, done, prio, deadline) in enumerate(TASKS):
        r = first + idx
        body_cell(ws, r, 1, idx + 1, align="center")
        body_cell(ws, r, 2, week, align="center")
        body_cell(ws, r, 3, tid, align="center", bold=True)
        body_cell(ws, r, 4, title)
        body_cell(ws, r, 5, owner, align="center")
        body_cell(ws, r, 6, support, align="center")
        body_cell(ws, r, 7, output)
        body_cell(ws, r, 8, done)
        body_cell(ws, r, 9, prio, align="center")
        st = body_cell(ws, r, 10, "Chưa làm", align="center")
        st.fill = PatternFill("solid", fgColor="E5E7EB")
        body_cell(ws, r, 11, "")
        body_cell(ws, r, 12, "")
        d = body_cell(ws, r, 13, deadline, align="center")
        d.number_format = "DD/MM/YYYY"
        body_cell(ws, r, 14, "")
        ws.row_dimensions[r].height = 36
    last = first + len(TASKS) - 1

    # dropdown trạng thái
    dv = DataValidation(
        type="list",
        formula1='"Chưa làm,Đang làm,Đang chờ,Hoàn thành,Bỏ (đã cắt)"',
        allow_blank=False,
        showDropDown=False,
        errorTitle="Trạng thái không hợp lệ",
        error="Chọn một trong: Chưa làm / Đang làm / Đang chờ / Hoàn thành / Bỏ (đã cắt)",
    )
    ws.add_data_validation(dv)
    dv.add(f"J{first}:J{last}")

    rng = f"A{first}:N{last}"
    ws.conditional_formatting.add(rng, FormulaRule(
        formula=[f'$J{first}="Hoàn thành"'], fill=PatternFill("solid", fgColor="ECFDF5"), stopIfTrue=False))
    ws.conditional_formatting.add(f"J{first}:J{last}", FormulaRule(
        formula=[f'$J{first}="Đang làm"'], fill=PatternFill("solid", fgColor="FEF3C7")))
    ws.conditional_formatting.add(f"J{first}:J{last}", FormulaRule(
        formula=[f'$J{first}="Đang chờ"'], fill=PatternFill("solid", fgColor="FEE2E2"),
        font=Font(bold=True, color="B3261E")))
    ws.conditional_formatting.add(rng, FormulaRule(
        formula=[f'$J{first}="Bỏ (đã cắt)"'], font=Font(color="9CA3AF", strike=True)))
    ws.conditional_formatting.add(f"M{first}:M{last}", FormulaRule(
        formula=[f'AND($M{first}<>"",$M{first}<TODAY(),$J{first}<>"Hoàn thành")'],
        font=Font(bold=True, color="B3261E")))

    ws.auto_filter.ref = f"A{HEAD_ROW}:N{last}"
    ws.freeze_panes = f"D{first}"

    # ---------------- Sheet 2: Theo người ----------------
    w2 = wb.create_sheet("Theo người")
    w2.merge_cells("A1:G1")
    h = w2["A1"]
    h.value = "Tải theo người và theo tuần"
    h.font = Font(bold=True, size=14, color="FFFFFF")
    h.fill = PatternFill("solid", fgColor=MEN_LAM)
    h.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    w2.row_dimensions[1].height = 26

    for i, wd in enumerate([14, 14, 14, 14, 14, 14, 14], start=1):
        w2.column_dimensions[get_column_letter(i)].width = wd

    heads2 = ["Người", "Tổng task", "Hoàn thành", "Đang làm", "Đang chờ", "Chưa làm", "Bỏ (đã cắt)"]
    for i, hh in enumerate(heads2, start=1):
        header_cell(w2, 3, i, hh)
    people = [A, Q, D]
    for j, p in enumerate(people):
        r = 4 + j
        body_cell(w2, r, 1, p, bold=True)
        body_cell(w2, r, 2, f'=COUNTIF(\'Phân công\'!$E${first}:$E${last},$A{r})', align="center")
        body_cell(w2, r, 3, f'=COUNTIFS(\'Phân công\'!$E${first}:$E${last},$A{r},\'Phân công\'!$J${first}:$J${last},"Hoàn thành")', align="center")
        body_cell(w2, r, 4, f'=COUNTIFS(\'Phân công\'!$E${first}:$E${last},$A{r},\'Phân công\'!$J${first}:$J${last},"Đang làm")', align="center")
        body_cell(w2, r, 5, f'=COUNTIFS(\'Phân công\'!$E${first}:$E${last},$A{r},\'Phân công\'!$J${first}:$J${last},"Đang chờ")', align="center")
        body_cell(w2, r, 6, f'=COUNTIFS(\'Phân công\'!$E${first}:$E${last},$A{r},\'Phân công\'!$J${first}:$J${last},"Chưa làm")', align="center")
        body_cell(w2, r, 7, f'=COUNTIFS(\'Phân công\'!$E${first}:$E${last},$A{r},\'Phân công\'!$J${first}:$J${last},"Bỏ (đã cắt)")', align="center")
        w2.row_dimensions[r].height = 20

    w2.merge_cells("A9:G9")
    t2 = w2["A9"]
    t2.value = "Danh sách task theo tuần (số trong ngoặc = số task)"
    t2.font = Font(bold=True, size=10, color="FFFFFF")
    t2.fill = PatternFill("solid", fgColor=DAT_NUNG)
    t2.alignment = Alignment(horizontal="left", vertical="center", indent=1)

    for i, hh in enumerate(["Tuần", A, Q, D], start=1):
        header_cell(w2, 10, i, hh)
    w2.column_dimensions["A"].width = 8
    for col in ("B", "C", "D"):
        w2.column_dimensions[col].width = 46

    for week in (1, 2, 3, 4):
        r = 10 + week
        body_cell(w2, r, 1, f"Tuần {week}", align="center", bold=True)
        for ci, person in enumerate(people, start=2):
            items = [f"{tid} · {title.split('—')[0].strip()[:60]}" for (wk, tid, title, owner, *_ ) in TASKS if wk == week and owner == person]
            txt = "\n".join(items) if items else "—"
            body_cell(w2, r, ci, txt)
        w2.row_dimensions[r].height = 60

    # ---------------- Sheet 3: Rubric ----------------
    w3 = wb.create_sheet("Rubric")
    w3.merge_cells("A1:F1")
    h3 = w3["A1"]
    h3.value = "Đối chiếu 9 tiêu chí chấm điểm (tổng hệ số = 1.00)"
    h3.font = Font(bold=True, size=14, color="FFFFFF")
    h3.fill = PatternFill("solid", fgColor=MEN_LAM)
    h3.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    w3.row_dimensions[1].height = 26
    for col, wd in {"A": 5, "B": 46, "C": 9, "D": 44, "E": 40, "F": 14}.items():
        w3.column_dimensions[col].width = wd
    for i, hh in enumerate(["#", "Tiêu chí chấm điểm", "Hệ số", "Đáp ứng ở đâu", "Bằng chứng khi demo", "Trạng thái"], start=1):
        header_cell(w3, 3, i, hh)
    for j, (n, name, weight, where, evidence) in enumerate(RUBRIC):
        r = 4 + j
        body_cell(w3, r, 1, n, align="center")
        body_cell(w3, r, 2, name)
        c = body_cell(w3, r, 3, weight, align="center")
        c.number_format = "0.00"
        body_cell(w3, r, 4, where)
        body_cell(w3, r, 5, evidence)
        st = body_cell(w3, r, 6, "Chưa làm", align="center")
        st.fill = PatternFill("solid", fgColor="E5E7EB")
        w3.row_dimensions[r].height = 40
    dv3 = DataValidation(type="list", formula1='"Chưa làm,Đang làm,Đang chờ,Hoàn thành"', allow_blank=False)
    w3.add_data_validation(dv3)
    dv3.add(f"F4:F{3 + len(RUBRIC)}")
    w3.conditional_formatting.add(f"F4:F{3 + len(RUBRIC)}", FormulaRule(
        formula=['$F4="Hoàn thành"'], fill=PatternFill("solid", fgColor="D1FAE5")))
    w3.conditional_formatting.add(f"F4:F{3 + len(RUBRIC)}", FormulaRule(
        formula=['$F4="Đang chờ"'], fill=PatternFill("solid", fgColor="FEE2E2")))
    r = 4 + len(RUBRIC) + 1
    body_cell(w3, r, 1, "")
    body_cell(w3, r, 2, "TỔNG", bold=True)
    tot = body_cell(w3, r, 3, f"=SUM(C4:C{3 + len(RUBRIC)})", align="center", bold=True)
    tot.number_format = "0.00"

    # ---------------- Sheet 4: Mốc kiểm tra ----------------
    w4 = wb.create_sheet("Mốc kiểm tra")
    for col, wd in {"A": 7, "B": 10, "C": 46, "D": 46, "E": 13}.items():
        w4.column_dimensions[col].width = wd
    for i, hh in enumerate(["Tuần", "Mã mốc", "Điều kiện xong", "Nếu trượt thì cắt gì", "Ngày"], start=1):
        header_cell(w4, 1, i, hh)
    for j, (week, mid, cond, cut, day) in enumerate(MILESTONES):
        r = 2 + j
        body_cell(w4, r, 1, week, align="center")
        body_cell(w4, r, 2, mid, align="center", bold=True)
        body_cell(w4, r, 3, cond)
        body_cell(w4, r, 4, cut)
        body_cell(w4, r, 5, day, align="center")
        w4.row_dimensions[r].height = 34

    # ---------------- Sheet 5: Stack từng người ----------------
    w5 = wb.create_sheet("Stack từng người")
    for col, wd in {"A": 12, "B": 16, "C": 26, "D": 46, "E": 22, "F": 26, "G": 30}.items():
        w5.column_dimensions[col].width = wd
    for i, hh in enumerate(["Người", "Vai trò", "Ngôn ngữ", "Framework / thư viện", "Test", "Hạ tầng", "Không đụng"], start=1):
        header_cell(w5, 1, i, hh)
    roles = {A: "Backend / Data", Q: "Frontend", D: "Infra / QA"}
    for j, (person, lang, fw, libs, test, infra, notouch) in enumerate(STACK):
        r = 2 + j
        body_cell(w5, r, 1, person, bold=True)
        body_cell(w5, r, 2, roles[person])
        body_cell(w5, r, 3, lang)
        body_cell(w5, r, 4, fw + " · " + libs)
        body_cell(w5, r, 5, test)
        body_cell(w5, r, 6, infra)
        body_cell(w5, r, 7, notouch)
        w5.row_dimensions[r].height = 52

    # ---------------- Sheet 6: Backlog ----------------
    w6 = wb.create_sheet("Backlog")
    for col, wd in {"A": 7, "B": 52, "C": 28, "D": 26}.items():
        w6.column_dimensions[col].width = wd
    for i, hh in enumerate(["ID", "Việc", "Giá trị cho", "Khi nào làm"], start=1):
        header_cell(w6, 1, i, hh)
    for j, (bid, title, value, when) in enumerate(BACKLOG):
        r = 2 + j
        body_cell(w6, r, 1, bid, align="center", bold=True)
        body_cell(w6, r, 2, title)
        body_cell(w6, r, 3, value)
        body_cell(w6, r, 4, when)
        w6.row_dimensions[r].height = 26

    # ---------------- Sheet 7: Hướng dẫn ----------------
    w7 = wb.create_sheet("Hướng dẫn")
    w7.column_dimensions["A"].width = 16
    w7.column_dimensions["B"].width = 12
    w7.column_dimensions["C"].width = 74
    w7.merge_cells("A1:C1")
    hh = w7["A1"]
    hh.value = "Hướng dẫn dùng file phân công"
    hh.font = Font(bold=True, size=14, color="FFFFFF")
    hh.fill = PatternFill("solid", fgColor=MEN_LAM)
    hh.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    w7.row_dimensions[1].height = 26

    w7["A3"] = "1. Năm trạng thái và màu"
    w7["A3"].font = Font(bold=True, size=11, color=DAT_NUNG)
    for j, (label, color, note) in enumerate(STATUSES):
        r = 4 + j
        c = w7.cell(row=r, column=1, value=label)
        c.fill = PatternFill("solid", fgColor=color)
        c.font = Font(size=10, bold=True)
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.border = BORDER
        n = w7.cell(row=r, column=2, value="")
        n.border = BORDER
        m = w7.cell(row=r, column=3, value=note)
        m.font = Font(size=10)
        m.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        m.border = BORDER
        w7.row_dimensions[r].height = 22

    start = 4 + len(STATUSES) + 2
    w7.cell(row=start, column=1, value="2. Định nghĩa “Hoàn thành”").font = Font(bold=True, size=11, color=DAT_NUNG)
    rules = [
        "Hoàn thành = PR đã merge vào main + test liên quan pass + demo được bằng tay + cột “Bằng chứng” có link/commit.",
        "Đang làm = có nhánh riêng + ít nhất 1 commit + không bị chặn.",
        "Đang chờ = BẮT BUỘC ghi cột K “Chờ (ID/người)”. Không ghi được đang chờ ai → hạ xuống “Chưa làm”.",
        "Chưa làm = chưa có nhánh, chưa ai bắt đầu.",
        "Bỏ (đã cắt) = cắt theo quy tắc cắt ở sheet “Mốc kiểm tra”; ghi lý do + ngày.",
    ]
    for j, txt in enumerate(rules):
        r = start + 1 + j
        w7.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
        c = w7.cell(row=r, column=1, value="• " + txt)
        c.font = Font(size=10)
        c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        w7.row_dimensions[r].height = 22

    start2 = start + 1 + len(rules) + 2
    w7.cell(row=start2, column=1, value="3. Quy tắc cập nhật").font = Font(bold=True, size=11, color=DAT_NUNG)
    rituals = [
        "Cuối mỗi buổi làm việc: mỗi người tự cập nhật cột J (trạng thái), K (chờ ai), L (bằng chứng) cho task của mình.",
        "Không cập nhật = coi như “Chưa làm”. Không có ngoại lệ.",
        "Cuối tuần: đọc dashboard (dòng 11) + lọc các task “Đang chờ”, giải quyết hết trước khi sang tuần mới.",
        "Không đổi trạng thái task của người khác — chỉ người phụ trách hoặc người review được đổi.",
        "Deadline ở cột M tô đỏ khi đã quá hạn mà task chưa Hoàn thành.",
    ]
    for j, txt in enumerate(rituals):
        r = start2 + 1 + j
        w7.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
        c = w7.cell(row=r, column=1, value="• " + txt)
        c.font = Font(size=10)
        c.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
        w7.row_dimensions[r].height = 22

    start3 = start2 + 1 + len(rituals) + 2
    w7.cell(row=start3, column=1, value="4. Dashboard đọc thế nào").font = Font(bold=True, size=11, color=DAT_NUNG)
    dashnotes = [
        "Tổng task / Hoàn thành / Đang làm / Đang chờ / Chưa làm: tự đếm từ cột J.",
        "% hoàn thành = Hoàn thành / Tổng task.",
        "Ô cảnh báo đỏ: hiện khi có hơn 3 task “Đang chờ” — lúc đó phải họp để gỡ, không chờ tới cuối tuần.",
    ]
    for j, txt in enumerate(dashnotes):
        r = start3 + 1 + j
        w7.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
        c = w7.cell(row=r, column=1, value="• " + txt)
        c.font = Font(size=10)
        c.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
        w7.row_dimensions[r].height = 22

    start4 = start3 + 1 + len(dashnotes) + 2
    w7.cell(row=start4, column=1, value="5. Sinh lại file").font = Font(bold=True, size=11, color=DAT_NUNG)
    w7.merge_cells(start_row=start4 + 1, start_column=1, end_row=start4 + 1, end_column=3)
    c = w7.cell(row=start4 + 1, column=1, value="• Chạy: python scripts/gen_assignment_xlsx.py  (ghi đè file này và tasks/todo.md — mất mọi chỉnh tay)")
    c.font = Font(size=10)
    c.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)

    out = ROOT / "tasks" / "phan-cong-4-tuan.xlsx"
    out.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)
    print("saved", out)

    # ---------------- tasks/todo.md ----------------
    lines = [
        "# Task list — vCraft (4 tuần)",
        "",
        "Bản theo dõi chính: **`tasks/phan-cong-4-tuan.xlsx`** (có dropdown trạng thái + dashboard).",
        "File này là bản đọc nhanh trong repo — cùng nội dung, cùng ID task.",
        "",
        "Trạng thái: `Chưa làm` · `Đang làm` · `Đang chờ` · `Hoàn thành` · `Bỏ (đã cắt)`.",
        "Định nghĩa Hoàn thành: PR merged + test pass + demo được + có link bằng chứng.",
        "",
    ]
    for week in (1, 2, 3, 4):
        lines += [f"## Tuần {week}", "",
                  "| ID | Việc | Phụ trách | Hỗ trợ | Tiêu chí xong | Ưu tiên | Deadline | Trạng thái |",
                  "|---|---|---|---|---|---|---|---|"]
        for (wk, tid, title, owner, support, output, done, prio, deadline) in TASKS:
            if wk != week:
                continue
            lines.append(f"| {tid} | {title} | {owner} | {support or '—'} | {done} | {prio} | {deadline} | Chưa làm |")
        lines.append("")
    lines += [
        "## Ngoài V1 (backlog)",
        "",
        "| ID | Việc | Giá trị | Khi nào |",
        "|---|---|---|---|",
    ]
    for (bid, title, value, when) in BACKLOG:
        lines.append(f"| {bid} | {title} | {value} | {when} |")
    lines += ["", "## Lịch sử", "", "| Ngày | Thay đổi | Người |", "|---|---|---|",
              "| 2026-11-17 | Sinh lại theo phân công 3 người (Anh/Quân/Đông), 41 task, 4 mốc tuần | Nhóm |", ""]

    (ROOT / "tasks" / "todo.md").write_text("\n".join(lines), encoding="utf-8")
    print("saved tasks/todo.md")


if __name__ == "__main__":
    build()
