# PromptZone 

PromptZone is a desktop app to manage prompt libraries, randomize prompt sets across configurable slots, and export combined output.

## What The App Can Do

### 1) Randomize prompts across dynamic slots
- Uses slot definitions from `settings.json` (`slots` list).
- Default first-run slot: `SLOT_1` with prefix `SLOT_1_`.
- Each slot can be:
  - enabled/disabled
  - minimized (hidden in UI)
  - locked (keep current text)
  - included/excluded from randomization
- Randomize all slots at once or randomize one slot at a time.

### 2) Build multiple prompt sets in one run
- `How many sets` controls batch count (1-50).
- Multi-set results are separated by the internal divider:
  - `------------------------------------------------`

### 3) Category selection per slot
- Each slot supports category mode:
  - `Any` (all folders with matching prefix)
  - `None` (empty output for that slot)
  - one or more specific categories
- Category menus are searchable/filterable in the right-panel exclude system and in browse dialogs.

### 4) Exclude system
- Exclude specific categories per slot.
- Filter exclude lists by filename/content.
- Global filter across all exclude blocks.
- Drag-check behavior supported in exclude checkbox lists.
- `Clear excludes` clears all category excludes.

### 5) Tag system + weighted sampling
- Tags are stored in `tags.json`.
- You can assign tags to categories from **Assign tag** dialog.
- Preferred tags influence weighted randomization (via `Weight strength`).
- Tags can be globally excluded from generation (`Exclude tag` button).

### 6) Repeat handling
- `Avoid repeats (session)` avoids reusing files until pool exhaustion.
- `Reset repeats` clears repeat history.
- `Only one per folder (per batch)` avoids reusing same folder inside one batch.

### 7) Prompt creation and library management
- Create new categories for any slot prefix.
- Create prompt files as `.md` or `.txt`.
- Optional media attachment saved with same basename as prompt.
- Add custom tags.
- Manage slots (add/remove/reorder/rename/prefix/enable/minimize/auto-prefix).

### 8) Browse and inject prompts
- Browse prompt files for any slot with search over filename + content.
- Inject selected prompt into slot.
- Inject + Lock sets value and locks slot.
- Shows media preview for files with same basename as prompt.

### 9) Media preview support
- Prompt preview media lookup: same folder + same basename as prompt file.
- Supported image preview:
  - `.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp`, `.gif`
- Supported video preview:
  - `.webm`, `.mp4`, `.m4v`, `.mov`, `.avi`, `.mkv`, `.wmv`, `.mpg`, `.mpeg`
- Video preview loops.

### 10) Output actions
- Output text area shows concatenated slot result.
- `Copy Output` copies output to clipboard.
- `Save TXT` writes to `selected_prompts.txt`.
- `Append output` appends to file instead of overwrite.

### 11) Theme system
- Built-in presets and custom color editing.
- Save custom preset names.
- Theme applied to main UI and dialogs.

### 12) UI state persistence
- Main window geometry/state saved.
- Popup geometry saved per dialog.
- Popup splitter positions saved (including Browse splitters).
- Last slot text, slot source labels, output text, and per-slot settings saved.

---

## Main UI Reference

## Top Bar
- `Copy Output`: copy output panel text.
- `Save TXT`: write output to `selected_prompts.txt`.
- `Create`: open Create dialog.
- `Assign tag`: open Assign Tag dialog.
- `Reload`: reload library/tags/weights from disk.
- `Manage Slots`: open slot manager.
- `Customise`: open theme editor.
- Preset combo: apply theme preset quickly.

## Left Panel (Randomize Settings)
- `How many sets` with `-` and `+` buttons.
- `Preferred tag` multi-select dropdown.
- `Exclude tag` popup list + clear.
- `Weight strength` slider with percentage preview.
- Per-slot category dropdown.
- Per-slot `Lock` checkbox.
- Global options:
  - `Skip minimized prompts`
  - `Append output`
  - `Avoid repeats (session)`
  - `Only one per folder (per batch)`
- Per-slot browse buttons (`Browse <slot>...`).
- Per-slot generation row:
  - `Randomize <slot>` checkbox
  - single-slot randomize icon button
  - `Clear` button
- Bottom `Randomize` button runs full generation.

## Center Panel (Slots + Output)
- One text area per slot.
- Source label per slot (folder/file used in latest generation).
- Output panel with combined prompt text.

## Right Panel (Exclude Categories)
- Per-slot exclude lists with search box.
- Global search filter for all exclude lists.
- `Clear excludes` and `Reset repeats`.

---

## Dialogs

## Manage Slots
- Columns:
  - `#` row order
  - `Name`
  - `Prefix`
  - `Auto` (auto-regenerate prefix from Name)
  - `Enabled`
  - `Minimized`
- Actions:
  - `Up` / `Down` reorder
  - `Add Slot`
  - `Remove Slot`
  - `Close` (save)

## Create
- Tab: **New Category**
  - choose slot type
  - create category folder
- Tab: **New Prompt**
  - choose slot type and category
  - optional filename (`.md`/`.txt`)
  - prompt text
  - optional media file (`Browse media...`)
  - Ctrl+V supports image clipboard and local file URL paste
  - saves media beside prompt using same basename
- Tab: **New Tag**
  - create custom tag

## Assign Tag
- Choose slot type and category.
- Check/uncheck tags to assign.
- Save updates `tags.json`.

## Browse
- Search prompts by filename/content.
- Preview text and media.
- Horizontal splitter between media preview and text preview.
- `Inject` or `Inject + Lock`.

## Theme Customise
- Edit color keys directly or with color picker.
- Apply preset/reset defaults.
- Save theme and save as named custom preset.

---

## Library Layout

PromptZone uses this structure relative to `promptzone_pyside`:

```text
promptzone_pyside/
  Prompt_Library/
    <PREFIX_CATEGORY_NAME>/
      prompt_01.md
      prompt_02.txt
      prompt_02.png   (optional media preview)
      prompt_03.mp4   (optional media preview)
  settings.json
  tags.json
  weights.json
  selected_prompts.txt
```

Notes:
- Category folders are matched by slot prefix.
- Prompt files considered by randomizer/browse: `.md`, `.txt`.
- Media preview is matched by basename (example: `prompt_02.txt` + `prompt_02.png`).

---

## Settings Persistence (`settings.json`)

The app stores, among others:
- slot definitions (`slots`)
- per-slot runtime settings (`slot_settings`)
- generation settings (`n_sets`, `weight_strength`, repeats, append, etc.)
- category and exclude selections
- excluded tags
- last output and last slot texts/sources
- theme colors + preset
- main window geometry/state
- popup geometry (`popup_geometry`)
- popup splitter states (`popup_splitters`)