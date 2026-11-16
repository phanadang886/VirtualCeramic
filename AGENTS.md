# vCraft — Agent Rules (OpenCode)

Dự án web cho Ban quản lý làng nghề (INT3306, team 3, demo trực tiếp cuối kỳ).

## Domain
- **Làng gốm Bát Tràng** — nội dung, tên sản phẩm, công đoạn, ảnh, dữ liệu mẫu đều theo nghề gốm Bát Tràng
- Chi tiết domain (sản phẩm, quy trình làm gốm, men, từ vựng, dữ liệu mẫu, cảnh báo pháp lý): `docs/domain-battrang.md`
- Khi sinh nội dung mẫu: tên xưởng dùng tên giả, ảnh dùng ảnh tự chụp hoặc CC0 — không dùng tên/ảnh thật khi chưa được phép

## Stack (đã chốt — `docs/decisions/ADR-001-stack.md`)
- **Backend:** FastAPI + Uvicorn · SQLAlchemy 2 (async) + asyncpg · Alembic · Pydantic v2 · PyJWT + argon2 · Pillow · qrcode
- **Frontend:** React + Vite + TypeScript · Tailwind + shadcn/ui · TanStack Query · React Router · Zod · react-leaflet
- **Hạ tầng:** PostgreSQL 16 · Docker Compose · Nginx + DNS công khai + HTTPS (`docs/decisions/ADR-002-nginx-public-dns.md`)
- **Test/lint:** pytest + httpx + pytest-cov · ruff · GitHub Actions (sau)
- **Cấu trúc:** `backend/` · `frontend/` · `deploy/` · `docs/` · `tasks/` · `scripts/`
- Không tự đổi stack. Muốn đổi → mở ADR mới, không sửa ADR cũ.

## Quy tắc bắt buộc khi code
- **Cấm lazy load** trong SQLAlchemy async — luôn `selectinload`/`joinedload`, nếu không sẽ dính `MissingGreenlet`
- **Mọi chuyển trạng thái** đi qua service, không `UPDATE status` trực tiếp trong router
- **Mọi thao tác đổi trạng thái** nằm trong transaction, khoá dòng với `SELECT ... FOR UPDATE` khi cần
- **`PUBLIC_BASE_URL`** là nguồn duy nhất cho URL trong QR — không hardcode domain
- **Ảnh**: resize bằng Pillow trong `run_in_threadpool`, tên file do server sinh, kiểm tra magic bytes
- **Hai nguồn sự thật không được lệch:** `docs/api.md` (thiết kế) và OpenAPI sinh từ FastAPI (code). Khi lệch → sửa code theo `docs/api.md`

## Constraints
- **Đọc `CONSTRAINTS.md` trước khi viết code. Không hạ tiêu chuẩn để cho một thay đổi pass.**
- Floor (chặn): không suppression comment, không stub/TODO, không xoá test, không secret, không nới ràng buộc trong `CONSTRAINTS.md`
- Kiểm tra floor trước khi báo xong: `node scripts/floor-guard.mjs` (exit 0 = sạch, 1 = vi phạm, 2 = chưa chạy được)

## Skill routing
- Process (brainstorm → plan → implement → test → review → ship): **superpowers** là router chính.
- Domain references (UI, API, security, perf, docs, launch, quality bar): các skill dưới đây.
- **Không chạy cả superpowers X và agent-skills Y cho cùng một bước.** Bảng overlap:
  - spec/design doc → superpowers `brainstorming` (không dùng agent-skills `spec-driven-development`)
  - plan → superpowers `writing-plans` (không dùng `planning-and-task-breakdown`)
  - review → superpowers `requesting-code-review` (không dùng `code-review-and-quality`)
  - debugging → superpowers `systematic-debugging`
  - git/worktree → superpowers `using-git-worktrees`
  - TDD → superpowers `test-driven-development` (ID trùng, giữ bản superpowers)
- caveman = style chat. Artifact (code, doc, commit) viết bình thường.

## Intent → skill
- UI/component/layout/a11y → `frontend-ui-engineering`
- API/module boundary/contract → `api-and-interface-design`
- Auth/input/upload/security/roles → `security-and-hardening`
- Perf/image/map/bundle → `performance-optimization`
- ADR/decision/doc drift → `documentation-and-adrs`
- Pre-demo checklist/rollback/monitoring → `shipping-and-launch`
- Quality bar số (coverage, a11y, CWV) → `constraint-driven-development`

## Đường dẫn tài liệu (override mặc định của superpowers)
- Design doc: `docs/specs/YYYY-MM-DD-<topic>-design.md`
- Implementation plan: `docs/plans/YYYY-MM-DD-<feature>.md`
- ADR: `docs/decisions/ADR-00N-<title>.md`
- Yêu cầu: `docs/requirements.md`
- Architecture: `docs/architecture.md`
- Demo script: `docs/demo-script.md`
- Quality bar: `CONSTRAINTS.md`
- Task list: `tasks/todo.md`

## Quy trình Git (3 người, GitHub)
- Nhánh chính: `main` — không push trực tiếp, mọi thay đổi qua Pull Request
- Mỗi tính năng 1 nhánh: `feat/<ten>`; sửa lỗi: `fix/<ten>`; tài liệu: `docs/<ten>`
- Commit message theo Conventional Commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`
- Không commit: `.env`, `node_modules/`, build output, ảnh lớn — dùng `.gitignore`
- Mỗi PR gắn với 1 mục `tasks/todo.md` và 1 tiêu chí `docs/requirements.md` §7
- Khi agent tạo commit/PR phải nêu: đổi file nào, vì sao, cách kiểm chứng

## Tham chiếu tài liệu (đọc theo thứ tự khi làm việc mới)
1. `docs/requirements.md` — cần làm gì (§4), tiêu chí nghiệm thu (§7), đối chiếu rubric (§7.1), thay đổi đã chốt (§9)
2. `docs/architecture.md` — ERD, máy trạng thái, luồng, design patterns (§12), độc lập CSDL + URL (§13)
3. `docs/design-system.md` — bản sắc, palette, typography, component, responsive (rubric #3)
4. `docs/api.md` — contract endpoint
5. `docs/domain-battrang.md` — ngữ cảnh nghiệp vụ gốm, dữ liệu mẫu
6. `docs/demo-script.md` — kịch bản demo + câu hỏi dự kiến
7. `docs/decisions/ADR-00N-*.md` — quyết định đã chốt, không sửa lịch sử
8. `CONSTRAINTS.md` — ngưỡng chất lượng
9. `tasks/todo.md` — việc đang làm

## Tham chiếu kỹ thuật
- Skill domain references: `.opencode/references/*.md`
- Agent personas: `.opencode/agents/*.md` (code-reviewer, security-auditor, test-engineer, web-performance-auditor)
- Agents orchestration doc: `.opencode/references/agents.md`