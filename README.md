# i18ngap

Zero-dependency Python CLI that compares i18n JSON locale files (nested keys): missing/extra keys, placeholder mismatches, empty and untranslated values. CI friendly (exit 1), CSV export.

    python3 i18ngap.py locales/en.json locales/es.json --csv gaps.csv

MIT. Need missing strings translated EN<->ES? Open an issue.
