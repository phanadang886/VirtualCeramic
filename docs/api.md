# API contract — vCraft

- **Phiên bản:** 1.0 | **Cập nhật:** 2026-11-16
- **Nguồn:** `docs/requirements.md` (F1–F12), `docs/architecture.md`
- **Base URL công khai:** `https://vcraft.vn` → qua Nginx → `/api`
- **Base URL dev:** `http://localhost:8000/api`

> **Nguồn chuẩn là OpenAPI sinh từ FastAPI**, không phải file này. File này là **hợp đồng thiết kế** để 3 người làm song song; khi backend chạy, FastAPI sinh `/openapi.json` và `openapi-typescript` sinh type TS cho frontend. Khi hai bên lệch → file này thắng, sửa code theo.

## Quy ước chung

| Mục | Quy ước |
|---|---|
| Định dạng | JSON, `snake_case` |
| Ngày giờ | ISO 8601 UTC (`2026-12-01T08:30:00Z`) |
| Ngày | `YYYY-MM-DD` |
| Tiền | số thập phân, không ký phân cách (`150000`) |
| ID | UUID v4 |
| Phân trang | `?page=1&page_size=20` — mặc định 20, tối đa 100 |
| Xác thực | cookie `access_token` (httpOnly) hoặc header `Authorization: Bearer <token>` |
| CORS | chỉ `CORS_ORIGINS` |

### Cấu trúc response

```json
{ "items": [...], "page": 1, "page_size": 20, "total": 137 }
```

Đối tượng đơn lẻ trả thẳng, không bọc:

```json
{ "id": "…", "name": "Bát tràng men lam" }
```

### Cấu trúc lỗi

```json
{
  "error": {
    "code": "QUOTE_NOT_BIDDING",
    "message": "Yêu cầu báo giá không ở trạng thái nhận chào giá.",
    "details": { "current_status": "sent" }
  }
}
```

| HTTP | `code` ví dụ | Khi nào |
|---|---|---|
| 400 | `VALIDATION_ERROR` | input sai định dạng |
| 401 | `UNAUTHENTICATED`, `TOKEN_EXPIRED` | chưa đăng nhập / token hết hạn |
| 403 | `FORBIDDEN_ROLE`, `FORBIDDEN_OWNER` | sai vai trò / không phải chủ sở hữu |
| 404 | `NOT_FOUND` | không tồn tại (kể cả QR không hợp lệ → **không** lỗi 500) |
| 409 | `CONFLICT_VERSION`, `DUPLICATE_BID`, `INVALID_TRANSITION` | xung đột trạng thái / phiên bản |
| 413 | `FILE_TOO_LARGE` | ảnh > `MAX_UPLOAD_MB` |
| 415 | `UNSUPPORTED_MEDIA_TYPE` | file không phải ảnh hợp lệ |
| 422 | `INVALID_QUANTITY` | nghiệp vụ không hợp lệ (số lượng vượt kho) |
| 429 | `RATE_LIMITED` | quá `rate=5r/m` ở `/api/auth/login` |

## Ma trận vai trò

Ký hiệu: ● bắt buộc · ○ tùy chọn · — không được

| Nhóm endpoint | Artisan | Buyer | Admin | Công khai |
|---|---|---|---|---|
| `/api/auth/*` | ● | ● | ● | ○ register |
| `/api/workshops/me` | ● | — | ○ đọc | — |
| `/api/workshops` | — | ○ đọc | ○ đọc | ● đọc |
| `/api/products` | ● của mình | ○ đọc published | ● đọc | ○ đọc published |
| `/api/public/products/{token}` | — | — | — | ● đọc |
| `/api/quote-requests` | ○ nhận + chào giá | ● tạo | ○ đọc | — |
| `/api/orders` | ○ lot của mình | ● của mình | ● đọc tất cả | — |
| `/api/order-lots/{id}/stages` | ● cập nhật lot của mình | — | ● đọc | — |
| `/api/map/workshops` | — | ○ đọc | ○ đọc | ● đọc |
| `/api/news` | ○ gửi bài của mình | ○ đọc | ● quản lý | ● đọc published |
| `/api/admin/*` | — | — | ● | — |

---

## 1. Xác thực

### `POST /api/auth/register`
Đăng ký tài khoản. Chỉ loại `artisan` cần admin duyệt; `buyer` kích hoạt ngay.

Body:
```json
{ "email": "x@vilabattrang.vn", "password": "…", "role": "artisan", "workshop_name": "Xưởng gốm men lam" }
```

- `201` → `{ "id": "…", "role": "artisan", "status": "pending" }`
- `409` → email đã tồn tại
- Tài khoản admin **không** tạo qua endpoint này (seed bằng `make seed`)

### `POST /api/auth/login`
Body `{ "email": "…", "password": "…" }` → `200`:
```json
{
  "user": { "id": "…", "email": "…", "role": "artisan", "status": "active" },
  "expires_in": 3600
}
```
Đặt cookie `access_token` (httpOnly, `secure` theo `COOKIE_SECURE`, `samesite=lax`).
- `401` sai mật khẩu · `403` tài khoản `pending` hoặc `rejected` (kèm `reject_reason`)
- `429` quá 5 lần/phút từ 1 IP

### `POST /api/auth/logout` → `204` (xoá cookie)

### `GET /api/auth/me` → `200` thông tin user hiện tại

---

## 2. Hồ sơ xưởng — Artisan (F3)

| Endpoint | Method | Mô tả |
|---|---|---|
| `/api/workshops/me` | GET | hồ sơ của tôi |
| `/api/workshops/me` | PATCH | sửa hồ sơ (`name`, `story`, `address`, `lat`, `lng`, `open_status`, `founded_year`) |
| `/api/workshops/me/images` | POST | upload ảnh xưởng (multipart) |
| `/api/workshops/me/images/{id}` | DELETE | xoá ảnh + chứng nhận của tôi |
| `/api/workshops/me/certifications` | POST | thêm chứng nhận (`name`, `issuer`, `year`, `image_url`) |

- `lat`/`lng` bắt buộc nếu muốn xuất hiện trên bản đồ (F7)
- `403` nếu artisan chưa được duyệt (`status != active`)

---

## 3. Sản phẩm & nhật ký sản xuất (F4, F5)

| Endpoint | Method | Mô tả |
|---|---|---|
| `/api/products` | GET | danh mục. Query: `workshop_id`, `category_id`, `q` (tìm tên), `page`, `page_size` |
| `/api/products` | POST | tạo sản phẩm (artisan) |
| `/api/products/{id}` | GET | chi tiết sản phẩm |
| `/api/products/{id}` | PATCH / DELETE | sửa / xoá (chủ workshop) |
| `/api/products/{id}/images` | POST | upload nhiều ảnh (multipart, từng file 1 request) |
| `/api/products/{id}/images/{image_id}` | DELETE | xoá ảnh |
| `/api/products/{id}/milestones` | GET | các mốc sản xuất, sắp theo `occurred_on` |
| `/api/products/{id}/milestones` | POST | thêm mốc |
| `/api/products/{id}/milestones/{mid}` | PATCH / DELETE | sửa / xoá mốc |
| `/api/products/{id}/qr` | GET | ảnh QR (PNG) của sản phẩm |

Tạo sản phẩm — body:
```json
{
  "name": "Bát tràng men lam",
  "category_id": "…",
  "price": 150000,
  "description": "Bát men lam nung lò củi, hoa văn vẽ tay",
  "status": "published"
}
```
- `201` → kèm `slug`, `qr_data_url`, `qr_download_url`
- `409` → `slug` trùng

Thêm mốc sản xuất — body:
```json
{
  "stage_item_id": "…",
  "title": "Nung trong lò củi",
  "occurred_on": "2026-11-20",
  "note": "Nung 3 ngày",
  "sort_order": 4
}
```
- `occurred_on` bắt buộc · `stage_item_id` xuất phát từ `stage_template_items` của nghề (xem `docs/domain-battrang.md` §4) — nhưng **cho phép nhập tự do** để hộ không theo khuôn mẫu

Upload ảnh:
- `multipart/form-data`, field `file`
- `MAX_UPLOAD_MB` = 10 · chỉ jpg/png/webp · kiểm tra magic bytes
- `201` → `{ "id", "url_small", "url_large", "width", "height", "bytes" }`
- `413` file quá lớn · `415` không phải ảnh
- **Một ảnh lỗi không được làm hỏng các ảnh khác** → FE gọi 1 request/ảnh, hiển thị lỗi riêng

---

## 4. Trang công khai / QR (F5)

### `GET /api/public/products/{token}`
Không cần đăng nhập. Token = `product_qr_token` (uuid), **không phải slug** (để đổi tên sản phẩm không làm hỏng QR đã in).

`200`:
```json
{
  "product": { "name": "…", "description": "…", "story": "…", "images": [ … ] },
  "workshop": { "name": "…", "story": "…", "address": "…" },
  "milestones": [
    { "title": "Nhão đất", "occurred_on": "2026-10-01", "note": "…", "images": [ … ] }
  ]
}
```
- `404` → token không tồn tại hoặc sản phẩm đã xoá (trả message dễ hiểu, **không** lỗi 500)

---

## 5. Danh mục & bản đồ (F6, F7)

| Endpoint | Method | Mô tả |
|---|---|---|
| `/api/products` | GET | công khai: chỉ `status='published'` |
| `/api/categories` | GET | danh sách phân loại |
| `/api/map/workshops` | GET | danh sách ghim |
| `/api/workshops/{id}` | GET | trang công khai của hộ (hồ sơ + sản phẩm) |

`GET /api/map/workshops` → `200`:
```json
[
  {
    "workshop_id": "…",
    "name": "Xưởng gốm men lam",
    "lat": 20.9851,
    "lng": 105.7422,
    "open_status": "open",
    "cover_image": "/uploads/workshops/…-400.webp",
    "product_count": 12
  }
]
```

---

## 6. Yêu cầu báo giá (F8)

| Endpoint | Method | Mô tả |
|---|---|---|
| `/api/quote-requests` | POST | buyer tạo → `draft` |
| `/api/quote-requests` | GET | buyer: đơn của tôi · artisan: `?scope=received` các đơn được mời |
| `/api/quote-requests/{id}` | GET | chi tiết + danh sách báo giá (buyer thấy giá; artisan chỉ thấy bid của mình) |
| `/api/quote-requests/{id}/send` | POST | buyer gửi → `sent`, mời các hộ phù hợp |
| `/api/quote-requests/{id}/bids` | POST | artisan chào giá |
| `/api/quote-requests/{id}/bids/{bid_id}/accept` | POST | buyer chấp nhận 1 báo giá → `accepted` + tạo order |
| `/api/quote-requests/{id}/cancel` | POST | hủy (chỉ khi chưa accept) |
| `/api/quote-requests/{id}/workshops` | GET | artisan: đơn này có được mời không |

Tạo đơn — body:
```json
{
  "title": "5.000 cốc in logo trường",
  "product_id": "…",
  "quantity": 5000,
  "unit": "chiếc",
  "spec": "Men lam, in 1 màu trắng, đường kính 9cm",
  "deadline": "2026-12-10"
}
```

Chào giá — body:
```json
{ "price": 150000, "lead_time_days": 25, "note": "Có thể chia 2 lần giao" }
```
- `409` `DUPLICATE_BID` — hộ đã chào giá đơn này
- `409` `INVALID_TRANSITION` — đơn không ở `sent`/`bidding`

Chấp nhận:
- `200` → `{ "order_id": "…", "quote_request_id": "…", "status": "accepted" }`
- `409` nếu đơn không ở `bidding`, hoặc bid đã bị chọn bởi người khác (khoá `FOR UPDATE`)

---

## 7. Đơn hàng & theo dõi công đoạn (F9, F12)

| Endpoint | Method | Mô tả |
|---|---|---|
| `/api/orders` | GET | buyer: đơn của tôi · admin: tất cả · artisan: `?scope=received` các lot của mình |
| `/api/orders/{id}` | GET | chi tiết: order + các lot + timeline công đoạn |
| `/api/order-lots/{lot_id}/stages` | GET | danh sách công đoạn của lot |
| `/api/order-lots/{lot_id}/stages/{stage_item_id}` | POST | artisan cập nhật công đoạn |

Cập nhật công đoạn — body:
```json
{ "status": "done", "note": "Đã nung xong lô 1", "image_url": "/uploads/orders/…-1200.webp" }
```
- `409` `INVALID_TRANSITION` — lot chưa `in_production`, hoặc công đoạn trước chưa `done` (cấm nhảy cóc)
- `403` — không phải hộ nhận lot đó

Chi tiết đơn (buyer) — `200`:
```json
{
  "id": "…",
  "status": "in_production",
  "total_amount": 750000000,
  "progress": { "done": 3, "total": 7, "percent": 43 },
  "lots": [
    {
      "id": "…",
      "workshop_name": "Xưởng men lam",
      "quantity": 2000,
      "status": "in_production",
      "stages": [
        { "stage_item_id": "…", "title": "Nung", "status": "done", "done_at": "2026-11-28T09:00:00Z", "updated_by_name": "Nguyễn Văn A" }
      ]
    }
  ]
}
```

---

## 8. Admin (F2, F9, F11)

| Endpoint | Method | Mô tả |
|---|---|---|
| `/api/admin/applications` | GET | danh sách hộ chờ duyệt |
| `/api/admin/applications/{id}/approve` | POST | duyệt → `active` |
| `/api/admin/applications/{id}/reject` | POST | từ chối, body `{ "reason": "…" }` |
| `/api/admin/orders` | GET | tất cả đơn |
| `/api/admin/orders/{id}/split` | POST | chia đơn cho nhiều hộ |
| `/api/admin/news` | GET / POST | duyệt toàn bộ tin (lọc `?status=pending`) |
| `/api/admin/news/{id}` | PATCH / DELETE | sửa / xoá tin đã publish |
| `/api/admin/news/{id}/approve` | POST | duyệt bài artisan → `published` |
| `/api/admin/news/{id}/reject` | POST | từ chối, body `{ "note": "…" }` |
| `/api/admin/stats` | GET | số liệu tổng quan (hộ, sản phẩm, đơn) — dùng cho dashboard admin |

Chia đơn — body:
```json
{ "allocations": [ { "workshop_id": "…", "quantity": 2000 }, { "workshop_id": "…", "quantity": 3000 } ] }
```
- `422` `INVALID_QUANTITY` — tổng vượt số lượng đơn, hoặc thiếu hộ chưa được duyệt

---

## 9. Tin cộng đồng & PR (F11)

| Endpoint | Method | Mô tả |
|---|---|---|
| `/api/news` | GET | tin đã publish (công khai) |
| `/api/news` | POST | artisan gửi bài → `pending`; admin đăng → `published` |
| `/api/news/mine` | GET | bài của tôi + trạng thái + `review_note` |
| `/api/news/{id}` | PATCH | artisan sửa bài của mình (nếu đã published → quay lại `pending`) |
| `/api/news/{id}` | DELETE | artisan xoá bài của mình (chưa publish) |

Body:
```json
{ "kind": "award", "title": "Hộ đạt giải thưởng gốm làng nghề", "body": "…", "cover_url": "…" }
```

---

## 10. Ràng buộc nghiệp vụ (validate ở tầng service)

| Quy tắc | Endpoint liên quan |
|---|---|
| Ảnh ≤ 10MB, chỉ jpg/png/webp, magic bytes hợp lệ | upload ảnh |
| Mỗi sản phẩm ≥ 3 mốc khi chuyển `published` | sản phẩm |
| Mỗi mốc có `occurred_on` | mốc sản xuất |
| Số lượng > 0; hạn > hôm nay | tạo đơn |
| Chỉ chuyển trạng thái hợp lệ (mục 5.1 của architecture) | quote machine |
| 1 hộ chỉ chào giá 1 lần cho 1 đơn | bids |
| Công đoạn trước phải `done` trước khi đánh dấu `done` | order stages |
| Tổng quantity các lot = quantity order | chia đơn |
| Artisan chưa `active` không được tạo sản phẩm / chào giá | nhiều |

## 11. Lịch sử

| Ngày | Thay đổi | Người |
|---|---|---|
| 2026-11-16 | Phiên bản 1.0: 9 nhóm endpoint, ma trận vai trò, định dạng lỗi, quy tắc nghiệp vụ | Nhóm |
