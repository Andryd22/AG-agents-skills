#!/usr/bin/env python3
"""
Audit UX - copertura completa del frontend design

Analizza il codice e ne verifica la conformità a:

1. LEGGI DI PSICOLOGIA FONDAMENTALI:
   - Legge di Hick (voci di navigazione, complessità dei form)
   - Legge di Fitts (dimensioni dei target, target touch)
   - Legge di Miller (chunking, limiti della memoria)
   - Effetto Von Restorff (visibilità della CTA principale)
   - Effetto di posizione seriale (elementi importanti all'inizio o alla fine)

2. DESIGN EMOTIVO (Don Norman):
   - Viscerale (prima impressione, gradienti, animazioni)
   - Comportamentale (feedback, usabilità, prestazioni)
   - Riflessivo (storia del brand, valori, identità)

3. COSTRUZIONE DELLA FIDUCIA:
   - Segnali di sicurezza (SSL, crittografia nei form)
   - Riprova sociale (testimonianze, recensioni, loghi)
   - Indicatori di autorevolezza (certificazioni, premi, media)

4. GESTIONE DEL CARICO COGNITIVO:
   - Progressive disclosure (accordion, tab, "Avanzate")
   - Rumore visivo (troppi colori/bordi)
   - Pattern familiari (label, convenzioni standard)

5. DESIGN PERSUASIVO (etico):
   - Default intelligenti (opzioni preselezionate)
   - Ancoraggio (prezzo originale vs prezzo scontato)
   - Riprova sociale (indicatori live, numeri)
   - Indicatori di avanzamento (barre di avanzamento, step)

6. SISTEMA TIPOGRAFICO (9 sezioni):
   - Abbinamento dei font (max 3 famiglie)
   - Lunghezza della riga (45-75ch)
   - Interlinea (rapporti corretti)
   - Spaziatura tra le lettere (maiuscolo, testo display)
   - Peso ed enfasi (livelli di contrasto)
   - Tipografia responsive (clamp())
   - Gerarchia (titoli in sequenza)
   - Scala modulare (rapporti coerenti)
   - Leggibilità (chunking, sottotitoli)

7. EFFETTI VISIVI (10 sezioni):
   - Glassmorphism (blur + trasparenza)
   - Neumorphism (doppia ombra, inset)
   - Gerarchia delle ombre (livelli di elevazione)
   - Gradienti (uso, abuso)
   - Effetti sui bordi (complessità)
   - Effetti glow (text-shadow, box-shadow)
   - Tecniche di overlay (leggibilità del testo sulle immagini)
   - Accelerazione GPU (transform/opacity vs proprietà di layout)
   - Prestazioni (uso di will-change)
   - Scelta degli effetti (lo scopo prima della decorazione)

8. SISTEMA DEI COLORI (7 sezioni):
   - DIVIETO DEL VIOLA (regola Maestro critica - #8B5CF6, #A855F7, ecc.)
   - Regola 60-30-10 (dominante, secondario, accento)
   - Schemi di colore (monocromatico, analogo)
   - Conformità alla dark mode (niente nero o bianco puri)
   - Contrasto WCAG (rilevamento del basso contrasto)
   - Psicologia del colore nel contesto (cibo + blu = male)
   - Palette basate su HSL (approccio consigliato)

9. GUIDA ALLE ANIMAZIONI (6 sezioni):
   - Durata adeguata (minimo 50ms, transizioni al massimo di 1s)
   - Funzioni di easing (ease-out in entrata, ease-in in uscita)
   - Micro-interazioni (feedback su hover/focus)
   - Stati di caricamento (skeleton, spinner, barra di avanzamento)
   - Transizioni di pagina (fade/slide nel routing)
   - Prestazioni delle animazioni allo scroll (niente proprietà di layout)

10. MOTION GRAPHICS (7 sezioni):
   - Animazioni Lottie (fallback per il reduced motion)
   - Memory leak di GSAP (kill/revert allo smontaggio)
   - Prestazioni delle animazioni SVG (stroke-dashoffset con parsimonia)
   - Trasformazioni 3D (perspective sul genitore, avviso per il mobile)
   - Effetti particellari (fallback per il mobile)
   - Animazioni guidate dallo scroll (throttling con rAF)
   - Albero decisionale del motion (funzionale vs decorativo)

11. ACCESSIBILITÀ:
   - Testo alternativo (alt) delle immagini
   - Controlli sul reduced motion
   - Label dei form

Totale: oltre 80 controlli su tutti i principi di design

Uso:
    python ux_audit.py <cartella_progetto | file> [--json]
"""

import sys
import os
import re
import json
from pathlib import Path

# Codifica della console di Windows (i messaggi contengono lettere accentate)
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except AttributeError:
    pass  # Python < 3.7

class UXAuditor:
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.passed_count = 0
        self.files_checked = 0
    
    def audit_file(self, filepath: str) -> None:
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except: return
        
        self.files_checked += 1
        filename = os.path.basename(filepath)

        # Flag comuni, calcolati una volta sola
        has_long_text = bool(re.search(r'<p|<div.*class=.*text|article|<span.*text', content, re.IGNORECASE))
        has_form = bool(re.search(r'<form|<input|password|credit|card|payment', content, re.IGNORECASE))
        complex_elements = len(re.findall(r'<input|<select|<textarea|<option', content, re.IGNORECASE))

        # --- 1. LEGGI DI PSICOLOGIA ---
        # Legge di Hick
        nav_items = len(re.findall(r'<NavLink|<Link|<a\s+href|nav-item', content, re.IGNORECASE))
        if nav_items > 7:
            self.issues.append(f"[Legge di Hick] {filename}: {nav_items} voci di navigazione (max 7)")
        
        # Legge di Fitts
        if re.search(r'height:\s*([0-3]\d)px', content) or re.search(r'h-[1-9]\b|h-10\b', content):
            self.warnings.append(f"[Legge di Fitts] {filename}: Target piccoli (< 44px)")
        
        # Legge di Miller
        form_fields = len(re.findall(r'<input|<select|<textarea', content, re.IGNORECASE))
        if form_fields > 7 and not re.search(r'step|wizard|stage', content, re.IGNORECASE):
            self.warnings.append(f"[Legge di Miller] {filename}: Form complesso ({form_fields} campi)")
            
        # Effetto Von Restorff
        if 'button' in content.lower() and not re.search(r'primary|bg-primary|Button.*primary|variant=["\']primary', content, re.IGNORECASE):
            self.warnings.append(f"[Von Restorff] {filename}: Nessuna CTA principale")

        # Effetto di posizione seriale: elementi importanti all'inizio o alla fine
        if nav_items > 3:
            # L'ultima voce di navigazione è importante? (contatti, login, ecc.)
            nav_content = re.findall(r'<NavLink|<Link|<a\s+href[^>]*>([^<]+)</a>', content, re.IGNORECASE)
            if nav_content and len(nav_content) > 2:
                last_item = nav_content[-1].lower() if nav_content else ''
                if not any(x in last_item for x in ['contact', 'login', 'sign', 'get started', 'cta', 'button']):
                    self.warnings.append(f"[Posizione seriale] {filename}: L'ultima voce di navigazione potrebbe non essere importante. Metti le azioni chiave all'inizio o alla fine.")

        # --- 1.5 DESIGN EMOTIVO (Don Norman) ---

        # Viscerale: prima impressione (estetica, gradienti, animazioni)
        has_hero = bool(re.search(r'hero|<h1|banner', content, re.IGNORECASE))
        if has_hero:
            # Elementi di impatto visivo
            has_gradient = bool(re.search(r'gradient|linear-gradient|radial-gradient', content))
            has_animation = bool(re.search(r'@keyframes|transition:|animate-', content))
            has_visual_interest = has_gradient or has_animation

            if not has_visual_interest and not re.search(r'background:|bg-', content):
                self.warnings.append(f"[Viscerale] {filename}: La sezione hero ha poco impatto visivo. Valuta gradienti o animazioni leggere.")

        # Comportamentale: feedback immediato e usabilità
        if 'onClick' in content or '@click' in content or 'onclick' in content:
            has_feedback = re.search(r'transition|animate|hover:|focus:|disabled|loading|spinner', content, re.IGNORECASE)
            has_state_change = re.search(r'setState|useState|disabled|loading', content)

            if not has_feedback and not has_state_change:
                self.warnings.append(f"[Comportamentale] {filename}: Gli elementi interattivi non danno un feedback immediato. Aggiungi gli stati hover/focus/disabled.")

        # Riflessivo: storia del brand, valori, identità
        has_reflective = bool(re.search(r'about|story|mission|values|why we|our journey|testimonials', content, re.IGNORECASE))
        if has_long_text and not has_reflective:
            self.warnings.append(f"[Riflessivo] {filename}: Contenuti lunghi senza storia o valori del brand. Aggiungi una sezione 'Chi siamo' o 'Perché esistiamo'.")

        # --- 1.6 COSTRUZIONE DELLA FIDUCIA (estesa) ---

        # Segnali di sicurezza
        if has_form:
            security_signals = re.findall(r'ssl|secure|encrypt|lock|padlock|https', content, re.IGNORECASE)
            if len(security_signals) == 0 and not re.search(r'checkout|payment', content, re.IGNORECASE):
                self.warnings.append(f"[Fiducia] {filename}: Form senza indicatori di sicurezza. Aggiungi 'Connessione sicura SSL' o l'icona di un lucchetto.")

        # Elementi di riprova sociale
        social_proof = re.findall(r'review|testimonial|rating|star|trust|trusted by|customer|logo', content, re.IGNORECASE)
        if len(social_proof) > 0:
            self.passed_count += 1
        else:
            if has_long_text:
                self.warnings.append(f"[Fiducia] {filename}: Nessuna riprova sociale. Valuta testimonianze, valutazioni o loghi 'Scelto da'.")

        # Indicatori di autorevolezza
        has_footer = bool(re.search(r'footer|<footer', content, re.IGNORECASE))
        if has_footer:
            authority = re.findall(r'certif|award|media|press|featured|as seen in', content, re.IGNORECASE)
            if len(authority) == 0:
                self.warnings.append(f"[Fiducia] {filename}: Il footer non ha segnali di autorevolezza. Aggiungi certificazioni, premi o citazioni sui media.")

        # --- 1.7 GESTIONE DEL CARICO COGNITIVO ---

        # Progressive disclosure
        if complex_elements > 5:
            has_progressive = re.search(r'step|wizard|stage|accordion|collapsible|tab|more\.\.\.|advanced|show more', content, re.IGNORECASE)
            if not has_progressive:
                self.warnings.append(f"[Carico cognitivo] {filename}: Molti elementi del form senza progressive disclosure. Valuta accordion, tab o un interruttore 'Avanzate'.")

        # Rumore visivo
        has_many_colors = len(re.findall(r'#[0-9a-fA-F]{3,6}|rgb|hsl', content)) > 15
        has_many_borders = len(re.findall(r'border:|border-', content)) > 10
        if has_many_colors and has_many_borders:
            self.warnings.append(f"[Carico cognitivo] {filename}: Rumore visivo elevato. Molti colori e bordi aumentano il carico cognitivo.")

        # Pattern familiari
        if has_form:
            has_standard_labels = bool(re.search(r'<label|placeholder|aria-label', content, re.IGNORECASE))
            if not has_standard_labels:
                self.issues.append(f"[Carico cognitivo] {filename}: Campi del form senza label. Usa <label> per accessibilità e chiarezza.")

        # --- 1.8 DESIGN PERSUASIVO (etico) ---

        # Default intelligenti
        if has_form:
            has_defaults = bool(re.search(r'checked|selected|default|value=["\'].*["\']', content))
            radio_inputs = len(re.findall(r'type=["\']radio', content, re.IGNORECASE))
            if radio_inputs > 0 and not has_defaults:
                self.warnings.append(f"[Persuasione] {filename}: Radio button senza selezione predefinita. Preseleziona l'opzione consigliata.")

        # Ancoraggio (mostrare il prezzo originale)
        if re.search(r'price|pricing|cost|\$\d+', content, re.IGNORECASE):
            has_anchor = bool(re.search(r'original|was|strike|del|save \d+%', content, re.IGNORECASE))
            if not has_anchor:
                self.warnings.append(f"[Persuasione] {filename}: Prezzi senza ancoraggio. Mostra il prezzo originale per dare valore allo sconto.")

        # Indicatori live di riprova sociale
        has_social = bool(re.search(r'join|subscriber|member|user', content, re.IGNORECASE))
        if has_social:
            has_count = bool(re.findall(r'\d+[+kmb]|\d+,\d+', content))
            if not has_count:
                self.warnings.append(f"[Persuasione] {filename}: Riprova sociale senza numeri precisi. Usa un formato come 'Unisciti a oltre 10.000 utenti'.")

        # Indicatori di avanzamento
        if has_form:
            has_progress = bool(re.search(r'progress|step \d+|complete|%|bar', content, re.IGNORECASE))
            if complex_elements > 5 and not has_progress:
                self.warnings.append(f"[Persuasione] {filename}: Form lungo senza indicatore di avanzamento. Aggiungi una barra di avanzamento o 'Passo X di Y'.")

        # --- 2. SISTEMA TIPOGRAFICO (copertura completa) ---

        # 2.1 Abbinamento dei font: troppe famiglie
        font_families = set()
        # Dichiarazioni @font-face, Google Fonts e font-family
        font_faces = re.findall(r'@font-face\s*\{[^}]*family:\s*["\']?([^;"\'\s}]+)', content, re.IGNORECASE)
        google_fonts = re.findall(r'fonts\.googleapis\.com[^"\']*family=([^"&]+)', content, re.IGNORECASE)
        font_family_css = re.findall(r'font-family:\s*([^;]+)', content, re.IGNORECASE)

        for font in font_faces: font_families.add(font.strip().lower())
        for font in google_fonts:
            for f in font.replace('+', ' ').split('|'):
                font_families.add(f.split(':')[0].strip().lower())
        for family in font_family_css:
            # Primo font dello stack
            first_font = family.split(',')[0].strip().strip('"\'')

            if first_font.lower() not in {'sans-serif', 'serif', 'monospace', 'cursive', 'fantasy', 'system-ui', 'inherit', 'arial', 'georgia', 'times new roman', 'courier new', 'verdana', 'helvetica', 'tahoma'}:
                font_families.add(first_font.lower())

        if len(font_families) > 3:
            self.issues.append(f"[Tipografia] {filename}: {len(font_families)} famiglie di font. Limitati a 2-3 per coerenza.")

        # 2.2 Lunghezza della riga: larghezza in caratteri
        if has_long_text and not re.search(r'max-w-(?:prose|[\[\\]?\d+ch[\]\\]?)|max-width:\s*\d+ch', content):
            self.warnings.append(f"[Tipografia] {filename}: Nessun limite alla lunghezza della riga (45-75ch). Usa max-w-prose o max-w-[65ch].")

        # 2.3 Interlinea: rapporti corretti
        # Testo senza una line-height adeguata
        text_elements = len(re.findall(r'<p|<span|<div.*text|<h[1-6]', content, re.IGNORECASE))
        if text_elements > 0 and not re.search(r'leading-|line-height:', content):
            self.warnings.append(f"[Tipografia] {filename}: Elementi di testo senza line-height. Testo: 1.4-1.6, titoli: 1.1-1.3")

        # Problemi di interlinea specifici dei titoli
        if re.search(r'<h[1-6]|text-(?:xl|2xl|3xl|4xl|5xl|6xl)', content, re.IGNORECASE):
            # Valori di line-height
            line_heights = re.findall(r'(?:leading-|line-height:\s*)([\d.]+)', content)
            for lh in line_heights:
                if float(lh) > 1.5:
                    self.warnings.append(f"[Tipografia] {filename}: Titolo con line-height {lh} (>1.3). I titoli vanno più stretti (1.1-1.3).")

        # 2.4 Spaziatura tra le lettere (tracking)
        # Maiuscolo senza tracking
        if re.search(r'uppercase|text-transform:\s*uppercase', content, re.IGNORECASE):
            if not re.search(r'tracking-|letter-spacing:', content):
                self.warnings.append(f"[Tipografia] {filename}: Testo maiuscolo senza tracking. Il TUTTO MAIUSCOLO vuole +5-10% di spaziatura.")

        # Il testo grande (display/hero) vuole un tracking negativo
        if re.search(r'text-(?:4xl|5xl|6xl|7xl|8xl|9xl)|font-size:\s*[3-9]\dpx', content):
            if not re.search(r'tracking-tight|letter-spacing:\s*-[0-9]', content):
                self.warnings.append(f"[Tipografia] {filename}: Testo display grande senza tracking-tight. Il testo grande vuole da -1% a -4% di spaziatura.")

        # 2.5 Peso ed enfasi: livelli di contrasto
        # Pesi adiacenti (contrasto scarso)
        weights = re.findall(r'font-weight:\s*(\d+)|font-(thin|extralight|light|normal|medium|semibold|bold|extrabold|black)\b|fw-(\d+)', content, re.IGNORECASE)
        weight_values = []
        for w in weights:
            val = w[0] or w[1] or w[2]
            if val:
                # Converte i pesi con nome in numeri
                weight_map = {'thin': '100', 'extralight': '200', 'light': '300', 'normal': '400', 'medium': '500', 'semibold': '600', 'bold': '700', 'extrabold': '800', 'black': '900'}
                val = weight_map.get(val.lower(), val)
                try:
                    weight_values.append(int(val))
                except: pass

        # Pesi adiacenti (400/500, 500/600, ecc.)
        for i in range(len(weight_values) - 1):
            diff = abs(weight_values[i] - weight_values[i+1])
            if diff == 100:
                self.warnings.append(f"[Tipografia] {filename}: Pesi del font adiacenti ({weight_values[i]}/{weight_values[i+1]}). Salta almeno 2 livelli per avere contrasto.")

        # Troppi livelli di peso
        unique_weights = set(weight_values)
        if len(unique_weights) > 4:
            self.warnings.append(f"[Tipografia] {filename}: {len(unique_weights)} pesi del font. Limitati a 3-4 per pagina.")

        # 2.6 Tipografia responsive: dimensioni fluide con clamp()
        has_font_sizes = bool(re.search(r'font-size:|text-(?:xs|sm|base|lg|xl|2xl)', content))
        if has_font_sizes and not re.search(r'clamp\(|responsive:', content):
            self.warnings.append(f"[Tipografia] {filename}: Dimensioni del font fisse senza clamp(). Valuta una tipografia fluida: clamp(MIN, IDEALE, MAX)")

        # 2.7 Gerarchia: struttura dei titoli
        headings = re.findall(r'<(h[1-6])', content, re.IGNORECASE)
        if headings:
            # Livelli saltati (h1 -> h3)
            for i in range(len(headings) - 1):
                curr = int(headings[i][1])
                next_h = int(headings[i+1][1])
                if next_h > curr + 1:
                    self.warnings.append(f"[Tipografia] {filename}: Livello di titolo saltato (h{curr} -> h{next_h}). Mantieni una gerarchia in sequenza.")

            # C'è un h1 per il contenuto principale?
            if 'h1' not in [h.lower() for h in headings] and has_long_text:
                self.warnings.append(f"[Tipografia] {filename}: Nessun h1. Ogni pagina dovrebbe avere un titolo principale.")

        # 2.8 Scala modulare: dimensioni coerenti
        # Valori di font-size
        font_sizes = re.findall(r'font-size:\s*(\d+(?:\.\d+)?)(px|rem|em)', content)
        size_values = []
        for size, unit in font_sizes:
            if unit == 'rem' or unit == 'em':
                size_values.append(float(size))
            elif unit == 'px':
                size_values.append(float(size) / 16)  # Normalizza in rem

        if len(size_values) > 2:
            # Le dimensioni seguono più o meno una scala modulare?
            sorted_sizes = sorted(set(size_values))
            ratios = []
            for i in range(1, len(sorted_sizes)):
                if sorted_sizes[i-1] > 0:
                    ratios.append(sorted_sizes[i] / sorted_sizes[i-1])

            # Rapporti di scala comuni: 1.067, 1.125, 1.2, 1.25, 1.333, 1.5, 1.618
            common_ratios = {1.067, 1.125, 1.2, 1.25, 1.333, 1.5, 1.618}
            for ratio in ratios[:3]:  # Solo i primi 3 rapporti
                if not any(abs(ratio - cr) < 0.05 for cr in common_ratios):
                    self.warnings.append(f"[Tipografia] {filename}: Le dimensioni del font potrebbero non seguire una scala modulare (rapporto: {ratio:.2f}). Valuta un rapporto costante come 1.25 (terza maggiore).")
                    break

        # 2.9 Leggibilità: suddivisione del contenuto
        # Paragrafi molto lunghi (più di 5 righe stimate)
        paragraphs = re.findall(r'<p[^>]*>([^<]+)</p>', content, re.IGNORECASE)
        for p in paragraphs:
            word_count = len(p.split())
            if word_count > 100:  # ~5-6 righe
                self.warnings.append(f"[Tipografia] {filename}: Paragrafo lungo ({word_count} parole). Spezzalo in blocchi di 3-4 righe per la leggibilità.")

        # Sottotitoli mancanti nei contenuti lunghi
        if len(paragraphs) > 5:
            subheadings = len(re.findall(r'<h[2-6]', content, re.IGNORECASE))
            if subheadings == 0:
                self.warnings.append(f"[Tipografia] {filename}: Contenuto lungo senza sottotitoli. Aggiungi h2/h3 per spezzare il testo.")

        # --- 3. EFFETTI VISIVI (visual-effects.md) ---
        
        # Glassmorphism
        if 'backdrop-filter' in content or 'blur(' in content:
            if not re.search(r'background:\s*rgba|bg-opacity|bg-[a-z0-9]+\/\d+', content):
                self.warnings.append(f"[Effetti visivi] {filename}: Blur senza sfondo semitrasparente (glassmorphism non riuscito)")
        
        # Accelerazione GPU / prestazioni
        if re.search(r'@keyframes|transition:', content):
            expensive_props = re.findall(r'width|height|top|left|right|bottom|margin|padding', content)
            if expensive_props:
                self.warnings.append(f"[Prestazioni] {filename}: Animazione di proprietà costose ({', '.join(sorted(set(expensive_props)))}). Usa transform/opacity dove possibile.")
            
            # Reduced motion
            if not re.search(r'prefers-reduced-motion', content):
                self.warnings.append(f"[Accessibilità] {filename}: Animazioni senza controllo di prefers-reduced-motion")

        # Ombre naturali
        shadows = re.findall(r'box-shadow:\s*([^;]+)', content)
        for shadow in shadows:
            # Naturale (Y > X) o a più livelli?
            if ',' not in shadow and not re.search(r'\d+px\s+[1-9]\d*px', shadow): # Euristica semplice per l'offset Y
                 self.warnings.append(f"[Effetti visivi] {filename}: Ombra semplice o innaturale. Valuta più livelli o un offset Y > X per più realismo.")

        # --- 3.1 NEUMORPHISM ---
        # Pattern di neumorphism (doppia ombra in direzioni opposte)
        neo_shadows = re.findall(r'box-shadow:\s*([^;]+)', content)
        for shadow in neo_shadows:
            # Il neumorphism ha due ombre: offset positivo + offset negativo
            if ',' in shadow and '-' in shadow:
                # Pattern inset (stato premuto)
                if 'inset' in shadow:
                    self.warnings.append(f"[Effetti visivi] {filename}: Neumorphism con inset. Garantisci un contrasto adeguato per l'accessibilità.")

        # --- 3.2 GERARCHIA DELLE OMBRE ---
        # Conta i livelli di ombra per verificare la coerenza dell'elevazione
        shadow_count = len(shadows)
        if shadow_count > 0:
            # Livelli di opacità delle ombre (dovrebbero indicare la gerarchia)
            opacities = re.findall(r'rgba?\([^)]+,\s*([\d.]+)\)', content)
            shadow_opacities = [float(o) for o in opacities if float(o) < 0.5]
            if shadow_count >= 3 and len(shadow_opacities) > 0:
                # Le opacità delle ombre variano con l'elevazione?
                unique_opacities = len(set(shadow_opacities))
                if unique_opacities < 2:
                    self.warnings.append(f"[Effetti visivi] {filename}: Tutte le ombre hanno la stessa opacità. Varia l'intensità delle ombre per la gerarchia di elevazione.")

        # --- 3.3 GRADIENTI ---
        # Uso dei gradienti
        has_gradient = bool(re.search(r'gradient|linear-gradient|radial-gradient|conic-gradient', content))
        if has_gradient:
            # Avvisa sui gradienti mesh/aurora (facili da abusare)
            gradient_count = len(re.findall(r'gradient', content, re.IGNORECASE))
            if gradient_count > 5:
                self.warnings.append(f"[Effetti visivi] {filename}: Molti gradienti ({gradient_count}). Assicurati che servano a uno scopo e non siano solo decorazione.")
        else:
            # Sezione hero senza gradiente?
            if has_hero and not re.search(r'background:|bg-', content):
                self.warnings.append(f"[Effetti visivi] {filename}: Sezione hero senza interesse visivo. Valuta un gradiente per dare profondità.")

        # --- 3.4 EFFETTI SUI BORDI ---
        # Bordi con gradiente o animati
        has_border = bool(re.search(r'border:|border-', content))
        if has_border:
            # Bordi troppo complessi
            border_count = len(re.findall(r'border:', content))
            if border_count > 8:
                self.warnings.append(f"[Effetti visivi] {filename}: Molte dichiarazioni di bordo ({border_count}). Semplifica per un aspetto più pulito.")

        # --- 3.5 EFFETTI GLOW ---
        # text-shadow o box-shadow a più livelli (effetti glow)
        text_shadows = re.findall(r'text-shadow:\s*([^;}\n]+)', content)
        for ts in text_shadows:
            # Più livelli di text-shadow (separati da virgole, escluse quelle dentro rgba()) indicano un glow
            if ',' in re.sub(r'\([^)]*\)', '', ts):
                self.warnings.append(f"[Effetti visivi] {filename}: Effetto glow sul testo. Assicurati che resti leggibile.")

        # Glow con box-shadow (più livelli con offset 0)
        glow_shadows = re.findall(r'box-shadow:\s*[^;]*0\s+0\s+', content)
        if len(glow_shadows) > 2:
            self.warnings.append(f"[Effetti visivi] {filename}: Molti effetti glow. Usali con parsimonia, solo per dare enfasi.")

        # --- 3.6 TECNICHE DI OVERLAY ---
        # Overlay sulle immagini (per la leggibilità)
        has_images = bool(re.search(r'<img|background-image:|bg-\[url', content))
        if has_images and has_long_text:
            has_overlay = bool(re.search(r'overlay|rgba\(0|gradient.*transparent|::after|::before', content))
            if not has_overlay:
                self.warnings.append(f"[Effetti visivi] {filename}: Testo sopra un'immagine senza overlay. Aggiungi un overlay con gradiente per la leggibilità.")

        # --- 3.7 PRESTAZIONI: will-change ---
        # Uso di will-change
        if re.search(r'will-change:', content):
            will_change_props = re.findall(r'will-change:\s*([^;]+)', content)
            for prop in will_change_props:
                prop = prop.strip().lower()
                if prop in ['width', 'height', 'top', 'left', 'right', 'bottom', 'margin', 'padding']:
                    self.issues.append(f"[Prestazioni] {filename}: will-change su '{prop}' (proprietà di layout). Usalo solo per transform/opacity.")

        # Uso eccessivo di will-change
        will_change_count = len(re.findall(r'will-change:', content))
        if will_change_count > 3:
            self.warnings.append(f"[Prestazioni] {filename}: Molte dichiarazioni will-change ({will_change_count}). Usale con parsimonia, solo per le animazioni pesanti.")

        # --- 3.8 SCELTA DEGLI EFFETTI ---
        # Abuso di effetti (troppi effetti visivi)
        effect_count = (
            (1 if has_gradient else 0) +
            shadow_count +
            len(re.findall(r'backdrop-filter|blur\(', content)) +
            len(re.findall(r'text-shadow:', content))
        )
        if effect_count > 10:
            self.warnings.append(f"[Effetti visivi] {filename}: Molti effetti visivi ({effect_count}). Assicurati che servano a uno scopo e non siano solo decorazione.")

        # Design statico o piatto (senza profondità)
        if has_long_text and effect_count == 0:
            self.warnings.append(f"[Effetti visivi] {filename}: Design piatto senza profondità. Valuta ombre o gradienti leggeri per la gerarchia.")

        # --- 4. SISTEMA DEI COLORI (color-system.md) ---

        # 4.1 DIVIETO DEL VIOLA: controllo critico da color-system.md
        purple_hexes = ['#8B5CF6', '#A855F7', '#9333EA', '#7C3AED', '#6D28D9',
                        '#8B5CF6', '#A78BFA', '#C4B5FD', '#DDD6FE', '#EDE9FE',
                        '#8b5cf6', '#a855f7', '#9333ea', '#7c3aed', '#6d28d9',
                        'purple', 'violet', 'fuchsia', 'magenta', 'lavender']
        for purple in purple_hexes:
            if purple.lower() in content.lower():
                self.issues.append(f"[Colore] {filename}: VIOLA RILEVATO ('{purple}'). Vietato dalle regole Maestro. Usa invece verde petrolio, ciano o smeraldo.")
                break

        # 4.2 Regola 60-30-10
        # Conta i colori usati per stimare le proporzioni
        color_hex_count = len(re.findall(r'#[0-9a-fA-F]{3,6}', content))
        hsl_count = len(re.findall(r'hsl\(', content))
        total_colors = color_hex_count + hsl_count
        if total_colors > 3:
            # Colori dominanti (dovrebbero essere ~60%)
            bg_declarations = re.findall(r'(?:background|bg-|bg\[)([^;}\s]+)', content)
            text_declarations = re.findall(r'(?:color|text-)([^;}\s]+)', content)
            if len(bg_declarations) > 0 and len(text_declarations) > 0:
                # Avvisa solo se ci sono troppi colori distinti
                unique_hexes = set(re.findall(r'#[0-9a-fA-F]{6}', content))
                if len(unique_hexes) > 5:
                    self.warnings.append(f"[Colore] {filename}: {len(unique_hexes)} colori distinti. Valuta la regola 60-30-10: dominante (60%), secondario (30%), accento (10%).")

        # 4.3 Riconoscimento dello schema di colori
        # Monocromatico (stessa tonalità, luminosità diverse)
        hsl_matches = re.findall(r'hsl\((\d+),\s*\d+%,\s*\d+%\)', content)
        if len(hsl_matches) >= 3:
            hues = [int(h) for h in hsl_matches]
            hue_range = max(hues) - min(hues)
            if hue_range < 10:
                self.warnings.append(f"[Colore] {filename}: Palette monocromatica (variazione di tonalità: {hue_range}deg). Garantisci un contrasto adeguato.")

        # 4.4 Conformità alla dark mode
        # Nero puro (#000000) o bianco puro (#FFFFFF) (vietati)
        if re.search(r'color:\s*#000000|#000\b', content):
            self.warnings.append(f"[Colore] {filename}: Nero puro (#000000). Usa #1a1a1a o grigi scuri per una dark mode migliore.")
        if re.search(r'background:\s*#ffffff|#fff\b', content) and re.search(r'dark:\s*|dark:', content):
            self.warnings.append(f"[Colore] {filename}: Sfondo bianco puro in un contesto di dark mode. Usa un bianco sporco (#f9fafb) per affaticare meno la vista.")

        # 4.5 Contrasto WCAG
        # Possibili combinazioni a basso contrasto
        light_bg_light_text = bool(re.search(r'bg-(?:gray|slate|zinc)-50|bg-white.*text-(?:gray|slate)-[12]', content))
        dark_bg_dark_text = bool(re.search(r'bg-(?:gray|slate|zinc)-9|bg-black.*text-(?:gray|slate)-[89]', content))
        if light_bg_light_text or dark_bg_dark_text:
            self.warnings.append(f"[Colore] {filename}: Possibile combinazione a basso contrasto. Verifica il livello WCAG AA (4.5:1 per il testo).")

        # 4.6 Psicologia del colore nel contesto
        # Avvisa se il blu compare in un contesto di cibo o ristorazione
        has_blue = bool(re.search(r'bg-blue|text-blue|from-blue|#[0-9a-fA-F]*00[0-9A-Fa-f]{2}|#[0-9a-fA-F]*1[0-9A-Fa-f]{2}', content))
        has_food_context = bool(re.search(r'restaurant|food|cooking|recipe|menu|dish|meal', content, re.IGNORECASE))
        if has_blue and has_food_context:
            self.warnings.append(f"[Colore] {filename}: Blu in un contesto alimentare. Il blu riduce l'appetito: valuta colori caldi (rosso, arancione, giallo).")

        # 4.7 Palette basate su HSL
        # La palette usa HSL? (consigliato in color-system.md)
        has_color_vars = bool(re.search(r'--color-|color-|primary-|secondary-', content))
        if has_color_vars and not re.search(r'hsl\(', content):
            self.warnings.append(f"[Colore] {filename}: Variabili di colore senza HSL. Valuta HSL per regolare più facilmente la palette (tonalità, saturazione, luminosità).")

        # --- 5. GUIDA ALLE ANIMAZIONI (animation-guide.md) ---

        # 5.1 Durata adeguata
        # Animazioni troppo lunghe o troppo brevi
        durations = re.findall(r'(?:duration|animation-duration|transition-duration):\s*([\d.]+)(s|ms)', content)
        for duration, unit in durations:
            duration_ms = float(duration) * (1000 if unit == 's' else 1)
            if duration_ms < 50:
                self.warnings.append(f"[Animazione] {filename}: Animazione molto veloce ({duration}{unit}). Servono almeno 50ms perché sia visibile.")
            elif duration_ms > 1000 and 'transition' in content.lower():
                self.warnings.append(f"[Animazione] {filename}: Transizione lunga ({duration}{unit}). Le transizioni dovrebbero durare 100-300ms per risultare reattive.")

        # 5.2 Funzioni di easing corrette
        # Pattern di easing sbagliati
        if re.search(r'ease-in\s+.*entry|fade-in.*ease-in', content):
            self.warnings.append(f"[Animazione] {filename}: Animazione di entrata con ease-in. In entrata usa ease-out per una sensazione di prontezza.")
        if re.search(r'ease-out\s+.*exit|fade-out.*ease-out', content):
            self.warnings.append(f"[Animazione] {filename}: Animazione di uscita con ease-out. In uscita usa ease-in per un effetto naturale.")

        # 5.3 Feedback con micro-interazioni
        # Elementi interattivi senza stati hover/focus
        interactive_elements = len(re.findall(r'<button|<a\s+href|onClick|@click', content))
        has_hover_focus = bool(re.search(r'hover:|focus:|:hover|:focus', content))
        if interactive_elements > 2 and not has_hover_focus:
            self.warnings.append(f"[Animazione] {filename}: Elementi interattivi senza stati hover/focus. Aggiungi micro-interazioni come feedback.")

        # 5.4 Indicatori dello stato di caricamento
        # Pattern di caricamento
        has_async = bool(re.search(r'async|await|fetch|axios|loading|isLoading', content))
        has_loading_indicator = bool(re.search(r'skeleton|spinner|progress|loading|<circle.*animate', content))
        if has_async and not has_loading_indicator:
            self.warnings.append(f"[Animazione] {filename}: Operazioni asincrone senza indicatore di caricamento. Aggiungi uno skeleton o uno spinner per migliorare le prestazioni percepite.")

        # 5.5 Transizioni di pagina
        # Transizioni tra pagine o viste
        has_routing = bool(re.search(r'router|navigate|Link.*to|useHistory', content))
        has_page_transition = bool(re.search(r'AnimatePresence|motion\.|transition.*page|fade.*route', content))
        if has_routing and not has_page_transition:
            self.warnings.append(f"[Animazione] {filename}: Routing senza transizioni di pagina. Valuta fade/slide per dare continuità al contesto.")

        # 5.6 Prestazioni delle animazioni allo scroll
        # Animazioni guidate dallo scroll
        has_scroll_anim = bool(re.search(r'onScroll|scroll.*trigger|IntersectionObserver', content))
        if has_scroll_anim:
            # Proprietà costose negli handler di scroll?
            if re.search(r'onScroll.*[^\w](width|height|top|left)', content):
                self.issues.append(f"[Animazione] {filename}: Handler di scroll che anima proprietà di layout. Usa transform/opacity per restare a 60fps.")

        # --- 6. MOTION GRAPHICS (motion-graphics.md) ---

        # 6.1 Animazioni Lottie
        has_lottie = bool(re.search(r'lottie|Lottie|@lottie-react', content))
        if has_lottie:
            # Fallback per il reduced motion
            has_lottie_fallback = bool(re.search(r'prefers-reduced-motion.*lottie|lottie.*isPaused|lottie.*stop', content))
            if not has_lottie_fallback:
                self.warnings.append(f"[Motion] {filename}: Animazione Lottie senza fallback per il reduced motion. Aggiungi pausa/stop per l'accessibilità.")

        # 6.2 Rischio di memory leak con GSAP
        has_gsap = bool(re.search(r'gsap|ScrollTrigger|from\(.*gsap', content))
        if has_gsap:
            # Pattern di cleanup
            has_gsap_cleanup = bool(re.search(r'kill\(|revert\(|useEffect.*return.*gsap', content))
            if not has_gsap_cleanup:
                self.issues.append(f"[Motion] {filename}: Animazione GSAP senza cleanup (kill/revert). Rischio di memory leak allo smontaggio.")

        # 6.3 Prestazioni delle animazioni SVG
        svg_animations = re.findall(r'<animate|<animateTransform|stroke-dasharray|stroke-dashoffset', content)
        if len(svg_animations) > 3:
            self.warnings.append(f"[Motion] {filename}: Molte animazioni SVG. Usa stroke-dashoffset con parsimonia per le prestazioni su mobile.")

        # 6.4 Prestazioni delle trasformazioni 3D
        has_3d_transform = bool(re.search(r'transform3d|perspective\(|rotate3d|translate3d', content))
        if has_3d_transform:
            # perspective sul genitore
            has_perspective_parent = bool(re.search(r'perspective:\s*\d+px|perspective\s*\(', content))
            if not has_perspective_parent:
                self.warnings.append(f"[Motion] {filename}: Trasformazione 3D senza perspective sul genitore. Aggiungi perspective: 1000px per una profondità realistica.")

            # Avviso sulle prestazioni su mobile
            self.warnings.append(f"[Motion] {filename}: Trasformazioni 3D. Prova su mobile: possono pesare sulle prestazioni dei dispositivi meno potenti.")

        # 6.5 Effetti particellari
        # Sistemi di particelle con canvas/WebGL
        has_particles = bool(re.search(r'particle|canvas.*loop|requestAnimationFrame.*draw|Three\.js', content))
        if has_particles:
            self.warnings.append(f"[Motion] {filename}: Effetti particellari. Prevedi un fallback o una versione a qualità ridotta per i dispositivi mobile.")

        # 6.6 Prestazioni delle animazioni guidate dallo scroll
        has_scroll_driven = bool(re.search(r'IntersectionObserver.*animate|scroll.*progress|view-timeline', content))
        if has_scroll_driven:
            # Throttling/debouncing
            has_throttle = bool(re.search(r'throttle|debounce|requestAnimationFrame', content))
            if not has_throttle:
                self.issues.append(f"[Motion] {filename}: Animazione guidata dallo scroll senza throttling. Usa requestAnimationFrame per restare a 60fps.")

        # 6.7 Albero decisionale del motion: contesto
        # L'animazione ha uno scopo (non è solo decorazione)?
        total_animations = (
            len(re.findall(r'@keyframes|transition:|animate-', content)) +
            (1 if has_lottie else 0) +
            (1 if has_gsap else 0)
        )
        if total_animations > 5:
            # Le animazioni sono funzionali?
            functional_animations = len(re.findall(r'hover:|focus:|disabled|loading|error|success', content))
            if functional_animations < total_animations / 2:
                self.warnings.append(f"[Motion] {filename}: Molte animazioni ({total_animations}). Assicurati che la maggior parte abbia uno scopo funzionale (feedback, guida) e non sia solo decorazione.")

        # --- 7. ACCESSIBILITÀ ---
        if re.search(r'<img(?![^>]*alt=)[^>]*>', content):
            self.issues.append(f"[Accessibilità] {filename}: Immagini senza testo alt")

    def audit_directory(self, directory: str) -> None:
        extensions = {'.tsx', '.jsx', '.html', '.vue', '.svelte', '.css'}
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in {'node_modules', '.git', 'dist', 'build', '.next', '.agent', '.agents'}]
            for file in files:
                if Path(file).suffix in extensions:
                    self.audit_file(os.path.join(root, file))

    def get_report(self):
        return {
            "files_checked": self.files_checked,
            "issues": self.issues,
            "warnings": self.warnings,
            "passed_checks": self.passed_count,
            "compliant": len(self.issues) == 0
        }

def main():
    if len(sys.argv) < 2:
        print("Uso: python ux_audit.py <cartella_progetto | file> [--json]")
        sys.exit(1)
    
    path = sys.argv[1]
    is_json = "--json" in sys.argv
    
    auditor = UXAuditor()
    if os.path.isfile(path): auditor.audit_file(path)
    else: auditor.audit_directory(path)
    
    report = auditor.get_report()
    
    if is_json:
        print(json.dumps(report))
    else:
        # Marcatori ASCII ([!], [*], [+]) per la compatibilità con la console di Windows
        print(f"\n[AUDIT UX] {report['files_checked']} file controllati")
        print("-" * 50)
        if report['issues']:
            print(f"[!] PROBLEMI ({len(report['issues'])}):")
            for i in report['issues'][:10]: print(f"  - {i}")
        if report['warnings']:
            print(f"[*] AVVISI ({len(report['warnings'])}):")
            for w in report['warnings'][:15]: print(f"  - {w}")
        print(f"[+] CONTROLLI SUPERATI: {report['passed_checks']}")
        status = "PASS" if report['compliant'] else "FAIL"
        print(f"ESITO: {status}")

    sys.exit(0 if report['compliant'] else 1)

if __name__ == "__main__":
    main()
