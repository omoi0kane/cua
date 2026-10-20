# Windows screenshot-space scroll regression

This is verification material, intentionally separate from the upstream fix diff.

## Requirements
Rust 1.97.1, Cargo, Python 3, Git; normal Cargo dependency access. Windows builds need an existing native Rust toolchain/SDK. Non-Windows tests exercise the production coordinate helper; they do not exercise Win32 delivery. No model, browser, account, customer data, GUI session or input is needed.

## Run
In the fork after approved publication, fetch `fix/windows-scroll-screenshot-coordinates` so both pinned commits are present. Obtain this script from this verification commit, then run:

```sh
python3 verify_regression.py /absolute/path/to/cua-checkout
```

The script creates isolated detached worktrees and removes only those owned temporary trees. Set `CUA_REPRO_TMPDIR` to choose an approved scratch directory. Set `CARGO_TARGET_DIR` outside those worktrees to reuse compiler outputs. It does not modify the checkout's branch or tracked files.

Expected: red commit `332d5b66efcd0fdc622062f6370baab9d977e3d0` exits 101 with 3 failures/2 passes; fixed commit `f1273c9ad3358181143a3e057cf126afdf7f0212` exits 0 with 5 passes. Overall script exit 0 means both expected outcomes occurred. The red commit extracts the old cast from ScrollTool without changing its behavior; it is not a pristine-base test addition.

The decisive case maps screenshot (1000,650), scale 1920/1400, to native bitmap (1371,891) before the existing bitmap-to-screen origin transform. The old path returns (1000,650). Tests also cover scale 1, independent windows/sessions, missing/foreign context, and trusted native pixels.

## Evidence and limitations
See evidence.json for actual command outcomes. The five mapping tests also ran successfully as a Windows executable on Windows. This does not prove wheel delivery, real nested scrolling, non-100% DPI, business extraction or a complete model comparison. The existing running environment was not upgraded.

The 0.28 backport uses that release's ResizeRegistry; current upstream uses session/window-bound SnapshotStore. Do not replace the modern context contract with the older per-PID registry.
