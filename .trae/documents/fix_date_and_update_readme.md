# Plan: Fix Date Parsing Issue and Update Documentation

## Summary
This plan addresses the issue where the model defaults to 2023 dates despite user input, and adds requested build script instructions to the README. The date issue is caused by inconsistent example formatting in `src/prompt.txt`.

## Current State Analysis
1.  **Date Parsing Issue**:
    - The user reported that voice input "I added 500 yuan gas today" results in a 2023 date.
    - Analysis of `src/prompt.txt` shows that while the first three examples were updated to include `Current Date: ...`, the last two examples (lines 50-56) still use the old format `Input: "text"`.
    - This inconsistency confuses the model, causing it to fall back to the hardcoded 2023 dates in the examples when it encounters simple text input.
2.  **Documentation Gap**:
    - The user previously requested adding build script instructions to `README.md`, which is currently missing.

## Proposed Changes

### 1. Fix `src/prompt.txt`
- Update the last two examples to strictly follow the `Current Date: ... \n Content: ...` format.
- This ensures the model learns to look for and use the provided `Current Date`.

### 2. Update `README.md`
- Add a "Developer Guide" or "Build Instructions" section.
- Document the command `python3 scripts/build.py` and its purpose (updating `public/` resources).

### 3. Rebuild Public Resources
- Run `python3 scripts/build.py` to propagate the prompt changes to `public/config.json`.

## Verification Steps
1.  Verify `src/prompt.txt` contains consistent example formats.
2.  Verify `public/config.json` contains the updated prompt.
3.  Verify `README.md` contains the new instructions.
