"""Sinh tasks/phan-cong-4-tuan.xlsx + tasks/todo.md cho vCraft.

Chạy: python scripts/gen_assignment_xlsx.py
Ghi đè file Excel và file markdown. Muốn sửa kế hoạch thì sửa TASKS dưới đây rồi chạy lại.
"""

from pathlib import Path
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule

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

# (tuần, id, việc, phụ trách, hỗ trợ, output, tiêu chí xong, ưu tiên, deadline, giờ)
TASKS = [
    # ---- Tuần 1 ----
    (1, "T1.1", "Repo GitHub, .gitignore, .gitattributes", D, "", "repo + 3 người clone được", "`git push` thành công, 3 người clone được", "Must", "2026-11-18", 1),
    (1, "T1.2", "Docker Compose (db + api + web)", A, D, "deploy/docker-compose.yml", "`make up` chạy, 3 service healthy", "Must", "2026-11-19", 4),
    (1, "T1.3", ".env.example + Makefile (up/down/seed/test/logs)", D, "", "Makefile, .env.example", "người mới chạy 1 lệnh là có app", "Must", "2026-11-19", 2),
    (1, "T1.4", "Schema 19 bảng + Alembic migration đầu", A, "", "backend/app/models/, alembic/", "`alembic upgrade head` sạch trên DB trống", "Must", "2026-11-21", 8),
    (1, "T1.5", "Auth: JWT cookie httpOnly, argon2, role dependency", A, "", "routers/auth.py, core/security.py", "3 vai trò đăng nhập, sai role bị 403", "Must", "2026-11-21", 6),
    (1, "T1.6", "docs/api.md → OpenAPI → type TS cho FE", A, Q, "openapi.json + src/lib/api.ts", "FE gọi /api/auth/me bằng type sinh tự động", "Must", "2026-11-23", 3),
    (1, "T1.7", "Design tokens + layout + trang đăng nhập/đăng ký", Q, "", "design-tokens.ts, tailwind.config.ts, routes/auth/", "2 trang chạy, responsive 320/1440", "Must", "2026-11-23", 10),
    (1, "T1.8", "Seed data Bát Tràng (5 hộ, 40-60 SP, 4 đơn, 5 ghim, 4 tin)", D, "", "backend/app/seed/", "`make seed` chạy 2 lần không nhân đôi dữ liệu", "Must", "2026-11-23", 8),
    (1, "T1.9", "Smoke test schema portable (tạo schema + CRUD trên SQLite)", D, "", "tests/test_schema_portable.py", "pytest pass — chứng minh độc lập CSDL", "Must", "2026-11-23", 3),
    (1, "T1.10", "MỐC TUẦN 1", ALL, "", "—", "`make up` + login 3 vai trò + seed có dữ liệu", "Mốc", "2026-11-23", 0),
    # ---- Tuần 2 ----
    (2, "T2.1", "Hồ sơ xưởng CRUD + ảnh + chứng nhận", D, A, "routers/workshops.py", "artisan sửa hồ sơ, trang công khai cập nhật", "Must", "2026-11-25", 6),
    (2, "T2.2", "Sản phẩm CRUD: list/filter/paginate", D, A, "routers/products.py", "CRUD theo contract, không lỗi 500", "Must", "2026-11-26", 4),
    (2, "T2.3", "Pipeline ảnh: Pillow WebP 400/1200 + magic bytes + ≤10MB", A, "", "services/image_pipeline.py", "upload 5 ảnh, 1 ảnh lỗi không chặn ảnh khác", "Must", "2026-11-27", 8),
    (2, "T2.4", "Tìm kiếm + index sản phẩm (ILIKE, phân trang server-side)", A, "", "repositories/product_query.py", "200 SP lọc/tìm < 1 giây", "Must", "2026-11-27", 4),
    (2, "T2.5", "QR token + qr_service (PUBLIC_BASE_URL)", A, "", "services/qr_service.py", "token không trùng, URL đúng môi trường", "Must", "2026-11-27", 2),
    (2, "T2.6", "Trang công khai /p/{token} + template timeline", D, A, "routers/public.py", "quét điện thoại mở đúng trang, không cần login", "Must", "2026-11-28", 3),
    (2, "T2.7", "Danh mục UI: lọc hộ/phân loại, tìm, skeleton/empty/error", Q, "", "features/catalog/", "đủ 4 trạng thái, không cuộn ngang", "Must", "2026-11-26", 6),
    (2, "T2.8", "Upload UI: progress từng ảnh, lỗi riêng từng ảnh", Q, "", "features/upload/", "upload 5 ảnh thấy 5 progress", "Must", "2026-11-28", 6),
    (2, "T2.9", "F13 nhập liệu: autocomplete, tự điền, format giá/ngày, lỗi theo field", Q, "", "features/forms/", "gõ 2 ký tự ra gợi ý, chọn bằng bàn phím", "Must", "2026-11-29", 8),
    (2, "T2.10", "Admin backend: duyệt/từ chối hộ", D, A, "routers/admin.py", "duyệt → đăng nhập được; từ chối có lý do", "Must", "2026-11-28", 6),
    (2, "T2.11", "Test auth + sản phẩm + upload", D, "", "tests/test_auth.py, test_products.py", "pytest pass, coverage dòng mới ≥ 80%", "Must", "2026-11-30", 8),
    (2, "T2.12", "MỐC TUẦN 2", ALL, "", "—", "§7 dòng 2, 8, 10 xanh", "Mốc", "2026-11-30", 0),
    # ---- Tuần 3 ----
    (3, "T3.1", "State machine quote + with_for_update()", A, "", "services/quote_machine.py", "đi đủ 6 trạng thái, chuyển sai trả 409", "Must", "2026-12-02", 10),
    (3, "T3.2", "Bidding (1 hộ 1 lần) + accept 1 bid + tạo order/lot", A, "", "services/order_service.py", "2 người accept cùng lúc → chỉ 1 thắng", "Must", "2026-12-03", 8),
    (3, "T3.3", "Công đoạn: cập nhật, cấm nhảy cóc, % hoàn thành", A, "", "services/stage_service.py", "không đánh dấu xong bước 3 khi bước 2 chưa xong", "Must", "2026-12-04", 6),
    (3, "T3.4", "Admin chia đơn + chặn vượt số lượng", A, "", "routers/admin.py (split)", "tổng lot ≤ quantity đơn", "Must", "2026-12-05", 5),
    (3, "T3.5", "Audit log mọi chuyển trạng thái", A, "", "services/audit.py", "tra được ai đổi, lúc nào, từ đâu sang đâu", "Must", "2026-12-05", 3),
    (3, "T3.6", "Luồng buyer UI: tạo đơn, xem bid, chấp nhận", Q, "", "features/quotes/", "3 màn hình chạy, không reload", "Must", "2026-12-04", 8),
    (3, "T3.7", "Timeline công đoạn + % tiến độ", Q, "", "features/orders/StageTimeline.tsx", "buyer thấy cập nhật ngay sau refresh", "Must", "2026-12-05", 5),
    (3, "T3.8", "F14: slug + 404 + SPA fallback (301 → backlog)", Q, A, "routes/ + slug util", "refresh /san-pham/x vẫn mở đúng", "Must", "2026-12-06", 4),
    (3, "T3.9", "Test state machine — VIẾT TRƯỚC khi code", D, "", "tests/test_quote_machine.py", "test fail trước khi Anh code, pass sau", "Must", "2026-12-02", 8),
    (3, "T3.10", "UI khu artisan: quản lý sản phẩm (form + mốc + upload) + danh sách đơn/chào giá", Q, "", "features/artisan/", "artisan tạo sản phẩm + chào giá không cần admin", "Must", "2026-12-06", 10),
    (3, "T3.11", "UI admin gộp 1 trang tabs: duyệt hộ + chia đơn + thống kê", D, Q, "features/admin/", "3 tab chạy, phân trang OK", "Must", "2026-12-07", 6),
    (3, "T3.12", "MỐC TUẦN 3", ALL, "", "—", "§7 dòng 3, 4, 5, 6 xanh", "Mốc", "2026-12-07", 0),
    # ---- Tuần 4 ----
    (4, "T4.1", "Index + EXPLAIN ANALYZE + ghi kế hoạch truy vấn", A, "", "alembic + docs/architecture.md", "danh mục 200 SP < 2.5 giây", "Must", "2026-12-10", 4),
    (4, "T4.2", "Analytics SQL: 3 truy vấn + view thống kê + ghi EXPLAIN", A, D, "repositories/stats.py + views", "3 truy vấn chạy < 200ms trên seed", "Should", "2026-12-10", 3),
    (4, "T4.3", "ETL bulk seed (COPY) + idempotent + --reset", D, A, "scripts/seed_bulk.py", "seed 60 SP < 5 giây, chạy 2 lần không nhân đôi", "Should", "2026-12-11", 3),
    (4, "T4.4", "Polish UI (timebox 5h): 4 trạng thái + responsive + bản sắc", Q, "", "frontend/src/", "checklist design-system §10 pass", "Must", "2026-12-12", 5),
    (4, "T4.5", "a11y (timebox 3h): axe, keyboard, focus, alt text", Q, "", "tests/a11y.spec.ts", "0 lỗi critical/serious", "Must", "2026-12-12", 3),
    (4, "T4.6", "Nginx + TLS + domain + rate limit", D, "", "deploy/nginx.conf, certs", "https://domain chạy, login 5 lần/phút bị chặn", "Must", "2026-12-11", 6),
    (4, "T4.7", "Demo script + video dự phòng + checklist trước thi", D, "", "docs/demo-script.md", "kịch bản A và B chạy được", "Must", "2026-12-13", 5),
    (4, "T4.8", "Tập demo 2 lần (kịch bản A và B)", ALL, "", "—", "10 phút, không vấp", "Mốc", "2026-12-13", 0),
    (4, "T4.9", "Rà 10 kiểm tra hướng rubric + MỐC CUỐI", D, ALL, "—", "tick hết 10 dòng + §7 dòng 9, 11 xanh", "Mốc", "2026-12-14", 3),
]

CUTS = [
    ("F7 Bản đồ làng nghề", "Chuyển V2", "Bỏ 6h; rubric #1 vẫn đủ với 13 feature còn lại", "2026-11-17"),
    ("F11 Tin cộng đồng (toàn bộ)", "Chuyển V2", "Bỏ 8h; admin chỉ còn duyệt hộ + chia đơn", "2026-11-17"),
    ("301 slug history (`slug_redirects`)", "Chuyển V2", "Giữ slug + 404 + SPA fallback; bỏ bảng redirect", "2026-11-17"),
    ("Chuyển đổi đơn vị kg ↔ chiếc (F13)", "Chuyển V2", "Giữ autocomplete + autofill + format giá/ngày", "2026-11-17"),
    ("Endpoint analytics riêng", "Gộp vào view SQL", "Đọc trực tiếp từ view trong admin UI", "2026-11-17"),
]

RUBRIC = [
    (1, "Chức năng và các features đã cài đặt", 0.35, "requirements §4 F1-F14 (trừ F7, F11 đã cắt) + §7", "Demo 12 bước §4 demo-script"),
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
    (1, "T1.10", "`make up` + login 3 vai trò + seed có dữ liệu", "Cắt F7 bản đồ + F11 tin cộng đồng xuống V2", "2026-11-23"),
    (2, "T2.12", "§7 dòng 2, 8, 10 xanh", "Giữ upload cơ bản, bỏ resize WebP 2 bản", "2026-11-30"),
    (3, "T3.12", "§7 dòng 3, 4, 5, 6 xanh", "Bỏ analytics + ETL bulk; chỉ giữ 1 view SQL", "2026-12-07"),
    (4, "T4.9", "§7 dòng 9, 11 xanh + demo sẵn sàng", "Dùng video dự phòng nếu domain/TLS lỗi", "2026-12-14"),
]

STACK = [
    (A, "Backend / Data", "Python 3.12, SQL", "FastAPI, Uvicorn, SQLAlchemy (sync), Alembic", "Pydantic v2, PyJWT, argon2-cffi, Pillow, qrcode", "pytest, pytest-cov", "Docker (tuần 1), Git", "React component, Nginx config, Grafana"),
    (Q, "Frontend", "TypeScript", "React 19, Vite", "Tailwind, shadcn/ui, TanStack Query, React Router, Zod, react-hook-form, react-leaflet", "Vitest (nhẹ), Playwright (a11y)", "Git", "Python, DB, Docker, state machine"),
    (D, "Infra / QA", "Bash / PowerShell, Python cơ bản", "Docker Compose, Nginx", "pytest, httpx, certbot", "pytest (integration), Playwright", "Docker, Nginx, Cloudflare DNS, GitHub Actions", "Schema, auth, state machine, React"),
]

BACKLOG = [
    ("B1", "GitHub Actions: lint + test + build image", "CI/CD, DevOps", "Nếu V1 xong sớm"),
    ("B2", "Redis: rate-limit + cache catalog", "DevOps/DE", "Sau V1"),
    ("B3", "Prometheus + Grafana (compose profile ops)", "AIOps, observability", "Sau V1"),
    ("B4", "Locust: 1 script load test + đọc số liệu", "DevOps/AIOps", "Tuần 4 nếu còn thời gian"),
    ("B5", "Tự gắn nhãn ảnh sản phẩm (MobileNet/CLIP offline)", "CV/AI portfolio", "V2 hoặc project cá nhân"),
    ("B6", "F7 Bản đồ làng nghề", "Tính năng", "V2 (đã cắt 2026-11-17)"),
    ("B7", "F11 Tin cộng đồng + duyệt bài", "Tính năng", "V2 (đã cắt 2026-11-17)"),
    ("B8", "301 slug history (`slug_redirects`)", "Kỹ thuật", "V2 (đã cắt 2026-11-17)"),
    ("B9", "Chuyển đổi đơn vị kg ↔ chiếc (F13)", "Tính năng", "V2 (đã cắt 2026-11-17)"),
]

CAPACITY = [
    (A, "4 tuần × 15h", 60),
    (Q, "4 tuần × 15h", 60),
    (D, "4 tuần × 15h", 60),
]

thin = Side(style="thin", color=GRID)
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)


def header_cell(ws, row, col, text):
    c = ws.cell(row=row, column=col, value=text)
    c.font = Font(bold=True, color="FFFFFF", size=10)
    c.fill = PatternFill("solid", fgColor=MEN_LAM)
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = BORDER
    return c


def body_cell(ws, row, col, value, wrap=True, align="left", size=10, bold=False):
    c = ws.cell(row=row, column=col, value=value)
    c.font = Font(size=size, bold=bold, color=TEXT)
    c.alignment = Alignment(horizontal=align, vertical="top", wrap_text=wrap)
    c.border = BORDER
    return c


def status_legend(ws, row, label, color, note, last_col):
    c = ws.cell(row=row, column=1, value=label)
    c.fill = PatternFill("solid", fgColor=color)
    c.font = Font(size=10, bold=True, color=TEXT)
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = BORDER
    ws.merge_cells(start_row=row, start_column=2, end_row=row, end_column=last_col)
    n = ws.cell(row=row, column=2, value=note)
    n.font = Font(size=9, color=TEXT)
    n.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)


def build():
    wb = Workbook()

    # ================= Sheet 1 =================
    ws = wb.active
    ws.title = "Phân công"
    for k, v in {"A": 5, "B": 6, "C": 8, "D": 44, "E": 11, "F": 9, "G": 30, "H": 36,
                 "I": 8, "J": 14, "K": 16, "L": 24, "M": 12, "N": 18, "O": 8}.items():
        ws.column_dimensions[k].width = v

    ws.merge_cells("A1:O1")
    t = ws["A1"]
    t.value = "vCraft — Phân công 4 tuần (đã cân tải)"
    t.font = Font(bold=True, size=16, color="FFFFFF")
    t.fill = PatternFill("solid", fgColor=MEN_LAM)
    t.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[1].height = 32

    ws.merge_cells("A2:O2")
    s = ws["A2"]
    s.value = ("Mục tiêu 2026-12-14 · Phan Anh (BE/Data) · Quân (FE) · Đông (Infra/QA) · "
               "Bản theo dõi chính — cập nhật cuối mỗi buổi làm việc")
    s.font = Font(size=9, italic=True, color=TEXT)
    s.alignment = Alignment(horizontal="left", vertical="center", indent=1)

    ws.merge_cells("A4:O4")
    lg = ws["A4"]
    lg.value = "CHÚ THÍCH MÀU TRẠNG THÁI (cột J có dropdown — bấm vào ô để chọn)"
    lg.font = Font(bold=True, size=10, color="FFFFFF")
    lg.fill = PatternFill("solid", fgColor=DAT_NUNG)
    lg.alignment = Alignment(horizontal="left", vertical="center", indent=1)

    for i, (label, color, note) in enumerate(STATUSES):
        status_legend(ws, 5 + i, label, color, note, 15)
        ws.row_dimensions[5 + i].height = 17

    dash = [(1, "Tổng task", "=COUNTA($C$15:$C$60)"),
            (3, "Hoàn thành", '=COUNTIF($J$15:$J$60,"Hoàn thành")'),
            (5, "Đang làm", '=COUNTIF($J$15:$J$60,"Đang làm")'),
            (7, "Đang chờ", '=COUNTIF($J$15:$J$60,"Đang chờ")'),
            (9, "Chưa làm", '=COUNTIF($J$15:$J$60,"Chưa làm")'),
            (11, "% hoàn thành", '=IF($B$11=0,0,$D$11/$B$11)'),
            (13, "Tổng giờ", "=SUM($O$15:$O$60)")]
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

    ws.merge_cells("A12:O12")
    w = ws["A12"]
    w.value = '=IF($H$11>3,"⚠ Có "&$H$11&" task bị chặn — họp ngay để gỡ","OK: số task bị chặn trong mức chấp nhận")'
    w.font = Font(size=9, bold=True, color="B3261E")
    w.alignment = Alignment(horizontal="left", vertical="center", indent=1)

    HEAD = 14
    heads = ["STT", "Tuần", "ID", "Việc", "Phụ trách", "Hỗ trợ", "Output", "Tiêu chí xong",
             "Ưu tiên", "Trạng thái", "Chờ (ID/người)", "Bằng chứng (PR/commit)", "Deadline", "Ghi chú", "Giờ"]
    for i, h in enumerate(heads, start=1):
        header_cell(ws, HEAD, i, h)
    ws.row_dimensions[HEAD].height = 30

    first = HEAD + 1
    for idx, (week, tid, title, owner, support, output, done, prio, deadline, hours) in enumerate(TASKS):
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
        body_cell(ws, r, 15, hours, align="center")
        ws.row_dimensions[r].height = 36
    last = first + len(TASKS) - 1

    dv = DataValidation(type="list",
                        formula1='"Chưa làm,Đang làm,Đang chờ,Hoàn thành,Bỏ (đã cắt)"',
                        allow_blank=False,
                        errorTitle="Trạng thái không hợp lệ",
                        error="Chọn: Chưa làm / Đang làm / Đang chờ / Hoàn thành / Bỏ (đã cắt)")
    ws.add_data_validation(dv)
    dv.add(f"J{first}:J{last}")

    rng = f"A{first}:O{last}"
    ws.conditional_formatting.add(rng, FormulaRule(
        formula=[f'$J{first}="Hoàn thành"'], fill=PatternFill("solid", fgColor="ECFDF5")))
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

    ws.auto_filter.ref = f"A{HEAD}:O{last}"
    ws.freeze_panes = f"D{first}"

    # ================= Sheet 2 =================
    w2 = wb.create_sheet("Theo người")
    for col, wd in {"A": 14, "B": 11, "C": 11, "D": 11, "E": 11, "F": 11, "G": 11, "H": 11}.items():
        w2.column_dimensions[col].width = wd
    w2.merge_cells("A1:H1")
    h = w2["A1"]
    h.value = "Tải theo người — ước lượng giờ so với năng lực"
    h.font = Font(bold=True, size=14, color="FFFFFF")
    h.fill = PatternFill("solid", fgColor=MEN_LAM)
    h.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    w2.row_dimensions[1].height = 26

    heads2 = ["Người", "Tổng task", "Hoàn thành", "Đang làm", "Đang chờ", "Chưa làm", "Tổng giờ", "Năng lực"]
    for i, hh in enumerate(heads2, start=1):
        header_cell(w2, 3, i, hh)
    cap = {A: 60, Q: 60, D: 60}
    for j, p in enumerate([A, Q, D]):
        r = 4 + j
        body_cell(w2, r, 1, p, bold=True)
        body_cell(w2, r, 2, f"=COUNTIF('Phân công'!$E${first}:$E${last},$A{r})", align="center")
        body_cell(w2, r, 3, f"=COUNTIFS('Phân công'!$E${first}:$E${last},$A{r},'Phân công'!$J${first}:$J${last},\"Hoàn thành\")", align="center")
        body_cell(w2, r, 4, f"=COUNTIFS('Phân công'!$E${first}:$E${last},$A{r},'Phân công'!$J${first}:$J${last},\"Đang làm\")", align="center")
        body_cell(w2, r, 5, f"=COUNTIFS('Phân công'!$E${first}:$E${last},$A{r},'Phân công'!$J${first}:$J${last},\"Đang chờ\")", align="center")
        body_cell(w2, r, 6, f"=COUNTIFS('Phân công'!$E${first}:$E${last},$A{r},'Phân công'!$J${first}:$J${last},\"Chưa làm\")", align="center")
        body_cell(w2, r, 7, f"=SUMIF('Phân công'!$E${first}:$E${last},$A{r},'Phân công'!$O${first}:$O${last})", align="center")
        body_cell(w2, r, 8, cap[p], align="center")
        w2.row_dimensions[r].height = 20

    w2.merge_cells("A10:H10")
    t2 = w2["A10"]
    t2.value = "Cảnh báo năng lực: nếu Tổng giờ > Năng lực → phải cắt task hoặc nhờ hỗ trợ"
    t2.font = Font(size=9, bold=True, color="B3261E")
    t2.alignment = Alignment(horizontal="left", vertical="center", indent=1)

    for i, hh in enumerate(["Tuần", A, Q, D], start=1):
        header_cell(w2, 12, i, hh)
    w2.column_dimensions["A"].width = 9
    for col in ("B", "C", "D"):
        w2.column_dimensions[col].width = 48
    for week in (1, 2, 3, 4):
        r = 12 + week
        body_cell(w2, r, 1, f"Tuần {week}", align="center", bold=True)
        for ci, person in enumerate([A, Q, D], start=2):
            items = [f"{tid} ({hours}h)" for (wk, tid, title, owner, *rest, hours) in TASKS
                     if wk == week and owner == person]
            body_cell(w2, r, ci, "\n".join(items) if items else "—")
        w2.row_dimensions[r].height = 60

    # ================= Sheet 3 =================
    w3 = wb.create_sheet("Rubric")
    w3.merge_cells("A1:F1")
    h3 = w3["A1"]
    h3.value = "Đối chiếu 9 tiêu chí chấm điểm (tổng hệ số = 1.00)"
    h3.font = Font(bold=True, size=14, color="FFFFFF")
    h3.fill = PatternFill("solid", fgColor=MEN_LAM)
    h3.alignment = Alignment(horizontal="left", vertical="center", indent=1)
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
    r = 4 + len(RUBRIC) + 1
    body_cell(w3, r, 2, "TỔNG", bold=True)
    tot = body_cell(w3, r, 3, f"=SUM(C4:C{3 + len(RUBRIC)})", align="center", bold=True)
    tot.number_format = "0.00"

    # ================= Sheet 4 =================
    w4 = wb.create_sheet("Mốc kiểm tra")
    for col, wd in {"A": 7, "B": 10, "C": 44, "D": 46, "E": 13}.items():
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

    # ================= Sheet 5 =================
    w5 = wb.create_sheet("Stack từng người")
    for col, wd in {"A": 12, "B": 16, "C": 20, "D": 44, "E": 40, "F": 22, "G": 26, "H": 30}.items():
        w5.column_dimensions[col].width = wd
    for i, hh in enumerate(["Người", "Vai trò", "Ngôn ngữ", "Framework", "Thư viện", "Test", "Hạ tầng", "Không đụng"], start=1):
        header_cell(w5, 1, i, hh)
    for j, row in enumerate(STACK):
        r = 2 + j
        for ci, val in enumerate(row, start=1):
            body_cell(w5, r, ci, val, bold=(ci == 1))
        w5.row_dimensions[r].height = 52

    # ================= Sheet 6 =================
    w6 = wb.create_sheet("Cắt & năng lực")
    for col, wd in {"A": 30, "B": 16, "C": 60, "D": 13}.items():
        w6.column_dimensions[col].width = wd
    w6.merge_cells("A1:D1")
    h6 = w6["A1"]
    h6.value = "Đã cắt khỏi V1 và kiểm tra năng lực"
    h6.font = Font(bold=True, size=14, color="FFFFFF")
    h6.fill = PatternFill("solid", fgColor=MEN_LAM)
    h6.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    for i, hh in enumerate(["Hạng mục cắt", "Chuyển sang", "Lý do", "Ngày"], start=1):
        header_cell(w6, 3, i, hh)
    for j, (item, to, why, day) in enumerate(CUTS):
        r = 4 + j
        body_cell(w6, r, 1, item)
        body_cell(w6, r, 2, to, align="center")
        body_cell(w6, r, 3, why)
        body_cell(w6, r, 4, day, align="center")
        w6.row_dimensions[r].height = 30

    r0 = 4 + len(CUTS) + 2
    body_cell(w6, r0, 1, "Năng lực thực tế", bold=True)
    body_cell(w6, r0, 2, "Giờ", align="center", bold=True)
    body_cell(w6, r0, 3, "Ghi chú", bold=True)
    notes = [
        ("Mỗi người / tuần (thấp)", 10, "4 tuần → 40h/người → 120h cả nhóm"),
        ("Mỗi người / tuần (cao)", 15, "4 tuần → 60h/người → 180h cả nhóm"),
        ("Tổng giờ trong kế hoạch", f"=SUM('Phân công'!$O${first}:$O${last})", "Xem ô này so với 120-180h"),
    ]
    for j, (label, val, note) in enumerate(notes):
        r = r0 + 1 + j
        body_cell(w6, r, 1, label)
        body_cell(w6, r, 2, val, align="center")
        body_cell(w6, r, 3, note)
        w6.row_dimensions[r].height = 22

    # ================= Sheet 7 =================
    w7 = wb.create_sheet("Backlog")
    for col, wd in {"A": 7, "B": 52, "C": 28, "D": 30}.items():
        w7.column_dimensions[col].width = wd
    for i, hh in enumerate(["ID", "Việc", "Giá trị cho", "Khi nào làm"], start=1):
        header_cell(w7, 1, i, hh)
    for j, (bid, title, value, when) in enumerate(BACKLOG):
        r = 2 + j
        body_cell(w7, r, 1, bid, align="center", bold=True)
        body_cell(w7, r, 2, title)
        body_cell(w7, r, 3, value)
        body_cell(w7, r, 4, when)
        w7.row_dimensions[r].height = 26

    # ================= Sheet 8 =================
    w8 = wb.create_sheet("Hướng dẫn")
    w8.column_dimensions["A"].width = 16
    w8.column_dimensions["B"].width = 4
    w8.column_dimensions["C"].width = 80
    w8.merge_cells("A1:C1")
    hh = w8["A1"]
    hh.value = "Hướng dẫn dùng file phân công"
    hh.font = Font(bold=True, size=14, color="FFFFFF")
    hh.fill = PatternFill("solid", fgColor=MEN_LAM)
    hh.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    w8.row_dimensions[1].height = 26

    w8["A3"] = "1. Năm trạng thái và ý nghĩa màu"
    w8["A3"].font = Font(bold=True, size=11, color=DAT_NUNG)
    for j, (label, color, note) in enumerate(STATUSES):
        r = 4 + j
        c = w8.cell(row=r, column=1, value=label)
        c.fill = PatternFill("solid", fgColor=color)
        c.font = Font(size=10, bold=True)
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.border = BORDER
        m = w8.cell(row=r, column=3, value=note)
        m.font = Font(size=10)
        m.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        m.border = BORDER
        w8.row_dimensions[r].height = 22

    def block(title, items, start_row):
        w8.cell(row=start_row, column=1, value=title).font = Font(bold=True, size=11, color=DAT_NUNG)
        for j, txt in enumerate(items):
            r = start_row + 1 + j
            w8.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
            c = w8.cell(row=r, column=1, value="• " + txt)
            c.font = Font(size=10)
            c.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
            w8.row_dimensions[r].height = 24
        return start_row + 1 + len(items) + 2

    y = block("2. Định nghĩa “Hoàn thành”", [
        "Hoàn thành = PR đã merge + test liên quan pass + demo được bằng tay + cột “Bằng chứng” có link/commit.",
        "Đang làm = có nhánh riêng + ít nhất 1 commit + không bị chặn.",
        "Đang chờ = BẮT BUỘC ghi cột “Chờ (ID/người)”. Không ghi được đang chờ ai → hạ xuống “Chưa làm”.",
        "Chưa làm = chưa có nhánh, chưa ai bắt đầu.",
        "Bỏ (đã cắt) = cắt theo sheet “Cắt & năng lực”; ghi lý do + ngày.",
    ], 4 + len(STATUSES) + 2)

    y = block("3. Quy tắc cập nhật", [
        "Cuối mỗi buổi làm việc: tự cập nhật cột Trạng thái, Chờ, Bằng chứng cho task của mình.",
        "Không cập nhật = coi như “Chưa làm”. Không có ngoại lệ.",
        "Cuối tuần: đọc dashboard + lọc các task “Đang chờ”, giải quyết hết trước khi sang tuần mới.",
        "Không đổi trạng thái task của người khác — chỉ người phụ trách hoặc người review được đổi.",
        "Deadline tô đỏ khi đã quá hạn mà task chưa Hoàn thành.",
    ], y)

    y = block("4. Đọc dashboard thế nào", [
        "Tổng task / Hoàn thành / Đang làm / Đang chờ / Chưa làm: tự đếm từ cột Trạng thái.",
        "% hoàn thành = Hoàn thành / Tổng task.",
        "Tổng giờ = tổng cột Giờ; so với năng lực ở sheet “Theo người” (60h/người nếu 15h/tuần).",
        "Ô cảnh báo đỏ hiện khi có hơn 3 task “Đang chờ” — lúc đó phải họp gỡ, không chờ cuối tuần.",
    ], y)

    block("5. Sinh lại file", [
        "Chạy: python scripts/gen_assignment_xlsx.py",
        "Ghi đè cả file Excel và tasks/todo.md — mất mọi chỉnh tay. Nếu đã track thật thì sửa trực tiếp trong Excel, đừng chạy lại.",
    ], y)

    out = ROOT / "tasks" / "phan-cong-4-tuan.xlsx"
    out.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)
    print("saved", out.name)

    # ================= todo.md =================
    lines = [
        "# Task list — vCraft (4 tuần)",
        "",
        "Bản theo dõi chính: **`tasks/phan-cong-4-tuan.xlsx`** (dropdown trạng thái + dashboard + ước lượng giờ).",
        "File này là bản đọc nhanh trong repo — cùng ID, cùng phân công.",
        "",
        "Trạng thái: `Chưa làm` · `Đang làm` · `Đang chờ` · `Hoàn thành` · `Bỏ (đã cắt)`.",
        "Hoàn thành = PR merged + test pass + demo được + có link bằng chứng.",
        "",
    ]
    for week in (1, 2, 3, 4):
        lines += [f"## Tuần {week}", "",
                  "| ID | Việc | Phụ trách | Hỗ trợ | Tiêu chí xong | Ưu tiên | Giờ | Deadline | Trạng thái |",
                  "|---|---|---|---|---|---|---|---|---|"]
        for (wk, tid, title, owner, support, output, done, prio, deadline, hours) in TASKS:
            if wk != week:
                continue
            lines.append(f"| {tid} | {title} | {owner} | {support or '—'} | {done} | {prio} | {hours}h | {deadline} | Chưa làm |")
        lines.append("")
    lines += ["## Đã cắt khỏi V1", "", "| Hạng mục | Chuyển sang | Lý do | Ngày |", "|---|---|---|---|"]
    for (item, to, why, day) in CUTS:
        lines.append(f"| {item} | {to} | {why} | {day} |")
    lines += ["", "## Backlog", "", "| ID | Việc | Giá trị | Khi nào |", "|---|---|---|---|"]
    for (bid, title, value, when) in BACKLOG:
        lines.append(f"| {bid} | {title} | {value} | {when} |")
    total_hours = sum(t[9] for t in TASKS)
    lines += ["", f"**Tổng ước lượng: {total_hours}h** (năng lực 120-180h cho 3 người × 4 tuần).",
              "", "## Lịch sử", "", "| Ngày | Thay đổi | Người |", "|---|---|---|",
              "| 2026-11-17 | Cân lại tải: chuyển 3 task CRUD/QR sang Đông, thêm 4 màn UI cho Quân, cắt F7+F11, thêm cột Giờ | Nhóm |", ""]

    (ROOT / "tasks" / "todo.md").write_text("\n".join(lines), encoding="utf-8")
    print("saved tasks/todo.md", f"total {total_hours}h")


if __name__ == "__main__":
    build()
