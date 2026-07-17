#!/bin/bash -e
mkdir -p .pdf-security
mkdir -p .pdf-forensics
cp *.pdf .pdf-forensics/ 2>/dev/null || true
ulimit -v 2097152
ulimit -f 2097152
for pdf in *.pdf; do
  [ -e "$pdf" ] || continue
  clamscan --no-summary --infected "$pdf"
  if yara security/pdf_rules.yar "$pdf"; then
    echo "warning"
  fi
done
for pdf in *.pdf; do
  [ -e "$pdf" ] || continue
  name=$(basename "$pdf")
  timeout 120s qpdf --check "$pdf"
done
echo "done"
