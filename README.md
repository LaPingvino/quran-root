# quran-root — Multilingual Root-Recovery Translations of the Qur'an

This project provides translations of the Qur'an that recover meanings hidden in the Arabic roots — in multiple languages. Each translation follows the same root-recovery method but uses natural, appropriate language for its target audience.

## Languages

| Language | Directory | Status |
|----------|-----------|--------|
| English | `en/` | Complete (114 surahs, 114 commentaries, roots guide) |
| Nederlands (Dutch) | `nl/` | In progress |
| Portugues (Portuguese) | `pt/` | In progress |
| Esperanto | `eo/` | In progress |
| Arabic (reference) | `ar/` | Complete (114 surahs, source text) |

## The Method

Every key term is translated by its Arabic root meaning rather than its received interpretation:

| Arabic root | Conventional | Root-recovery |
|-------------|-------------|---------------|
| k-f-r (conceal) | disbeliever, infidel | those who conceal |
| s-l-m (devote/submit/be whole) | Muslim / Islam | the Devoted / Devotion |
| h-w-r (return) | houris, fair maidens | the Returners (= Jesus's disciples) |
| q-r-' (recite) | the Quran | the Recitation |
| j-n-n (conceal) | jinn, paradise | spectres, hidden Realm |

See `en/roots.md` for the full catalogue of 22+ root discoveries.

## Structure

Each language directory contains:
- `XXX.md` — translation of each surah (001-114)
- `roots.md` — root discoveries guide in that language
- `README.md` — language-specific introduction
- `comments/` — scholarly annotations (where available)

The `ar/` directory contains Arabic reference texts (`XXX-ar.md`) shared across all languages.

## Contributing

Fork and send pull requests. Each language needs native speakers who understand the root-recovery approach. Read `en/roots.md` first, then the target language's README.

## Origin

The English translation began with two seed surahs (55 and 77) translated by hand by Joop Kiefte, then expanded through collaborative root analysis into a complete translation. See `en/README.md` for the full story.
