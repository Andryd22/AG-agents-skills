# Compatibilità con Antigravity

Verifica del 29 settembre 2026, CLI locale `agy 1.2.12`.

## Distribuzione supportata dal kit

L'installer copia agenti, skill, regole e script nella `.agents/` del progetto. Il percorso delle skill è documentato per app, CLI e IDE. I custom subagent sono documentati per app e CLI; dove gli strumenti nativi non sono disponibili, il kit applica direttamente le istruzioni dello specialista.

- [Skill e percorsi ufficiali](https://antigravity.google/docs/skills)
- [Custom subagent e strumenti](https://antigravity.google/docs/subagents)

Le liste di strumenti nel validatore sono un controllo statico, non una prova dell'effettiva disponibilità su ogni versione. La nota su `agy 1.2.7` nel validatore descrive l'origine di una limitazione osservata; non è una certificazione della 1.2.12.

## Comando di pianificazione

Antigravity ha un comando nativo `/plan`. Il kit usa `/kit-plan` per il piano in `docs/PLAN-{slug}.md`, eliminando la necessità di dipendere dalla precedenza tra skill e comando integrato. Non è stata simulata una sessione di modello per stabilire quella precedenza.

Gli aggiornamenti da manifest v2 possono eliminare la vecchia skill gestita se non modificata. Da manifest legacy senza hash, la vecchia `skills/plan/` resta e l'installer la elenca: va confrontata, salvata se personalizzata e rimossa esplicitamente dall'utente.

- [Comando nativo Plan](https://antigravity.google/docs/plan/)

## Plugin nativo: prova e limiti

In una directory temporanea è stato copiato il contenuto del kit, aggiungendo un `plugin.json` con nome e descrizione. `agy plugin validate <percorso>` ha restituito **exit 0**, riportando `skills: 33 processed` e `agents: 12 processed`. Il kit contiene 32 cartelle di skill e anche `skills/README.md`: il contatore del validatore non prova che siano state attivate 33 skill.

Questa prova conferma l'accettazione statica del bundle. Non sono stati eseguiti installazione globale, attivazione delle regole o task con modelli.

Prima di offrire il plugin come distribuzione supportata servono:

1. Percorsi risolti rispetto al bundle per skill, script, asset e riferimenti. Oggi molti testi e comandi puntano esplicitamente a `.agents/skills/` e `.agents/scripts/`, che non identificano un plugin installato altrove.
2. Una prova di caricamento delle regole e dei subagent in una sessione isolata. L'output di `plugin validate` non elenca una validazione delle regole.
3. Una strategia per evitare duplicazioni con una copia del kit già nel workspace.
4. Prove LaTeX e ML con il bundle installato, nella fase finale delle valutazioni.

La distribuzione per workspace resta quindi quella supportata. I plugin sono un percorso verificato nel formato, ancora da verificare nell'esecuzione.

- [Formato e gestione dei plugin](https://antigravity.google/docs/plugins)

## Profili e dipendenze

Tutte le skill restano installate: nessun profilo riduce l'accesso agli strumenti. I controlli si adattano ai file del progetto. Per LaTeX controllano la struttura quando trovano `main.tex`; la compilazione è affidata al workflow LaTeX esistente. Per ML eseguono la suite configurata, senza certificare automaticamente qualità del dataset, assenza di leakage o correttezza del protocollo sperimentale.

Un futuro comando `doctor` potrà diagnosticare TeX/PyMuPDF e ambiente ML. Non è necessario introdurre subito un sistema separato di profili. `scroll-world` resta invariata, inclusi i riferimenti alle sue dipendenze esterne.
