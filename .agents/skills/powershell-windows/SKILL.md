---
name: powershell-windows
description: Schemi di PowerShell su Windows. Trappole critiche, sintassi degli operatori, gestione degli errori, codifica dei file con lettere accentate.
---

# Schemi di PowerShell su Windows

> Schemi e trappole critiche di Windows PowerShell.

---

## 1. Sintassi degli operatori

### CRITICO: servono le parentesi

| ❌ Sbagliato | ✅ Giusto |
| --- | --- |
| `if (Test-Path "a" -or Test-Path "b")` | `if ((Test-Path "a") -or (Test-Path "b"))` |
| `if (Get-Item $x -and $y -eq 5)` | `if ((Get-Item $x) -and ($y -eq 5))` |

**Regola:** con gli operatori logici, ogni chiamata a un cmdlet VA tra parentesi.

---

## 2. Codifica, lettere accentate ed emoji

### CRITICO: Windows PowerShell 5.1 e l'UTF-8

Windows PowerShell 5.1 legge un file `.ps1` UTF-8 **senza BOM** con la code page di sistema: "è" diventa "Ã¨" e le emoji rompono lo script. PowerShell 7 legge l'UTF-8 senza BOM correttamente.

| Scopo | ❌ Da non usare | ✅ Da usare |
| --- | --- | --- |
| Successo | ✅ ✓ | [OK] [+] |
| Errore | ❌ ✗ 🔴 | [!] [X] |
| Avviso | ⚠️ 🟡 | [*] [WARN] |
| Informazione | ℹ️ 🔵 | [i] [INFO] |
| Avanzamento | ⏳ | [...] |

**Regola:** niente emoji negli script PowerShell. Se ci sono lettere accentate (i messaggi in italiano), salva il file come UTF-8 **con BOM**, oppure richiedi PowerShell 7.

---

## 3. Controllo dei null

### Controlla sempre prima di accedere

| ❌ Sbagliato | ✅ Giusto |
| --- | --- |
| `$array.Count -gt 0` | `$array -and $array.Count -gt 0` |
| `$text.Length` | `if ($text) { $text.Length }` |

---

## 4. Interpolazione nelle stringhe

### Proprietà ed espressioni

| ❌ Sbagliato | ✅ Giusto |
| --- | --- |
| `"Valore: $obj.prop.sub"` (espande solo `$obj`) | `"Valore: $($obj.prop.sub)"` oppure prima una variabile |

**Schema:**

```powershell
$value = $obj.prop.sub
Write-Output "Valore: $value"
```

---

## 5. Gestione degli errori

### ErrorActionPreference

| Valore | Uso |
| --- | --- |
| Stop | Sviluppo (fallisci subito) |
| Continue | Script in produzione |
| SilentlyContinue | Quando gli errori sono previsti |

### Schema try/catch

- Non fare return dentro il blocco try
- Usa finally per la pulizia
- Fai return dopo il try/catch

---

## 6. Percorsi dei file

### Regole per i percorsi di Windows

| Schema | Uso |
| --- | --- |
| Percorso letterale | `C:\Users\User\file.txt` |
| Percorso da variabile | `Join-Path $env:USERPROFILE "file.txt"` |
| Relativo | `Join-Path $ScriptDir "data"` |

**Regola:** usa Join-Path, così il percorso funziona anche su altri sistemi.

---

## 7. Operazioni sugli array

### Schemi giusti

| Operazione | Sintassi |
| --- | --- |
| Array vuoto | `$array = @()` |
| Aggiungere un elemento | `$array += $item` |
| Aggiungere a un ArrayList | `$list.Add($item) \| Out-Null` |

---

## 8. Operazioni con JSON

### CRITICO: il parametro Depth

| ❌ Sbagliato | ✅ Giusto |
| --- | --- |
| `ConvertTo-Json` | `ConvertTo-Json -Depth 10` |

**Regola:** con oggetti annidati specifica sempre `-Depth`.

### Operazioni sui file

| Operazione | Schema |
| --- | --- |
| Lettura | `Get-Content "file.json" -Raw -Encoding UTF8 \| ConvertFrom-Json` |
| Scrittura | `$data \| ConvertTo-Json -Depth 10 \| Out-File "file.json" -Encoding UTF8` |

---

## 9. Errori comuni

| Messaggio di errore | Causa | Correzione |
| --- | --- | --- |
| "parameter 'or'" | Mancano le parentesi | Metti i cmdlet tra () |
| "Unexpected token" | Carattere Unicode in un file senza BOM | Salva come UTF-8 con BOM, niente emoji |
| "Cannot find property" | Oggetto null | Controlla prima il null |
| "Cannot convert" | Tipi diversi | Usa .ToString() |

---

## 10. Modello di script

```powershell
# Modalità rigorosa
Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"

# Percorsi
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Corpo principale
try {
    # Logica qui
    Write-Output "[OK] Fatto"
    exit 0
}
catch {
    Write-Warning "Errore: $_"
    exit 1
}
```

---

> **Ricorda:** PowerShell ha regole di sintassi tutte sue. Parentesi, codifica dei file e controllo dei null non sono negoziabili.
