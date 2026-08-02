# Lessons

## 2026-08-02 — Conteggi doc vs disco

**Pattern:** README/ARCHITECTURE dicevano 14 workflow, disco ne aveva 15 (e "Total Workflows 13"). Bug preesistente scoperto aggiungendo `/scroll-experience`.

**Why:** I numeri nei doc si degradano quando si aggiungono/rimuovono file senza aggiornarli.

**How to apply:** Mai fidarsi dei conteggi dichiarati nei doc. Verificare sempre con `ls <dir> | wc -l` prima di modificare conteggi in README/ARCHITECTURE. Soglie di verifica nei piani: stima generosa (es. `grep -c >= 10`) può fallire su contenuto valido — verificare contenuto reale, non soglia stimata.
