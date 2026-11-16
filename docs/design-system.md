# Design system — vCraft

- **Phiên bản:** 1.0 | **Cập nhật:** 2026-11-16
- **Phục vụ tiêu chí rubric #3 (hệ số 0.2):** giao diện responsive, đẹp, hiện đại, có bản sắc, nhận dạng thương hiệu
- **Nguồn domain:** `docs/domain-battrang.md` — gốm Bát Tràng, men lam, đất nung

> Quy tắc: mọi component lấy token từ file này. **Không hardcode mã màu, font, khoảng cách trong component.** Token sống ở `frontend/src/lib/design-tokens.ts` và `tailwind.config.ts`.

## 1. Bản sắc thương hiệu

| Thành phần | Nội dung |
|---|---|
| Tên | **vCraft** |
| Tagline | **"Tinh hoa làng nghề, muôn phương lan toả"** |
| Định vị | Triển lãm số cho làng nghề truyền thống — không phải sàn thương mại điện tử |
| Giọng điệu | Ấm, kể chuyện, tôn trọng người làm nghề. Không dùng từ "siêu hot", "deal sốc", "mua ngay kẻo lỡ" |
| Logo (concept) | Vòng xoay bàn xoay gốm nhìn nghiêng + chữ V cách điệu. Tối giản, nét đơn sắc |
| Dấu ấn nhận dạng | Đường viền mảnh màu men lam + ảnh tràn viền; chữ tiêu đề kiểu serif |

**Điều tuyệt đối tránh** (để không ra "AI aesthetic"):

- Palette tím/indigo mặc định
- Gradient mạnh ở hero
- Bo tròn toàn bộ (`rounded-2xl` mọi nơi)
- Grid card đều tăm tắp không phân cấp
- Ảnh stock, chữ mẫu "Lorem ipsum"
- Shadow chồng nhiều lớp
- Icon bộ generic dùng lẫn nhiều style

## 2. Palette

Lấy từ vật liệu gốm Bát Tràng. **5 màu chính, không thêm.**

| Token | Hex | Dùng cho | Ghi chú |
|---|---|---|---|
| `brand.men-lam` | `#1B3A6B` | primary, heading, link | xanh cobalt của men lam |
| `brand.men-lam-600` | `#24518F` | hover primary | |
| `brand.dat-nung` | `#B4552D` | accent, CTA phụ, badge giải thưởng | terracotta đất nung |
| `brand.men-ngoc` | `#6E8F7A` | success, trạng thái "đang làm" | xanh men ngọc |
| `brand.trang-nga` | `#F7F3EA` | surface, nền trang | trắng ngà của men trắng |
| `neutral.900` | `#22201D` | text chính | than |
| `neutral.600` | `#5C574F` | text phụ | |
| `neutral.300` | `#D9D3C7` | border | |
| `danger` | `#B3261E` | lỗi, từ chối, huỷ | |
| `warning` | `#9A6700` | cảnh báo, chờ duyệt | |

**Quy tắc tương phản:** text trên `trang-nga` phải đạt 4.5:1. `men-lam` trên `trang-nga` đạt ~10:1. Không dùng `dat-nung` cho body text (chỉ dùng cho accent hoặc chữ ≥ 18px đậm).

## 3. Typography

| Vai trò | Font | Cỡ / line-height | Weight |
|---|---|---|---|
| Tiêu đề trang (h1) | **Playfair Display** (subset vietnamese) | 40/48 · mobile 32/40 | 700 |
| Tiêu đề mục (h2) | Playfair Display | 32/40 | 600 |
| Tiêu đề phụ (h3) | Be Vietnam Pro | 24/32 | 600 |
| Thân bài | **Be Vietnam Pro** | 16/26 | 400 |
| Nhấn / label | Be Vietnam Pro | 14/20 | 500 |
| Chú thích | Be Vietnam Pro | 12/18 | 400 |
| Giá tiền | Be Vietnam Pro | 20/28 | 600, `font-variant-numeric: tabular-nums` |

- Tối đa **2 họ font** (1 serif + 1 sans). Không thêm font thứ ba.
- Tiêu đề không nhảy cấp (h1 → h2 → h3).
- Không dùng heading style cho nội dung không phải heading.

## 4. Spacing, radius, shadow

| Token | Giá trị | Dùng cho |
|---|---|---|
| `space-1..12` | 4px × n | scale duy nhất, không dùng số lẻ |
| `radius-sm` | 4px | input, badge |
| `radius-md` | 12px | card, dialog |
| `radius-pill` | 999px | chip trạng thái |
| `shadow-sm` | `0 1px 2px rgb(34 32 29 / 0.06)` | card nghỉ |
| `shadow-md` | `0 4px 16px rgb(34 32 29 / 0.10)` | hover card, dialog |

Không dùng padding 13px, margin 2.3rem, hay bất kỳ giá trị ngoài scale.

## 5. Component bắt buộc

| Component | Yêu cầu | Trạng thái phải có |
|---|---|---|
| `Button` | primary / secondary / ghost / danger, 3 cỡ | hover, focus-visible, disabled, loading |
| `ProductCard` | ảnh 4:3 + tên + hộ + giá | hover, ảnh lỗi, skeleton |
| `Gallery` | grid ảnh + lightbox | keyboard, alt text, lazy |
| `StageTimeline` | 7 công đoạn gốm, dòng thời gian | todo/doing/done, ảnh minh chứng, "chưa tới bước" |
| `StatusBadge` | trạng thái đơn/bài/tài khoản | 6 màu ngữ nghĩa, không chỉ dùng màu (kèm icon + chữ) |
| `Field` | label + hint + error + required | error dưới field, `aria-describedby` |
| `Autocomplete` | gợi ý khi gõ (hộ, phân loại, sản phẩm) | loading, không kết quả, chọn bằng bàn phím |
| `EmptyState` | icon + câu giải thích + CTA | — |
| `Skeleton` | khung xám nhấp nháy theo layout thật | — |
| `ErrorState` | thông báo + nút "Thử lại" | — |
| `Table` (admin) | sắp xếp, phân trang, hàng chọn | hàng trống, loading |
| `Toast` | thành công / lỗi | tự đóng 4s, có nút đóng |
| `ConfirmDialog` | xác nhận hành động không hoàn tác | focus trap, Esc |

**Không có màn hình nào được trắng trơn.** Mỗi trang phải có đủ 4 trạng thái: loading, rỗng, lỗi, có dữ liệu.

## 6. Responsive

Mobile-first. Breakpoint: `sm 640` · `md 768` · `lg 1024` · `xl 1440`.

| Khu vực | Mobile (<768) | Tablet | Desktop |
|---|---|---|---|
| Điều hướng | bottom bar 4 mục | top bar thu gọn | top bar đầy đủ |
| Danh mục sản phẩm | 1 cột | 2 cột | 3-4 cột |
| Trang chi tiết | ảnh trên, thông tin dưới | ảnh 60% | ảnh 55% + cột thông tin dính |
| Bảng admin | chuyển thành card | bảng cuộn ngang | bảng đầy đủ |
| Form | 1 cột | 2 cột | 2 cột |
| Bản đồ | cao 50vh | 60vh | 70vh, cột phụ danh sách |

Kiểm tra ở 320 / 768 / 1024 / 1440 — không có cuộn ngang.

## 7. Hình ảnh

| Quy tắc | Giá trị |
|---|---|
| Tỉ lệ card sản phẩm | 4:3 |
| Tỉ lệ gallery | 1:1 hoặc 4:3, thống nhất 1 loại |
| Kích thước xuất | 400px (card) + 1200px (chi tiết), WebP |
| Khai báo `width`/`height` | **bắt buộc** — chống CLS |
| Lazy load | ảnh ngoài màn hình đầu |
| Hover | zoom 1.03, 200ms, `ease-out` |
| Alt text | bắt buộc, mô tả sản phẩm + hộ (không viết "ảnh") |

## 8. Accessibility (WCAG 2.1 AA)

- Keyboard: mọi tương tác dùng được bằng Tab/Enter/Space/Esc
- Focus ring: 2px `men-lam` + offset 2px, không `outline: none` mà không thay thế
- Form: `<label>` thật, lỗi gắn `aria-describedby`, `aria-invalid`
- Bảng: `<th scope>`, caption
- Ảnh: alt text; ảnh trang trí `alt=""`
- Không dùng màu làm tín hiệu duy nhất → luôn kèm icon/chữ
- `prefers-reduced-motion` → tắt animation

## 9. Token trong Tailwind

```ts
// tailwind.config.ts (rút gọn)
theme: {
  extend: {
    colors: {
      brand: {
        'men-lam': '#1B3A6B',
        'men-lam-600': '#24518F',
        'dat-nung': '#B4552D',
        'men-ngoc': '#6E8F7A',
        'trang-nga': '#F7F3EA',
      },
      neutral: { 900: '#22201D', 600: '#5C574F', 300: '#D9D3C7' },
      danger: '#B3261E',
      warning: '#9A6700',
    },
    fontFamily: {
      display: ['"Playfair Display"', 'serif'],
      sans: ['"Be Vietnam Pro"', 'system-ui', 'sans-serif'],
    },
    borderRadius: { sm: '4px', md: '12px', pill: '999px' },
    boxShadow: {
      sm: '0 1px 2px rgb(34 32 29 / 0.06)',
      md: '0 4px 16px rgb(34 32 29 / 0.10)',
    },
  },
}
```

## 10. Checklist duyệt UI (dùng trong PR)

- [ ] Dùng token, không hardcode hex/font/spacing
- [ ] Có đủ 4 trạng thái: loading, rỗng, lỗi, dữ liệu
- [ ] Responsive 320/768/1024/1440, không cuộn ngang
- [ ] Keyboard dùng được toàn bộ luồng chính
- [ ] Ảnh có `width`/`height` + alt text
- [ ] Không có dấu hiệu "AI aesthetic" (mục 1)
- [ ] Tương phản ≥ 4.5:1 cho body text
- [ ] Có 1 chi tiết nhận dạng thương hiệu (đường men lam / serif / vòng xoay)

## 11. Lịch sử

| Ngày | Thay đổi | Người |
|---|---|---|
| 2026-11-16 | Phiên bản 1.0 — bản sắc, palette, typography, component, responsive, a11y | Nhóm |
