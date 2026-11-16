# Task list — vCraft (4 tuần)

Bản theo dõi chính: **`tasks/phan-cong-4-tuan.xlsx`** (dropdown trạng thái + dashboard + ước lượng giờ).
File này là bản đọc nhanh trong repo — cùng ID, cùng phân công.

Trạng thái: `Chưa làm` · `Đang làm` · `Đang chờ` · `Hoàn thành` · `Bỏ (đã cắt)`.
Hoàn thành = PR merged + test pass + demo được + có link bằng chứng.

## Tuần 1

| ID | Việc | Phụ trách | Hỗ trợ | Tiêu chí xong | Ưu tiên | Giờ | Deadline | Trạng thái |
|---|---|---|---|---|---|---|---|---|
| T1.1 | Repo GitHub, .gitignore, .gitattributes | Đông | — | `git push` thành công, 3 người clone được | Must | 1h | 2026-11-18 | Chưa làm |
| T1.2 | Docker Compose (db + api + web) | Phan Anh | Đông | `make up` chạy, 3 service healthy | Must | 4h | 2026-11-19 | Chưa làm |
| T1.3 | .env.example + Makefile (up/down/seed/test/logs) | Đông | — | người mới chạy 1 lệnh là có app | Must | 2h | 2026-11-19 | Chưa làm |
| T1.4 | Schema 19 bảng + Alembic migration đầu | Phan Anh | — | `alembic upgrade head` sạch trên DB trống | Must | 8h | 2026-11-21 | Chưa làm |
| T1.5 | Auth: JWT cookie httpOnly, argon2, role dependency | Phan Anh | — | 3 vai trò đăng nhập, sai role bị 403 | Must | 6h | 2026-11-21 | Chưa làm |
| T1.6 | docs/api.md → OpenAPI → type TS cho FE | Phan Anh | Quân | FE gọi /api/auth/me bằng type sinh tự động | Must | 3h | 2026-11-23 | Chưa làm |
| T1.7 | Design tokens + layout + trang đăng nhập/đăng ký | Quân | — | 2 trang chạy, responsive 320/1440 | Must | 10h | 2026-11-23 | Chưa làm |
| T1.8 | Seed data Bát Tràng (5 hộ, 40-60 SP, 4 đơn, 5 ghim, 4 tin) | Đông | — | `make seed` chạy 2 lần không nhân đôi dữ liệu | Must | 8h | 2026-11-23 | Chưa làm |
| T1.9 | Smoke test schema portable (tạo schema + CRUD trên SQLite) | Đông | — | pytest pass — chứng minh độc lập CSDL | Must | 3h | 2026-11-23 | Chưa làm |
| T1.10 | MỐC TUẦN 1 | Cả nhóm | — | `make up` + login 3 vai trò + seed có dữ liệu | Mốc | 0h | 2026-11-23 | Chưa làm |

## Tuần 2

| ID | Việc | Phụ trách | Hỗ trợ | Tiêu chí xong | Ưu tiên | Giờ | Deadline | Trạng thái |
|---|---|---|---|---|---|---|---|---|
| T2.1 | Hồ sơ xưởng CRUD + ảnh + chứng nhận | Đông | Phan Anh | artisan sửa hồ sơ, trang công khai cập nhật | Must | 6h | 2026-11-25 | Chưa làm |
| T2.2 | Sản phẩm CRUD: list/filter/paginate | Đông | Phan Anh | CRUD theo contract, không lỗi 500 | Must | 4h | 2026-11-26 | Chưa làm |
| T2.3 | Pipeline ảnh: Pillow WebP 400/1200 + magic bytes + ≤10MB | Phan Anh | — | upload 5 ảnh, 1 ảnh lỗi không chặn ảnh khác | Must | 8h | 2026-11-27 | Chưa làm |
| T2.4 | Tìm kiếm + index sản phẩm (ILIKE, phân trang server-side) | Phan Anh | — | 200 SP lọc/tìm < 1 giây | Must | 4h | 2026-11-27 | Chưa làm |
| T2.5 | QR token + qr_service (PUBLIC_BASE_URL) | Phan Anh | — | token không trùng, URL đúng môi trường | Must | 2h | 2026-11-27 | Chưa làm |
| T2.6 | Trang công khai /p/{token} + template timeline | Đông | Phan Anh | quét điện thoại mở đúng trang, không cần login | Must | 3h | 2026-11-28 | Chưa làm |
| T2.7 | Danh mục UI: lọc hộ/phân loại, tìm, skeleton/empty/error | Quân | — | đủ 4 trạng thái, không cuộn ngang | Must | 6h | 2026-11-26 | Chưa làm |
| T2.8 | Upload UI: progress từng ảnh, lỗi riêng từng ảnh | Quân | — | upload 5 ảnh thấy 5 progress | Must | 6h | 2026-11-28 | Chưa làm |
| T2.9 | F13 nhập liệu: autocomplete, tự điền, format giá/ngày, lỗi theo field | Quân | — | gõ 2 ký tự ra gợi ý, chọn bằng bàn phím | Must | 8h | 2026-11-29 | Chưa làm |
| T2.10 | Admin backend: duyệt/từ chối hộ | Đông | Phan Anh | duyệt → đăng nhập được; từ chối có lý do | Must | 6h | 2026-11-28 | Chưa làm |
| T2.11 | Test auth + sản phẩm + upload | Đông | — | pytest pass, coverage dòng mới ≥ 80% | Must | 8h | 2026-11-30 | Chưa làm |
| T2.12 | MỐC TUẦN 2 | Cả nhóm | — | §7 dòng 2, 8, 10 xanh | Mốc | 0h | 2026-11-30 | Chưa làm |

## Tuần 3

| ID | Việc | Phụ trách | Hỗ trợ | Tiêu chí xong | Ưu tiên | Giờ | Deadline | Trạng thái |
|---|---|---|---|---|---|---|---|---|
| T3.1 | State machine quote + with_for_update() | Phan Anh | — | đi đủ 6 trạng thái, chuyển sai trả 409 | Must | 10h | 2026-12-02 | Chưa làm |
| T3.2 | Bidding (1 hộ 1 lần) + accept 1 bid + tạo order/lot | Phan Anh | — | 2 người accept cùng lúc → chỉ 1 thắng | Must | 8h | 2026-12-03 | Chưa làm |
| T3.3 | Công đoạn: cập nhật, cấm nhảy cóc, % hoàn thành | Phan Anh | — | không đánh dấu xong bước 3 khi bước 2 chưa xong | Must | 6h | 2026-12-04 | Chưa làm |
| T3.4 | Admin chia đơn + chặn vượt số lượng | Phan Anh | — | tổng lot ≤ quantity đơn | Must | 5h | 2026-12-05 | Chưa làm |
| T3.5 | Audit log mọi chuyển trạng thái | Phan Anh | — | tra được ai đổi, lúc nào, từ đâu sang đâu | Must | 3h | 2026-12-05 | Chưa làm |
| T3.6 | Luồng buyer UI: tạo đơn, xem bid, chấp nhận | Quân | — | 3 màn hình chạy, không reload | Must | 8h | 2026-12-04 | Chưa làm |
| T3.7 | Timeline công đoạn + % tiến độ | Quân | — | buyer thấy cập nhật ngay sau refresh | Must | 5h | 2026-12-05 | Chưa làm |
| T3.8 | F14: slug + 404 + SPA fallback (301 → backlog) | Quân | Phan Anh | refresh /san-pham/x vẫn mở đúng | Must | 4h | 2026-12-06 | Chưa làm |
| T3.9 | Test state machine — VIẾT TRƯỚC khi code | Đông | — | test fail trước khi Anh code, pass sau | Must | 8h | 2026-12-02 | Chưa làm |
| T3.10 | UI khu artisan: quản lý sản phẩm (form + mốc + upload) + danh sách đơn/chào giá | Quân | — | artisan tạo sản phẩm + chào giá không cần admin | Must | 10h | 2026-12-06 | Chưa làm |
| T3.11 | UI admin gộp 1 trang tabs: duyệt hộ + chia đơn + thống kê | Đông | Quân | 3 tab chạy, phân trang OK | Must | 6h | 2026-12-07 | Chưa làm |
| T3.12 | MỐC TUẦN 3 | Cả nhóm | — | §7 dòng 3, 4, 5, 6 xanh | Mốc | 0h | 2026-12-07 | Chưa làm |

## Tuần 4

| ID | Việc | Phụ trách | Hỗ trợ | Tiêu chí xong | Ưu tiên | Giờ | Deadline | Trạng thái |
|---|---|---|---|---|---|---|---|---|
| T4.1 | Index + EXPLAIN ANALYZE + ghi kế hoạch truy vấn | Phan Anh | — | danh mục 200 SP < 2.5 giây | Must | 4h | 2026-12-10 | Chưa làm |
| T4.2 | Analytics SQL: 3 truy vấn + view thống kê + ghi EXPLAIN | Phan Anh | Đông | 3 truy vấn chạy < 200ms trên seed | Should | 3h | 2026-12-10 | Chưa làm |
| T4.3 | ETL bulk seed (COPY) + idempotent + --reset | Đông | Phan Anh | seed 60 SP < 5 giây, chạy 2 lần không nhân đôi | Should | 3h | 2026-12-11 | Chưa làm |
| T4.4 | Polish UI (timebox 5h): 4 trạng thái + responsive + bản sắc | Quân | — | checklist design-system §10 pass | Must | 5h | 2026-12-12 | Chưa làm |
| T4.5 | a11y (timebox 3h): axe, keyboard, focus, alt text | Quân | — | 0 lỗi critical/serious | Must | 3h | 2026-12-12 | Chưa làm |
| T4.6 | Nginx + TLS + domain + rate limit | Đông | — | https://domain chạy, login 5 lần/phút bị chặn | Must | 6h | 2026-12-11 | Chưa làm |
| T4.7 | Demo script + video dự phòng + checklist trước thi | Đông | — | kịch bản A và B chạy được | Must | 5h | 2026-12-13 | Chưa làm |
| T4.8 | Tập demo 2 lần (kịch bản A và B) | Cả nhóm | — | 10 phút, không vấp | Mốc | 0h | 2026-12-13 | Chưa làm |
| T4.9 | Rà 10 kiểm tra hướng rubric + MỐC CUỐI | Đông | Cả nhóm | tick hết 10 dòng + §7 dòng 9, 11 xanh | Mốc | 3h | 2026-12-14 | Chưa làm |

## Đã cắt khỏi V1

| Hạng mục | Chuyển sang | Lý do | Ngày |
|---|---|---|---|
| F7 Bản đồ làng nghề | Chuyển V2 | Bỏ 6h; rubric #1 vẫn đủ với 13 feature còn lại | 2026-11-17 |
| F11 Tin cộng đồng (toàn bộ) | Chuyển V2 | Bỏ 8h; admin chỉ còn duyệt hộ + chia đơn | 2026-11-17 |
| 301 slug history (`slug_redirects`) | Chuyển V2 | Giữ slug + 404 + SPA fallback; bỏ bảng redirect | 2026-11-17 |
| Chuyển đổi đơn vị kg ↔ chiếc (F13) | Chuyển V2 | Giữ autocomplete + autofill + format giá/ngày | 2026-11-17 |
| Endpoint analytics riêng | Gộp vào view SQL | Đọc trực tiếp từ view trong admin UI | 2026-11-17 |

## Backlog

| ID | Việc | Giá trị | Khi nào |
|---|---|---|---|
| B1 | GitHub Actions: lint + test + build image | CI/CD, DevOps | Nếu V1 xong sớm |
| B2 | Redis: rate-limit + cache catalog | DevOps/DE | Sau V1 |
| B3 | Prometheus + Grafana (compose profile ops) | AIOps, observability | Sau V1 |
| B4 | Locust: 1 script load test + đọc số liệu | DevOps/AIOps | Tuần 4 nếu còn thời gian |
| B5 | Tự gắn nhãn ảnh sản phẩm (MobileNet/CLIP offline) | CV/AI portfolio | V2 hoặc project cá nhân |
| B6 | F7 Bản đồ làng nghề | Tính năng | V2 (đã cắt 2026-11-17) |
| B7 | F11 Tin cộng đồng + duyệt bài | Tính năng | V2 (đã cắt 2026-11-17) |
| B8 | 301 slug history (`slug_redirects`) | Kỹ thuật | V2 (đã cắt 2026-11-17) |
| B9 | Chuyển đổi đơn vị kg ↔ chiếc (F13) | Tính năng | V2 (đã cắt 2026-11-17) |

**Tổng ước lượng: 211h** (năng lực 120-180h cho 3 người × 4 tuần).

## Lịch sử

| Ngày | Thay đổi | Người |
|---|---|---|
| 2026-11-17 | Cân lại tải: chuyển 3 task CRUD/QR sang Đông, thêm 4 màn UI cho Quân, cắt F7+F11, thêm cột Giờ | Nhóm |
