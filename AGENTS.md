# vCraft — Agent Rules (OpenCode)

Dự án web cho Ban quản lý làng nghề (INT3306, team 3, demo trực tiếp cuối kỳ).

## Domain
- **Làng gốm Bát Tràng** — nội dung, tên sản phẩm, công đoạn, ảnh, dữ liệu mẫu đều theo nghề gốm Bát Tràng
- Chi tiết domain (sản phẩm, quy trình làm gốm, men, từ vựng, dữ liệu mẫu, cảnh báo pháp lý): `docs/domain-battrang.md`
- Khi sinh nội dung mẫu: tên xưởng dùng tên giả, ảnh dùng ảnh tự chụp hoặc CC0 — không dùng tên/ảnh thật khi chưa được phép

## Stack
- (chưa chốt — điền sau khi team chọn)

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

## Tham chiếu
- Skill domain references: `.opencode/references/*.md`
- Agent personas: `.opencode/agents/*.md` (code-reviewer, security-auditor, test-engineer, web-performance-auditor)
- Agents orchestration doc: `.opencode/references/agents.md`