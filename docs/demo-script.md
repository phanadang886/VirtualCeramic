# Kịch bản demo vCraft

- **Phiên bản:** 1.0 | **Cập nhật:** 2026-11-16
- **Dùng cho:** buổi thi vấn đáp demo trực tiếp (không slide)
- **Liên quan:** `docs/requirements.md` §7 (11 tiêu chí nghiệm thu), `docs/architecture.md`, `docs/decisions/ADR-002-nginx-public-dns.md`

## 0. Mục tiêu

- Chạy trọn **10 phút**, mỗi bước đúng 1 tiêu chí ở §7
- Giảng viên nhìn thấy sản phẩm, không nghe diễn giải
- **Mỗi bước demo đều có bằng chứng trên màn hình** (không nói "em đã làm được")
- Có phương án B khi mạng chết

## 1. Chuẩn bị trước buổi thi (làm xong từ hôm trước, không phải tại chỗ)

| # | Việc | Cách kiểm tra | Lệnh |
|---|---|---|---|
| 1 | DNS trỏ đúng IP | `dig +short vcraft.vn` ra IP máy ảo | `dig +short vcraft.vn` |
| 2 | HTTPS còn hạn | trình duyệt không cảnh báo | `certbot certificates` |
| 3 | Chỉ mở 80/443 | quét từ máy ngoài | `nmap -p 1-1000 <ip>` |
| 4 | Image Docker đã tải sẵn | không cần mạng | `docker pull postgres:16-alpine && docker pull nginx:alpine` |
| 5 | App đã build & chạy | mở domain thấy trang chủ | `docker compose up -d && curl -I https://vcraft.vn` |
| 6 | Dữ liệu mẫu đúng | đủ 5 hộ, 40+ sản phẩm, 4 đơn | `make seed && make seed-check` |
| 7 | **QR quét bằng điện thoại thật** | mở đúng trang sản phẩm | quét QR mẫu |
| 8 | Phương án B chạy được | mở `http://vcraft.local` | `docker compose -f deploy/docker-compose.offline.yml up` |
| 9 | Tài khoản demo nhớ sẵn | xem bảng §2 | — |
| 10 | Có màn hình/điện thoại làm thiết bị thứ hai | dùng để quét QR | — |
| 11 | Ảnh chụp màn hình dự phòng (video) | quay sẵn 3 phút đầy đủ luồng | — |
| 12 | Sách vở không, chỉ dùng app | đề bài yêu cầu demo trực tiếp | — |

## 2. Tài khoản demo

| Vai trò | Email | Mật khẩu | Dùng để demo |
|---|---|---|---|
| Admin | `admin@vcraft.vn` | (nhớ) | duyệt hộ, duyệt tin, chia đơn, dashboard |
| Artisan (đã duyệt) | `xungmai@vcraft.vn` | (nhớ) | hồ sơ, sản phẩm, chào giá, cập nhật công đoạn |
| Artisan (chờ duyệt) | `xungmoi@vcraft.vn` | (nhớ) | luồng duyệt hộ |
| Buyer | `khachsieu@vcraft.vn` | (nhớ) | danh mục, bản đồ, tạo đơn, chấp nhận báo giá |

> Mật khẩu đặt trong `.env`, không commit. In ra giấy làm phương án dự phòng.

## 3. Dữ liệu mẫu

| Loại | Số lượng | Ghi chú |
|---|---|---|
| Hộ gia đình | 5 | 4 đã duyệt + 1 chờ duyệt |
| Sản phẩm | 40-60 | 6 nhóm phân loại, mỗi sản phẩm 4-7 mốc sản xuất |
| Ảnh | 3-5 / sản phẩm | ảnh CC0 hoặc tự chụp, đã resize sẵn |
| Yêu cầu báo giá | 4 | 1 đơn lớn 5000 cốc, 1 đang bidding, 1 đã chia 3 hộ, 1 đã giao |
| Báo giá | 2-3 / đơn | có 1 bid được chọn, các bài còn lại "không chọn" |
| Ghim bản đồ | 5 | toạ độ thật Bát Tràng từ OSM |
| Tin cộng đồng | 4-5 | 1 bài chờ duyệt, 1 bài bị từ chối có lý do |
| Mốc công đoạn đơn | theo đơn | 1 đơn đang dở giữa chừng để demo timeline |

Mọi màn hình demo có nhãn nhỏ: **"Dữ liệu trong bản demo là dữ liệu mẫu"**.

## 4. Kịch bản A — demo qua domain (kịch bản chính)

> Thời lượng mục tiêu: 10 phút. Ba vai trò mở sẵn 3 tab (Admin / Artisan / Buyer).

| Bước | Thời lượng | Ai thao tác | Hành động trên màn hình | Tiêu chí §7 |
|---|---|---|---|---|
| 1 | 0:00-0:30 | — | Mở trang chủ: banner "Triển lãm số làng gốm Bát Tràng", tin cộng đồng mới nhất | — (mở đầu) |
| 2 | 0:30-1:30 | Admin | Tab Admin → "Hộ chờ duyệt" → duyệt 1 hộ → tab Artisan của hộ đó báo "Đã được duyệt" | dòng 1 (duyệt hộ) |
| 3 | 1:30-3:00 | Artisan | Tab Artisan → "Sản phẩm" → mở 1 sản phẩm có sẵn → thêm 1 mốc sản xuất kèm ảnh → lưu | dòng 2 (sản phẩm + mốc) |
| 4 | 3:00-4:00 | Artisan | Bấm "Tạo QR" → hiện mã QR → **quét bằng điện thoại** → mở trang công khai: câu chuyện + timeline mốc | dòng 2 (QR hoạt động) |
| 5 | 4:00-5:00 | Buyer | Tab Buyer → "Danh mục" → lọc theo hộ → lọc theo phân loại → tìm theo tên → mở 1 sản phẩm | dòng 9 (danh mục) |
| 6 | 5:00-5:45 | Buyer | Tab "Bản đồ" → thấy 5 ghim → bấm 1 ghim → popup tên xưởng + trạng thái mở/đóng | dòng 8 (bản đồ) |
| 7 | 5:45-7:00 | Buyer | Tạo yêu cầu báo giá 5.000 cốc → gửi | — (đặt đơn) |
| 8 | 7:00-7:45 | Artisan | Vào "Đơn được mời" → chào giá (giá + số ngày) | dòng 3 (bidding) |
| 9 | 7:45-8:30 | Buyer | Mở đơn → thấy 2 báo giá → chấp nhận 1 → trạng thái chuyển `accepted` → đơn hàng tạo ra | dòng 3 (accept) |
| 10 | 8:30-9:15 | Artisan | Mở đơn → cập nhật 2 công đoạn (đánh dấu xong) → Buyer xem timeline cập nhật theo + % hoàn thành | dòng 4, 5 |
| 11 | 9:15-9:45 | Admin | Mở đơn lớn → "Chia đơn" → giao 3 hộ với số lượng → xem tiến độ tổng hợp | dòng 6 (chia đơn) |
| 12 | 9:45-10:00 | Artisan | Vào "Tin cộng đồng" → gửi 1 bài PR (hộ đạt giải thưởng) → Admin duyệt → bài hiện trên trang chủ | dòng 7 (tin PR) |

**Cách mở đầu (nói 1 câu, không đọc slide):**
> "vCraft là nền tảng triển lãm số cho làng gốm Bát Tràng: mỗi hộ có không gian riêng, mỗi sản phẩm có mã QR truy xuất nguồn gốc, và BQL điều phối được đơn hàng lớn. Em demo luồng chính."

**Cách kết (1 câu):**
> "11 tiêu chí nghiệm thu trong `docs/requirements.md` đều đã chạy trực tiếp, đây là bảng điều khiển đơn hàng."

## 5. Kịch bản B — offline (khi mạng chết)

Kích hoạt khi: domain không resolve, VM tắt, mạng trường chặn, hoặc thầy yêu cầu thử ở máy nhóm.

```bash
# 1. chạy bản tối giản
docker compose -f deploy/docker-compose.offline.yml up -d

# 2. trỏ domain giả về localhost
echo "127.0.0.1 vcraft.local" | sudo tee -a /etc/hosts   # Windows: mở file hosts bằng Notepad (quyền admin)

# 3. mở
start http://vcraft.local
```

| Khác biệt so với kịch bản A | Xử lý |
|---|---|
| HTTP, không có HTTPS → cookie `secure=false` | `COOKIE_SECURE=false` trong `.env` của bản offline |
| QR trỏ `http://<IP-LAN>` thay vì domain | `PUBLIC_BASE_URL=http://192.168.x.y` (IP LAN của máy đang chạy) — **điện thoại phải cùng Wi-Fi** |
| Không có DNS, không có cert | Không cần |

Nếu cả kịch bản B cũng hỏng → dùng video dự phòng (quay sẵn 3 phút) và nói: "Em quay sẵn toàn bộ luồng, em thuyết minh bằng video và sau đó em chạy trực tiếp nếu được."

## 6. Bẫy thường gặp và cách xử lý

| Bẫy | Biểu hiện | Xử lý trong 10 giây |
|---|---|---|
| DNS chưa kịp lan | domain không mở | chuyển ngay sang kịch bản B (đã chuẩn bị sẵn) |
| Ảnh chưa tải xong | ô trống | đã resize sẵn 2 bản, chỉ cần CDN/ng local — nếu vẫn lỗi thì nói "ảnh mẫu, em nạp sẵn trong repo" và tiếp tục |
| Đăng nhập bị đuổi | văng ra login giữa chừng | token 60 phút; nếu hết hạn → login lại (biết sẵn mật khẩu) |
| QR không mở trên điện thoại | trang trắng | kiểm tra `PUBLIC_BASE_URL`; nếu sai → dùng IP LAN và nói rõ đó là bản offline |
| Click nhầm "xoá" | mất sản phẩm demo | dùng bản seed có sẵn; `make seed` khôi phục trong 10 giây |
| Mạng lag | trang đơ | chuyển kịch bản B |
| Có người hỏi câu ngoài kịch bản | — | xem bảng §7 |

## 7. Câu hỏi dự kiến và câu trả lời

| Câu hỏi | Trả lời ngắn |
|---|---|
| "Vì sao chọn FastAPI?" | Sinh OpenAPI tự động → contract sinh từ code, frontend sinh type TS từ `/openapi.json`, không bao giờ lệch. Thêm validation Pydantic miễn phí. |
| "Vì sao PostgreSQL mà không SQLite?" | Yêu cầu 4.2 của đề bài cần khoá bản ghi khi 2 người cùng thao tác 1 đơn. Postgres có `SELECT ... FOR UPDATE`; SQLite khoá cả DB nên không demo được tình huống đó. |
| "Làm sao chống 2 người cùng chấp nhận 1 báo giá?" | Transaction + `FOR UPDATE` trên dòng `quote_requests`, kiểm tra trạng thái trong transaction, chỉ 1 bid được chuyển `accepted`, các bài còn lại `rejected`. Ghi `audit_log`. |
| "Ảnh nén ở đâu, không làm chậm server không?" | Pillow resize trong `run_in_threadpool` (không chặn event loop), xuất WebP 2 bản 400px/1200px, Nginx phục vụ file tĩnh nên request ảnh không đi qua Python. |
| "QR chứa gì?" | UUID token lưu DB, không phải slug — nên đổi tên sản phẩm không làm hỏng QR đã in. URL dựng từ `PUBLIC_BASE_URL`. |
| "Phân quyền thế nào?" | 3 vai trò trong `users.role`, middleware/dependency kiểm tra ở từng route, kiểm tra sở hữu (chỉ chủ workshop sửa sản phẩm của mình). |
| "Có test không?" | `pytest` + `httpx.AsyncClient`; báo cáo coverage trong `CONSTRAINTS.md`; ngưỡng dòng mới ≥ 80%. |
| "Nếu mạng chết lúc demo?" | Có sẵn kịch bản B: chạy offline qua `docker compose -f deploy/docker-compose.offline.yml`, domain giả trong `/etc/hosts`, dữ liệu mẫu nằm trong repo. |
| "Demo trên máy nào?" | Máy cá nhân nhóm + máy ảo Linux chạy public domain; nếu thầy muốn, chạy trên máy giảng viên bằng kịch bản B. |
| "Có làm CI/CD không?" | GitHub Actions: lint + test + build image. Chi tiết trong ADR-001. |
| "Tại sao không dùng AI để làm UI?" | UI được xây từ design system + component có sẵn accessibility (WCAG 2.1 AA), kiểm tra bằng axe. AI tạo UI dễ ra "AI aesthetic" và thiếu trạng thái lỗi/rỗng. |

## 8. Phân vai khi demo

| Người | Nói | Thao tác |
|---|---|---|
| A | Mở đầu, điều phối, trả lời câu hỏi | — |
| B | Artisan: sản phẩm, mốc, QR, chào giá, công đoạn | tab Artisan |
| C | Buyer + Admin: duyệt hộ, danh mục, bản đồ, đơn, chia | tab Buyer + tab Admin |

Chuẩn bị trước: 3 tab đã đăng nhập sẵn, đúng trình duyệt, màn hình chính là tab Buyer, 1 điện thoại đã mở sẵn camera.

## 9. Lịch sử

| Ngày | Thay đổi | Người |
|---|---|---|
| 2026-11-16 | Phiên bản 1.0: kịch bản A (domain) + B (offline), bẫy thường gặp, câu hỏi dự kiến | Nhóm |
