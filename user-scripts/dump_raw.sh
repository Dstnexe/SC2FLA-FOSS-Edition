#!/bin/bash
# dump_raw.sh - Dumpt RAW-Ressourcen aus .sc Dateien
# macOS/Linux-Alternative zu dump raw.bat

# Zum Projektverzeichnis wechseln
cd "$(dirname "$0")/.." || exit 1

# Prüfen ob Python verfügbar ist
if ! command -v python3 &amp;> /dev/null; then
    echo "❌ Python3 nicht gefunden. Bitte installieren."
    exit 1
fi

echo "🔄 Starte SC2FLA RAW Dump..."
echo ""

# main.py mit --dump-raw und --process ausführen
python3 main.py --dump-raw --process "\$assets"

echo ""
echo "✅ Fertig!"
read -p "Drücke Enter zum Beenden..."
