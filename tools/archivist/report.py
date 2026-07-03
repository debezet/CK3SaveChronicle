from __future__ import annotations
from .characters import Character, CharacterIndex
from .memories import Memory
from .names import normalize_text


def _format_values(values: list[str]) -> str:
    return ", ".join(f"`{x}`" for x in values) if values else "brak"


def _append_trait_section(lines: list[str], c: Character) -> None:
    profile = c.trait_profile
    lines.append("## Osobowość i cechy według save")
    lines.append("")

    if not profile.ids:
        lines.append("- Brak zapisanych traitów.")
        lines.append("")
        return

    lines.append("_Sekcja źródłowa: Archiwista wypisuje klucze mechanik CK3, bez interpretacji literackiej._")
    lines.append("")
    lines.append(f"- Cechy osobowości: {_format_values(profile.personality)}")
    lines.append(f"- Edukacja: {_format_values(profile.education)}")
    lines.append(f"- Styl życia i doświadczenie: {_format_values(profile.lifestyle)}")
    lines.append(f"- Radzenie sobie ze stresem / nawyki: {_format_values(profile.coping)}")
    lines.append(f"- Dowodzenie: {_format_values(profile.commander)}")
    lines.append(f"- Zdrowie i ciało: {_format_values(profile.health_and_body)}")
    lines.append(f"- Status, sława i piętna: {_format_values(profile.status)}")
    lines.append(f"- Inne: {_format_values(profile.other)}")
    if profile.unknown_ids:
        lines.append("- Nierozpoznane ID traitów: " + ", ".join(f"`{x}`" for x in profile.unknown_ids))
    lines.append("")


def _append_profile_section(lines: list[str], c: Character, idx: CharacterIndex) -> None:
    profile = c.trait_profile
    lines.append("## Profil bohatera")
    lines.append("")
    lines.append("_Syntetyczna kartoteka źródłowa dla Redaktora i Brata Mateusza._")
    lines.append("")
    lines.append(f"- Zakres życia: {c.birth or 'brak danych'} – {c.death or 'brak danych'}")
    lines.append(f"- Małżonkowie zapisani w raporcie: {len(c.spouses)}")
    lines.append(f"- Dzieci zapisane w raporcie: {len(c.children)}")
    lines.append(f"- Zabójstwa zapisane w save: {len(c.kills)}")
    lines.append(f"- Wspomnienia zapisane w save: {len(c.memories)}")
    if profile.personality:
        lines.append("- Mechaniczny rdzeń osobowości: " + _format_values(profile.personality))
    if profile.education:
        lines.append("- Wykształcenie według gry: " + _format_values(profile.education))
    notable = profile.lifestyle + profile.commander + profile.status
    if notable:
        lines.append("- Cechy pomocne narracyjnie: " + _format_values(notable))
    lines.append("")


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
    _append_trait_section(lines, c)
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
    _append_profile_section(lines, c, idx)
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
    return "\n".join(lines)
