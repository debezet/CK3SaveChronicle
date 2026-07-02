from __future__ import annotations
import re

def matching_brace(text: str, open_pos: int) -> int:
    depth = 0
    in_string = False
    escape = False
    for i in range(open_pos, len(text)):
        ch = text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i
    raise ValueError("matching brace not found")

def named_block(text: str, name: str) -> str | None:
    m = re.search(rf'(?m)(^|\s){re.escape(name)}\s*=\s*\{{', text)
    if not m:
        return None
    open_pos = text.find("{", m.start())
    end = matching_brace(text, open_pos)
    return text[open_pos+1:end]

def iter_id_blocks(section: str):
    pos = 0
    pat = re.compile(r'(?m)(^|\s)(\d+)\s*=\s*\{')
    while True:
        m = pat.search(section, pos)
        if not m:
            break
        open_pos = section.find("{", m.start())
        end = matching_brace(section, open_pos)
        yield int(m.group(2)), section[open_pos+1:end]
        pos = end + 1

def scalar(block: str, key: str) -> str | None:
    m = re.search(rf'(?m)^\s*{re.escape(key)}\s*=\s*("[^"]*"|[^\s{{}}]+)', block)
    if not m:
        return None
    val = m.group(1)
    return val[1:-1] if val.startswith('"') and val.endswith('"') else val

def number_list(block: str, key: str) -> list[int]:
    m = re.search(rf'(?ms)^\s*{re.escape(key)}\s*=\s*\{{(.*?)\}}', block)
    if not m:
        return []
    return [int(x) for x in re.findall(r'\b\d+\b', m.group(1))]

def repeated_numbers(block: str, key: str) -> list[int]:
    return [int(x) for x in re.findall(rf'(?m)^\s*{re.escape(key)}\s*=\s*(\d+)\b', block)]
