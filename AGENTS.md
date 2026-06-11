# AI-Assisted Development Guide for Air Defence ATech

This file helps developers use AI coding assistants effectively with this repository. It is designed for ChatGPT, Claude, Gemini, Cursor, Copilot, Windsurf, Codex-style agents, and similar tools.

Use this guide when onboarding, debugging, refactoring, writing tests, improving documentation, or extending the Air Defence AI + UI + hardware-control stack.

---

## Repository context for AI agents

**Project name:** Air Defence ATech  
**Domain:** Computer vision, robotics, mechatronics, PyQt5 control station, serial MCU integration.  
**Primary runtime:** Python 3.10+.  
**Main AI package:** `src/balloon_shooter/`.  
**Main UI entry:** `src/main_window.py`.  
**Configuration:** `config.yaml`.  
**Model weights:** `models/best.pt`.  
**Tests:** `tests/`.  
**CI:** `.github/workflows/ci.yml`.

The repository is an educational and supervised balloon-target robotics prototype. Keep the language and implementation focused on safe robotics research, not weaponization.

---

## High-value files to inspect first

When asking an AI agent to understand the repository, tell it to inspect these files first:

```text
README.md
README_AI.md
README_UI.md
config.yaml
pyproject.toml
requirements.txt
requirements-dev.txt
src/balloon_shooter/main.py
src/balloon_shooter/config.py
src/balloon_shooter/detector.py
src/balloon_shooter/tracker.py
src/balloon_shooter/targeting.py
src/balloon_shooter/safety.py
src/balloon_shooter/target_distance.py
src/balloon_shooter/overlays.py
src/ui/frames/upper_frame.py
src/ui/frames/middle_frame.py
src/ui/frames/lower_frame.py
src/ui/signals_controller.py
src/hardware_manager/mcu_communication.py
src/hardware_manager/pid_tracker.py
src/mcu_bridge/JsonMessenger.cpp
src/mcu_bridge/JsonMessenger.h
tests/
```

---

## Agent working rules

Use these rules in prompts:

1. Do not invent files or APIs that are not present.
2. Prefer small, reviewable diffs.
3. Preserve Python 3.10 compatibility.
4. Keep code PEP8-compliant and compatible with `ruff check .`.
5. Add or update tests for behavior changes.
6. Keep hardware actions safe by default.
7. Do not enable physical outputs without explicit simulation/safety flags.
8. Use `Air Defence` consistently in documentation.
9. Keep asset references under `docs/assets/general`, `docs/assets/ai`, `docs/assets/diagrams`, and `docs/assets/ui`.
10. Explain assumptions when repository state is incomplete.

---

## Prompt: repository onboarding

```text
You are helping me onboard to the Air Defence ATech repository.

Inspect the repository structure and explain:
1. The main AI runtime path.
2. The PyQt5 UI path.
3. The hardware/MCU communication path.
4. How config.yaml affects the system.
5. The current test coverage.
6. The top 5 files a new developer should read first.

Do not invent missing files. Use exact paths from the repository.
```

---

## Prompt: fix a bug safely

```text
You are a senior Python robotics engineer.

I will give you an error trace from the Air Defence ATech repository.
Your task:
1. Identify the likely root cause.
2. Point to the exact file/function involved.
3. Propose the smallest safe fix.
4. Show a unified diff.
5. Add or update a pytest test if possible.
6. Keep the change compatible with Python 3.10 and ruff.

Do not make hardware outputs active. Keep safety behavior conservative.
```

---

## Prompt: create the missing AI detection widget adapter

```text
The PyQt5 UI imports balloon_shooter.ai_detection_widget.AIDetectionWidget, but the repository may not include this file.

Create a safe adapter at:
src/balloon_shooter/ai_detection_widget.py

Requirements:
1. It must be a PyQt5 QWidget.
2. It must expose these signals:
   - status_message(str)
   - AI_detection_running(bool)
   - balloon_position(float, float)
   - balloon_counts(int, int)
   - camera_size(int, int)
3. It must wrap the existing detector/tracker/targeting/safety logic where practical.
4. It must fail gracefully if model weights or camera are unavailable.
5. It must not send hardware commands.
6. It must include a minimal smoke test if possible.

Show the full file content and a diff for any changed files.
```

---

## Prompt: stabilize Python↔MCU JSON schema

```text
Review the Python serial command code and the embedded JsonMessenger C++ files.

Goal: define one canonical JSON command and telemetry schema for Air Defence ATech.

Deliverables:
1. Identify current schema mismatches.
2. Propose docs/protocol.md.
3. Update Python code only if needed.
4. Update C++ parsing/serialization only if needed.
5. Add a Python test that validates command JSON shape.
6. Keep all physical outputs disabled unless explicitly commanded by the operator.

Show diffs and explain migration impact.
```

---

## Prompt: improve tests

```text
Analyze the tests/ folder and the src/ code.

Suggest and implement the highest-value missing tests for:
1. Configuration validation.
2. Target selection strategies.
3. Forbidden-zone safety.
4. Tracker persistence.
5. PID command clamping.
6. Serial payload formatting.

Use pytest. Avoid requiring camera hardware, GPU, real serial ports, or a real YOLO model in CI.
Show all diffs.
```

---

## Prompt: documentation update

```text
Update the Air Defence ATech documentation after my code changes.

Requirements:
1. Keep README.md, README_AI.md, and README_UI.md consistent.
2. Use Air Defence consistently.
3. Reference existing assets only.
4. Do not overclaim hardware readiness.
5. Add a concise changelog-style summary of documentation changes.
6. Keep Markdown clean and GitHub-friendly.

Show the final changed sections and explain why each change was needed.
```

---

## Prompt: release-readiness review

```text
Perform a release-readiness review of this repository.

Prioritize issues by severity:
- Critical: prevents fresh clone from running or creates unsafe behavior.
- High: hurts reproducibility, packaging, tests, or integration reliability.
- Medium: documentation, naming, cleanup, maintainability.
- Low: polish.

For each issue, provide:
1. Exact file/path evidence.
2. Why it matters.
3. Recommended fix.
4. Whether it should block public release.

Keep the review concise and actionable.
```

---

## Prompt: optimize AI inference

```text
Review the AI inference pipeline in src/balloon_shooter.

Suggest optimizations for:
1. CPU inference.
2. CUDA inference.
3. Frame resizing and capture settings.
4. Overlay drawing cost.
5. Tracker update cost.
6. Optional ONNX export.

Do not change behavior unless you show a benchmark plan and a safe diff.
```

---

## Prompt: UI modernization

```text
Review the PyQt5 UI code.

Improve maintainability and operator experience while preserving behavior.
Focus on:
1. Layout clarity.
2. Signal naming.
3. Error handling.
4. Port configuration UX.
5. PID input validation.
6. Safe simulation mode.
7. Logs and telemetry readability.

Show small diffs. Do not rewrite the whole UI unless necessary.
```

---

## Suggested agent workflow

For serious work, use this sequence:

```text
1. Ask the agent to scan and summarize the repo.
2. Ask it to identify missing/broken integration points.
3. Fix one issue at a time.
4. Run tests after every change.
5. Ask for a diff review.
6. Update documentation after code stabilizes.
7. Run release-readiness review before publishing.
```

---

## Common mistakes to prevent

- Do not rename modules without updating imports and tests.
- Do not assume the UI is fully integrated if `ai_detection_widget.py` is missing.
- Do not claim hardware is production-ready.
- Do not require real camera, serial ports, GPU, or model weights in CI tests.
- Do not commit `__pycache__`, `.env`, logs, or generated run folders.
- Do not mix `Air Defense`, `Hava Savunma`, and `Air Defence`; use `Air Defence` in docs.

---

## Good first AI-agent tasks

- Add `src/balloon_shooter/ai_detection_widget.py` adapter.
- Add `docs/protocol.md` for JSON serial schema.
- Add `requirements-ui.txt` or package extras.
- Add a Qt offscreen UI smoke test.
- Add serial-payload tests.
- Normalize asset folder names to lowercase.
- Remove cached/generated files from version control.
- Improve README screenshots and video links after uploading media to GitHub.
