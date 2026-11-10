# i18ngap

Zero-dependency Python CLI that checks i18n JSON locale files in CI: missing keys, extra keys, placeholder mismatches ({name}, {{name}}, %s, %d, ${x}), empty values and untranslated values. Exit code 1 when problems are found. Optional CSV export.

    python3 i18ngap.py locales/en.json locales/es.json --csv gaps.csv

MIT licensed.
