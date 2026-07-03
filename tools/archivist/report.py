from __future__ import annotations
from .characters import Character, CharacterIndex
from .memories import Memory
from .names import normalize_text

def render(c: Character, idx: CharacterIndex, memories: dict[int, Memory], current: Character | None = None) -> str:
    lines = []
    lines.append(f"# Raport Archiwisty — {c.display_name or c.name or c.id}")
    lines.append("")
    if current:
        lines.append(f"_Poprzedni bohater kroniki względem aktualnej postaci: {idx.name(current.id)}._")
        lines.append("")
    lines.append("## Dane podstawowe")
    lines.append("")
    lines.append(f"- ID: `{c.id}`")
    lines.append(f"- Imię: {c.display_name or c.name or 'brak danych'}")
    if c.name and c.display_name and c.name != c.display_name:
        lines.append(f"- Imię w save: `{c.name}`")
    lines.append(f"- Urodzony: {c.birth or 'brak danych'}")
    lines.append(f"- Zmarł: {c.death or 'brak danych'}")
    lines.append(f"- Przydomek: {normalize_text(c.nickname) or 'brak'}")
    lines.append(f"- Przyczyna śmierci: {normalize_text(c.death_reason) or 'brak danych'}")
    lines.append(f"- Kultura: {normalize_text(c.culture) or 'brak danych'}")
    lines.append("")
    lines.append("## Najbliższa rodzina")
    lines.append("")
    lines.append("- Małżonkowie: " + (", ".join(idx.name(x) for x in c.spouses) if c.spouses else "brak danych"))
    if c.former_spouses:
        lines.append("- Dawni małżonkowie: " + ", ".join(idx.name(x) for x in c.former_spouses))
    lines.append("- Dzieci: " + (", ".join(idx.name(x) for x in c.children) if c.children else "brak danych"))
    lines.append("")
    lines.append("## Zabójstwa")
    lines.append("")
    if c.kills:
        for kid in c.kills:
            lines.append(f"- {idx.name(kid)}")
    else:
        lines.append("- Brak zapisanych zabójstw.")
    lines.append("")
    lines.append("## Wspomnienia")
    lines.append("")
    if c.memories:
        lines.append(f"Liczba wspomnień: **{len(c.memories)}**")
        lines.append("")
        for mid in c.memories:
            mem = memories.get(mid)
            if not mem:
                lines.append(f"- `{mid}` — brak rozwinięcia")
                continue
            parts = ", ".join(idx.name(x) for x in (mem.participants or [])[:8])
            extra = f" — uczestnicy: {parts}" if parts else ""
            lines.append(f"- `{mid}` — {mem.date or 'brak daty'} — `{normalize_text(mem.type) or 'unknown'}`{extra}")
    else:
        lines.append("- Brak zapisanych wspomnień.")
    lines.append("")
    lines.append("## Hipotezy Archiwisty")
    lines.append("")
    lines.append("- [do uzupełnienia po ręcznej analizie]")
    lines.append("")
    lines.append("## Pytania do gracza")
    lines.append("")
    lines.append("- [do uzupełnienia po ręcznej analizie]")
    lines.append("")
    return "\\n".join(lines)
