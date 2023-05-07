# Hledání nejkratší cesty v bludišti

## Autor: Dominik Seidler
## Textový popis

Tento projekt se zabývá řešením (hledáním nejkratší cesty) a také
základním generováním bludišť. Základním vstupem bude bludiště
$n\times n$, přičemž vstup do bludiště bude vždy levý horní roh a výstup
bude vždy pravý dolní roh. Z jedné buňky do druhé se lze dostat pouze
přes společnou hranu (nikoliv přes roh). Cílem projektu je implementovat
algoritmy pro načítání, hledání nejkratší cesty a generování bludiště.

Na začátku bude implementována funkce pro načítání bludiště z CSV
souboru. Tato funkce bude umět načítat bludiště o libovolném rozměru
$n\times n$ a uložit ho do paměti v podobě NumPy matice s True/False
hodnotami (True = buňka je neprůchozí). Poté bude implementován
algoritmus pro hledání nejkratší cesty. Poslední částí bude vytvoření
generátoru bludiště za použití algoritmu pro hledání nejkratší cesty.

Výstup bude formou obrázku (černá = neprostupná část, bílá = průchozí,
červená = nejkratší cesta).

Jedná se o projekt do předmětu VVP

## Funcionality

-   Implementovat načítání bludiště z CSV souboru
-   Implementovat algoritmus pro hledání nejkratší cesty (mezi levým horním rohem a pravým dolním rohem) za použití knihovny NumPy,který bude pracovat v následujících dvou krocích:
    -   Sestavení incidenční matice
    -   Hledání nejkratší cesty pomocí Dijkstrova algoritmu
-   Zapsat bludiště a nalezenou cestu do černobílého obrázku, kde cesta bude vyznačena červeně
-   Vytvořit funkci pro generování bludiště tak, aby mělo řešení (tj. aby existovala cesta mezi levým horním a pravým dolním rohem)
    -   funkce začne s nějakou šablonou (předdefinované v kódu) a poté bude zaplňovat bludiště v náhodných místech a kontrolovat, zda je stále průchozí
    -   šablon bude více (např. empty = volné bludiště, slalom = bariéry
        aby cesta musela minimálně mít tvar S, \...) - budou s obrázky ukázané v Readme nebo examples.ipynb

## Knihovna se skládá:

- 	VVP_SEI0082.py vytváří PNG obrázky nejkratší cesty v daném bludišti, šablony bludiště jsou 4:
	-	'R' nebo 'random' pro náhodně vygenerované bludiště
	- 	'S' nebo 'slalom' pro bludiště, kde vytvoří cestu typu 'Z'
	-	'L' nebo 'ladder' (viz. data/ObrázekLadder.png)
	-	'E' nebo 'edges' pro bludiště, kde je trubka z levého-dolního rohu do pravého-horního rohu tak, aby cesta tím musela projít
-	examples.ipynb, který má v sobě zobrazené jednotlivé výsledky pro dané šablony a velikosti
-	složka "data" má v sobě obrázky šablony "Ladder", výstup větších bludišť a vstupní bludiště (To bylo potřeba převážně na startu)
-	readme.md soubor, který obsahuje stručný popis projektu, jeho funkcionalit a z čeho se knihovna projektu skládá