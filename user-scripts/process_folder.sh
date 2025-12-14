#!/bin/bash
# process_folder.sh - Verarbeitet alle .sc Dateien im $assets Ordner
# macOS/Linux-Alternative zu process folder.bat

# Zum Projektverzeichnis wechseln
cd "$(dirname "$0")/.." || exit 1

# Prüfen ob Python verfügbar ist
if ! command -v python3 &amp;> /dev/null; then
    echo "❌ Python3 nicht gefunden. Bitte installieren."
    exit 1
fi

echo "🔄 Starte SC2FLA Verarbeitung..."
echo ""

# main.py mit --process auf $assets ausführen
python3 main.py --process "\$assets"

echo ""
echo "✅ Fertig!"
read -p "Drücke Enter zum Beenden..."
