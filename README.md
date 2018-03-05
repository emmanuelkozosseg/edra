# Üdv!

Itt tároljuk az Emmánuel Közösség énekeit az OpenSong vetítőprogram formátumában.

## Hogyan telepítsem?

1. Töltsd le és telepítsd az OpenSongot [az opensong.org-ról](http://www.opensong.org/home/download).
2. Töltsd le [az Emmánueles alapcsomagot](https://bitbucket.org/eckerg/emmet-enekek/downloads/OpenSong.zip), amibe már beletettünk:
    * néhány képet, amit énekek között lehet vetíteni;
    * illetve pár alapbeállítást, pl. az előtér és háttér színét, a szöveg elrendezését, az animációkat, stb.
3. Töltsd le [az itteni énekeket egy csomagban](https://bitbucket.org/eckerg/emmet-enekek/get/HEAD.zip), és tedd be az alapcsomag _Songs_ mappájába az _Emmánuel_ mappát.
4. Indítsd el az OpenSongot, és add meg neki, hogy hova tetted a (most már teljes) alapcsomagot.

> **Tipp:** Az alapértelmezett Arialnél egy kicsit jobban olvasható a [Mentone betűtípus](https://bitbucket.org/eckerg/emmet-enekek/downloads/mentone-semibold.otf).
> Ha telepíted, akkor a _EM Fekete Mentone_ összeállításban fogod tudni használni.

## Hogyan használjam?

Az összes vetítőprogram arra van felkészítve, hogy az esemény előtt összeállítasz egy énekrendet, amit aztán (esetleg kicsi változtatásokkal) levetítesz az esemény közben. Az Emmánueles dicsőítéseken azonban ez nem így működik, általában közvetlenül a következő ének előtt derül ki, hogy melyik lesz az, ezért egy kicsit kreatívan kell használni az OpenSongot is.

### Előkészületek (dicsőítés előtt)

1. Állítsd át az asztalod háttérképét sima feketére. (Windows 10-ben: jobb gomb az asztalon, _Személyre szabás_, és a középső, _Háttér_ legördülő menüben válaszd ki az _Egyszínű_ lehetőséget, a színek között pedig válaszd ki a feketét, ha nem eleve az van kiválasztva.)
2. Kösd össze a projektort a géppel, és a _Windows+P_ billentyűkombinációval ellenőrizd, hogy a kép _Kiterjesztés_ módban legyen.
3. Nyisd ki az OpenSongot, és menj át _Összeállítás mód_ba, ha még nem vagy ott.
4. Baloldalt felül az _Összeállítások_ listájából válaszd ki az _EM Fekete.xml_ vagy _EM Fekete Mentone.xml_ összeállítást (utóbbit akkor, ha telepítetted a Mentone betűtípust, lásd fent).
5. Mivel nem tudunk semmit az énekekről, kattints a legfelső, _Aktuális összeállítás_ dobozban a _Vetítés_, majd a _Két képernyő_ gombokra.
    * Ha csak az _Egy képernyő_ és a _Két képernyő előnézettel_ opciók elérhetők, akkor ellenőrizd, hogy tényleg _Kiterjesztés_ módban van-e a kép.

### Működtetés (dicsőítés közben)

Amikor elindítod a vetítést, az OpenSong főablaka eltűnik, és a vetítési segédablak jelenik meg.

* Középen fent látod az énekek listáját. Egyelőre eléggé üres.
* Baloldalt alul látod az aktuális dia előnézetét. Egyelőre ez is üres, mert nincs mit vetíteni. Ha elrejted a képernyőt, itt akkor is látod a szöveget, csak áthúzva.
* Jobboldalt látod a lehetőségeidet. Ezekre nem kell rákattintani, egy-egy billentyűvel is kiválaszthatók (szögletes zárójelben).

A képernyőt a **K** billentyűvel sötétíted el (fekete mód), az Emmánueles logót pedig az **L**-lel teszed ki (logó mód), és az **N**-nel térsz vissza normál módba, ahol látszanak a dalszövegek. Az N-et nem feltétlenül kell használnod: ha pl. logó módban megnyomod még egyszer az L gombot (ami a logó módot aktiválná), akkor visszatérsz normál módba.

Éneket a **Q** gombbal tudsz hozzáadni. 

1. Ha megnyomod, előjön a _Dal keresése_ ablak, és a kurzor a _Gyorskeresés_ mezőben villog.
2. Felül, a _Mappa kiválasztása_ legördülő menüben ki tudod választani az énekeskönyvet, ha nem stimmel.
3. A _Gyorskeresés_ mezőbe írd be az ének sorszámát 3 számjegyre kiegészítve, pl. `003`. (E-s énekeknél az E utáni számot 2 jegyre kell kiegészíteni, pl. `E05`.)
    * (Tartsd észben, hogy a gyorskeresés az énekcímek **elejét** nézi a lenti listában. Például hiába tudod, hogy az _Örülj az Úrban, áldd az Ő nevét_ kezdetű éneket keresed, ha így keresel rá, nem fogja megtalálni, mert az ének címe: `024 Örülj az Úrban, áldd az Ő nevét.xml`. Ha teljes keresésre van szükséged, nyomd meg a Ctrl+F-et, de ez általában elég lassú.)
4. Ha megvan az ének, kattints a _Hozzáad_ gombra (néha a sima Enter is működik).

Ezután válts át normál módra, és szintén billentyűkkel tudsz váltani a versszakok között.

* A **fel/le nyilak** értelemszerűen az előző/következő versszakra ugranak.
* A **balra/jobbra nyilak** az előző/következő énekközbe ugranak. (Két ének közé az OpenSong mindig automatikusan berak egy üres diát.)
* Az **1, 2, 3, ...** gombokkal tudsz a megfelelő számú versszakra ugrani (V1, V2, V3, ...).
    * Néha egy versszak több darabra van szétszedve (V1, V12), ilyenkor a **fel/le nyilakat** használd.
* A **C** gomb a refrénre ugrik vissza (C = Chorus), a **B** pedig az átkötésre (B = Bridge).
* (Van még a **T**, ami a codára, és a **P**, ami az előrefrénre ugrik, de ezeket nem használjuk a dalszövegekben.)
* Az **Esc** gombbal lépsz ki az egész vetítésből.

### Tippek

* Érdemes _Két képernyő előnézettel_ vetítési módban játszani a programmal, amíg kitapasztalod, hogy hogyan működik.
* Amikor egy ének véget ér, az **L** billentyűvel kitesszük a logót, és rögtön elő is hozzuk a _Dal keresése_ ablakot a **Q** gombbal, hogy amint kiderül a következő ének, gyorsan be lehessen tölteni.

> **Figyelem:** vetítési módban nem lehet törölni éneket. Ha rossz éneket ütöttél be, simán csak hagyd ott.

## Hogyan segíthetek?

### Ha ismered a Git verziókezelőt

Ebben az esetben két opciód van -- bár ha ismered a Gitet, akkor ezt valószínűleg nem kell magyarázni. :)

* Kérj hozzáférést a repóhoz Ecker Gábortól (ecker pont gabor kukac gmail pont com), klónozd le a repót, változtasd meg az énekeket kézzel vagy az OpenSong Dal módjával, majd a változtatásaidat pushold vissza.
* Forkold le a repót, változtasd meg, amit szeretnél, pushold vissza a privát repódba, majd küldj egy pull requestet.

### Ha nem ismered a Gitet

Ebben az esetben küldj egy hibajegyet: kattints baloldalt az _Issues_ linkre, ott kattints a _New Issue_ gombra, majd kövesd az ottani utasításokat.

A változtatásaidat magad is elvégezheted a letöltött énekeken az OpenSong Dal módjával, de nem muszáj, szívesen megcsináljuk mi is. Ilyenkor a megváltoztatott fájlokat hozzá tudod csatolni a hibajegyhez.
