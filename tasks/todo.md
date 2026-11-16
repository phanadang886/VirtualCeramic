# Task list — vCraft

Nguồn: `docs/requirements.md` §4 (12 tính năng) và §7 (11 tiêu chí nghiệm thu).
Cột **Phụ trách** để trống — nhóm tự chia khi bắt đầu code.

Cách dùng: mỗi PR phải gắn với 1 mục ở đây và 1 tiêu chí ở `docs/requirements.md` §7 (xem `AGENTS.md` → Quy trình Git).

## Tuần 1 — Nền

| ID | Việc | Phụ trách | Tiêu chí §7 | Trạng thái |
|---|---|---|---|---|
| T1.1 | `git init`, remote GitHub, `.gitignore`, `.env.example`, Makefile | | — | [x] |
| T1.2 | Chốt tên miền, DNS, tạo repo GitHub | | — | [ ] |
| T1.3 | Dựng compose: postgres + api + web; `make up`, `make seed` | | — | [ ] |
| T1.4 | Model DB đầy đủ theo ERD (`docs/architecture.md` §4) + Alembic migration đầu | | — | [ ] |
| T1.5 | Chốt `/api` contract → FastAPI sinh `/openapi.json` → `openapi-typescript` sinh type TS | | — | [ ] |
| T1.6 | Auth: JWT cookie httpOnly, argon2, dependency `get_current_user`, phân quyền 3 vai trò | | dòng 1 | [ ] |
| T1.7 | Cấu hình Nginx + HTTPS + `PUBLIC_BASE_URL` + QR base URL | | — | [ ] |
| T1.8 | Script seed dữ liệu Bát Tràng (5 hộ, 40-60 sản phẩm, 4 đơn, 5 ghim, 4 tin) | | — | [ ] |

## Tuần 2 — Artisan + Buyer cơ bản

| ID | Việc | Phụ trách | Tiêu chí §7 | Trạng thái |
|---|---|---|---|---|
| T2.1 | Hồ sơ xưởng: CRUD + ảnh + chứng nhận | | — | [ ] |
| T2.2 | Sản phẩm: CRUD + phân loại + tìm kiếm + phân trang | | dòng 9 | [ ] |
| T2.3 | Pipeline ảnh: Pillow resize 400/1200 WebP + validate magic bytes + ≤10MB | | dòng 10 | [ ] |
| T2.4 | Nhật ký sản xuất: mốc + ngày + ảnh, template công đoạn dùng chung | | dòng 2 | [ ] |
| T2.5 | QR: sinh QR từ `PUBLIC_BASE_URL`, trang công khai `/p/{token}` (không cần login) | | dòng 2 | [ ] |
| T2.6 | Danh mục buyer: lọc theo hộ / phân loại / tìm tên | | dòng 9 | [ ] |
| T2.7 | Bản đồ: react-leaflet, ghim, popup, tile cache | | dòng 8 | [ ] |
| T2.8 | Admin duyệt/từ chối hộ + audit log | | dòng 1 | [ ] |
| T2.9 | Tin cộng đồng: admin đăng trực tiếp, artisan gửi bài chờ duyệt | | dòng 7 | [ ] |

## Tuần 3 — Nghiệp vụ lõi

| ID | Việc | Phụ trách | Tiêu chí §7 | Trạng thái |
|---|---|---|---|---|
| T3.1 | Máy trạng thái quote (draft→sent→bidding→accepted→in_production→delivered) + `FOR UPDATE` | | dòng 3 | [ ] |
| T3.2 | Chào giá (1 hộ 1 lần), chấp nhận 1 bid, tạo order + lot | | dòng 3 | [ ] |
| T3.3 | Theo dõi công đoạn: cập nhật, cấm nhảy cóc, timeline + % hoàn thành | | dòng 4, 5 | [ ] |
| T3.4 | Admin chia đơn lớn cho nhiều hộ + chặn giao vượt số lượng | | dòng 6 | [ ] |
| T3.5 | Audit log cho mọi chuyển trạng thái | | — | [ ] |
| T3.6 | Test: unit service + integration API (pytest, httpx) | | — | [ ] |

## Tuần 4 — Hoàn thiện & demo

| ID | Việc | Phụ trách | Tiêu chí §7 | Trạng thái |
|---|---|---|---|---|
| T4.1 | Tối ưu: index DB, ảnh 400px, lazy-load route, kiểm tra LCP/CLS | | dòng 9 | [ ] |
| T4.2 | Accessibility: kiểm tra axe, focus, alt text, tương phản | | — | [ ] |
| T4.3 | Rà soát lỗi 500 trên toàn bộ luồng | | dòng 11 | [ ] |
| T4.4 | Nạp đủ dữ liệu mẫu + ảnh (nằm trong repo) | | — | [ ] |
| T4.5 | `README.md` + `docs/demo-script.md` hoàn chỉnh | | — | [ ] |
| T4.6 | Chạy kịch bản A và B ít nhất 1 lần mỗi kịch bản | | — | [ ] |
| T4.7 | Quay video dự phòng 3 phút | | — | [ ] |
| T4.8 | Kiểm tra checklist trước buổi thi (`docs/demo-script.md` §1) | | — | [ ] |

## Ngoài V1 (backlog)

Xem `docs/requirements.md` §10. Ưu tiên cao nhất cho hướng nghề, chỉ làm nếu V1 xong sớm:

| ID | Việc | Ghi chú |
|---|---|---|
| B1 | GitHub Actions: lint + test + build image | DevOps |
| B2 | Redis: rate-limit + cache catalog | DevOps/DE |
| B3 | Prometheus + Grafana (compose profile `ops`) | AIOps |
| B4 | Locust: 1 script load test + đọc số liệu | AIOps |
| B5 | Nginx cache nâng cao / CDN | DevOps |

## Lịch sử

| Ngày | Thay đổi | Người |
|---|---|---|
| 2026-11-16 | Tạo khung task từ §7, chưa phân công | Nhóm |
