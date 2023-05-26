TODO dokončenie tejto časti dokumentácie

# Chord generator

Program obsahuje dve triedy: Chord a Program.
Trieda Chord zodpovedá za generovanie akordu zo zadaných údajov.
Trieda Program má na starosti grafické rozhranie pre ovládanie
objektov triedy Chord, históriu generovaných akordov
a informácie o programe.

## Trieda Chord

Táto trieda implementuje metódy pre preklad tónov strún, názvu akordu
a ďalších voliteľných parametrov do postupnosti sekvencií čísel
(respektíve hodnôt None), ktoré obsahujú čísla pražcov, ktoré majú
byť zahrané.

Prvým krokom je preloženie názvov strún a základného tónu akordu
do internej číslovacej schémy (každý poltón má číslo 0 -- 11),
nasleduje preloženie názvu akordu do množiny poltónov, ktoré
majú byť zahrané. Toto prebieha už pri vytvorení objektu typu Chord.

Metóda .generate() pre daný akord vygeneruje všetky valídne možnosti.
Robí to tak, že skúša postupne pre všetky struny všetky valídne tóny,
a pokiaľ počet stlačených tónov presiahne zadaný maximálny počet prstov
(alebo nie je možné ich zahrať barovým akordom,
ak je nastavený ako hrateľný), prípadne maximálna vzdialenosť stlačených
tónov presiahne zadaný limit, daná vetva prehľadávania sa utne.

Každá vygenerovaná možnosť sa ohodnotí heuristikou, ktorá berie ohľad
na hrateľnosť a znenie akordu, napríklad výrazne znižuje skóre možnostiam,
ktoré obsahujú veľa nezahratých strún, prípadne rovno vyhadzuje tie,
ktoré majú nehrané struny medzi hranými (hoci aj takéto akordy môžu byť
valídne, pre potreby hrania akordov ľuďmi používajúcimi tento nástroj
by skôr zavadzali). Takisto lepšie hodnotí jednoduchšie akordy,
teda také, kde treba použiť menej prstov, prípadne také,
ktoré sa hrajú bližšie ku koncu hmatníka, a ďalšie parametre.
Heuristika je veľmi subjektívna a optimalizovaná tak, aby štandardné
gitarové akordy dosiahli najlepšie hodnotenie.

Na základe výstupu z heuristickej funkcie sa vyberú akordy s hodnotou
prekračujúvcou hranicu, ktoré sa zoradia a uložia ako výstup,
spolu so svojim skóre. V prípade nenájdenia akordov s dostatočným skóre
sa vyberú akordy prekračujúce aspoň druhú stanovenú hranicu,
čo by mali byť všetky aspoň trochu rozumne zahrateľné akordy.
Ak ani takéto neexistujú, výstupom je prázdny zoznam.

Výstup poskytuje metóda .get(), ktorá mimo iné spustí .generate(),
ak sa tak ešte nestalo, a vráti zoznam možností v poradí podľa skóre,
od najleopšieho po najhorší, ale bez samotného skóre (keďže to je
dôležité len interne a neposkytuje žiadnu hodnotu použiteľnú mimo
heuristiky).

## Trieda Program

Táto trieda implementuje grafické rozhranie prostredníctvom knižnice
tkinter, teda okienkovú aplikáciu, ktorá s ovláda klávesnicou a myšou.
Jej veľkosť je možné najstaviť na niektorú z možností.

Sprostredkováva získavanie vstupu od uživateľa a výtvaranie
zodpovedajúcich objektov Chord, ktoré zároveň nechá vygenerovať
a získa z nich všetky valídne možnosti, ktoré potom zobrazí.
Medzi jednotlivými možnosťami je možné sa presúvať, takisto je možné
vrátiť sa k predtým vygenerovaným akordom cez históriu,
ktorú tiež uchováva objekt tejto triedy.

Umožňuje tiež zobraziť informácie o programe a návod na použitie.
