# Constraints

Ràng buộc chất lượng của dự án vCraft. Đây là **nguồn chuẩn duy nhất** — `AGENTS.md`, script và CI phải phản ánh đúng file này. Nếu chúng lệch nhau, file này thắng.

Last reviewed: 2026-11-16 by nhóm vCraft

**Quyết định trong interview 2026-11-16:**
- Chọn kiểm tra: (a) coverage dòng mới, (b) bảo mật (code + secret + dependency), (c) hiệu năng, (d) accessibility
- Không chọn: (e) ranh giới kiến trúc (cần viết luật riêng, chưa đáng cho 3 người 1 học kỳ)
- Khi check fail giữa task: **Floor chặn**, các số khác **cảnh báo** cho tới 2026-11-30, sau đó chuyển dần sang chặn
- Số liệu: **đo hiện tại rồi giữ**, không đặt mục tiêu cao khi chưa có code
- Ngân sách thời gian: **90 giây** cho bộ check cuối task

---

## Floor (luôn chặn, không cần cài gì)

Áp dụng cho mọi thay đổi. Không có ngoại lệ nào trong Floor — muốn bỏ thì sửa file này bằng một PR riêng, có lý do.

- Không thêm suppression comment: `@ts-ignore`, `@ts-nocheck`, `eslint-disable`, `biome-ignore`, `# noqa`, `# type: ignore`, `istanbul ignore`, `nosemgrep`, `gitleaks:allow`, `Stryker disable`
- Không để lại việc chưa làm: `throw new Error("Not implemented")`, `catch {}` rỗng, `TODO`
- Không xoá test, không thêm `.skip` / `.todo` / `xit` mà không ghi lý do trong commit message
- Không chứa secret trong mã nguồn (API key, mật khẩu, token) — dùng biến môi trường, file `.env` không commit
- Không hạ hoặc xoá bất kỳ dòng ràng buộc nào trong file này để cho một thay đổi pass
- Không commit: `.env`, `node_modules/`, output build, ảnh > 1MB

**Cơ chế:** `node scripts/floor-guard.mjs` — quét diff so với nhánh gốc, phát hiện 5 kiểu "đi tắt tiêu chuẩn" (mục Guard bên dưới). Exit `0` sạch · `1` vi phạm (chặn) · `2` không chạy được (thiếu git base — **không được hiểu là sạch**).

---

## Enforced with numbers

Mỗi dòng có **số** và **lệnh tạo ra phán quyết**. Dòng có số mà không có lệnh là tham vọng, không phải ràng buộc — nên những dòng chưa cài tool được đánh dấu rõ.

| Dimension | Rule | Checked by | Runs at | Trạng thái |
|-----------|------|-----------|---------|-----------|
| Types | 0 lỗi type | `npm run typecheck` | mỗi edit | Chờ chốt stack |
| Lint | 0 lỗi từ config của dự án | `npm run lint` | mỗi edit | Chờ chốt stack |
| Secrets | 0 phát hiện | `gitleaks dir . --redact --no-banner` | mỗi edit | Cài được ngay |
| Coverage | dòng code mới ≥ 80% được test | `npm run check:coverage` (vitest + `git diff`) | task end, CI | Chờ chốt stack |
| Security: code | 0 phát hiện mức high/critical | `npm run check:security` (semgrep + `scripts/quality-gate.mjs`) | CI | Chờ chốt stack |
| Security: deps | 0 lỗ hổng mức high trở lên | `osv-scanner scan source -r .` | CI | Chờ chốt stack |
| Accessibility | 0 lỗi axe mức critical/serious | `npm run check:a11y` (axe + `scripts/quality-gate.mjs`) | preview deploy | Chờ app chạy |
| Performance: trang | LCP ≤ 2500ms, CLS ≤ 0.1 | `npm run check:perf` (lighthouse) | preview deploy | Chờ app chạy |
| Performance: bundle | main bundle ≤ 250 kB (gzip) | `size-limit` | CI | Chờ chốt stack |
| Upload ảnh | ≤ 10MB, chỉ jpg/png/webp, tên file do server sinh | validate ở API (`security-and-hardening`) | mỗi edit | Chờ chốt stack |
| Ảnh xuất bản | 2 bản: 400px (danh mục) + 1200px (chi tiết), định dạng WebP | `npm run check:images` | task end | Chờ chốt stack |
| Ranh giới vai trò | buyer không ghi được dữ liệu của artisan và ngược lại | test + middleware check | task end | Chờ chốt stack |

**Vì sao các con số này**

| Số | Lý do |
|---|---|
| Coverage dòng mới ≥ 80% | Đủ cao để bắt buộc có test, đủ thấp để không chặn dòng config. Đo theo dòng mới vì đó là thứ agent kiểm soát được |
| LCP ≤ 2500ms | Ngưỡng "good" của Core Web Vitals — cũng là ngưỡng đề bài ngụ ý ("web không được chậm khi tải danh mục hàng trăm sản phẩm") |
| CLS ≤ 0.1 | Ngưỡng "good" của Core Web Vitals — ảnh sản phẩm tải chậm rất dễ làm trang nhảy |
| axe: chặn critical/serious, bỏ moderate/minor | Mức vừa và nhỏ thường còn tranh luận được; chặn cả hai sẽ khiến agent dán nhãn "vô lý" để xanh |
| Lỗ hổng dependency: chặn từ high trở lên | Mức thấp hơn phần lớn là nhiễu, xử lý sau |
| Ảnh upload ≤ 10MB | Ảnh chụp từ điện thoại thường 2-8MB; trần 10MB chặn rác mà không cản người dùng thật |
| 2 bản ảnh 400px + 1200px | Trực tiếp từ F10 trong `docs/requirements.md`; danh mục chỉ cần ảnh nhỏ |
| Bundle ≤ 250 kB gzip | Chặn việc nhét Leaflet + thư viện ảnh vào bundle chính; buộc lazy-load |

---

## Hạ tầng & triển khai (bắt buộc)

Các quy tắc này kiểm tra thủ công hoặc bằng lệnh shell — chưa tự động hoá vì cần hạ tầng thật (máy ảo, DNS, cert).

| Quy tắc | Kiểm tra bằng | Khi nào |
|---------|---------------|---------|
| `PUBLIC_BASE_URL` là URL https của tên miền (chế độ A) hoặc IP LAN (chế độ B) — **không bao giờ `localhost`** khi sinh QR | đọc `.env` + **quét QR bằng điện thoại thật** | trước buổi thi |
| `client_max_body_size` ở Nginx ≥ trần upload (12m) | `nginx -t` + thử upload 11MB | mỗi lần đổi Nginx |
| PostgreSQL không được map port ra host | `docker ps` không có `0.0.0.0:5432` | mỗi lần đổi compose |
| Chỉ mở 80/443 ra internet (thêm 22 cho SSH) | `ufw status` + quét cổng từ máy khác | trước buổi thi |
| `/api/auth/login` rate limit ≤ 5 lần/phút/IP | thử 10 lần sai mật khẩu liên tiếp | mỗi lần đổi Nginx |
| Cookie `secure=true` khi HTTPS, `false` khi demo offline | xem header `Set-Cookie` trong DevTools | mỗi lần đổi môi trường |
| Chứng thư TLS còn hạn ≥ 7 ngày | `certbot certificates` | hằng tuần |
| Không bật HSTS trước khi domain ổn định | đọc response header | mỗi lần đổi Nginx |
| Không secret trong repo hoặc trong ảnh Docker | `gitleaks dir . --redact` + đọc `Dockerfile` | mỗi PR |
| `.env` không được commit | `git ls-files .env` phải rỗng | mỗi PR |
| Demo offline dùng được khi mạng chết | `docker compose -f deploy/docker-compose.offline.yml up` | trước buổi thi |

---

## Kiểm tra hướng rubric (thủ công — trước buổi thi / mỗi PR)

| Quy tắc | Kiểm tra bằng | Khi nào |
|---------|---------------|---------|
| Điều hướng không tải lại toàn trang | DevTools → Network → lọc Fetch/XHR; request `document` chỉ 1 lần | trước demo |
| URL không có `#`, không lộ UUID | mở 5 route chính: `/`, `/san-pham/{slug}`, `/ho-gia-dinh/{slug}`, `/ban-do`, `/p/{token}` | trước demo |
| Slug unique; đổi slug trả 301 | đổi slug 1 sản phẩm, mở slug cũ | khi làm F14 |
| Không hardcode màu / font / spacing ngoài token | grep hex và `text-[` trong `frontend/src` | mỗi PR FE |
| Mỗi trang có đủ 4 trạng thái: loading, rỗng, lỗi, có dữ liệu | duyệt từng trang ở 320px và 1440px | mỗi PR FE |
| Lỗi validate hiện dưới từng field, không popup chung | submit form sai 3 trường | mỗi PR FE |
| API trả JSON (trừ ảnh/QR) | `curl -H "Accept: application/json"` | mỗi PR BE |
| Không dùng `JSONB`, `pg_trgm`, `ARRAY`, `ENUM` native | grep trong `backend/app/models/` | mỗi PR BE |
| Schema tạo được trên SQLite (kiểm chứng độc lập CSDL) | `pytest tests/test_schema_portable.py` | CI |
| Có ≥ 1 chi tiết nhận dạng thương hiệu trên mọi trang chính | review UI theo `docs/design-system.md` §1 | trước demo |

---

## Measured, not yet enforced (ratchet)

Đo một lần khi có code rồi ghi vào đây. Mọi check so với giá trị đã ghi, không so với mơ ước. Số tốt lên thì cập nhật; số tụt xuống thì đó là phát hiện.

| Metric | Hôm nay | Hướng | Sẽ đo ở |
|--------|----------|-------|----------|
| Project coverage | chưa đo — chưa có code | không giảm | tuần 1, sau khi có test đầu tiên |
| Bundle size main | chưa đo | không tăng quá 5% | tuần 1 |
| Số lỗi axe | chưa đo | không tăng | tuần 4 |
| Thời gian build | chưa đo | không tăng quá 20% | tuần 1 |
| Số ảnh trong repo | chưa đo | không tăng (dùng link ngoài hoặc LFS) | tuần 2 |

**Dung sai ratchet:** 0.5% — để một file không liên quan di chuyển cả con số.

---

## Guard: 5 nước đi hạ tiêu chuẩn

Kiểm tra khi review diff. `scripts/floor-guard.mjs` tự phát hiện 4/5; cái thứ 5 cần người đọc.

1. **Ngưỡng bị hạ** — một số trong bảng trên bị giảm, hoặc một dòng bị xoá khỏi bảng
2. **Test bị làm dễ hơn** — thêm `.skip`, xoá file test, bỏ assertion khỏi test còn lại
3. **Checker bị tắt** — thêm `@ts-ignore`, `eslint-disable`, `istanbul ignore`, `nosemgrep`, `gitleaks:allow`
4. **Việc chưa làm xong** — stub ném lỗi, `catch {}` rỗng nuốt lỗi, `TODO` đứng chỗ code
5. **Ngoại lệ mới xuất hiện** — thêm dòng vào bảng Exceptions mà không ai bàn

Siết tiêu chuẩn thì im lặng. Nới tiêu chuẩn thì phải ồn.

---

## Exceptions

Mỗi ngoại lệ có người chịu trách nhiệm và ngày hết hạn. Hết hạn mà chưa xử lý thì ngoại lệ tự bị bỏ.

| ID | Rule | Path | Reason | Owner | Expires |
|----|------|------|--------|-------|---------|
| — | — | — | — | — | — |

**Quy tắc:** ngoại lệ tồn tại tối đa **90 ngày**. Muốn giữ lâu hơn thì mở PR mới nêu lý do và đặt hạn mới.

---

## Kích hoạt từng chiều (việc còn phải làm)

| Việc | Cần gì | Khi nào |
|------|--------|---------|
| `git init` + commit đầu | có git, merge base | xong ở lần commit đầu tiên |
| Cài `gitleaks` | máy hoặc CI | ngay, không phụ thuộc stack |
| Cài `semgrep`, `osv-scanner` | máy hoặc CI | sau khi có `package.json` |
| Cài test runner + coverage | chốt stack | tuần 1 |
| Cài `axe`, `lighthouse` | app chạy được | tuần 2-3 |
| `size-limit` | chốt stack | tuần 1 |
| Thêm script vào `package.json` | chốt stack | tuần 1 |

**Sau khi có stack**, `package.json` cần các script:

```json
{
  "scripts": {
    "check:fast": "npm run typecheck && npm run lint && gitleaks dir . --redact --no-banner",
    "check:task": "npm run check:fast && npm run check:coverage && npm run check:images",
    "check:security": "semgrep scan --config p/default --strict --json > semgrep-results.json && node scripts/quality-gate.mjs semgrep semgrep-results.json",
    "check:a11y": "axe \"$PREVIEW_URL\" --tags wcag2a,wcag2aa,wcag21aa --stdout > axe-results.json && node scripts/quality-gate.mjs axe axe-results.json",
    "check:full": "npm run check:task && npm run check:security && osv-scanner scan source -r ."
  }
}
```

`check:fast` chạy sau mỗi edit (dưới 5 giây, chỉ file đổi) · `check:task` khi agent xong việc (≤ 90 giây) · `check:full` trong CI (không giới hạn).

---

## Ràng buộc riêng của dự án vCraft

Không phải kiểm tra tự động, nhưng là đường đỏ về mặt nghiệp vụ — vi phạm là sai, không phải "chậm".

- Không phụ thuộc dịch vụ trả phí (API key, hosting) — demo phải chạy được trên máy cá nhân của thành viên
- Demo phải chạy được khi **không có mạng** → dữ liệu mẫu + ảnh sẵn phải nằm trong repo
- Không tích hợp thanh toán thật; bước thanh toán (nếu có) dùng tài khoản demo của nhóm
- Tên xưởng / tên người trong dữ liệu mẫu phải là **tên giả**; ảnh phải là ảnh nhóm tự chụp hoặc ảnh CC0
- Mọi màn hình demo có nhãn "dữ liệu mẫu"
- Không có thao tác xoá cứng dữ liệu đã được buyer chấp nhận — phải qua trạng thái `Cancelled`

---

## Lịch sử thay đổi ràng buộc

| Ngày | Thay đổi | Người |
|------|----------|------|
| 2026-11-16 | Phiên bản đầu. Floor + 4 chiều kiểm tra (coverage, security, perf, a11y) | Nhóm |
| 2026-11-16 | Thêm ràng buộc hạ tầng: `PUBLIC_BASE_URL`, port mở, rate limit, cookie secure, cert hạn, `.env` | Nhóm |
| 2026-11-16 | Thêm 10 kiểm tra hướng rubric: không reload, URL slug, token thiết kế, 4 trạng thái UI, lỗi theo field, JSON API, độc lập CSDL | Nhóm |
