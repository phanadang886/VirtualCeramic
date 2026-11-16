# ADR-001: Chọn stack công nghệ cho vCraft

- **Trạng thái:** Đã chốt
- **Ngày:** 2026-11-16
- **Người quyết định:** Nhóm vCraft (3 thành viên)
- **Liên quan:** `docs/requirements.md`, `docs/architecture.md`, `CONSTRAINTS.md`

## Bối cảnh

Ràng buộc đã chốt (xem `docs/requirements.md` §6):

- Nhóm 3 người, deadline 4 tuần (target 2026-12-14), demo trực tiếp tại buổi thi vấn đáp
- Công nghệ do nhóm tự chọn (đề bài cho phép)
- Demo phải chạy được **cả khi không có mạng** → dữ liệu mẫu + ảnh sẵn nằm trong repo
- Domain công khai + HTTPS (xem ADR-002)
- Hệ thống xử lý ảnh nhiều (catalog hàng trăm sản phẩm), state machine phức tạp, bản đồ, phân quyền 3 vai trò
- Hướng nghề sau đồ án của nhóm: DevOps / Data Engineering / Data AIOps

11 tiêu chí nghiệm thu ở `docs/requirements.md` §7 là thang điểm thực dụng. Mọi lựa chọn dưới đây đều phải phục vụ **tick hết 11 dòng**, không phục vụ sở thích công nghệ.

## Quyết định

### Lõi V1 (bắt buộc — phải có để tick đủ §7)

| Tầng | Công nghệ | Dùng cho yêu cầu nào |
|---|---|---|
| Backend framework | **FastAPI** (Python 3.12) | toàn bộ API |
| ASGI server | **Uvicorn** | chạy FastAPI, hỗ trợ `--proxy-headers` phía sau Nginx |
| Database | **PostgreSQL 16** (Docker) | dữ liệu, transaction, khoá bản ghi |
| ORM | **SQLAlchemy 2 (async)** + **asyncpg** | truy vấn |
| Migration | **Alembic** | quản lý schema |
| Validation | **Pydantic v2** | validate input + response schema |
| Auth | **PyJWT** + **argon2-cffi**, token trong cookie httpOnly | F1, F2 |
| Ảnh | **Pillow** + **aiofiles** | F10 — resize 400px/1200px, xuất WebP |
| QR | **qrcode[pil]** | F5 — sinh QR mỗi sản phẩm |
| Frontend | **React 19 + Vite + TypeScript** | toàn bộ UI |
| Styling | **Tailwind CSS + shadcn/ui** | UI image-centric, component có sẵn a11y |
| Server state | **TanStack Query** | dữ liệu từ API |
| Routing | **React Router** | điều hướng + route bảo vệ theo role |
| Validation FE | **Zod** | validate form, khớp với Pydantic |
| Bản đồ | **react-leaflet** + tile OSM | F7 |
| Hạ tầng | **Docker Compose** (db + api + web) | chạy 1 lệnh, môi trường giống nhau cho 3 người |
| Test | **pytest** + **httpx.AsyncClient** + **pytest-cov** | chứng minh chức năng chạy |
| Lint/format | **ruff** (BE) + **eslint/prettier** (FE) | giữ code đồng nhất |
| Reverse proxy | **Nginx** | domain + TLS + file tĩnh (ADR-002) |

### Để sau (không tính vào V1)

| Công nghệ | Khi nào thêm | Vì sao để sau |
|---|---|---|
| **Redis** | Khi cần rate-limit ở nhiều instance, hoặc cache catalog | 11 tiêu chí §7 không cần Redis. Thêm 1 service = thêm 1 thứ có thể chết lúc demo |
| **GitHub Actions** | Tuần 1 nếu rảnh (lint + test) | Rẻ, giá trị CV cao, nhưng không điểm đồ án |
| **Locust** | Tuần 4, 1 script load test | Đúng chuyên môn DevOps/AIOps, nhưng không có trong đề bài |
| **Prometheus + Grafana** | Tuần 4, compose profile `ops` | Số liệu RED + dashboard — cần cho hướng AIOps, không cần cho §7 |
| **Nginx cache nâng cao / CDN** | Khi lưu lượng tăng | Vài trăm sản phẩm thì Nginx + gzip là đủ |

### Cố ý không làm

| Không làm | Lý do |
|---|---|
| Hàng đợi ảo (xây queue tự chuyển) | Không có trong đề bài. Tự xây queue là 1 feature không chấm mà ăn thời gian |
| Thanh toán thật / cổng thanh toán | Đề bài không yêu cầu; demo dùng tài khoản nhóm |
| MongoDB | State machine + quan hệ đơn hàng cần transaction; Mongo làm sinh bug khó demo |
| Firebase | Không chạy offline → vi phạm ràng buộc demo |
| Google Maps API | Cần key + billing + chết khi mất mạng. Đề bài cho phép Leaflet (mã nguồn mở) |
| Microservices / message broker | Quá xa cho 4 tuần, 3 người |
| Kubernetes / Terraform | Học ở project khác. 4 tuần không đủ |
| Next.js (full-stack) | Xem "phương án bị loại" |

## Lý do chi tiết

**FastAPI + Uvicorn (thay vì Flask/Django/NestJS/Next.js)**
Sinh OpenAPI tự động → **contract sinh từ code**, đúng nguyên tắc ở `docs/api.md`. Cùng hệ sinh thái với hướng DE/AIOps sau này. FastAPI có sẵn Pydantic validation, kiểu type rõ ràng — tài liệu API tự sinh gần như miễn phí.

**PostgreSQL thay vì SQLite**
Yêu cầu 4.2 của đề bài nói rõ "logic khóa bản ghi và cập nhật trạng thái phức tạp hơn mua bán thông thường". SQLite khoá cả database nên khó demo hai người cùng thao tác một đơn. Postgres có `SELECT ... FOR UPDATE` → demo được tình huống "2 người cùng chấp nhận 1 báo giá" một cách thuyết phục. Đây là điểm ăn điểm rõ nhất của đồ án.

**SQLAlchemy async**
Phải cấm lazy load (`selectinload`/`joinedload` mọi nơi) — nếu không sẽ dính lỗi `MissingGreenlet` khi truy cập quan hệ ngoài ngữ cảnh async. Đây là lỗi phổ biến nhất của stack này, ghi trong `docs/architecture.md`.

**React + Vite + Tailwind + shadcn/ui**
shadcn/ui cho component có sẵn accessibility (focus trap, ARIA) — `frontend-ui-engineering` trong `CONSTRAINTS.md` yêu cầu WCAG 2.1 AA. Tailwind để có design token thống nhất, tránh giao diện "AI aesthetic". Vite build nhanh, dev server nhẹ.

**Docker Compose**
Ba người phải chạy giống nhau. `docker compose up` + `make seed` là đủ. Với kinh nghiệm DevOps sau này thì Compose là nền tảng, không phí.

## Phương án bị loại

| Phương án | Vì sao loại |
|---|---|
| **Next.js full-stack** | Nhanh nhất tới demo, ít thứ phải học nhất. Nhưng: không có backend Python (đi ngược hướng nghề DE/AIOps), khoá bản ghi yếu hơn, React + Node + Python = 2 stack thay vì 1 |
| **Django + templates** | Có admin panel miễn phí, ORM + auth + migration sẵn. Nhưng UI image-centric khó làm đẹp nhanh, template server-rendered làm nặng phần UI đẹp nhất của bài |
| **Laravel + Blade/Tailwind** | Tương tự Django, mạnh nhưng PHP lệch hướng nghề |
| **NestJS + React** | 2 server, boilerplate nhiều, cần Nest CLI, tốn thời gian học |
| **Express + React** | Thiếu type safety, thiếu validation tích hợp, thiếu OpenAPI → phải tự viết contract |
| **Next.js + Postgres** (hybrid) | 2 codebase mà vẫn thiếu hệ sinh thái Python cho hướng DE/AIOps |

## Hệ quả

**Tích cực**
- 1 ngôn ngữ backend (Python), 1 frontend (TypeScript) → 3 người chia việc theo vai trò rõ ràng
- OpenAPI sinh tự động → `openapi-typescript` sinh type TS cho FE, không bao giờ lệch contract
- Docker → môi trường giống nhau, demo offline được
- Nền tảng đúng hướng DevOps/DE/AIOps sau này

**Tiêu cực (phải quản lý)**
- Async SQLAlchemy dễ sai → bắt buộc quy ước trong `docs/architecture.md`
- 2 tiến trình chạy (api + web) → CORS, cookie, proxy
- Docker trên Windows đôi lúc chậm → dev dùng native, chỉ db trong Docker
- Học 3 thứ mới cùng lúc (FastAPI async, Docker, Nginx) → tuần 1 dành riêng cho đồng bộ cả nhóm

## Câu hỏi còn mở

| Câu hỏi | Ảnh hưởng | Chốt khi |
|---|---|---|
| Postgres chạy trong Docker hay cài native? | Trong Docker = 1 lệnh cho cả nhóm. Native = nhanh hơn nhưng mỗi người cài riêng | Tuần 1 |
| Có ai trong nhóm đã viết FastAPI async chưa? | Nếu không ai → cân nhắc SQLAlchemy **sync** + `psycopg` để giảm rủi ro | Trước khi code |
| Ai làm hạ tầng (Docker, Nginx, CI)? | Cần 1 người giữ vai trò DevOps trong nhóm | Khi chia việc |

## Lịch sử

| Ngày | Thay đổi | Người |
|---|---|---|
| 2026-11-16 | Quyết định đầu tiên. FastAPI + Postgres + React/Vite/Tailwind. Cắt Redis/Locust/Prometheus khỏi V1 | Nhóm |
