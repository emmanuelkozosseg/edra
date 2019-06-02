# Technikai részletek
Az énekeket egy **Emmet.yaml** nevű egyedi formátumban tároljuk.

A formátum hasonlít az elterjedt OpenLyrics formátumhoz, de XML helyett YAML-t használ és jobban kielégíti a mi igényeinket. Felépítése miatt a többi formátumba viszonylag egyszerűen átkonvertálható.

# Fordítási infrastruktúra
A fordítást az ebben a könyvtárban található `build.sh` script végzi:

* Konvertálja az énekeket OpenSong formátumba, és visszatölti a repó letöltései közé `opensong.zip` néven.
    * Ez használható énekek vetítésére OpenSonggal.
* Összeömleszti az összes éneket, minifikált JSON formátumba konvertálja, és visszatölti a repó letöltései közé `songs.json` néven.
    * Ezt az Emmet használja.

A fordítás egy Bitbucket pipeline-on keresztül történik. A beállításokért lásd: [../bitbucket-pipelines.yml](../bitbucket-pipelines.yml)

# Énekfájlok
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

## Könyvinformáció (books)
Megadja, hogy az ének melyik énekeskönyvekben jelenik meg, milyen nyelven, és milyen szám alatt.

```yaml
books:
  - id: mybook  # A könyv azonosítója, léteznie kell a _books.yaml fájlban
    number: '23'  # Az ének sorszáma ebben a könyvben
    lang: en  # Ezen a nyelven szerepel az ének a könyvben; kell léteznie egy ilyen nyelvű dalszövegnek a 'lyrics' szekcióban
  - id: emm_hu
    number: E2
    lang: hu
  - id: emm_fr
    number: 01-02  # Nincs fordításhoz kötve, csak rögzíti, hogy az 'emm_fr' könyvben az ének száma '01-02'
```

## Hangfelvételek (records)
Felsorolja az énekhez elérhető hangfelvételeket.

```yaml
records:
  - url: http://emmanuel.hu/hangfajl/eleresi/utja.mp3  # Az MP3 hangfájl elérési útja
    lang: hu  # A felvétel nyelve; kell léteznie egy ilyen nyelvű dalszövegnek a 'lyrics' szekcióban
```

## Leíró adatok (about)
A szerzői adatokat tartalmazza.

```yaml
about:
  music: J. Smith
  lyrics: J. Doe
  year: 2019
```

## Dalszöveg (lyrics)
A fájl központi része, amely a dal szövegeit tartalmazza.

### Fordítások
A legfelső szinten az elérhető fordításokat sorolja fel. Ezek adatai:
* `lang`: ISO 639-1 szerinti nyelvkód
* `title`: a dal címe ebben a fordításban
* `adapted_by`: a fordító(k) neve(i), vesszővel elválasztva
* `verses`: a versszakok listája

```yaml
lyrics:
  - lang: hu
    title: Az én dalom
    adapted_by: Gipsz J., Kovács J.
    verses:
      - (...)
```

### Versszakok
A versszakokat a következő szerkezettel írjuk le:
* `name`: a versszak kódja, amely lehet:
  * `c`: refrén (szükség esetén számozható: `c1`, `c2`, stb.)
  * `v1`, `v2`, ...: versszak
  * `b`: átkötés (szükség esetén számozható: `b1`, `b2`, stb.)
* `label`: a versszak megnevezése (nem kötelező, ritkán használjuk)
* `lines`: a versszak sorainak listája

```yaml
    verses:
      - name: c
        lines:
          - Ez a dal refrénje
          - Kis C betű jelöli
      - name: v1
        lines:
          - Ez az első versszak
          - Ez is csak két sor
```

### Versszakok tördelése
A versszakok háromféle módon tördelhetők.
* A **sortörés** (függőleges vonal) egy "törési javaslatot" tesz: a sor logikailag összetartozik, de ha muszáj, akkor itt lehet eltörni.
  * Például az OpenSong konverter ezt normál sortörésként értelmezi, az Emmet figyelmen kívül hagyja.

```yaml
      - name: v2
        lines:
          - Ha egy sort csak a | vetítéskor kell darabolni,
          - mert oda túl hosszú, | de máshol így jobb,
          - akkor a függőleges vonal | karakterrel lehet ezt elérni
```

* A **"puha" törés** (sor egy üres karakterlánccal) csak egy üres sort iktat be.

```yaml
      - name: v3
        lines:
          - A versszak közepén
          - egy puha törés.
          - ""
          - Egy sortörést iktat be,
          - de egy dián marad az egész.
```

* A **"kemény" törés** (teljesen üres sor) külön diára helyezi a darabokat.
  * Lehet, hogy egy alkalmazásban a "dia" fogalma nem létezik; az Emmet például a kemény törést ugyanúgy értelmezi, mint a puhát, és egy üres sort iktat be a helyén.

```yaml
      - name: v4
        lines:
          - Itt a következő versszak,
          - szét van darabolva.
          -
          - Két részre osztották,
          - ami két külön dián fog megjelenni.
```

### Sorcsoportok
Egy versszak sorait csoportokba lehet rendezni. Jelenleg egyfajta csoport létezik, az ismétlés.

#### Ismétlés
Ha néhány sort ismételni kell, akkor azokat a versszakon belül egy ismétlésbe lehet csoportosítani.

Az ismétlési csoportot a következő szerkezettel írjuk le:
* `group`: mindig `repeat`; jelzi, hogy ez egy ismétlési csoport
* `times`: szám; ennyi alkalommal kell ismételni
* `lines`: az ismétlendő sorok listája

A csoportok és a "normál" sorok keverhetők.

```yaml
      - name: v5
        lines:
          - group: repeat
            times: 2
            lines:
              - Ezeket a sorokat
              - kétszer ismételjük.
          - Közbülső sorok, amiket
          - nem ismétlünk.
          - group: repeat
            times: 4
            lines:
              - Ezeket pedig
              - négyszer énekeljük.
```

## Gitárakkordok (chords)
A dal gitárakkordjait tartalmazza.

Mivel gyakran több versszak is ugyanazokat az akkordokat használja, ezért egy versszaknyi akkordot "sablonnak" nevez, amit a neve alapján egy vagy több versszakra tud alkalmazni.
* `all`: minden versszakra érvényes
* `c`, `v`, `b`: minden refrénre/egyszerű versszakra/átkötésre érvényes
* `v2`: csak az adott versszakra érvényes

Ha egy versszakra több sablon is illeszkedik, akkor a legszűkebb lesz érvényes.

```yaml
chords:
  - template: c
    chords:
      - ['G', 'C', 'Am', 'Dm']
      - ['G', 'C', 'Am', 'Dm']
  - template: v
    chords:
      - ['G', 'Em']
      - ['A', 'Fism']
  - template: v2
    chords:
      - ['C', 'D', 'E']
      - ['D', 'E', 'F']
      - ['E', 'F', 'G']
      - ['F', 'G', 'A']
```

### Ismétlések
Ha a dalszöveg egy ismétlési csoportot tartalmaz, akkor azt az akkordokhoz is fel kell venni, a csoport típusa pedig ugyanúgy `repeat` lesz. Azonban felmerül két eset: lehet, hogy mindegyik ismétlésnek ugyanazok az akkordjai, de lehet, hogy mindegyiknek más.

* Az egyszerűbb eset, ha minden ismétlésnek ugyanazok az akkordjai. Ilyenkor a `uniform` típust kell megadni, és a `chords` listában egyszerűen felsorolni az akkordokat.

```yaml
(...)
      - name: c
        lines:
          - group: repeat
            times: 2
            lines:
              - Ezeket a sorokat
              - kétszer ismételjük.
(...)
chords:
  - template: c
    chords:
      - group: repeat
        type: uniform
        chords:
          - ['D', 'A']
          - ['hm', 'D']
```

* Bonyolultabb, ha minden ismétléskor mások az akkordok. Ilyenkor a `unique` típust kell használni, és minden egyes ismétlésre megadni az akkordokat.

```yaml
chords:
  - template: c
    chords:
      - group: repeat
        type: unique
        chords:
          - - ['D', 'A']  # 1. ismétlés
            - ['hm', 'D']
          - - ['G', 'D']  # 2. ismétlés
            - ['em', 'G']
```

### Horgonyok
A gitárakkordokat horgonyokkal lehet a dalszövegben bizonyos helyekre rögzíteni.

```yaml
(...)
      - name: c
        lines:
          - ^Ez a ^dal ref^rén^je
          - ^Kis C ^betű ^jelö^li
(...)
chords:
  - template: c
    chords:
      - ['G', 'C', 'Am', 'Dm']
      - ['G', 'C', 'Am', 'Dm']
```

A fenti horgonyok a következőképpen rögzítik az akkordokat:

```
G    C      Am Dm
Ez a dal refrénje
G     C    Am  Dm
Kis C betű jelöli
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