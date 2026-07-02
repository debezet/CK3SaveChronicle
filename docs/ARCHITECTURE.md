# Architecture

Projekt oddziela dane źródłowe, raport Archiwisty, tekst Brata Mateusza oraz końcowy skład.

## Warstwy

- `archive/saves/` — save'y CK3.
- `archive/reports/` — raporty Archiwisty.
- `chronicle/books/` — kanoniczny tekst ksiąg.
- `chronicle/frontmatter/` — przedmowa i materiały początkowe.
- `chronicle/appendices/` — genealogia, oś czasu, Uwagi Archiwisty.
- `tools/` — przyszłe narzędzia.
- `output/` — artefakty budowania.

## Workflow

1. Save po śmierci władcy.
2. Raport Archiwisty.
3. Kontekst gracza.
4. Księga Brata Mateusza.
5. Redakcja.
6. Wydanie.

## Chronicle Subject

Od v0.5.0 Archiwista śledzi przede wszystkim **linię narracyjną kroniki**, nie historię państwa ani tytułu.

Kronika Domu Wędrowyczów opisuje jedną gałąź rodu wywodzącą się od pierwszej grywalnej postaci i kolejnych grywalnych dziedziców lub dziedziczek.

W praktyce oznacza to, że domyślnym celem raportu jest:

> poprzedni zmarły, grywalny przodek aktualnej postaci.

Nie jest to automatycznie:

- poprzedni posiadacz Korony Wolski;
- ojciec aktualnej postaci;
- poprzedni władca konkretnego państwa.

Historia tytułów i państw może być analizowana później jako osobna warstwa, ale nie wyznacza głównego bohatera kroniki.
