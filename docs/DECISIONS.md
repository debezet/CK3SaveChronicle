# Decision Log

## 2026-07-02 — Markdown jako źródło

Źródłem tekstów kroniki jest Markdown. DOCX i PDF są artefaktami wydań, nie źródłem prawdy.

## 2026-07-02 — Brat Mateusz nie zna przyszłości

W tekście kroniki nie wolno zapowiadać wydarzeń, które nastąpią dopiero w późniejszych księgach, chyba że są zapisane jako późniejsza uwaga Archiwisty.

## 2026-07-02 — Niepewna chronologia Jakuba

Nie podajemy dokładnej daty narodzin Jakuba w głosie Brata Mateusza. Wczesna słowiańska wspólnota nie prowadzi dokładnej kancelarii, dlatego początek księgi operuje przybliżeniem wieku.

## 2026-07-02 — Wolska odmienia się jak Polska

Poprawne formy: Wolska, Wolski, Wolskę, Wolską.

## 2026-07-02 — Przydomek Andrzeja

Przydomek `with the Tress` oddajemy jako **Andrzej z Warkoczem**.

## 2026-07-02 — Konrad

Kanonicznie Konrad poległ w wojnie z Cesarstwem Wschodniorzymskim, podczas drugiej bitwy pod Foggią.

## 2026-07-02 — Brak stron „Dziedzictwo”

Zrezygnowano z redakcyjnych stron podsumowujących dziedzictwo każdego władcy. Wnioski mają wynikać z samej kroniki.

## 2026-07-02 — Wykrywanie aktualnej postaci z `meta_main_portrait`

Pierwsza wersja Archiwisty nie znajdowała aktualnej postaci w save'ie `KronikiWedrowycza1046.ck3`, ponieważ CK3 zapisał ID aktualnego władcy w bloku:

```text
meta_main_portrait={
    id=...
}
```

Od wersji v0.4.1 Archiwista używa tego pola jako praktycznego fallbacku do identyfikacji aktualnie grywanej postaci.

## 2026-07-02 — Poprawka wyboru poprzedniego władcy

Archiwista v0.4.1 potrafił błędnie wybrać matkę aktualnej postaci jako poprzedniego władcę. Przyczyną było to, że CK3 przechowuje datę śmierci w bloku `dead_data={ date=... }`, a parser rozpoznawał tylko proste pole `death=`.

Od wersji v0.4.2 parser odczytuje `dead_data.date`, `dead_data.reason`, `was_playable`, `female` oraz `dynasty_house`, a wybór poprzedniego władcy jest punktowany według: grywalność, zgodność domu dynastycznego, płeć męska, śmierć, liczba wspomnień.

## 2026-07-02 — Wspomnienia w `character_memory_manager`

Wspomnienia w testowym save'ie znajdują się pod `character_memory_manager`, nie pod `memory_manager`. Od wersji v0.4.2 Archiwista obsługuje ten blok oraz odczytuje `creation_date` jako datę wspomnienia.

## 2026-07-02 — Chronicle Subject zamiast Previous Ruler

Zdecydowano, że Archiwista nie będzie domyślnie śledził poprzednich posiadaczy tytułów państwowych. Kronika opisuje jedną linię narracyjną rodu: kolejne grywalne postacie wywodzące się od pierwszego bohatera kroniki.

Domyślny raport ma więc dotyczyć poprzedniego zmarłego, grywalnego przodka aktualnej postaci, niezależnie od płci. Historia państw i tytułów pozostaje potencjalnym dodatkiem, ale nie decyduje o wyborze bohatera księgi.
