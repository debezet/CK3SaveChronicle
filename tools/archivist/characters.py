from __future__ import annotations
from dataclasses import dataclass, field
import re
from . import pdx
from .names import normalize_name

@dataclass
class Character:
    id: int
    raw: str
    name: str | None = None
    display_name: str | None = None
    birth: str | None = None
    death: str | None = None
    death_reason: str | None = None
    nickname: str | None = None
    culture: str | None = None
    dynasty_house: str | None = None
    female: bool = False
    was_playable: bool = False
    father: int | None = None
    mother: int | None = None
    spouses: list[int] = field(default_factory=list)
    former_spouses: list[int] = field(default_factory=list)
    children: list[int] = field(default_factory=list)
    memories: list[int] = field(default_factory=list)
    kills: list[int] = field(default_factory=list)

def parse_character(cid: int, raw: str) -> Character:
    def maybe_int(x):
        return int(x) if x and x.isdigit() else None

    raw_name = pdx.scalar(raw, "first_name") or pdx.scalar(raw, "name")
    dead_data = pdx.named_block(raw, "dead_data")
    death = pdx.scalar(raw, "death")
    death_reason = pdx.scalar(raw, "death_reason")

    if dead_data:
        death = death or pdx.scalar(dead_data, "date")
        death_reason = death_reason or pdx.scalar(dead_data, "reason")

    memories = pdx.number_list(raw, "memories")
    kills = pdx.number_list(raw, "kills")
    if dead_data:
        memories = memories or pdx.number_list(dead_data, "memories")
        kills = kills or pdx.number_list(dead_data, "kills")

    return Character(
        id=cid,
        raw=raw,
        name=raw_name,
        display_name=normalize_name(raw_name),
        birth=pdx.scalar(raw, "birth"),
        death=death,
        death_reason=death_reason,
        nickname=pdx.scalar(raw, "nickname"),
        culture=pdx.scalar(raw, "culture"),
        dynasty_house=pdx.scalar(raw, "dynasty_house"),
        female=bool(re.search(r'(?m)^\s*female\s*=\s*yes\b', raw)),
        was_playable=bool(re.search(r'(?m)^\s*was_playable\s*=\s*yes\b', raw)),
        father=maybe_int(pdx.scalar(raw, "father")),
        mother=maybe_int(pdx.scalar(raw, "mother")),
        spouses=pdx.repeated_numbers(raw, "spouse") + pdx.number_list(raw, "spouse"),
        former_spouses=pdx.repeated_numbers(raw, "former_spouse") + pdx.number_list(raw, "former_spouse"),
        children=pdx.repeated_numbers(raw, "child") + pdx.number_list(raw, "child"),
        memories=memories,
        kills=kills,
    )

class CharacterIndex:
    def __init__(self):
        self.by_id: dict[int, Character] = {}
        self.parent_candidates: dict[int, list[int]] = {}

    def add(self, c: Character):
        self.by_id[c.id] = c
        for child in c.children:
            self.parent_candidates.setdefault(child, []).append(c.id)

    def get(self, cid: int | None) -> Character | None:
        return self.by_id.get(cid) if cid is not None else None

    def name(self, cid: int | None) -> str:
        c = self.get(cid)
        if not c:
            return str(cid) if cid is not None else "brak danych"
        return f"{c.display_name or c.name or '?'} ({c.id})"

    def parents_of(self, child_id: int) -> list[Character]:
        out: list[Character] = []
        child = self.get(child_id)
        if child:
            for pid in [child.father, child.mother]:
                p = self.get(pid)
                if p and p.id not in {x.id for x in out}:
                    out.append(p)
        for pid in self.parent_candidates.get(child_id, []):
            p = self.get(pid)
            if p and p.id not in {x.id for x in out}:
                out.append(p)
        return out

def build_index(gamestate: str) -> CharacterIndex:
    idx = CharacterIndex()
    seen = set()
    for section_name in ["living", "dead_unprunable", "dead_prunable", "characters"]:
        section = pdx.named_block(gamestate, section_name)
        if not section:
            continue
        for cid, raw in pdx.iter_id_blocks(section):
            if cid in seen:
                continue
            if "first_name" not in raw and "birth" not in raw:
                continue
            seen.add(cid)
            idx.add(parse_character(cid, raw))
    return idx

def find_current_id(gamestate: str) -> int | None:
    patterns = [
        r'meta_player\s*=\s*(\d+)',
        r'player_character\s*=\s*(\d+)',
        r'played_character\s*=\s*(\d+)',
        r'current_character\s*=\s*(\d+)',
        r'player\s*=\s*\{\s*id\s*=\s*(\d+)',
        r'meta_main_portrait\s*=\s*\{.*?\bid\s*=\s*(\d+)',
    ]
    for pat in patterns:
        m = re.search(pat, gamestate, re.S)
        if m:
            return int(m.group(1))
    return None

def _date_key(date: str | None) -> tuple[int, int, int]:
    if not date:
        return (0, 0, 0)
    nums = [int(x) for x in re.findall(r'\d+', date)[:3]]
    while len(nums) < 3:
        nums.append(0)
    return tuple(nums[:3])

def ancestors_of(character: Character, idx: CharacterIndex, max_depth: int = 20) -> list[Character]:
    seen: set[int] = set()
    result: list[Character] = []
    def walk(c: Character, depth: int):
        if depth >= max_depth:
            return
        for parent in idx.parents_of(c.id):
            if parent.id in seen:
                continue
            seen.add(parent.id)
            result.append(parent)
            walk(parent, depth + 1)
    walk(character, 0)
    return result

def find_previous_chronicle_subject(current: Character, idx: CharacterIndex) -> Character | None:
    ancestors = ancestors_of(current, idx)
    if not ancestors:
        return None
    candidates = [a for a in ancestors if a.was_playable and a.death]
    if current.dynasty_house:
        same_house = [a for a in candidates if a.dynasty_house == current.dynasty_house]
        if same_house:
            candidates = same_house
    if candidates:
        return max(candidates, key=lambda c: (_date_key(c.death), len(c.memories)))
    dead_ancestors = [a for a in ancestors if a.death]
    if dead_ancestors:
        return max(dead_ancestors, key=lambda c: (_date_key(c.death), len(c.memories)))
    return None

def infer_previous_ruler(current: Character, idx: CharacterIndex) -> Character | None:
    return find_previous_chronicle_subject(current, idx)
