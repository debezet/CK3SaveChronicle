#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path

from archivist.save import load_gamestate
from archivist.characters import build_index, find_current_id, find_previous_chronicle_subject
from archivist.memories import build_index as build_memory_index
from archivist.report import render

def main() -> int:
    ap = argparse.ArgumentParser(description="CK3SaveChronicle Archivist")
    ap.add_argument("save", help="Path to .ck3 save")
    ap.add_argument("-o", "--output", help="Output Markdown report")
    ap.add_argument("--character-id", type=int, help="Analyze explicit character ID")
    ap.add_argument("--current", action="store_true", help="Analyze current player character")
    args = ap.parse_args()

    gamestate = load_gamestate(args.save)
    print(f"[archivist] gamestate: {len(gamestate):,} chars")

    print("[archivist] indexing characters...")
    chars = build_index(gamestate)
    print(f"[archivist] characters: {len(chars.by_id):,}")

    print("[archivist] indexing memories...")
    memories = build_memory_index(gamestate)
    print(f"[archivist] memories: {len(memories):,}")

    current = None
    if args.character_id:
        target = chars.get(args.character_id)
        if not target:
            raise SystemExit(f"Character not indexed: {args.character_id}")
    else:
        current_id = find_current_id(gamestate)
        if not current_id:
            raise SystemExit("Could not identify current character. Use --character-id.")
        current = chars.get(current_id)
        if not current:
            raise SystemExit(f"Current character {current_id} not indexed.")
        target = current if args.current else find_previous_chronicle_subject(current, chars)
        if not target:
            raise SystemExit("Could not infer previous chronicle subject. Use --character-id.")

    md = render(target, chars, memories, current)
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(md, encoding="utf-8")
        print(f"[archivist] wrote {out}")
    else:
        print(md)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
