# vCraft — Yêu cầu sản phẩm (V1)

> Nguồn: `vCraft.pdf` — bài tập lớn INT3306, Fall 2026. Nhóm 3 sinh viên. Demo trực tiếp tại buổi thi vấn đáp.
> File này là bản diễn giải của nhóm: chốt phạm vi V1, tiêu chí nghiệm thu, và phần cố tình không làm.
> Phiên bản: 1.3 | Cập nhật: 2026-11-16
> Domain: **làng gốm Bát Tràng** — dùng làm ngữ cảnh sản phẩm và dữ liệu demo. Xem `docs/domain-battrang.md`.

## 1. Mục tiêu

Làng nghề truyền thống (ví dụ Bát Tràng, Vạn Phúc) chủ yếu bán lẻ. Khách không biết sản phẩm được làm ở đâu, ai làm, quy trình ra sao. Ban quản lý (BQL) không có công cụ điều phối các đơn hàng lớn cho nhiều hộ cùng làm.

vCraft xây "Triển lãm số": mỗi hộ gia đình/nghệ nhân có không gian riêng để kể câu chuyện làm nghề, trưng bày sản phẩm độc bản, và công khai quy trình sản xuất. BQL dùng cùng hệ thống để duyệt hộ, quản lý tin cộng đồng, và chia đơn lớn cho nhiều hộ.

**Phạm vi domain trong V1: làng gốm Bát Tràng** (thôn Thanh Hà, Thanh Tây, Thanh Ninh và xã Bát Tràng). Hệ thống được thiết kế cho nghề gốm trước — công đoạn, sản phẩm, câu chuyện xưởng, toạ độ bản đồ đều lấy từ Bát Tràng. Việc mở rộng sang làng lụa Vạn Phúc để sau, không nằm trong V1.

Toàn bộ nội dung trong hệ thống (sản phẩm, ảnh, câu chuyện xưởng, tin cộng đồng) dùng ngữ ngữ gốm Bát Tràng. Chi tiết domain: `docs/domain-battrang.md`.

## 2. Người dùng & vai trò

### 2.1 Artisan — hộ gia đình / nghệ nhân
Cần hồ sơ xưởng (lịch sử gia đình, ảnh xưởng, chứng nhận chất lượng), đăng sản phẩm kèm nhật ký sản xuất, nhận và phản hồi yêu cầu báo giá từ khách sỉ.

### 2.2 Buyer — khách sỉ / khách tham quan
Cần xem sản phẩm theo hộ hoặc theo phân loại, xem bản đồ làng nghề để biết xưởng nào đang mở cửa, và gửi yêu cầu báo giá cho sản phẩm số lượng lớn.

### 2.3 Admin — BQL (Chủ tịch xã / Hội làng nghề)
Cần duyệt và cấp tài khoản cho hộ (đảm bảo đúng người trong làng, tránh hàng nhái), quản lý tin cộng đồng và duyệt bài PR của hộ, và điều phối đơn hàng chung.

## 3. Phạm vi

**Trong V1 (Must / Should):**
- Đăng nhập, phân quyền 3 vai trò; admin duyệt tài khoản artisan
- Hồ sơ xưởng của artisan
- Sản phẩm + nhật ký sản xuất + mã QR + trang công khai
- Danh mục sản phẩm cho buyer (theo hộ, theo phân loại)
- Bản đồ làng nghề có ghim + popup
- Yêu cầu báo giá + chào giá + state machine
- Theo dõi tiến độ đơn hàng theo từng công đoạn
- Admin chia đơn lớn cho nhiều hộ
- Upload nhiều ảnh + resize phía backend
- Tin cộng đồng: admin đăng trực tiếp + artisan gửi bài PR chờ duyệt

**Ngoài V1 (Won't):**
- Thanh toán online
- Chat realtime giữa buyer và artisan
- Ứng dụng mobile native
- Xếp hạng / đánh giá sản phẩm
- Đa ngôn ngữ
- Gợi ý sản phẩm bằng AI

## 4. Tính năng

Mỗi tính năng ghi: ai dùng, làm gì, tiêu chí nghiệm thu, priority.
Priority theo MoSCoW: Must / Should / Could / Won't.

### F1. Đăng nhập & phân quyền — Must
- **Ai dùng:** cả 3 vai trò
- **Làm gì:** đăng ký / đăng nhập; mỗi vai trò chỉ thấy và thao tác được chức năng của mình
- **Tiêu chí nghiệm thu:**
  - Đăng nhập sai mật khẩu 5 lần → bị chặn tạm thời
  - Artisan không vào được trang admin; buyer không sửa được sản phẩm
  - Artisan mới đăng ký → trạng thái "chờ duyệt", chưa đăng sản phẩm được
- **Không cần:** đăng nhập mạng xã hội, 2FA

### F2. Admin duyệt tài khoản artisan — Must
- **Ai dùng:** Admin
- **Làm gì:** xem danh sách chờ duyệt, xem thông tin hộ, duyệt hoặc từ chối kèm lý do
- **Tiêu chí nghiệm thu:**
  - Duyệt → artisan đăng nhập được ngay và thấy thông báo trạng thái
  - Từ chối → ghi lý do, artisan thấy lý do khi đăng nhập
  - Mọi hành động duyệt / từ chối có log (ai, lúc nào, hộ nào)
- **Không cần:** gửi email / SMS

### F3. Hồ sơ xưởng — Must
- **Ai dùng:** Artisan
- **Làm gì:** nhập lịch sử gia đình, ảnh xưởng, chứng nhận chất lượng
- **Tiêu chí nghiệm thu:**
  - Lưu được ≥10 ảnh xưởng, mỗi ảnh có chú thích
  - Trang công khai hiển thị đúng thứ tự: câu chuyện → ảnh → chứng nhận
  - Sửa hồ sơ → trang công khai cập nhật ngay
- **Không cần:** video, chỉnh sửa ảnh trong web

### F4. Đăng sản phẩm + nhật ký sản xuất — Must
- **Ai dùng:** Artisan
- **Làm gì:** tạo sản phẩm (tên, giá, phân loại, mô tả) và thêm các mốc sản xuất kèm ngày + ảnh
- **Tiêu chí nghiệm thu:**
  - Mỗi sản phẩm có ≥3 mốc, lấy từ quy trình gốm Bát Tràng: nhão đất → tạo hình → cham → tráng men → vẽ/khắc → nung → hoàn thiện (xem `docs/domain-battrang.md` §4)
  - Mỗi mốc có ngày và ≥1 ảnh chứng minh
  - Không cho lưu mốc không có ngày hoặc ngày không hợp lệ
  - Sản phẩm hiển thị ở danh mục buyer ngay sau khi lưu
- **Không cần:** kéo-thả sắp xếp mốc, nhiều người cùng sửa

### F5. Mã QR + trang truy xuất nguồn gốc — Must
- **Ai dùng:** hệ thống tạo mã, buyer / tourist quét
- **Làm gì:** mỗi sản phẩm có 1 mã QR; quét → mở trang công khai kể câu chuyện + toàn bộ mốc sản xuất
- **Tiêu chí nghiệm thu:**
  - QR sinh tự động khi tạo sản phẩm, không trùng giữa các sản phẩm
  - Quét bằng điện thoại → mở đúng trang sản phẩm, không cần đăng nhập
  - Trang hiện đúng thứ tự mốc theo ngày, kèm ảnh
  - QR của sản phẩm đã xoá → trang báo "không tìm thấy", không lỗi 500
- **Không cần:** in QR, QR động đổi nội dung

### F6. Danh mục sản phẩm — Must
- **Ai dùng:** Buyer
- **Làm gì:** xem sản phẩm theo hộ gia đình hoặc theo phân loại; tìm theo tên
- **Tiêu chí nghiệm thu:**
  - Lọc theo hộ → chỉ hiện sản phẩm của hộ đó
  - Lọc theo phân loại (gốm, lụa...) → đúng loại
  - Tìm theo tên → có kết quả trong ≤1 giây với 200 sản phẩm mẫu
  - Trang danh mục 200 sản phẩm mở được dưới 2.5 giây trên mạng thường
- **Không cần:** so sánh sản phẩm, wishlist

### F7. Bản đồ làng nghề — Should
- **Ai dùng:** Buyer / Tourist
- **Làm gì:** bản đồ có ghim vị trí các xưởng (latitude / longitude); click ghim → popup thông tin ngắn
- **Tiêu chí nghiệm thu:**
  - Ghim hiện đúng vị trí theo toạ độ lưu trong DB (toạ độ thật của làng gốm Bát Tràng, lấy từ OpenStreetMap)
  - Click ghim → popup có tên xưởng, ảnh đại diện, trạng thái mở / đóng
  - Bản đồ không chặn trang tải (lazy-load)
- **Không cần:** chỉ đường, tìm kiếm địa chỉ, clustering nâng cao

### F8. Yêu cầu báo giá + chào giá (bidding) — Must
- **Ai dùng:** Buyer tạo, Artisan chào giá, Buyer chọn
- **Làm gì:** buyer mô tả đơn (số lượng, mẫu, hạn giao); hệ thống gửi tới các hộ phù hợp; hộ chào giá kèm giá và thời gian hoàn thành; buyer chấp nhận 1 báo giá
- **Tiêu chí nghiệm thu:**
  - State machine: Draft → Sent → Bidding → Accepted → In Production → Delivered
  - Chỉ chuyển được trạng thái hợp lệ; chuyển sai → báo lỗi rõ ràng
  - Hộ không chào giá sau hạn → không còn thấy đơn
  - Buyer chấp nhận 1 báo giá → các báo giá khác tự chuyển "không chọn"
  - Hai người thao tác cùng đơn → không ghi đè trạng thái của nhau
  - Mọi lần chuyển trạng thái có log (ai, từ trạng thái nào, lúc nào)
- **Không cần:** đàm phán nhiều vòng, chat trong đơn

### F9. Admin chia đơn lớn — Must
- **Ai dùng:** Admin
- **Làm gì:** nhận đơn quá lớn, chia thành nhiều phần giao cho 3-4 hộ
- **Tiêu chí nghiệm thu:**
  - Tổng số lượng các phần = số lượng đơn gốc
  - Mỗi phần giao cho 1 hộ, có trạng thái riêng
  - Đơn gốc hiển thị tiến độ tổng hợp từ các phần
  - Không cho giao vượt số lượng còn lại
- **Không cần:** tự động chia theo năng lực hộ

### F10. Upload nhiều ảnh + tối ưu — Must
- **Ai dùng:** Artisan, Admin
- **Làm gì:** chọn nhiều ảnh, xem tiến trình, thấy lỗi từng ảnh
- **Tiêu chí nghiệm thu:**
  - Chọn 5 ảnh → hiện thumbnail từng ảnh
  - Ảnh >10MB → báo lỗi riêng ảnh đó, ảnh khác vẫn tải lên
  - File không phải ảnh → từ chối, không lưu
  - Backend resize: bản nhỏ (400px) cho danh mục, bản lớn (1200px) cho chi tiết
  - Trang chi tiết sản phẩm tải ≤2 giây với 5 ảnh
- **Không cần:** kéo-thả, crop, watermark

### F11. Tin cộng đồng & PR hộ gia đình — Should
- **Ai dùng:** Admin đăng trực tiếp; Artisan gửi bài để admin duyệt
- **Làm gì:** đăng tin giá nguyên vật liệu, lịch cúp điện, chính sách hỗ trợ, hộ đạt giải thưởng / chứng nhận; artisan gửi bài PR xưởng mình
- **Tiêu chí nghiệm thu:**
  - Admin đăng → hiện trang chủ trong ≤5 giây
  - Artisan gửi bài → trạng thái "chờ duyệt", KHÔNG hiện công khai
  - Admin duyệt → hiện công khai; từ chối → kèm lý do, artisan thấy lý do
  - Bài gắn được 1 hộ + 1 loại (giải thưởng / chứng nhận / tin chung)
  - Artisan sửa bài đã duyệt → quay lại "chờ duyệt"
  - Chỉ admin được xoá bài công khai
- **Không cần:** bình luận, like, ghim nhiều ảnh phức tạp

### F12. Theo dõi tiến độ đơn hàng — Must
- **Ai dùng:** Artisan cập nhật, Buyer theo dõi, Admin xem tổng
- **Làm gì:** đơn hàng có danh sách công đoạn theo nghề (gốm Bát Tràng: nhão đất → tạo hình → cham → tráng men → vẽ/khắc → nung → hoàn thiện). Artisan đánh dấu xong từng công đoạn kèm thời điểm và ảnh minh chứng (tuỳ chọn). Buyer xem timeline để biết đơn đang ở đâu, gốm đã vào lò chưa.
- **Tiêu chí nghiệm thu:**
  - Chỉ đơn ở trạng thái In Production mới cập nhật được công đoạn
  - Mỗi công đoạn có: tên, trạng thái (chưa làm / đang làm / xong), thời điểm xong, người cập nhật
  - Buyer thấy công đoạn hiện tại + % hoàn thành (số công đoạn xong / tổng)
  - Không nhảy cóc: không đánh dấu xong công đoạn N khi công đoạn N-1 chưa xong
  - Công đoạn cuối xong → hệ thống gợi ý "sẵn sàng giao"
  - Admin xem được timeline của mọi đơn
  - Buyer refresh → thấy cập nhật mới nhất
- **Không cần:** realtime websocket, push notification, dự đoán thời gian xong

## 5. Luồng nghiệp vụ chính

### 5.1 Luồng báo giá
```
Buyer tạo yêu cầu             → Draft
Buyer gửi                     → Sent (hệ thống chọn hộ phù hợp)
Hộ chào giá (giá + thời gian) → Bidding
Buyer chấp nhận 1 báo giá      → Accepted (các báo giá khác: không chọn)
Hộ bắt đầu làm                → In Production
Hộ giao xong                  → Delivered
```
Ở mỗi bước ghi rõ: ai được chuyển, ai nhìn thấy gì.

### 5.2 Luồng truy xuất nguồn gốc
```
Artisan tạo sản phẩm → thêm mốc sản xuất (ngày + ảnh)
Hệ thống sinh QR → in / dán lên sản phẩm
Khách quét QR → trang công khai: câu chuyện + timeline + ảnh
```

### 5.3 Luồng chia đơn lớn
```
Buyer gửi đơn lớn → Admin nhận
Admin chia N phần → giao cho N hộ
Mỗi hộ làm phần của mình → cập nhật trạng thái
Admin thấy tiến độ tổng → giao buyer khi đủ
```

### 5.4 Luồng theo dõi đơn hàng
```
Buyer chấp nhận báo giá      → In Production
Artisan đánh dấu công đoạn 1 xong (+ thời điểm, ảnh)
... lần lượt các công đoạn
Công đoạn cuối xong          → "sẵn sàng giao"
Artisan giao                 → Delivered
Buyer xem timeline: công đoạn nào xong, lúc nào, ai cập nhật, ảnh minh chứng
```

## 6. Ràng buộc & giả định

**Ràng buộc đã chốt:**
- Nhóm 3 người; hạn nộp khoảng 4 tuần kể từ 2026-11-16 → target **2026-12-14** (cần xác nhận ngày chính xác)
- Công nghệ tự do chọn (theo đề bài) — đã chốt tại `docs/decisions/ADR-001-stack.md`
- Quản lý mã nguồn trên **GitHub** (repo private, 3 người cùng đẩy)
- Demo trực tiếp tại buổi thi vấn đáp, không dùng slide
- Demo chạy trên **máy cá nhân của thành viên nhóm** → phải chạy được cả khi mạng yếu hoặc không có mạng
- Có **tên miền + HTTPS** cho bản demo chính; bản demo phụ trên máy cá nhân dùng đường dẫn giả nội bộ (`docs/decisions/ADR-002-nginx-public-dns.md`)
- Không phụ thuộc dịch vụ trả phí (API key, hosting)

**Lịch gợi ý (4 tuần):**
| Tuần | Việc |
|---|---|
| 1 | Chốt stack + schema + API contract; dựng repo GitHub |
| 2 | Auth 3 vai trò + hồ sơ xưởng + sản phẩm + upload ảnh |
| 3 | Báo giá + bidding + theo dõi công đoạn + admin chia đơn |
| 4 | Bản đồ + tin cộng đồng + dựng dữ liệu mẫu + test + chuẩn bị demo |

**Giả định:**
- Mỗi hộ có 1 tài khoản artisan duy nhất
- Dữ liệu mẫu lấy theo làng gốm Bát Tràng: tên xưởng dùng **tên giả**, ảnh dùng **ảnh nhóm tự chụp hoặc ảnh CC0**, toạ độ lấy từ OpenStreetMap — không dùng tên/ảnh thật khi chưa được phép (xem `docs/domain-battrang.md` §10)
- Ảnh do người dùng cung cấp, không cần AI kiểm duyệt nội dung
- Số hộ trong demo: 5-10; số sản phẩm: 50-200
- **Thanh toán diễn ra ngoài hệ thống**; nếu luồng demo cần bước thanh toán thì dùng tài khoản demo của nhóm — không có giao dịch tiền thật
- Demo cần **dữ liệu mẫu + ảnh sẵn** (không upload ảnh thật lúc thi, không phụ thuộc internet)
- Trong demo có 1 dòng chú thích "dữ liệu là dữ liệu mẫu"

## 7. Tiêu chí nghiệm thu V1

- [ ] 3 vai trò đăng nhập được, phân quyền đúng
- [ ] Artisan tạo sản phẩm + ≥3 mốc + ≥2 ảnh; trang công khai có QR hoạt động
- [ ] Buyer tạo yêu cầu báo giá; 2 hộ chào giá; buyer chấp nhận 1; đơn đi đủ 6 trạng thái
- [ ] Artisan cập nhật 3 công đoạn → buyer thấy timeline đúng thứ tự + % hoàn thành
- [ ] Artisan không đánh dấu xong công đoạn sau khi công đoạn trước chưa xong
- [ ] Admin duyệt 1 tài khoản artisan và chia 1 đơn lớn cho 3 hộ
- [ ] Artisan gửi bài PR → admin duyệt → hiện công khai; từ chối → artisan thấy lý do
- [ ] Bản đồ hiện ≥5 ghim đúng vị trí, click ra popup
- [ ] Danh mục 200 sản phẩm mở dưới 2.5 giây
- [ ] Upload 5 ảnh cùng lúc thành công, ảnh lỗi không chặn ảnh khác
- [ ] Không có lỗi 500 ở các luồng trên

(4 tiêu chí đầu là điều kiện demo tối thiểu.)

## 8. Câu hỏi & điều đã chốt

### 8.1 Đã chốt (2026-11-16)

| Câu hỏi | Trả lời | Ảnh hưởng tới thiết kế |
|---|---|---|
| Hạn nộp? | Khoảng 4 tuần từ 2026-11-16 → target 2026-12-14 | Lịch ở §6, cần freeze scope trước deadline 1 tuần |
| Dùng GitHub? | Có — dùng để cộng tác 3 người | Quy tắc commit/PR ghi trong `AGENTS.md` |
| Bảng điểm / rubric? | **Chưa có trong `vCraft.pdf`** (file này 4 trang, hết ở mục 4.4) | Cần tìm bảng điểm ở nơi khác — quyết định phân bổ công sức |
| Demo trên máy nào? | Máy cá nhân của thành viên nhóm | Cần bản chạy local, seed data và ảnh sẵn |
| Thanh toán? | Không tích hợp cổng thanh toán thật; dùng tài khoản demo của nhóm | F8 / F12 không có bước thanh toán |

### 8.2 Còn cần hỏi giảng viên

1. Ngày nộp source + ngày demo chính xác?
2. Bảng điểm / rubric chi tiết nằm ở đâu? (chưa có trong file PDF trong repo)
3. Demo có bắt buộc chạy trên máy giảng viên không? Có mạng không?
4. Có bắt buộc framework / library cụ thể nào không?
5. Có yêu cầu bảo mật nào ngoài mô tả trong đề bài không?

## 9. Lịch sử thay đổi

| Ngày | Phiên bản | Thay đổi | Người |
|---|---|---|---|
| 2026-11-16 | 1.0 | Bản đầu, sinh từ `vCraft.pdf` | Nhóm |
| 2026-11-16 | 1.1 | Thêm F12 theo dõi tiến độ đơn hàng; mở rộng F11 cho artisan gửi bài PR chờ duyệt | Nhóm |
| 2026-11-16 | 1.2 | Chốt deadline 4 tuần, dùng GitHub, demo trên máy cá nhân, không tích hợp thanh toán thật; thêm lịch 4 tuần ở §6 | Nhóm |
| 2026-11-16 | 1.3 | Chốt domain làng gốm Bát Tràng; thêm `docs/domain-battrang.md`; đồng bộ công đoạn gốm ở F4/F12 | Nhóm |
| 2026-11-16 | 1.4 | Chốt stack (ADR-001) + Nginx/tên miền công khai (ADR-002); thêm `docs/architecture.md`, `docs/api.md`, `docs/demo-script.md`, `tasks/todo.md`; §6 cập nhật demo qua domain + phương án offline | Nhóm |

## 10. Backlog V2 (chưa làm)

Tính năng mới ghi vào đây trước. Khi quyết định làm trong V1 thì mới thêm section F vào §4 + dòng vào §3 + tiêu chí ở §7 + dòng ở §9.

- Thanh toán online
- Chat realtime buyer ↔ artisan
- Đánh giá / xếp hạng sản phẩm
- Gợi ý sản phẩm bằng AI
- Ứng dụng mobile
- Đa ngôn ngữ
- In QR / dán nhãn hàng loạt
- Xếp hạng xưởng theo số đơn đã hoàn thành
