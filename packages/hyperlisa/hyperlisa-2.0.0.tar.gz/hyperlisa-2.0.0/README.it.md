[English](README.md) | [Italiano](https://www.google.com/search?q=README.it.md)

# Lisa - Analizzatore di Codice per LLM

Lisa (ispirato a Lisa Simpson) è uno strumento progettato per semplificare l'analisi del codice sorgente attraverso i Large Language Models (LLM). Intelligente e analitica come il personaggio da cui prende il nome, Lisa aiuta a studiare e interpretare il codice con logica e metodo.

## Guida Rapida

Questa sezione contiene le istruzioni essenziali per essere operativi in pochi minuti, sia partendo da zero sia aggiornando un progetto esistente.

### Per un Nuovo Progetto

1.  **Installazione**: Apri il terminale nella cartella del tuo progetto e lancia il comando:

    ```bash
    pip install hyperlisa
    ```

2.  **Configurazione**: Esegui il comando per creare la configurazione di default.

    ```bash
    hyperlisa-configure
    ```

    Verrà creata una cartella `.hyperlisa` con all'interno il file `config.yaml`.

## 1. Per Aggiornare un Progetto Esistente (dalla v1.x)

1.  **Aggiornamento**: Per prima cosa, aggiorna il pacchetto all'ultima versione:

    ```bash
    pip install --upgrade hyperlisa
    ```

2.  **Migrazione**: Spostati nella cartella del tuo progetto e lancia il comando di migrazione automatica:

    ```bash
    hyperlisa-migrate
    ```

    Questo comando rinominerà la vecchia cartella `hyperlisa` in `.hyperlisa` e convertirà il tuo vecchio file di configurazione al nuovo formato.

## 2. Utilizzo Base

### 2.1.  **Esecuzione**: Dalla cartella del progetto, esegui semplicemente:

    ```bash
    cmb
    ```

### 2.2.  **Output**: Lo script genererà, all'interno della cartella `.hyperlisa`, un file di testo per ogni profilo abilitato nel tuo `config.yaml`. Di default, ogni file inizierà con la **struttura ad albero** del progetto analizzato, per dare subito un contesto architetturale. Il nome dei file verrà costruito secondo il template definito nella configurazione.


## 3. Descrizione: Il Pieno Controllo del Contesto

Gli assistenti AI integrati nel nostro editor, come GitHub Copilot, sono diventati dei potentissimi "piloti automatici" per lo sviluppo. Analizzano il nostro codice in tempo reale e, con grande efficacia, decidono quale contesto recuperare dal progetto per rispondere alle nostre domande. Sono progettati per essere veloci, convenienti e per ridurre al minimo l'intervento manuale.

Hyperlisa nasce da una filosofia differente e complementare, basata non sull'automazione, ma sul **controllo deliberato da parte dello sviluppatore**. Non si propone di sostituire questi strumenti, ma di offrire una console di regia per tutti quei casi in cui è il programmatore, e non l'assistente, a voler dettare le regole del gioco.

Il vantaggio di Lisa si riassume in una parola: **controllo**.

### 3.1. Controllo su *Cosa* Condividere

Mentre un assistente inline utilizza euristiche per decidere quali snippet di codice inviare al modello, Lisa ti dà il potere di creare un "dossier" di analisi con una precisione chirurgica.

* **Focus Mirato**: Invece di far cercare all'IA un ago in un pagliaio, sei tu a darle solo gli aghi di cui ha bisogno. Hai un bug nell'interfaccia? Crea un profilo che includa solo i componenti UI e i relativi stili. Stai ottimizzando una query? Fornisci solo i modelli e il data-access layer. Questo riduce il rumore e permette all'LLM di concentrarsi sul problema specifico con una chiarezza assoluta.

* **Privacy e Sicurezza Garantite**: Con i profili di Lisa, puoi escludere in modo esplicito e garantito qualsiasi file o cartella contenente segreti, dati sensibili o algoritmi proprietari. Hai la certezza matematica di cosa stai inviando al modello, senza doverti affidare alle policy di esclusione, a volte opache, di uno strumento terzo.

* **Contesto Deterministico**: L'input che fornisci all'LLM non è un costrutto dinamico e potenzialmente variabile assemblato da un algoritmo, ma un artefatto stabile e riproducibile. Sai esattamente cosa sta "vedendo" il modello in ogni momento.

### 3.2. Controllo sulla *Sessione* di Lavoro

Questo è forse l'aspetto più potente. Il file generato da Lisa non è solo un input, ma una **baseline stabile** per un'intera sessione di lavoro con l'LLM.

Questo permette di trasformare una semplice chat in una vera e propria **sessione di refactoring stateful**. L'intera conversazione con il modello diventa una "patch" vivente applicata virtualmente al codice sorgente originale che gli hai fornito.

Considera questo flusso di lavoro:

1.  **Tu**: "*Ecco il codice del mio backend.*" (carichi il file generato da Lisa).
2.  **LLM**: "*Ok, ho analizzato l'intero backend. Cosa vuoi fare?*"
3.  **Tu**: "*Nella classe `UserManager`, riscrivi la funzione `get_user` in modo che sia asincrona.*"
4.  **LLM**: "*Fatto. Ecco la nuova funzione asincrona. Ho notato che questo richiederà una modifica anche nel controller che la invoca.*"
5.  **Tu**: "*Ottima osservazione. Mostrami anche come aggiornare il controller, tenendo conto della modifica che abbiamo appena discusso.*"

In questo dialogo, l'LLM non sta ricaricando il contesto a ogni domanda. Sta mantenendo lo stato delle modifiche richieste e ragiona in modo incrementale sulla baseline stabile che gli hai fornito all'inizio. Diventa un partner di refactoring consapevole dell'evoluzione della conversazione.

In sintesi, Hyperlisa non è un copilota, è la tua **console di regia**. Ti mette al posto di comando, dandoti il controllo totale sul contesto per analisi profonde, refactoring complessi e interazioni mirate con i modelli di linguaggio più avanzati.

## 4. Installazione e Configurazione Dettagliata

Questa sezione ti guiderà passo dopo passo nell'installazione di Lisa e nella configurazione del tuo ambiente di lavoro, sia che tu stia partendo da zero o aggiornando un progetto esistente.

### 4.1. Prerequisiti

Prima di iniziare, assicurati di avere sul tuo sistema:

  * Python 3.6 o superiore. 
  * Un editor di codice come Visual Studio Code. 
  * Accesso a un terminale o prompt dei comandi.

### 4.2. Installazione del Pacchetto

L'installazione di Lisa avviene tramite `pip`, il gestore di pacchetti standard di Python. Apri il terminale nella cartella radice del tuo progetto e digita:

```bash
pip install hyperlisa
```

Questo comando installerà l'ultima versione di Lisa e renderà disponibili i suoi comandi nel tuo ambiente.

### 4.3. Configurazione di un Progetto

Una volta installato il pacchetto, devi configurare il tuo progetto. Lo scenario cambia a seconda che tu sia un nuovo utente o stia aggiornando da una versione precedente.

#### 4.3.1. Scenario 1: Nuovo Progetto (`hyperlisa-configure`)

Se stai iniziando un nuovo progetto con Lisa, il setup è immediato. Esegui questo comando:

```bash
hyperlisa-configure
```

Questo comando esegue le seguenti operazioni:

1.  **Crea una cartella nascosta `.hyperlisa`** nella root del tuo progetto. 
2.  **Copia un file di esempio `config.yaml`** al suo interno. Questo file contiene una configurazione di default completa e commentata, pronta per essere personalizzata.
3.  **Aggiorna il file `.gitignore`**, se presente, per assicurarsi che la cartella `.hyperlisa` venga ignorata dal controllo di versione.

#### 4.3.2. Scenario 2: Migrazione di un Progetto Esistente (`hyperlisa-migrate`)

Se usavi già Lisa (v1.x) su un progetto, dopo aver aggiornato il pacchetto con `pip install --upgrade hyperlisa`, devi eseguire una sola volta il comando di migrazione:

```bash
hyperlisa-migrate
```

Questo strumento automatizzato si occuperà di:

1.  **Rinominare** la vecchia cartella di configurazione `hyperlisa` in `.hyperlisa`.
2.  **Aggiornare** il `.gitignore` con il nuovo nome della cartella.
3.  **Leggere** il tuo vecchio file di configurazione e **convertirlo** al nuovo formato, creando un profilo di default chiamato `migrated_default` e facendo un backup del vecchio file.

### 4.4. Struttura del File di Configurazione (`.hyperlisa/config.yaml`)

Il cuore della flessibilità di Lisa risiede nel suo file di configurazione. La nuova struttura ti dà un controllo granulare su cosa includere e come generare i dossier di analisi.

#### 4.4.1. Visione d'insieme

Il file è organizzato in sezioni principali:

  * `log_level`: Imposta il livello di dettaglio dei messaggi durante l'esecuzione (es. `INFO`, `DEBUG`). 
  * `variables`: Un'area dove definire ancore YAML per riutilizzare liste e valori.
  * `global_excludes`: Una lista di file e cartelle da ignorare *sempre*, in ogni profilo.
  * `profiles`: La sezione principale dove definisci i tuoi profili di analisi.

#### 4.4.2. La sezione `global_excludes` e la Logica di Matching

Qui puoi elencare tutto ciò che non vuoi mai vedere nei tuoi file di analisi. La logica per distinguere file e cartelle è stringente:

  * Un pattern che **termina con `/`** (es. `__pycache__/`) viene considerato **esclusivamente una cartella**.
  * Un pattern che **non termina con `/`** (es. `*.log`) viene considerato **esclusivamente un file**.

#### 4.4.3. La sezione `variables`

Per evitare ripetizioni, puoi usare le ancore YAML. Ad esempio:

```yaml
variables:
  PYTHON_FILES: &py_files ["*.py"]

...
# in un profilo
includes: *py_files
```

#### 4.4.4. La sezione `profiles`

Questa sezione contiene due elementi:

  * `name_template`: Un template per definire come verranno nominati i file di output. Utilizza i placeholder `$n` (nome progetto), `$p` (nome profilo) e `$ts` (timestamp).
  * `profiles_list`: La lista vera e propria dei tuoi profili di analisi.

#### 4.4.5. Dettaglio di un Profilo

Ogni profilo nella `profiles_list` è un oggetto con tre chiavi:

  * `name`: Un nome descrittivo per il profilo (es. `backend`, `frontend`).
  * `enable`: Un booleano (`true`/`false`) per attivare o disattivare il profilo senza doverlo cancellare.
  * `blocks`: Una lista di "blocchi" di regole di analisi.

#### 4.4.6. Dettaglio di un Blocco

Ogni blocco definisce un set di regole da applicare a uno o più percorsi:

  * `paths`: Una lista di oggetti che specificano i percorsi da analizzare.
  * `includes`: Una lista di pattern per i file da includere in quei percorsi.
  * `excludes`: Una lista di pattern per file/cartelle da escludere specificamente per quei percorsi.

#### 4.4.7. Il controllo di profondità (`depth`)

All'interno di `paths`, ogni oggetto definisce il percorso e la profondità della scansione:

```yaml
paths:
  - { path: "/app/services/", depth: 0 }
  - { path: "/app/utils/", depth: "*" }
```

  * `depth: 0`: Analizza solo i file presenti nella cartella specificata, senza entrare nelle sottocartelle.
  * `depth: N` (es. `1`, `2`, ...): Analizza fino a N livelli di profondità.
  * `depth: "*"`: Analizza senza limiti di profondità (scansione ricorsiva completa).

#### 4.4.8. Esempio di un file `config.yaml` completo

```yaml
# Hyperlisa v2.1 Configuration File
log_level: INFO

variables:
  PYTHON_EXT: &py_files ["*.py"]
  FRONTEND_EXT: &web_files ["*.css", "*.js", "*.html"]

global_excludes:
  - "__pycache__/"
  - ".vscode/"
  - ".git/"
  - "venv/"
  - ".hyperlisa/"

profiles:
  name_template: "$n_$p_$ts"
  profiles_list:
    - name: "backend"
      enable: true
      blocks:
        - paths: 
            - { path: "/app/", depth: "*" }
          includes: *py_files
          excludes:
            - "static/"
            - "tests/"
    - name: "frontend_shallow"
      enable: true
      blocks:
        - paths:
            - { path: "/app/static/", depth: 0 }
          includes: *web_files
          excludes:
            - "svg/"
```


## 5. Utilizzo Avanzato (CLI)

Una volta che hai messo a punto il tuo file `config.yaml`, interagire con Lisa dal terminale è un'operazione semplice e potente. La Command-Line Interface (CLI) ti offre la flessibilità di generare i dossier di analisi esattamente come ti servono, a seconda del contesto e dei tuoi obiettivi.

### 5.1. Riepilogo dei Comandi

Tutti i comandi vanno eseguiti dalla cartella radice del tuo progetto.

* **`cmb`**
    Questo è il comando di default, il più comune. Senza nessun argomento, Lisa scorrerà il tuo `config.yaml`, identificherà **tutti i profili abilitati** (`enable: true`) e genererà un file di testo separato per ciascuno di essi. È il modo perfetto per creare diverse "viste" del tuo progetto in un colpo solo.

* **`cmb <nome_profilo>`**
    Quando hai bisogno di un'analisi specifica, questo è il comando che fa per te. Sostituisci `<nome_profilo>` con il `name` esatto di uno dei profili definiti nel tuo `config.yaml`. Lisa ignorerà tutti gli altri e processerà solo quello richiesto, generando un unico file di output. È l'ideale per iterare rapidamente su un set di file mirato.

* **`cmb --merge-all`**
    Questo comando è pensato per creare il "dossier definitivo". Lisa processerà, come per il comando di default, tutti i profili abilitati, ma invece di creare file separati, **unirà tutto il codice raccolto in un unico, grande file di testo**. È la soluzione perfetta quando vuoi dare a un LLM la visione più completa possibile dell'intero sistema che hai configurato, senza suddivisioni.

### 5.2. Gestione dell'Output

Capire dove finiscono i file generati e come vengono nominati è fondamentale.

* **Posizione dei File**
    Per mantenere la cartella principale del tuo progetto pulita e ordinata, **tutti i file di testo generati da Lisa vengono salvati all'interno della cartella `.hyperlisa`**.

* **Nomenclatura dei File**
    Il nome di ogni file viene costruito dinamicamente seguendo la regola definita nel `name_template` all'interno del tuo `config.yaml`. Questo template utilizza dei placeholder speciali:
    * `$n`: Verrà sostituito con il **nome del progetto** (il nome della cartella radice, in maiuscolo).
    * `$p`: Verrà sostituito con il **nome del profilo** (`name`) che ha generato il file.
    * `$ts`: Verrà sostituito con il **timestamp** (data e ora) della generazione del file.

    Ad esempio, con un template come `"$n-$p_$ts"`, eseguendo il profilo `backend` sul progetto `MIO-PROGETTO` si potrebbe ottenere un file chiamato `MIO-PROGETTO-backend_20250620_2300.txt`.

    Quando si usa `--merge-all`, il placeholder `$p` viene semplicemente ignorato, producendo un nome file generico come `MIO-PROGETTO_20250620_2300.txt`.

### 5.3. Opzioni Aggiuntive

Puoi aggiungere i seguenti flag opzionali a qualsiasi comando `cmb` per modificarne il comportamento:

* **`--notree`**
    Utilizza questo flag per sopprimere la generazione della struttura ad albero all'inizio del file di output. È utile quando vuoi un dossier più snello o quando il contesto della struttura non è necessario. Esempio: `cmb --merge-all --notree`.

* **`--clean`**
    Prima di eseguire la generazione, questo comando cercherà ed eliminerà tutti i file di analisi (`.txt`) creati in precedenza nella cartella `.hyperlisa`. Ti verrà chiesta una conferma prima della cancellazione. È perfetto per fare pulizia prima di una nuova analisi. Esempio: `cmb --clean`.


## 6. Utilizzare il File Generato con gli LLM

Il file di testo generato da Lisa è la chiave per sbloccare un'analisi del codice profonda e interattiva con qualsiasi Large Language Model (LLM) moderno, come ChatGPT, Claude o Gemini. Caricando questo "dossier" completo, fornisci al modello una visione d'insieme senza precedenti, permettendogli di ragionare sull'architettura, sulle dipendenze e sulle logiche complesse del tuo progetto.

### 6.1. Vantaggi di Questo Approccio

  * **Accesso alle Ultime Funzionalità**: L'LLM può analizzare il codice più recente, anche se non è stato ancora documentato, fornendoti un vantaggio sulla comprensione delle API emergenti.
  * **Comprensione Profonda**: Avendo accesso al codice sorgente completo e strutturato, l'intelligenza artificiale può offrire suggerimenti molto più precisi e contestualizzati rispetto a quando analizza snippet isolati.
  * **Debugging Efficace**: Se riscontri un problema, puoi chiedere all'LLM di analizzare le implementazioni specifiche e le loro interazioni per aiutarti a identificare la causa principale.
  * **Personalizzazione Informata**: Puoi creare soluzioni personalizzate basate sulle reali implementazioni interne della libreria che stai studiando, non solo sulle sue API pubbliche.
  * **Contesto Architettonurale Immediato**: Grazie alla struttura ad albero inserita all'inizio del file, l'LLM ha subito una mappa completa del progetto, portando a una comprensione più rapida e a risposte di alto livello più accurate.

### 6.2. Esempi di Prompt

Una volta caricato il file `.txt` generato da Lisa nella chat del tuo LLM preferito, puoi iniziare a porre domande. Ecco alcuni esempi, dal generale allo specifico.

**Prompt di Partenza (per iniziare la sessione)**

```
Ho generato un'analisi completa del codice sorgente di questo progetto usando Hyperlisa. Il file che ti ho fornito contiene la struttura completa e tutti i riferimenti necessari. Ora, per favore, analizza la struttura del codice e preparati a rispondere alle mie domande. 
```

**Per Analisi Architetturale**

```
1. Basandoti sulla struttura ad albero che vedi all'inizio del file, descrivi l'architettura generale di questo progetto.
2. Identifica i moduli principali e disegnami un diagramma (in formato Mermaid o PlantUML) che mostri le loro dipendenze.
3. Basandoti sul codice, qual è il modo migliore per implementare [descrivi il tuo caso d'uso]?
```

**Per Comprendere Funzionalità Esistenti**

```
Analizza come questo progetto implementa la gestione della memoria nelle conversazioni. Voglio capire come ottimizza l'uso dei token.Puoi spiegarmi la logica e fornirmi un esempio di implementazione basato sul codice attuale? 
```

**Per Implementare Nuove Funzionalità**

```
Basandoti sul codice sorgente fornito, aiutami a creare un agente personalizzato che:
1. Accede a un database SQL.
2. Elabora query in linguaggio naturale.
3. Genera ed esegue le query SQL appropriate.
4. Formatta i risultati in modo leggibile per l'utente.
Mostrami il codice necessario, utilizzando i componenti più adatti che trovi nel progetto.
```

**Per il Refactoring**

```
Ho bisogno di rinominare la classe `OldClassName` in `NewClassName`. Analizza l'intero codice che ti ho fornito e elencami, file per file, tutti i punti che dovrò modificare per completare questo refactoring.
```

### 6.3. Suggerimenti per un Uso Efficace

Per ottenere il massimo dalle tue sessioni di analisi, tieni a mente questi consigli:

1.  **Sii Specifico**: Descrivi chiaramente il tuo obiettivo e le funzionalità che desideri ottenere.
2.  **Chiedi Spiegazioni**: Se un suggerimento non è chiaro, chiedi all'LLM di spiegarti il funzionamento interno di quella parte di codice.
3.  **Itera**: Usa le risposte dell'LLM come punto di partenza per raffinare le tue domande e arrivare a soluzioni migliori.
4.  **Verifica Sempre**: Testa il codice generato dall'intelligenza artificiale e chiedi chiarimenti se incontri errori.
5.  **Esplora Alternative**: Chiedi all'LLM di proporti approcci diversi per risolvere lo stesso problema, basandosi sempre sul codice sorgente fornito



## 7. Contribuire al Progetto

Lisa è un progetto aperto e ogni contributo è più che benvenuto. Se ti piace l'idea e vuoi aiutare a migliorarla, ci sono molti modi per partecipare:

* Aprire segnalazioni (issues) per riportare bug o proporre nuove funzionalità. 
* Proporre richieste di integrazione (pull request) con miglioramenti o correzioni. 
* Migliorare la documentazione per renderla ancora più chiara e completa. 
* Condividere i tuoi casi d'uso, i tuoi suggerimenti e i dossier di analisi più interessanti che hai creato. 

## 8. Licenza

Il progetto è rilasciato sotto licenza MIT.

Copyright (c) 2024 

È concesso gratuitamente il permesso a chiunque ottenga una copia di questo software e dei relativi file di documentazione (il "Software"), di trattare il Software senza restrizioni, inclusi, senza limitazioni, i diritti di utilizzare, copiare, modificare, unire, pubblicare, distribuire, concedere in sublicenza e/o vendere copie del Software, e di permettere alle persone a cui il Software è fornito di farlo, alle seguenti condizioni:

L'avviso di copyright sopra riportato e questo avviso di permesso devono essere inclusi in tutte le copie o parti sostanziali del Software.

IL SOFTWARE VIENE FORNITO "COSÌ COM'È", SENZA GARANZIE DI ALCUN TIPO, ESPLICITE O IMPLICITE, INCLUSE, MA NON SOLO, LE GARANZIE DI COMMERCIABILITÀ, IDONEITÀ PER UN PARTICOLARE SCOPO E NON VIOLAZIONE. IN NESSUN CASO GLI AUTORI O I TITOLARI DEL COPYRIGHT SARANNO RESPONSABILI PER QUALSIASI RECLAMO, DANNO O ALTRA RESPONSABILITÀ, SIA IN UN'AZIONE DI CONTRATTO, ILLECITO O ALTRO, DERIVANTE DA, FUORI O IN CONNESSIONE CON IL SOFTWARE O L'USO O ALTRE OPERAZIONI NEL SOFTWARE. 