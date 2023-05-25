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
