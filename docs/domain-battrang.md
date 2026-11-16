# Domain: làng gốm Bát Tràng

> Ghi chú làm việc cho nhóm + cho AI agent khi sinh dữ liệu mẫu, viết nội dung UI, viết bài demo.
> Mọi dòng có đánh dấu **[xác nhận]** là thông tin cần kiểm lại từ nguồn chính thức (UBND phường Bát Tràng, Sở Công Thương, Bộ Văn hoá) trước khi đưa vào bài bảo vệ.
> Nguồn chi tiết: `docs/domain-battrang.md`

## 1. Bối cảnh

- Bát Tràng là làng nghề gốm nổi tiếng nhất nước, được gọi là "thủ phủ gốm Việt Nam".
- Vị trí: phía tây Nam Hà Nội, cạnh Hồ Tây, đối diện huyện Thanh Oai.
- Ranh giới hành chính có thay đổi trong các đợt sáp nhập 2024-2025. **[xác nhận]** Trước khi demo, chỉ nói chung "Bát Tràng, Hà Nội" — đừng khẳng định cấp hành chính cụ thể.
- Nghề gốm Bát Tràng có từ khoảng thế kỷ XIV. **[xác nhận]**

## 2. Đơn vị trong làng (dùng cho seed data)

| Tên | Loại | Ghi chú |
|---|---|---|
| Thanh Hà | thôn | trung tâm làng gốm, nhiều xưởng, chợ gốm |
| Thanh Tây | thôn | khu sản xuất gốm lớn |
| Thanh Ninh | thôn | khu dân cư, xưởng gốm nhỏ lẻ |
| Bát Tràng (xã, phía Hưng Yên) | xã | phía bên kia ranh giới, cùng nghề gốm |

Tọa độ gợi ý để test bản đồ (dùng để seed, không cần chính xác tuyệt đối): vùng Bát Tràng nằm quanh **20.98 – 21.01 vĩ độ, 105.72 – 105.76 kinh độ**. Lấy toạ độ thật từ OpenStreetMap khi dựng dữ liệu mẫu (miễn phí, không cần key).

## 3. Sản phẩm & phân loại

Dùng 4-6 nhóm phân loại trong danh mục (không cần nhiều hơn cho V1):

| Nhóm | Ví dụ sản phẩm | Ghi chú |
|---|---|---|
| **Bình / chum** | bình cổ, chum rượu, bình phong, lư cảnh | giá trị cao, trưng bày |
| **Bát / đũa / ấm chén** | bát tràng men lam, bát cơm, đũa, ấm chén, bộ ấm trà | bán số lượng lớn, đơn hàng của khách sỉ |
| **Tượng / linh vật** | tượng trang điểm, tượng thần, rồng | biểu tượng |
| **Đèn lồng / trang trí** | đèn lồng gốm, bình cổ trang trí | bán theo mùa, lễ hội |
| **Đồ thờ / lễ vật** | bát hương, lư hương, bộ đồ thờ | dùng trong đình, đền |
| **Gốm mới / sáng tạo** | gốm in logo, sản phẩm theo yêu cầu | phục vụ đơn lớn |

Tên sản phẩm tiêu biểu: **bát tràng men lam**, **bình cổ men lam**, **phượng men lam**, **lư men ngọc**, **ấm chén men trắng**, **tượng trang điểm**, **đèn lồng Bát Tràng**.

## 4. Quy trình làm gốm (dùng cho F4 + F12)

Đây là danh sách công đoạn chuẩn. **Cùng một danh sách này** dùng cho cả 2 nơi:
- F4 — nhật ký sản xuất của một sản phẩm mẫu (marketing, truy xuất nguồn gốc)
- F12 — công đoạn của một đơn hàng (vận hành, buyer theo dõi)

| # | Công đoạn | Mô tả ngắn (viết cho timeline) | Ảnh minh chứng gợi ý |
|---|---|---|---|
| 1 | Nhão đất | Trộn đất, nhão nhuyễn, loại bỏ tạp chất | đất, bàn nhão |
| 2 | Tạo hình | Đặt khối đất lên bàn xoay, vuốt tạo hình | bàn xoay, tay đang vuốt |
| 3 | Cham / gắn thêm | Nối các phần (thân, cổ, chân, núm), làm mượt | sản phẩm chưa nung |
| 4 | Tráng men | Lớn men, để khô, lau bỏ men thừa ở chỗ cần sắc | sản phẩm phủ men |
| 5 | Vẽ / khắc hoa văn | Vẽ men hoặc khắc hoa văn trên thân sản phẩm | chi tiết hoa văn |
| 6 | Nung | Xếp vào lò, nung ở nhiệt độ cao; men lam đạt màu xanh lam trong lò | lò nung, sản phẩm trong lò |
| 7 | Hoàn thiện | Cạo men thừa, hoàn thiện, đóng gói | sản phẩm thành phẩm |

Lưu ý cần xác nhận với thợ thật: **với cốc in logo theo đơn lớn, công đoạn nào được rút gọn nhất** (thường bỏ khắc hoa văn, dùng khuôn). **[xác nhận]**

## 5. Nguyên liệu, dụng cụ, lò nung, men

| Nhóm | Chi tiết |
|---|---|
| Nguyên liệu | đất sét (đất Bát Tràng, đất mang từ nơi khác), bột đá, bột sắt (tạo màu), cát |
| Dụng cụ | bàn xoay (kỹ thuật Tày), khuôn, tay khuấy, dao cắt, chà sạch |
| Lò nung | lò củi truyền thống, lò gas; xếp sản phẩm vào "khu" (khu tâm, khu giáp, khu lưu, khu hơi) |
| Men | men lam (đặc trưng Bát Tràng), men trắng, men ngọc, men xanh, men nâu, men đen, men vẽ |
| Màu đặc trưng | xanh lam của men lam Bát Tràng, men ngọc xanh nhạt, men trắng ngà |

**[xác nhận]** Màu men lam đặc trưng nhờ hỗn hợp men và điều kiện lò nung; đừng nói quá tuyệt đối ("men nào cũng thành xanh lam") — thợ Bát Tràng hay nói men lam Bát Tràng có xanh lam đậm hơn men lam các nơi khác.

## 6. Nhân vật trong hồ sơ xưởng (F3)

| Vai | Ghi chú cho hồ sơ |
|---|---|
| Nghệ nhân / chủ xưởng | người đại diện hộ, người ký tên trên sản phẩm |
| Thợ tạo hình | người vuốt, tạo dáng |
| Thợ vẽ men / khắc | người trang trí |
| Thợ nung | người đốt lò, giữ lò |
| Thợ nung phụ / khoét lò | hỗ trợ xếp khu, kéo khu ra |

Hồ sơ xưởng nên có: tên hộ, năm thành lập, số thợ, giới thiệu ngắn về dòng sản phẩm, ảnh xưởng, chứng nhận (giải thưởng, OCOP, bảo hộ thương hiệu).

**[xác nhận]** OCOP là chương trình "mỗi xã một sản phẩm" — phổ biến ở làng gốm, nhưng phải kiểm tra xưởng nào thực sự có.

## 7. Đơn vị & giá tham khảo

| Loại | Đơn vị bán | Ghi chú |
|---|---|---|
| Bình, lư, tượng | chiếc | giá theo kích thước, độ phức tạp hoa văn |
| Bát, ấm chén | bộ / chiếc | khách sỉ đặt theo bộ |
| Đơn số lượng lớn | chiếc, có mốc thời gian | ví dụ đề bài: 5.000 chiếc cốc in logo trong 1 tháng |
| Cốc in logo | chiếc | ngân sách đơn lớn rất rộng: 5k cốc giống nhau có thể rẻ hơn cốc thủ công |

Trong demo: 1-2 đơn số lượng lớn (để chạy luồng bidding + chia đơn), vài đơn nhỏ.

## 8. Từ vựng song ngữ (cho UI và tài liệu)

| Tiếng Việt | Tiếng Anh | Ghi chú trong hệ thống |
|---|---|---|
| Hộ gia đình / nghệ nhân | Artisan | tài khoản loại artisan |
| Hồ sơ xưởng | Workshop profile | |
| Sản phẩm | Product | |
| Nhật ký sản xuất | Production journal | gắn với sản phẩm |
| Công đoạn | Stage / Process step | gắn với đơn hàng |
| Yêu cầu báo giá | Quotation request | |
| Chào giá | Bid | |
| Đơn hàng | Order | |
| Lô / phần đơn | Order lot (khi admin chia) | |
| Bản đồ làng nghề | Craft village map | |
| Tin cộng đồng | Community news | |
| Hội làng nghề | Craft village council | |

Dùng thuật ngữ Anh trong tên bảng DB, tiếng Việt trên UI.

## 9. Dữ liệu mẫu cần có (seed)

| Bảng / loại | Số lượng mẫu | Ghi chú |
|---|---|---|
| Hộ gia đình | 5-6 | trải đều 3 thôn + xã; trạng thái: 4 duyệt, 1 chờ duyệt, 1 bị từ chối |
| Tài khoản buyer | 1-2 | có tài khoản sẵn để demo nhanh |
| Tài khoản admin | 1 | đăng nhập demo |
| Sản phẩm | 40-60 | chia đều 6 nhóm phân loại; mỗi sản phẩm có 4-7 mốc sản xuất |
| Ảnh | 3-5 mỗi sản phẩm | ảnh tự chụp tại xưởng hoặc ảnh CC0 |
| Yêu cầu báo giá | 4-5 | 1 đơn lớn, 2 đơn nhỏ, 1 đơn đang Bidding, 1 đơn đã chia |
| Báo giá | 2-3 mỗi đơn | 1 báo giá được chấp nhận, các bài còn lại "không chọn" |
| Công đoạn đơn hàng | theo đơn | 1 đơn đang dở giữa chừng để demo timeline |
| Ghim bản đồ | 5-6 | toạ độ thật từ OSM |
| Tin cộng đồng | 4-5 | giá đất, lịch lễ, hộ đạt giải thưởng; 1 bài artisan gửi chờ duyệt, 1 bài bị từ chối |
| Tài khoản artisan chờ duyệt | 1 | để demo luồng duyệt |

## 10. Cảnh báo pháp lý & đạo đức

1. **Tên xưởng thật, tên người thật**: chỉ dùng khi đã được phép. Mặc định dùng tên giả (vd "Xưởng gốm nhà Nghè", "Xưởng men lam Bích") để tránh rủi ro.
2. **Ảnh**: dùng ảnh nhóm tự chụp (xin phép người trong ảnh) hoặc ảnh CC0/Unsplash. Không cào ảnh Google Images.
3. **Giải thưởng, chứng nhận**: chỉ nêu nếu có thật; nếu không chắc thì dùng giải thưởng giả (có ghi "dữ liệu mẫu").
4. **Ghi nhãn rõ trong demo**: 1 dòng "Dữ liệu trong bản demo là dữ liệu mẫu" — giảng viên đánh giá cao sự minh bạch này.
