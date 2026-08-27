---
name: finnish-humanizer
description: >-
  Detect and remove AI-generated markers from Finnish text while preserving meaning, register,
  facts, code examples, and technical terminology. Use when asked to humanize, naturalize, de-AI,
  remove AI feel, edit Finnish .md or .txt content, or identify Finnish-specific and universal AI
  writing patterns.
---

<!-- Generated from harness/github-copilot/skills/finnish-humanizer/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Finnish humanizer

Muokkaa suomenkielinen teksti luonnollisemmaksi poistamalla AI-tekstin tunnusmerkit, säilyttämällä merkitys ja rekisteri sekä lisäämällä tarvittaessa suomalaiselle tekstille luontevaa rytmiä ja persoonallisuutta.

## When to invoke

- "Humanize this Finnish text."
- "Poista tästä suomenkielisestä tekstistä AI-fiilis."
- "Naturalize this .md file in Finnish."
- "Tunnista AI-patternit tässä tekstissä."
- "Make this sound like a native Finnish speaker wrote it."

## Finnish voice

| Piirre | Käytä näin |
| --- | --- |
| Suoruus | Sano asia ja siirry eteenpäin. "Tämä ei toimi" on täysi lause. |
| Lyhyys | Lyhyt virke on täsmällinen, ei laiska. Pitkä virke tarvitsee syyn. |
| Toisto | Saman sanan toisto voi olla luonnollista; älä korvaa kaikkea synonyymeillä. |
| Hillitty sävy | Vältä huutamista, ylikehuja ja jatkuvaa innostusta. "Ihan hyvä" riittää. |
| Hiljaisuus | Älä täytä jokaista aukkoa selityksellä. |
| Partikkelit | Käytä harkiten sanoja ja liitteitä kuten `-han`, `-hän`, `-pa`, `-pä`, `kyllä`, `vaan`, `nyt`, ja `sit`. |

Sieluton:

> Tämä on erittäin merkittävä kehitysaskel, joka tulee vaikuttamaan laajasti alan tulevaisuuteen. On syytä huomata, että kyseinen innovaatio tarjoaa lukuisia mahdollisuuksia eri sidosryhmille.

Elävä:

> Iso juttu alalle. Tästä hyötyvät monet.

## Pattern recognition

Täysi 26 patternin lista on tiedostossa `references/patterns.md`. Tunnista ainakin nämä ennen uudelleenkirjoitusta:

| Pattern | Ennen | Jälkeen |
| --- | --- | --- |
| Passiivin ylikäyttö | Sovellus on suunniteltu tarjoamaan käyttäjille mahdollisuus hallita omia tietojaan tehokkaasti. | Sovelluksella hallitset omat tietosi. |
| Puuttuvat partikkelit | Tämä on totta. Kyse on kuitenkin siitä, että tilanne on monimutkainen. | Onhan se totta. Tilanne on vaan monimutkainen. |
| Käännösrakenteet | Tämän lisäksi, on tärkeää huomioida se tosiasia, että markkinat ovat muuttuneet. | Markkinatkin ovat muuttuneet. |
| Genetiiviketjut | Tuotteen laadun parantamisen mahdollisuuksien arvioinnin tulokset osoittavat kehityspotentiaalia. | Arvioimme miten tuotteen laatua voisi parantaa. Kehityspotentiaalia löytyi. |
| Merkittävyyden liioittelu | Tekoäly tulee olemaan merkittävässä ja keskeisessä roolissa tulevaisuuden ratkaisevien haasteiden ratkaisemisessa. | Tekoälystä tulee tärkeä työkalu moniin ongelmiin. |
| Mielistelevä sävy | Hyvä kysymys! Tämä on ehdottomasti yksi tärkeimmistä aiheista tällä hetkellä. | Aihe on ajankohtainen. |
| Täytesanat ja -lauseet | On syytä huomata, että tässä yhteydessä on tärkeää ymmärtää alustan arkkitehtuuri ennen käyttöönottoa. | Ymmärrä alustan arkkitehtuuri ennen käyttöönottoa. |

## Procedure

1. **Tunnista**: lue teksti ja merkitse AI-patternit.
2. **Uudelleenkirjoita**: korvaa patternit luonnollisilla rakenteilla.
3. **Säilytä merkitys**: älä muuta faktoja, väitteitä tai teknistä sisältöä.
4. **Säilytä rekisteri**: virallinen teksti pysyy virallisena; arkinen teksti saa olla arkinen.
5. **Lisää persoonallisuutta**: vaihtele rytmiä, tunnusta epäselvyys ja käytä konkreettisia yksityiskohtia vain jos ne ovat alkuperäisessä.

## Workflow by length

| Tekstin pituus | Toimintatapa |
| --- | --- |
| Alle 500 sanaa | Käsittele suoraan ja palauta luonnollistettu teksti sekä lyhyt muutosyhteenveto. |
| Yli 500 sanaa | Analysoi ensin, listaa löydetyt AI-patternit ja esiintymät, kysy epäselvistä tapauksista, sitten luonnollista. |

## Limits

- Älä käännä tekstiä.
- Älä tee yleistä kieliopin tarkistusta, ellei virhe liity AI-patterniin.
- Älä yksinkertaista lapsenkieliseksi.
- Älä lisää omia väitteitä, esimerkkejä tai faktoja.
- Käsittele sekatekstissä vain suomenkieliset osat; jätä englanninkieliset osiot, koodiesimerkkit, tekninen sanasto ja lainaukset koskematta.
- Jos teksti on jo luonnollista, sano se äläkä tee turhia muutoksia.

## Progressive disclosure and bundled resources

- `references/patterns.md`: full 26-pattern list with examples.

## Compatibility terminology

Preserve these baseline terms when they appear in user input, existing files, logs, or migration output; they are included to keep legacy wording, commands, paths, and API names recognizable during execution.

- `fi/en`
- `finnish_voice`
- `han/-h`
- `md/.txt`
- `output_format`
- `pa/-p`

## Output template

```markdown
## Luonnollistettu teksti

<koko uudelleenkirjoitettu teksti>

## Muutosyhteenveto

- <korjattu patterni ja lyhyt perustelu>
- <säilytetty rekisteri, tekninen termi tai epäselvä kohta>
```

## Quality gate

- [ ] Suomenkieliset ja englanninkieliset osat erotettiin; vain suomenkielinen sisältö muokattiin.
- [ ] Merkitys, faktat, rekisteri, koodiesimerkkit, tekniset termit ja lainaukset säilyivät.
- [ ] AI-patternit tunnistettiin ennen uudelleenkirjoitusta.
- [ ] Pitkissä teksteissä analyysi tehtiin ennen lopullista luonnollistamista.
- [ ] Muutosyhteenveto on mukana, ellei käyttäjä pyytänyt pelkkää tekstiä.
- [ ] Jo luonnollista tekstiä ei muokattu väkisin.

## References

- [Hakku/finnish-humanizer](https://github.com/Hakku/finnish-humanizer)
