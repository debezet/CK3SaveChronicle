from __future__ import annotations
from dataclasses import dataclass
import re
from . import pdx

@dataclass
class Memory:
    id: int
    raw: str
    type: str | None
    date: str | None
    participants: list[int]

def parse_memory(mid: int, raw: str) -> Memory:
    typ = pdx.scalar(raw, "type") or pdx.scalar(raw, "memory_type")
    date = pdx.scalar(raw, "date") or pdx.scalar(raw, "creation_date")
    participants_block = pdx.named_block(raw, "participants")
    source = participants_block if participants_block else raw
    participants = [int(x) for x in re.findall(r'(?m)^\s*\w+\s*=\s*(\d+)\b', source)]
    return Memory(mid, raw, typ, date, participants)

def build_index(gamestate: str) -> dict[int, Memory]:
    out: dict[int, Memory] = {}

    # Observed CK3 save stores memories under character_memory_manager.
    for section_name in ["character_memory_manager", "memory_manager", "memories"]:
        section = pdx.named_block(gamestate, section_name)
        if not section:
            continue

        database = pdx.named_block(section, "database")
        scan = database if database else section

        for mid, raw in pdx.iter_id_blocks(scan):
            if "type=" not in raw:
                continue
            if "creation_date" not in raw and "date" not in raw:
                continue
            out[mid] = parse_memory(mid, raw)

        if out:
            break

    return out
