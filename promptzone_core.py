# promptzone_core.py
# PromptZone core logic for CustomTkinter UI (ACTIONSTYLE, CLOTHES, COMPOSITION, I2V)
# Folder layout (under root_dir):
#   ACTIONSTYLE_*/prompt_*.md|.txt
#   CLOTHES_*/prompt_*.md|.txt
#   COMPOSITION_*/prompt_*.md|.txt
#   I2V_*/prompt_*.md|.txt
#
# Settings stored in settings.json next to this file.

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import random
import re

DIVIDER = "\n\n" + ("-" * 48) + "\n\n"

ACTION_PREFIX = "ACTIONSTYLE_"
CLOTHES_PREFIX = "CLOTHES_"
COMPOSITION_PREFIX = "COMPOSITION_"
I2V_PREFIX = "I2V_"

TAGS_FILE = "tags.json"
WEIGHTS_FILE = "weights.json"
SETTINGS_FILE = "settings.json"
PROMPT_TEXT_EXTENSIONS = (".md", ".txt")

DEFAULT_SLOTS = [
    {"id": "slot_1", "label": "SLOT_1", "prefix": "SLOT_1_", "enabled": True, "minimized": False},
]


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="ignore")


def write_text(p: Path, s: str):
    p.write_text(s, encoding="utf-8")


def safe_name(s: str) -> str:
    # Uppercase + allow alnum/_ only
    return "".join(ch for ch in s.upper() if ch.isalnum() or ch == "_").strip("_")

def safe_filename(name: str) -> str:
    # Only a filename (no paths), strip invalid Windows chars, ensure .md/.txt.
    n = (name or "").strip()
    if not n:
        raise ValueError("Filename is empty.")
    if any(sep in n for sep in ("/", "\\")):
        raise ValueError("Filename must not include folders.")
    if n in (".", ".."):
        raise ValueError("Invalid filename.")
    invalid = '<>:"|?*'
    n = "".join(ch for ch in n if ch not in invalid and ord(ch) >= 32).strip()
    if not n:
        raise ValueError("Invalid filename.")
    if not n.lower().endswith(PROMPT_TEXT_EXTENSIONS):
        n = n + ".md"
    return n

def infer_tags_from_name(folder_name: str) -> list[str]:
    n = folder_name.lower()
    tags = set()
    if any(k in n for k in ["street", "paparazzi", "candid", "urban", "alley", "sidewalk", "flash", "night"]):
        tags.add("street")
    if any(k in n for k in ["studio", "backdrop", "seamless", "softbox", "keylight", "portrait"]):
        tags.add("studio")
    if any(k in n for k in ["vintage", "retro", "pinup", "noir", "film", "classic", "cafe"]):
        tags.add("vintage")
    if any(k in n for k in ["fantasy", "gothic", "dark", "myth", "angel", "demon", "castle", "sorcer"]):
        tags.add("fantasy")
    if not tags:
        tags.add("other")
    return sorted(tags)


def next_prompt_filename(folder: Path, ext: str = ".md") -> str:
    ext = str(ext or ".md").lower().strip()
    if ext not in PROMPT_TEXT_EXTENSIONS:
        ext = ".md"
    nums = []
    for f in _prompt_text_files(folder):
        m = re.match(r"prompt_(\d+)\.(?:md|txt)$", f.name, flags=re.IGNORECASE)
        if m:
            nums.append(int(m.group(1)))
    n = (max(nums) + 1) if nums else 1
    return f"prompt_{n:02d}{ext}"


def load_json(path: Path, default):
    try:
        if path.exists():
            obj = json.loads(read_text(path))
            return obj
    except Exception:
        pass
    return default


def save_json(path: Path, obj):
    try:
        write_text(path, json.dumps(obj, indent=2, ensure_ascii=False))
    except Exception:
        pass


def _split_sets(text: str, n: int) -> list[str]:
    t = (text or "").strip()
    if not t:
        return [""] * n
    parts = t.split(DIVIDER)
    parts = [p.strip() for p in parts if p.strip()]
    if len(parts) == 1:
        return [parts[0]] * n
    # pad/trim to n
    if len(parts) < n:
        parts = parts + [parts[-1]] * (n - len(parts))
    return parts[:n]


def _prompt_text_files(folder: Path) -> list[Path]:
    files = []
    for f in sorted(folder.iterdir(), key=lambda p: p.name.lower()):
        if f.is_file() and f.suffix.lower() in PROMPT_TEXT_EXTENSIONS:
            files.append(f)
    return files


def _nonempty_prompt_files(folder: Path) -> list[Path]:
    files = []
    for f in _prompt_text_files(folder):
        if read_text(f).strip():
            files.append(f)
    return files


def _normalize_tag(tag: str) -> str:
    t = (tag or "").strip().lower().replace(" ", "_")
    return "".join(ch for ch in t if ch.isalnum() or ch == "_").strip("_")


def _coerce_list(value, default: str) -> list[str]:
    if isinstance(value, list):
        out = [str(v) for v in value if str(v)]
        return out or [default]
    if isinstance(value, str) and value.strip():
        return [value]
    return [default]


class PromptZoneCore:
    def __init__(self, root_dir: Path):
        self.root_dir = Path(root_dir)
        if self.root_dir.name.lower() == "promptzone_pyside":
            self.library_dir = self.root_dir / "Prompt_Library"
        else:
            pyside_dir = self.root_dir / "promptzone_pyside"
            if pyside_dir.exists() and pyside_dir.is_dir():
                self.library_dir = pyside_dir / "Prompt_Library"
            else:
                self.library_dir = self.root_dir / "Prompt_Library"
        self.library_dir.mkdir(parents=True, exist_ok=True)
        self.settings_path = self.root_dir / SETTINGS_FILE
        self.tags_path = self.root_dir / TAGS_FILE
        self.weights_path = self.root_dir / WEIGHTS_FILE

        self.output_path = self.root_dir / "selected_prompts.txt"

        self.settings = load_json(self.settings_path, {})
        if not isinstance(self.settings, dict):
            self.settings = {}

        self.tags_map: dict[str, list[str]] = {}
        self.weights_map: dict[str, float] = {}

        self.used_action_files: set[Path] = set()
        self.used_clothes_files: set[Path] = set()
        self.used_composition_files: set[Path] = set()
        self.used_i2v_files: set[Path] = set()

        self.last_action_sources = ""
        self.last_clothes_sources = ""
        self.last_composition_sources = ""
        self.last_i2v_sources = ""

        self.reload_library()
        self._ensure_slot_settings()

    def _ensure_slot_settings(self):
        slots = self.settings.get("slots")
        if not isinstance(slots, list) or not slots:
            self.settings["slots"] = [dict(s) for s in DEFAULT_SLOTS]
            self.save_settings()

    def get_slots(self) -> list[dict]:
        slots = self.settings.get("slots")
        if not isinstance(slots, list) or not slots:
            return [dict(s) for s in DEFAULT_SLOTS]
        out = []
        for idx, s in enumerate(slots):
            if not isinstance(s, dict):
                continue
            label = str(s.get("label") or f"Slot {idx + 1}").strip()
            prefix = str(s.get("prefix") or "").strip()
            if prefix and not prefix.endswith("_"):
                prefix = prefix + "_"
            out.append(
                {
                    "id": str(s.get("id") or f"slot_{idx+1}"),
                    "label": label,
                    "prefix": prefix,
                    "enabled": bool(s.get("enabled", True)),
                    "minimized": bool(s.get("minimized", False)),
                }
            )
        if not out:
            out = [dict(s) for s in DEFAULT_SLOTS]
        return out

    def save_settings(self):
        save_json(self.settings_path, self.settings)

    def all_tags(self) -> list[str]:
        tags = set()
        for vals in self.tags_map.values():
            if isinstance(vals, list):
                tags.update([_normalize_tag(v) for v in vals if _normalize_tag(v)])
        custom = self.settings.get("custom_tags", [])
        if isinstance(custom, list):
            tags.update([_normalize_tag(v) for v in custom if _normalize_tag(v)])
        if not tags:
            tags.update(["street", "studio", "vintage", "fantasy", "other"])
        return sorted(tags)

    def add_tag(self, name: str) -> str:
        tag = _normalize_tag(name)
        if not tag:
            raise ValueError("Invalid tag name.")
        custom = self.settings.get("custom_tags", [])
        if not isinstance(custom, list):
            custom = []
        if tag not in custom:
            custom.append(tag)
            self.settings["custom_tags"] = sorted(set(custom))
            self.save_settings()
        return tag

    def get_folder_tags(self, folder_name: str) -> list[str]:
        tags = self.tags_map.get(folder_name)
        if not tags:
            tags = infer_tags_from_name(folder_name)
        return [_normalize_tag(t) for t in tags if _normalize_tag(t)]

    def set_folder_tags(self, folder_name: str, tags: list[str]):
        if not folder_name:
            raise ValueError("Folder name required.")
        norm = [_normalize_tag(t) for t in tags if _normalize_tag(t)]
        self.tags_map[folder_name] = sorted(set(norm))
        # Ensure tags are discoverable in UI
        custom = self.settings.get("custom_tags", [])
        if not isinstance(custom, list):
            custom = []
        for t in norm:
            if t not in custom:
                custom.append(t)
        self.settings["custom_tags"] = sorted(set(custom))
        save_json(self.tags_path, self.tags_map)
        self.save_settings()

    # ---------- folder discovery ----------
    def _folders_by_prefix(self, prefix: str) -> list[Path]:
        return sorted([p for p in self.library_dir.iterdir() if p.is_dir() and p.name.startswith(prefix)])

    def folders_by_prefix(self, prefix: str) -> list[Path]:
        if not prefix:
            return []
        return self._folders_by_prefix(prefix)

    def action_folder_names(self) -> list[str]:
        return [p.name for p in self._folders_by_prefix(ACTION_PREFIX)]

    def clothes_folder_names(self) -> list[str]:
        return [p.name for p in self._folders_by_prefix(CLOTHES_PREFIX)]

    def composition_folder_names(self) -> list[str]:
        return [p.name for p in self._folders_by_prefix(COMPOSITION_PREFIX)]

    def i2v_folder_names(self) -> list[str]:
        return [p.name for p in self._folders_by_prefix(I2V_PREFIX)]

    def counts(self):
        def count_files(folders: list[Path]) -> int:
            return sum(len(_prompt_text_files(f)) for f in folders)
        a = self._folders_by_prefix(ACTION_PREFIX)
        c = self._folders_by_prefix(CLOTHES_PREFIX)
        m = self._folders_by_prefix(COMPOSITION_PREFIX)
        i = self._folders_by_prefix(I2V_PREFIX)
        return (len(a), count_files(a), len(c), count_files(c), len(m), count_files(m), len(i), count_files(i))

    def reload_library(self):
        # Load tags/weights (optional)
        t = load_json(self.tags_path, {})
        w = load_json(self.weights_path, {})
        self.tags_map = t if isinstance(t, dict) else {}
        self.weights_map = w if isinstance(w, dict) else {}

        # Ensure each ACTION folder has inferred tags if missing
        for folder in self._folders_by_prefix(ACTION_PREFIX):
            self.tags_map.setdefault(folder.name, infer_tags_from_name(folder.name))

        save_json(self.tags_path, self.tags_map)

    # ---------- browsing/search ----------
    def browse_entries(self, kind: str, query: str, prefix: str | None = None):
        if prefix:
            folders = self._folders_by_prefix(str(prefix).strip())
        else:
            kind = kind.upper().strip()
            if kind == "ACTIONSTYLE":
                folders = self._folders_by_prefix(ACTION_PREFIX)
            elif kind == "CLOTHES":
                folders = self._folders_by_prefix(CLOTHES_PREFIX)
            elif kind == "COMPOSITION":
                folders = self._folders_by_prefix(COMPOSITION_PREFIX)
            elif kind == "I2V":
                folders = self._folders_by_prefix(I2V_PREFIX)
            else:
                raise ValueError(f"Unknown kind: {kind}")

        q = (query or "").strip().lower()
        out = []
        for folder in folders:
            for f in _nonempty_prompt_files(folder):
                label = f"{folder.name}/{f.name}"
                text = read_text(f)
                if not q or (q in label.lower()) or (q in text.lower()):
                    out.append((label, f, text))
        return out

    # ---------- creation ----------
    def _resolve_slot_prefix(self, kind_or_prefix: str) -> str:
        token = str(kind_or_prefix or "").strip()
        if not token:
            raise ValueError("Unknown kind.")
        upper = token.upper()
        legacy = {
            "ACTIONSTYLE": ACTION_PREFIX,
            "CLOTHES": CLOTHES_PREFIX,
            "COMPOSITION": COMPOSITION_PREFIX,
            "I2V": I2V_PREFIX,
        }
        if upper in legacy:
            return legacy[upper]
        if token.endswith("_"):
            return token

        low = token.lower()
        for slot in self.get_slots():
            slot_id = str(slot.get("id") or "").strip().lower()
            label = str(slot.get("label") or "").strip().lower()
            prefix = str(slot.get("prefix") or "").strip()
            if not prefix:
                continue
            if low == slot_id or low == label:
                return prefix
            if upper == prefix.rstrip("_").upper():
                return prefix
        raise ValueError("Unknown kind.")

    def create_category(self, kind: str, name: str) -> str:
        raw = safe_name(name)
        if not raw:
            raise ValueError("Invalid category name.")

        prefix = self._resolve_slot_prefix(kind)

        folder_name = raw
        if not folder_name.startswith(prefix):
            folder_name = prefix + folder_name

        folder = self.library_dir / folder_name
        folder.mkdir(parents=True, exist_ok=True)
        return folder_name

    def create_prompt_file(
        self, kind: str, folder_name: str, text: str, filename: str | None = None, overwrite: bool = False
    ) -> Path:
        kind = kind.upper().strip()
        folder = self.library_dir / folder_name
        if not folder.exists() or not folder.is_dir():
            raise ValueError(f"Folder not found: {folder_name}")

        if filename:
            fn = safe_filename(filename)
        else:
            fn = next_prompt_filename(folder)
        path = folder / fn
        if path.exists() and not overwrite:
            raise ValueError(f"File already exists: {fn}")
        write_text(path, (text or "").strip() + "\n")
        return path

    # ---------- selection helpers ----------
    def _normalize_tag_set(self, tags: set[str] | list[str]) -> set[str]:
        return {_normalize_tag(t) for t in (tags or []) if _normalize_tag(t)}

    def _folder_has_excluded_tags(self, folder_name: str, excluded_tags: set[str]) -> bool:
        if not excluded_tags:
            return False
        ex = self._normalize_tag_set(excluded_tags)
        if not ex:
            return False
        tags = self.get_folder_tags(folder_name)
        return any(t in ex for t in tags)

    def _eligible_folders(self, kind: str, excluded: set[str], excluded_tags: set[str]) -> list[Path]:
        if kind == "ACTIONSTYLE":
            folders = self._folders_by_prefix(ACTION_PREFIX)
        elif kind == "CLOTHES":
            folders = self._folders_by_prefix(CLOTHES_PREFIX)
        elif kind == "COMPOSITION":
            folders = self._folders_by_prefix(COMPOSITION_PREFIX)
        else:
            folders = self._folders_by_prefix(I2V_PREFIX)
        return [
            p
            for p in folders
            if p.name not in excluded
            and _nonempty_prompt_files(p)
            and not self._folder_has_excluded_tags(p.name, excluded_tags)
        ]

    def _pick_file(self, folder: Path, used: set[Path], avoid_repeats: bool) -> Path | None:
        files = _nonempty_prompt_files(folder)
        if not files:
            return None
        if not avoid_repeats:
            return random.choice(files)

        choices = [f for f in files if f not in used]
        if not choices:
            # exhausted: reset only for this folder
            for f in files:
                used.discard(f)
            choices = files[:]
        f = random.choice(choices)
        used.add(f)
        return f

    def _choose_action_folder_weighted(
        self,
        excluded: set[str],
        excluded_tags: set[str],
        tag_pref,
        weight_strength: float,
    ) -> Path | None:
        folders = self._eligible_folders("ACTIONSTYLE", excluded, excluded_tags)
        if not folders:
            return None

        pref_vals = _coerce_list(tag_pref, "All")
        prefs = [_normalize_tag(p) for p in pref_vals if _normalize_tag(p) and _normalize_tag(p) != "all"]
        if not prefs:
            return random.choice(folders)

        # Weight boost if folder has preferred tag
        weights = []
        for f in folders:
            base_w = float(self.weights_map.get(f.name, 1.0))
            tags = self.get_folder_tags(f.name)
            match_count = sum(1 for p in prefs if p in tags)
            boost = 1.0 + (weight_strength * 2.0 * match_count) if match_count else 1.0
            weights.append(max(0.001, base_w * boost))

        return random.choices(folders, weights=weights, k=1)[0]

    # ---------- generate ----------
    def generate(self, action_slot: str, clothes_slot: str, composition_slot: str, i2v_slot: str):
        s = self.settings

        n = max(1, int(s.get("n_sets", 3)))

        action_choices = _coerce_list(s.get("action_category", "Any"), "Any")
        clothes_choices = _coerce_list(s.get("clothes_category", "Any"), "Any")
        composition_choices = _coerce_list(s.get("composition_category", "Any"), "Any")
        i2v_choices = _coerce_list(s.get("i2v_category", "Any"), "Any")

        excluded_action = set(s.get("excluded_action", []) or [])
        excluded_clothes = set(s.get("excluded_clothes", []) or [])
        excluded_composition = set(s.get("excluded_composition", []) or [])
        excluded_i2v = set(s.get("excluded_i2v", []) or [])
        excluded_tags = set(s.get("excluded_tags", []) or [])

        lock_action = bool(s.get("lock_action", False))
        lock_clothes = bool(s.get("lock_clothes", False))
        lock_composition = bool(s.get("lock_composition", False))
        lock_i2v = bool(s.get("lock_i2v", False))

        append_output = bool(s.get("append_output", False))
        avoid_repeats = bool(s.get("avoid_repeats", True))
        only_one_per_folder = bool(s.get("only_one_per_folder", False))

        tag_pref = s.get("tag_pref", "All")
        weight_strength = float(s.get("weight_strength", 0.65))

        # If locked, treat current slot as source per-set (divider aware)
        locked_action_sets = _split_sets(action_slot, n) if lock_action else None
        locked_clothes_sets = _split_sets(clothes_slot, n) if lock_clothes else None
        locked_composition_sets = _split_sets(composition_slot, n) if lock_composition else None
        locked_i2v_sets = _split_sets(i2v_slot, n) if lock_i2v else None

        actions, clothes, compositions, i2vs, prompts = [], [], [], [], []
        action_sources, clothes_sources, composition_sources, i2v_sources = [], [], [], []

        batch_used_action_folders = set()
        batch_used_clothes_folders = set()
        batch_used_composition_folders = set()
        batch_used_i2v_folders = set()

        def category_mode(vals: list[str]) -> tuple[str, list[str]]:
            if "None" in vals:
                return ("None", [])
            if "Any" in vals or not vals:
                return ("Any", [])
            filtered = [v for v in vals if v not in ("Any", "None")]
            return ("List", filtered)

        action_mode, action_list = category_mode(action_choices)
        clothes_mode, clothes_list = category_mode(clothes_choices)
        composition_mode, composition_list = category_mode(composition_choices)
        i2v_mode, i2v_list = category_mode(i2v_choices)

        for idx in range(n):
            # ACTIONSTYLE
            if lock_action and locked_action_sets and locked_action_sets[idx].strip():
                atext = locked_action_sets[idx].strip()
                action_sources.append("")
            else:
                if action_mode == "None":
                    atext = ""
                    action_sources.append("")
                else:
                    if action_mode == "List":
                        candidates = []
                        for name in action_list:
                            if name in excluded_action:
                                continue
                        afolder = self.library_dir / name
                        if not afolder.exists():
                            continue
                            if not _nonempty_prompt_files(afolder):
                                continue
                            if self._folder_has_excluded_tags(afolder.name, excluded_tags):
                                continue
                            candidates.append(afolder)
                        if not candidates:
                            raise ValueError("No ACTIONSTYLE folders found (or all excluded).")
                        if only_one_per_folder:
                            tries = 0
                            afolder = random.choice(candidates)
                            while afolder.name in batch_used_action_folders and tries < 50:
                                afolder = random.choice(candidates)
                                tries += 1
                        else:
                            afolder = random.choice(candidates)
                    else:
                        # choose weighted
                        afolder = self._choose_action_folder_weighted(
                            excluded_action, excluded_tags, tag_pref, weight_strength
                        )
                        if only_one_per_folder and afolder:
                            tries = 0
                            while afolder.name in batch_used_action_folders and tries < 50:
                                afolder = self._choose_action_folder_weighted(
                                    excluded_action, excluded_tags, tag_pref, weight_strength
                                )
                                tries += 1
                    if not afolder:
                        raise ValueError("No ACTIONSTYLE folders found (or all excluded).")
                    if only_one_per_folder:
                        batch_used_action_folders.add(afolder.name)

                    afile = self._pick_file(afolder, self.used_action_files, avoid_repeats)
                    if not afile:
                        atext = ""
                        action_sources.append("")
                    else:
                        atext = read_text(afile).strip()
                        action_sources.append(f"{afolder.name}\\{afile.name}")

            # CLOTHES
            if lock_clothes and locked_clothes_sets and locked_clothes_sets[idx].strip():
                ctext = locked_clothes_sets[idx].strip()
                clothes_sources.append("")
            else:
                if clothes_mode == "None":
                    ctext = ""
                    clothes_sources.append("")
                else:
                    if clothes_mode == "List":
                        candidates = []
                        for name in clothes_list:
                            if name in excluded_clothes:
                                continue
                        cfolder = self.library_dir / name
                        if not cfolder.exists():
                            continue
                            if not _nonempty_prompt_files(cfolder):
                                continue
                            if self._folder_has_excluded_tags(cfolder.name, excluded_tags):
                                continue
                            candidates.append(cfolder)
                        if not candidates:
                            raise ValueError("No CLOTHES folders found (or all excluded).")
                        if only_one_per_folder:
                            tries = 0
                            cfolder = random.choice(candidates)
                            while cfolder.name in batch_used_clothes_folders and tries < 50:
                                cfolder = random.choice(candidates)
                                tries += 1
                        else:
                            cfolder = random.choice(candidates)
                    else:
                        cfolders = self._eligible_folders("CLOTHES", excluded_clothes, excluded_tags)
                        if not cfolders:
                            raise ValueError("No CLOTHES folders found (or all excluded).")
                        cfolder = random.choice(cfolders)
                        if only_one_per_folder:
                            tries = 0
                            while cfolder.name in batch_used_clothes_folders and tries < 50:
                                cfolder = random.choice(cfolders)
                                tries += 1
                    if only_one_per_folder:
                        batch_used_clothes_folders.add(cfolder.name)

                    cfile = self._pick_file(cfolder, self.used_clothes_files, avoid_repeats)
                    if not cfile:
                        ctext = ""
                        clothes_sources.append("")
                    else:
                        ctext = read_text(cfile).strip()
                        clothes_sources.append(f"{cfolder.name}\\{cfile.name}")

            # COMPOSITION
            if lock_composition and locked_composition_sets and locked_composition_sets[idx].strip():
                mtext = locked_composition_sets[idx].strip()
                composition_sources.append("")
            else:
                if composition_mode == "None":
                    mtext = ""
                    composition_sources.append("")
                else:
                    if composition_mode == "List":
                        candidates = []
                        for name in composition_list:
                            if name in excluded_composition:
                                continue
                        mfolder = self.library_dir / name
                        if not mfolder.exists():
                            continue
                            if not _nonempty_prompt_files(mfolder):
                                continue
                            if self._folder_has_excluded_tags(mfolder.name, excluded_tags):
                                continue
                            candidates.append(mfolder)
                        if not candidates:
                            raise ValueError("No COMPOSITION folders found (or all excluded).")
                        if only_one_per_folder:
                            tries = 0
                            mfolder = random.choice(candidates)
                            while mfolder.name in batch_used_composition_folders and tries < 50:
                                mfolder = random.choice(candidates)
                                tries += 1
                        else:
                            mfolder = random.choice(candidates)
                    else:
                        mfolders = self._eligible_folders("COMPOSITION", excluded_composition, excluded_tags)
                        if not mfolders:
                            raise ValueError("No COMPOSITION folders found (or all excluded).")
                        mfolder = random.choice(mfolders)
                        if only_one_per_folder:
                            tries = 0
                            while mfolder.name in batch_used_composition_folders and tries < 50:
                                mfolder = random.choice(mfolders)
                                tries += 1
                    if only_one_per_folder:
                        batch_used_composition_folders.add(mfolder.name)

                    mfile = self._pick_file(mfolder, self.used_composition_files, avoid_repeats)
                    if not mfile:
                        mtext = ""
                        composition_sources.append("")
                    else:
                        mtext = read_text(mfile).strip()
                        composition_sources.append(f"{mfolder.name}\\{mfile.name}")

            # I2V
            if lock_i2v and locked_i2v_sets and locked_i2v_sets[idx].strip():
                itext = locked_i2v_sets[idx].strip()
                i2v_sources.append("")
            else:
                if i2v_mode == "None":
                    itext = ""
                    i2v_sources.append("")
                else:
                    if i2v_mode == "List":
                        candidates = []
                        for name in i2v_list:
                            if name in excluded_i2v:
                                continue
                        ifolder = self.library_dir / name
                        if not ifolder.exists():
                            continue
                            if not _nonempty_prompt_files(ifolder):
                                continue
                            if self._folder_has_excluded_tags(ifolder.name, excluded_tags):
                                continue
                            candidates.append(ifolder)
                        if not candidates:
                            raise ValueError("No I2V folders found (or all excluded).")
                        if only_one_per_folder:
                            tries = 0
                            ifolder = random.choice(candidates)
                            while ifolder.name in batch_used_i2v_folders and tries < 50:
                                ifolder = random.choice(candidates)
                                tries += 1
                        else:
                            ifolder = random.choice(candidates)
                    else:
                        ifolders = self._eligible_folders("I2V", excluded_i2v, excluded_tags)
                        if not ifolders:
                            raise ValueError("No I2V folders found (or all excluded).")
                        ifolder = random.choice(ifolders)
                        if only_one_per_folder:
                            tries = 0
                            while ifolder.name in batch_used_i2v_folders and tries < 50:
                                ifolder = random.choice(ifolders)
                                tries += 1
                    if only_one_per_folder:
                        batch_used_i2v_folders.add(ifolder.name)

                    ifile = self._pick_file(ifolder, self.used_i2v_files, avoid_repeats)
                    if not ifile:
                        itext = ""
                        i2v_sources.append("")
                    else:
                        itext = read_text(ifile).strip()
                        i2v_sources.append(f"{ifolder.name}\\{ifile.name}")

            actions.append(atext)
            clothes.append(ctext)
            compositions.append(mtext)
            i2vs.append(itext)

            parts = [p for p in [atext, ctext, mtext] if p.strip()]
            prompts.append("\n".join(parts).strip())

        def join_sets(arr: list[str]) -> str:
            if n == 1:
                return arr[0] if arr else ""
            return DIVIDER.join([a.strip() for a in arr])

        out = join_sets(prompts)
        self.last_action_sources = join_sets(action_sources)
        self.last_clothes_sources = join_sets(clothes_sources)
        self.last_composition_sources = join_sets(composition_sources)
        self.last_i2v_sources = join_sets(i2v_sources)

        # Write output file
        try:
            mode = "a" if append_output else "w"
            existed = self.output_path.exists()
            with self.output_path.open(mode, encoding="utf-8") as f:
                if mode == "a" and existed:
                    f.write(DIVIDER)
                f.write(out)
        except Exception:
            # UI handles warnings
            pass

        return join_sets(actions), join_sets(clothes), join_sets(compositions), join_sets(i2vs), out

    # ---------- dynamic slots ----------
    def _slot_settings(self, slot_id: str) -> dict:
        slots_settings = self.settings.get("slot_settings", {})
        if not isinstance(slots_settings, dict):
            slots_settings = {}
        entry = slots_settings.get(slot_id, {})
        return entry if isinstance(entry, dict) else {}

    def _slot_mode(self, vals: list[str]) -> tuple[str, list[str]]:
        if "None" in vals:
            return ("None", [])
        if "Any" in vals or not vals:
            return ("Any", [])
        filtered = [v for v in vals if v not in ("Any", "None")]
        return ("List", filtered)

    def generate_slots(self, slots: list[dict], slot_texts: dict[str, str], skip_minimized: bool = False):
        s = self.settings
        n = max(1, int(s.get("n_sets", 3)))
        avoid_repeats = bool(s.get("avoid_repeats", True))
        only_one_per_folder = bool(s.get("only_one_per_folder", False))
        append_output = bool(s.get("append_output", False))
        weight_strength = float(s.get("weight_strength", 0.65))
        tag_pref = s.get("tag_pref", "All")
        excluded_tags = set(s.get("excluded_tags", []) or [])

        slots_out = {slot["id"]: [] for slot in slots}
        sources_out = {slot["id"]: [] for slot in slots}

        batch_used = {slot["id"]: set() for slot in slots}

        for idx in range(n):
            for slot in slots:
                slot_id = slot["id"]
                if not slot.get("enabled", True):
                    slots_out[slot_id].append("")
                    sources_out[slot_id].append("")
                    continue
                if skip_minimized and slot.get("minimized", False):
                    slots_out[slot_id].append("")
                    sources_out[slot_id].append("")
                    continue

                st = self._slot_settings(slot_id)
                lock = bool(st.get("lock", False))
                gen = bool(st.get("gen", True))
                category_vals = _coerce_list(st.get("category", "Any"), "Any")
                excluded = set(st.get("excluded", []) or [])
                prefix = slot.get("prefix", "")

                if lock and slot_texts.get(slot_id, "").strip():
                    slots_out[slot_id].append(slot_texts[slot_id].strip())
                    sources_out[slot_id].append("")
                    continue

                if not gen:
                    category_vals = ["None"]

                mode, lst = self._slot_mode(category_vals)
                if mode == "None":
                    slots_out[slot_id].append("")
                    sources_out[slot_id].append("")
                    continue

                if mode == "List":
                    candidates = []
                    for name in lst:
                        if name in excluded:
                            continue
                        folder = self.library_dir / name
                        if not folder.exists():
                            continue
                        if not _nonempty_prompt_files(folder):
                            continue
                        if self._folder_has_excluded_tags(folder.name, excluded_tags):
                            continue
                        candidates.append(folder)
                    if not candidates:
                        current_text = (slot_texts.get(slot_id, "") or "").strip()
                        if current_text:
                            slots_out[slot_id].append(current_text)
                            sources_out[slot_id].append("")
                            continue
                        raise ValueError(f"No folders found for slot: {slot.get('label', slot_id)}")
                    folder = random.choice(candidates)
                    if only_one_per_folder:
                        tries = 0
                        while folder.name in batch_used[slot_id] and tries < 50:
                            folder = random.choice(candidates)
                            tries += 1
                    if only_one_per_folder:
                        batch_used[slot_id].add(folder.name)
                else:
                    # Any
                    folders = self.folders_by_prefix(prefix)
                    folders = [
                        f
                        for f in folders
                        if f.name not in excluded
                        and _nonempty_prompt_files(f)
                        and not self._folder_has_excluded_tags(f.name, excluded_tags)
                    ]
                    if not folders:
                        current_text = (slot_texts.get(slot_id, "") or "").strip()
                        if current_text:
                            slots_out[slot_id].append(current_text)
                            sources_out[slot_id].append("")
                            continue
                        raise ValueError(f"No folders found for slot: {slot.get('label', slot_id)}")
                    # weight boost by preferred tags (if any)
                    pref_vals = _coerce_list(tag_pref, "All")
                    prefs = [
                        _normalize_tag(p) for p in pref_vals if _normalize_tag(p) and _normalize_tag(p) != "all"
                    ]
                    if prefs:
                        weights = []
                        for f in folders:
                            base_w = float(self.weights_map.get(f.name, 1.0))
                            tags = self.get_folder_tags(f.name)
                            match_count = sum(1 for p in prefs if p in tags)
                            boost = 1.0 + (weight_strength * 2.0 * match_count) if match_count else 1.0
                            weights.append(max(0.001, base_w * boost))
                        folder = random.choices(folders, weights=weights, k=1)[0]
                    else:
                        folder = random.choice(folders)
                    if only_one_per_folder:
                        tries = 0
                        while folder.name in batch_used[slot_id] and tries < 50:
                            folder = random.choice(folders)
                            tries += 1
                        batch_used[slot_id].add(folder.name)

                file_path = self._pick_file(folder, set(), avoid_repeats)
                if not file_path:
                    slots_out[slot_id].append("")
                    sources_out[slot_id].append("")
                else:
                    slots_out[slot_id].append(read_text(file_path).strip())
                    sources_out[slot_id].append(f"{folder.name}\\{file_path.name}")

        def join_sets(arr: list[str]) -> str:
            if n == 1:
                return arr[0] if arr else ""
            return DIVIDER.join([a.strip() for a in arr])

        joined = {slot_id: join_sets(vals) for slot_id, vals in slots_out.items()}
        sources_joined = {slot_id: join_sets(vals) for slot_id, vals in sources_out.items()}

        # Write output file from enabled slots
        out_sets = []
        for idx in range(n):
            parts = []
            for slot in slots:
                slot_id = slot["id"]
                if not slot.get("enabled", True):
                    continue
                if skip_minimized and slot.get("minimized", False):
                    continue
                text = slots_out[slot_id][idx].strip()
                if text:
                    parts.append(text)
            out_sets.append("\n".join(parts).strip())
        out = join_sets(out_sets)

        try:
            mode = "a" if append_output else "w"
            existed = self.output_path.exists()
            with self.output_path.open(mode, encoding="utf-8") as f:
                if mode == "a" and existed:
                    f.write(DIVIDER)
                f.write(out)
        except Exception:
            pass

        return joined, sources_joined, out
