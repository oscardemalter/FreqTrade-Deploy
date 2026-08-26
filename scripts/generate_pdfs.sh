#!/usr/bin/env bash
set -euo pipefail

# scripts/generate_pdfs.sh
# Convertit les fichiers Markdown importants en PDF à l'aide de pandoc + wkhtmltopdf (ou texlive)
# Usage: sudo bash scripts/generate_pdfs.sh

OUTDIR="docs/pdf"
mkdir -p "$OUTDIR"

# Installer pandoc et wkhtmltopdf si nécessaire
if ! command -v pandoc >/dev/null 2>&1; then
  echo "Installation de pandoc..."
  apt update
  apt install -y pandoc
fi

if ! command -v wkhtmltopdf >/dev/null 2>&1; then
  echo "Installation de wkhtmltopdf... (peut être lourd)"
  apt install -y wkhtmltopdf || echo "wkhtmltopdf non disponible via apt, pandoc peut nécessiter texlive pour générer des PDFs." >&2
fi

# Convertir les fichiers
if [ -f "docs/Guide_Freqtrade_VPS.md" ]; then
  echo "Conversion Guide_Freqtrade_VPS.md -> $OUTDIR/Guide_Freqtrade_VPS.pdf"
  pandoc docs/Guide_Freqtrade_VPS.md -o "$OUTDIR/Guide_Freqtrade_VPS.pdf" --pdf-engine=wkhtmltopdf || pandoc docs/Guide_Freqtrade_VPS.md -o "$OUTDIR/Guide_Freqtrade_VPS.pdf"
fi

if [ -f "docs/OKX_Testnet_Keys.md" ]; then
  echo "Conversion OKX_Testnet_Keys.md -> $OUTDIR/OKX_Testnet_Keys.pdf"
  pandoc docs/OKX_Testnet_Keys.md -o "$OUTDIR/OKX_Testnet_Keys.pdf" --pdf-engine=wkhtmltopdf || pandoc docs/OKX_Testnet_Keys.md -o "$OUTDIR/OKX_Testnet_Keys.pdf"
fi

echo "PDFs générés dans $OUTDIR (si pandoc a réussi)."