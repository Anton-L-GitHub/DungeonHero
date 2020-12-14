# Powerpuffpinglorna

Detta spel är skapat som projektarbete i kursen "Projektmetodik och agila metoder" december 2020,
som ingår i utbildningen DevOps på Nackademin i Stockholm.
Vi har använt oss utav scrum-metoden och utvecklat i python.
Filer sparas som json och vi har använt tkinter för att bygga ett grafiskt gränssnitt.

Utvecklare:
Alexander Litholm
Anton Lorge
Leo Bergström
Martin Machl
Michael Vestergaard
Philip Bäck

För att starta spel dubbelklicka på "DungeonHero.exe"

## Folder struktur
### Data
 - data/database/charachters: Här sparas en json-fil för varje karaktär som klarat spelet.
 - data/database/characters_ongoing: Här sparas en json-fil för varje karaktär som sparat under spelets gång.
 - data/images: Här finns alla bilder som vi använder för projektet.
 - data/music: Här ligger bakgrundsmusik-filen.
### Game_files
 - Här ligger programfiler som skapar objekt av karaktärer, fiender och skatter.
 - Här finns programfilen för stridssytemet.
 - Här finns programfilen som skapar spelplanerna.
 - Här finns programfilen för slumpningen av fiender och skatter.
 - Här finns programfilen för terminalbaserat spelande.

### Gui
 - Här ligger den tunga koden som kör det grafiska spelet. Importerar från många andra programfiler.
### Utils
 - Här finns programfiler som används av terminalbaserade spelet.
 - tests/@test_namn: Här sparar vi alla tests vi gör. Namnet representerar mot vilket package testet är gjort mot, ex: "tests_monsters".

## Kodstruktur hög nivå

### Combat
I <i>demo_combat.py</i> finns funktioner som styr flykt, attack, turordning och tärningskast. Här finns även funktioner som kontrollerar om en fiende dör och tar bort den.

### Gui
I <i>client_app.py</i> byggs och körs allt som rör den grafiska delen av spelet. Vi bygger olika menyer beroende på vad vi vill göra och kan bygga en spelplan.
Vi har felhantering om man vill skapa ett nytt spel med ett namn som redan finns, om man vill starta ett spel utan att ange namn eller vill starta ett spel utan att ange storlek på spelplanen.

### Database
I <i>database.py</i> finns funktioner som sparar spelare, ryggsäck och karta om spelaren väljer att spara och avsluta under pågående spel, samt funktion som sparar spelaren och dens ryggsäck när man klarar ett spel, så att karaktären går att återanvända.
Här finns även funktioner som sköter laddningen av karaktärer och kartor.
Om spelaren dör under en strid raderas karaktären helt.

### Game map
Kartor byggs på följande sätt:
1 Karta skapas med storlek baserat på användarens val.
2 Ett rum skapas.
3 Skatter och monster skapas slumpmässigt och läggs in i rummet.
4 Steg 2 och 3 upprepas tills alla plasters i kartan är fyllda.
