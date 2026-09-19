# Analisi dei compromessi e ADR

> Documenta ogni decisione di architettura con i suoi compromessi.

## Metodo di decisione

Per OGNI componente dell'architettura, documenta:

```markdown
## Architecture Decision Record

### Contesto
- **Problema**: [quale problema stiamo risolvendo?]
- **Vincoli**: [dimensione del team, scala, tempi, budget]

### Opzioni considerate

| Opzione | Pro | Contro | Complessità | Quando va bene |
|---------|-----|--------|-------------|----------------|
| Opzione A | Vantaggio 1 | Costo 1 | Bassa | [condizioni] |
| Opzione B | Vantaggio 2 | Costo 2 | Alta | [condizioni] |

### Decisione
**Scelta**: [Opzione B]

### Motivazione
1. [Motivo 1 - legato ai vincoli]
2. [Motivo 2 - legato ai requisiti]

### Compromessi accettati
- [A cosa rinunciamo]
- [Perché va bene così]

### Conseguenze
- **Positive**: [vantaggi che otteniamo]
- **Negative**: [costi e rischi che accettiamo]
- **Mitigazione**: [come gestiamo i negativi]

### Quando riconsiderarla
- [Quando rivedere questa decisione]
```

## Modello di ADR

```markdown
# ADR-[XXX]: [titolo della decisione]

## Stato
Proposta | Accettata | Deprecata | Sostituita da [ADR-YYY]

## Contesto
[Quale problema? Quali vincoli?]

## Decisione
[Cosa abbiamo scelto, con precisione]

## Motivazione
[Perché, legato a requisiti e vincoli]

## Compromessi
[A cosa rinunciamo, con onestà]

## Conseguenze
- **Positive**: [vantaggi]
- **Negative**: [costi]
- **Mitigazione**: [come gestirle]
```

## Dove salvare gli ADR

```text
docs/
└── architecture/
    ├── adr-001-use-nextjs.md
    ├── adr-002-postgresql-over-mongodb.md
    └── adr-003-adopt-repository-pattern.md
```
