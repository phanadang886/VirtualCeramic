# ADR-002: Reverse proxy Nginx + DNS công khai + tên miền

- **Trạng thái:** Đã chốt nguyên tắc · còn 1 nhánh kỹ thuật phụ thuộc hạ tầng máy chủ
- **Ngày:** 2026-11-16
- **Người quyết định:** Nhóm vCraft
- **Liên quan:** `docs/decisions/ADR-001-stack.md`, `docs/architecture.md`, `docs/demo-script.md`

## Bối cảnh

Nhóm cần:

1. **Tên miền riêng** để demo trông như sản phẩm thật, không phải `localhost:5173`
2. **HTTPS** — camera/QR demo bằng điện thoại, và trình duyệt chặn mixed content
3. **Mã QR quét được từ điện thoại** — QR chứa `localhost` thì điện thoại không mở được
4. **Demo vẫn chạy khi mạng chết** — ràng buộc đã chốt ở `docs/requirements.md` §6
5. **Hạ tầng gần với thực tế** vì hướng nghề sau đồ án là DevOps

Máy ảo Linux của nhóm đã có sẵn Nginx.

## Quyết định

| Hạng mục | Quyết định |
|---|---|
| Reverse proxy + static server | **Nginx** (không Apache) |
| DNS | **Cloudflare** (free tier) — quản lý A/CNAME record |
| TLS | **Let's Encrypt** (nếu máy ảo có IP công khai) hoặc **Cloudflare Tunnel** (nếu sau NAT) |
| Kiểm soát DNS của Cloudflare | **DNS only** lúc setup → bật proxy sau khi HTTPS chạy ổn |
| Kiến trúc | **2 chế độ dùng chung một cấu hình Nginx** |
| Port mở ra internet | **chỉ 80 và 443** |
| Cơ sở dữ liệu | **không** expose ra host — chỉ trong network nội bộ Docker |

### Hai chế độ

```
CHẾ ĐỘ A — PUBLIC (máy ảo Linux)
  Điện thoại/laptop (4G, Wi-Fi bất kỳ)
     → https://vcraft.vn  → Cloudflare DNS → IP máy ảo
     → Nginx :443 (TLS)
         ├── /          → frontend/dist (file tĩnh)
         ├── /uploads/  → ảnh WebP đã resize (file tĩnh)
         └── /api/      → uvicorn 127.0.0.1:8000
             └── PostgreSQL 127.0.0.1:5432 (KHÔNG mở ra ngoài)

CHẾ ĐỘ B — OFFLINE (máy cá nhân, dự phòng khi mạng trường chết)
  Browser → http://vcraft.local → /etc/hosts → 127.0.0.1
     → Nginx trong Docker :80
         ├── /          → frontend/dist
         └── /api/      → api:8000
             └── PostgreSQL (network nội bộ)
```

Khác biệt giữa 2 chế độ chỉ nằm ở: `server_name`, đường dẫn chứng thư, `PUBLIC_BASE_URL`. Code không đổi.

### `PUBLIC_BASE_URL` — biến môi trường then chốt

QR được sinh từ `PUBLIC_BASE_URL`. Đặt sai thì điện thoại quét QR không mở được → mất điểm ở F5.

| Chế độ | `PUBLIC_BASE_URL` | Ghi chú |
|---|---|---|
| A (public) | `https://vcraft.vn` | điện thoại mở được bằng 4G |
| B (offline) | `http://192.168.x.y` (IP LAN của máy chạy app) | `vcraft.local` **không** resolve trên điện thoại Android — dùng IP LAN |

Quy tắc: **URL trong QR phải là URL mà điện thoại truy cập được**, không phải URL laptop đang dùng.

## Vì sao Nginx, không phải Apache

| | Nginx | Apache |
|---|---|---|
| Reverse proxy + static + TLS | rất tốt | tốt nhưng config nặng hơn nhiều |
| Event-driven, chịu nhiều kết nối đồng thời | tốt | cần prefork/event MPM, config phức tạp |
| Làm chuẩn trong hệ sinh thái Python/ASGI | là | không phải |
| `mod_wsgi` | không dùng được (WSGI, đồng bộ) | dùng được nhưng lệch FastAPI |

FastAPI chỉ chạy ASGI → Apache `mod_wsgi` không dùng được. Apache làm reverse proxy được nhưng cấu hình dài hơn Nginx và không phải chuẩn. Thêm vào đó máy ảo đã có sẵn Nginx.

## Cấu hình chuẩn (rút gọn)

```nginx
limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;

server {
    listen 80;
    server_name vcraft.vn www.vcraft.vn vcraft.local;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name vcraft.vn www.vcraft.vn vcraft.local;

    ssl_certificate     /etc/letsencrypt/live/vcraft.vn/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/vcraft.vn/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;

    # khớp trần upload 10MB trong CONSTRAINTS.md
    client_max_body_size 12m;

    add_header X-Content-Type-Options nosniff;
    add_header Referrer-Policy strict-origin-when-cross-origin;
    add_header X-Frame-Options SAMEORIGIN;
    # HSTS: KHÔNG bật cho tới khi cert + domain ổn định (browser cache, gỡ rất phiền)
    # add_header Strict-Transport-Security "max-age=86400" always;

    gzip on;
    gzip_types text/css application/javascript application/json image/svg+xml;

    root /usr/share/nginx/html;
    location / { try_files $uri $uri/ /index.html; }
    location /assets/ { expires 1y; add_header Cache-Control "public, immutable"; }
    location /uploads/ { alias /srv/uploads/; expires 30d; }

    location /api/auth/login {
        limit_req zone=login burst=3 nodelay;
        proxy_pass http://api:8000/auth/login;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/ {
        proxy_pass http://api:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Ba chỗ dễ sai:

| Chỗ | Sai thì |
|---|---|
| `location /api/` + `proxy_pass http://api:8000/` (có `/` cuối) | sai dấu `/` → FastAPI nhận `/api/products` → 404 hàng loạt |
| `X-Forwarded-Proto` + uvicorn `--proxy-headers` | không có → cookie `Secure` sai, URL QR sai scheme |
| `client_max_body_size` ≥ trần upload | ảnh 5MB bị 413 dù app cho phép 10MB |

Khi bật Cloudflare proxy: dùng `$http_x_forwarded_proto` thay cho `$scheme`, và thêm `set_real_ip_from` cho dải IP của Cloudflare, nếu không log sẽ toàn IP của tunnel.

## Yêu cầu bảo mật khi mở ra internet

Mở ra internet = thay đổi rủi ro thật, không còn là demo nội bộ. Thực hiện theo đúng thứ tự này **trước khi** bật DNS:

1. Chỉ mở `22/tcp`, `80/tcp`, `443/tcp` bằng `ufw`; PostgreSQL không map `ports` ra host
2. SSH: chỉ key, tắt `PasswordAuthentication`, cài `fail2ban`
3. Đổi mật khẩu admin mặc định trước khi DNS trỏ về — bot quét cổng 443 trong vài phút
4. `.env` không commit, secret không nằm trong repo và không nằm trong ảnh Docker
5. Rate limit `/api/auth/login` (5 lần/phút/IP) + `client_max_body_size`
6. Cron `pg_dump` hằng ngày, giữ 7 bản
7. Không bật HSTS cho tới khi chắc chắn domain + cert ổn định
8. Kiểm tra từ máy ngoài: `curl -I https://vcraft.vn` và quét cổng — chỉ thấy 80/443

## Hệ quả

**Tích cực**
- Demo trông như sản phẩm thật, có HTTPS, QR quét được bằng 4G
- Kinh nghiệm thực tế: DNS, TLS, reverse proxy, firewall, phân tách public/private — đúng hướng DevOps
- 1 cấu hình Nginx dùng cho cả demo public lẫn offline

**Tiêu cực**
- Thêm 2 biến thể môi trường (`PUBLIC_BASE_URL`, `COOKIE_SECURE`) → phải test cả 2 chế độ trước hôm thi
- Phụ thuộc DNS + cert → nếu hết hạn hoặc sai cấu hình là demo chết. **Bắt buộc giữ chế độ B**
- Thêm 1 dịch vụ phải sống lúc demo (DNS + máy ảo)

## Phương án bị loại

| Phương án | Vì sao loại |
|---|---|
| Apache | Không hợp ASGI, config nặng hơn, không phải chuẩn hệ sinh thái Python |
| Caddy | Tốt, tự cấp cert — nhưng đã có Nginx sẵn trên máy ảo, đổi thêm công |
| Traefik | Động, label-driven — quá nặng cho 1 VPS |
| Host Vercel / Netlify | Trả phí, và không chạy được offline → vi phạm ràng buộc demo |
| Cloudflare Tunnel (nếu VM có IP public) | Không cần NAT traversal khi đã có IP public; thêm 1 bớt vận hành |
| A record + certbot (nếu VM sau NAT) | Cần mở port 80 từ router — ở mạng trường thường không làm được |
| HSTS ngay từ đầu | Browser cache, khó gỡ khi cấu hình sai |
| Domain dùng chung cho nhiều nhóm | Mỗi nhóm 1 domain riêng, tránh xung đột DNS |

## Câu hỏi còn mở

| Câu hỏi | Ảnh hưởng | Chốt khi |
|---|---|---|
| Máy ảo có IP công khai hay sau NAT? | Chọn certbot (HTTP-01) hay Cloudflare Tunnel | Trước khi cấu hình |
| Tên miền đã mua ở đâu? | Đổi nameserver sang Cloudflare hay giữ DNS ở nhà cung cấp hiện tại | Tuần 1 |
| Bật Cloudflare proxy hay DNS only? | Ẩn IP + chống DDoS, nhưng phải sửa `X-Forwarded-Proto` và `real_ip` | Sau khi HTTPS chạy |
| Tên miền chính thức là gì? | Ghi vào `PUBLIC_BASE_URL`, DNS record, `server_name`, QR | Tuần 1 |

## Lịch sử

| Ngày | Thay đổi | Người |
|---|---|---|
| 2026-11-16 | Quyết định đầu tiên. Nginx + Cloudflare DNS + 2 chế độ (public + offline dự phòng) | Nhóm |
