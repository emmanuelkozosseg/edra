# Technikai részletek
Az énekeket egy **Emmet.yaml** nevű egyedi formátumban tároljuk.

A formátum hasonlít az elterjedt OpenLyrics formátumhoz, de XML helyett YAML-t használ és jobban kielégíti a mi igényeinket. Felépítése miatt a többi formátumba viszonylag egyszerűen átkonvertálható.

## Fordítási infrastruktúra
A fordítást az ebben a könyvtárban található `build.sh` script végzi:

* Konvertálja az énekeket OpenSong formátumba, és visszatölti a repó letöltései közé `opensong.zip` néven.
    * Ez használható énekek vetítésére OpenSonggal.
* Összeömleszti az összes éneket, minifikált JSON formátumba konvertálja, és visszatölti a repó letöltései közé `songs.json` néven.
    * Ezt az Emmet használja.

A fordítás egy Bitbucket pipeline-on keresztül történik. A beállításokért lásd: [../bitbucket-pipelines.yml](../bitbucket-pipelines.yml)

## Emmet.yaml

### Énekek
Az énekeket a `songs` mappában tároljuk. Minden fájl éneket tartalmaz, aminek a neve nem alulvonással (_) kezdődik.

Az énekek számozásánál az Emmánueles énekeskönyv számait követjük, kivéve az imádságokat, amelyek **I** betűvel kezdődő számot kapnak.

A fájlnév a következő formátumú:
```
012-enek-cime.yaml
```
* Nem tartalmazhat ékezetes- és nagybetűt.
* Az ének számával kell kezdődnie.
    * Szám esetén 3 számjegyre egészítjük ki: 001, 012, 123
    * Ha betűvel kezdődik, akkor 2 számjegyre: E01, E12

Szerkezetük:

```yaml
books:
  - id: mybook  # Léteznie kell a _books.yaml fájlban
    number: '23'  # Az ének sorszáma ebben a könyvben
    lang: en  # Ezen a nyelven szerepel az ének a könyvben; kell léteznie egy ilyen nyelvű dalszövegnek lentebb
  - id: emmet
    number: E2
    lang: hu
lyrics:
  - lang: hu  # ISO 639-1 szerinti nyelvkód
    title: Az én dalom
    verses:
      - name: c
        lines:
          - Ez a dal refrénje
          - Kis c betű jelöli
      - name: v1
        lines:
          - Ez az első versszak
          - Ez is csak két sor
      - name: v2
        lines:
          - Itt a második versszak
          - Szét van darabolva
          -
          - Két részre
          - Ami két külön dián fog megjelenni
      - name: v3
        lines:
          - A harmadik versszak érdekesebb
          - Van a közepén egy üres sor
          - ""
          - Ami egy sortörést iktat be
          - De egy dián marad az egész
      - name: b
        label: Átkötés  # Ha szükséges, címke adható a versszaknak; az Emmetben ez a versszak tetején jelenik meg
        lines:
          - Az átkötést a kis b betű jelzi
  - lang: en
    title: My Song
    verses:
      - name: c
        lines:
          - This is the chorus
          - But it's in English now
      - name: v1
        lines:
          - It doesn't have to look the same
          - As the other languages
          - It may have more or fewer verses
```

### Könyvek
A könyvek adatait a `songs/` könyvtár `_books.yaml` fájljában tároljuk.

Szerkezete:

```yaml
- id: mybook  # Ezzel az azonosítóval lehet hivatkozni a könyvre az énekeknél
  name: Az én énekeskönyvem  # A könyv teljes címe
  selectable: n  # Ha igen (y), akkor kiválasztható az énekeskönyvek listájában. Egyébként csak az énekek adatlapján jelenik meg.

- id: emmet
  name: Emmet
  selectable: y
```