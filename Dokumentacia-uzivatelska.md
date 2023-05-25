# Chord generator

Program je napísaný v jazyku Python prostredníctvom knižnice tkinter,
na jeho spustenie je potrebné mať tieto komponenty nainštalované.
Spúšťa sa priamo spustením kódu v Pythone.

## Použitie

Program slúži na generovanie a vizualizáciu akordov pre ľubovoľnú konfiguráciu strún
počtu od 1 do 12 vrátane. Počet strún sa automaticky určí z ich zápisu.
Na posuvníkoch je možné nastaviť si schopnosti, ako počet použiteľných prstov (1 - 5),
maximálnu dosiahnuteľnú vzdialenosť prstov (1 - 5 pražcov).
Tiež je možné zvoliť si schopnosť hrať barové akordy,
či zvoliť si preferovanú notáciu (použitie tónu H alebo B) cez zaklikávacie políčka.

Program pre každý akord vygeneruje všetky možnosti, ktoré sú ohodnotené ako použiteľné,
v poradí od najlepšej po najhoršiu, prípadne oznámi, že možnosť spĺňajúcu obmedzenia
nenašiel.

## Ovládanie

Program je spustený vždy na vrchu nad ostatnými oknami (pokiaľ nie je schovaný do lišty)
a je možné cyklicky meniť veľkosť okna podľa preferencie používateľa (Alt + R).

Generovanie akordov sa spúšťa pomocou Alt + G alebo stlačením Enter s kurzorom
v políčku s názvom akordu.
Stlačenie Enter s kurzorom v políčku so strunami presunie kurzor do políčka s akordom.

K predtým vygenerovaným akorodom sa dá dostať pomocou histórie, v ktorej je možné
pohybovať sa oboma smermi až po prvý a posledný generovaný akord, pričom nový
akord sa vždy zaradí na koniec histórie.
Pohyb do minulosti funguje pomocou Alt + P, do budúcnosti pomocou Alt + N

Predtým vygenerované akordy sú zapamätané až do skončenia aplikácie,
čo sa dá vyriešiť pomocou vymazania histórie klávesovou skratkou Alt + C.

Všetky klávesové skratky spúšťajú príkazy vo vrchnom menu programu, preto sa dajú
okrem klávesy Alt a podčiarknutého písmena spustiť aj myšou.

Zaklikávacie políčka a posuvníky je nutné ovládať mišou
(prípadne zvážiť alternatívne použitie).

## Podporovaná notácia akordov

Program rozpoznáva tóny C, D, E, F, G, A, H (respektíve B),
ktoré sa dajú posúvať jedným # alebo b (B). Pri notácií
zahŕňajúcej B ako tón sa primárne prekladá takto, teda
struny je nutné zadávať vo formáte s #.

Program akceptuje nasledujúce derivácie akordov:

- MI -- minor (bez použitia bude akord major) - znížený tretí tón o poltón
- AUG -- zvýšený piaty tón o poltón
- DIM -- znížený tretí a piaty tón o poltón
- SUS2 / SUS4 -- tretí tón nahradený druhým / štvrtým
- ADD2 / ADD(4/6/9/11/13) -- pridaný tón s daným číslom (modulo 12)
- 7 / MAJ7 -- pridaný siedmy / zvýšený siedmy tón

## Alternatívne použitie

Je možné zo súboru importovať triedu Chord, ktorá zodpovedá vytvoreniu akordu s parametrami,
ktoré sú v programe nastavované cez grafické rozhranie, bez použitia tohoto rozhrania.
V tom prípade sa parametre akordu nastavujú pri vytvorení jeho inštancie
(pozri metódu __init\__ a jej argumenty), metóda .generate() vygeneruje akordy
a metóda .get() ich vráti ako pole polí, každé s dĺžkou počtu strún,
kde čísla označujú stlačený pražec, 0 znamená nestlačený pražec a None znamená
nezahranú strunu (táto metóda tiež spúšťa .generate(), ak ešte nebol akord vygenerovaný).

V takomto prípade je nutné si akordy pamätať, aby bolo možné pristupovať k histórií,
keďže tá je implementovaná v triede Program.
