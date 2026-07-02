# Tools

## Archiwista CK3

Pierwsza wersja narzędzia do raportów z save'ów CK3.

### Użycie

```bash
python tools/archivist_cli.py archive/saves/KronikiWedrowycza1046.ck3 -o archive/reports/boleslaw.md
```

Domyślnie narzędzie:

1. rozpakowuje save,
2. próbuje znaleźć aktualną postać,
3. próbuje znaleźć poprzedniego władcę przez relacje rodzinne,
4. generuje raport Markdown.

Wymuszenie konkretnej postaci:

```bash
python tools/archivist_cli.py save.ck3 --character-id 16898423 -o archive/reports/boleslaw.md
```

Analiza aktualnej postaci:

```bash
python tools/archivist_cli.py save.ck3 --current -o archive/reports/current.md
```

### Status

Eksperymentalne v0.4. Parser jest ostrożny i będzie rozwijany na podstawie kolejnych save'ów.

## v0.4.1

Poprawiono wykrywanie aktualnej postaci.

Jeżeli save nie zawiera pól typu `player_character` lub `current_character`, Archiwista próbuje odczytać ID z:

```text
meta_main_portrait={ id=... }
```

Dzięki temu użytkownik nie musi znać `--character-id`.

## v0.4.2

Poprawki:

- poprzedni władca nie powinien już być mylony z matką aktualnej postaci;
- parser odczytuje `dead_data.date` i `dead_data.reason`;
- parser uwzględnia `was_playable`, `female` i `dynasty_house` przy wyborze poprzedniego władcy;
- wspomnienia są odczytywane z `character_memory_manager`;
- `creation_date` jest traktowane jako data wspomnienia.

## v0.5.0

Zmiana architektoniczna: Archiwista nie szuka już „poprzedniego władcy” państwa ani nie zakłada, że poprzednikiem musi być ojciec.

Domyślny tryb szuka **poprzedniego bohatera kroniki**:

1. znajduje aktualną postać;
2. zbiera jej znanych przodków;
3. wybiera ostatniego zmarłego przodka oznaczonego `was_playable=yes`;
4. preferuje tę samą gałąź/dynasty house, jeśli dane są dostępne.

Dzięki temu workflow obsługuje również dziedziczki i sukcesję przez matkę, a jednocześnie nie miesza kroniki rodu z historią tytułów państwowych.
