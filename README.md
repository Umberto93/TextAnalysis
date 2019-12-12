# KENCY APP

## AVVIO DEL SISTEMA

Avviare la classe main.py; una volta avviata l'applicazione verrà caricata l'ontologia (of4-ontology.owl), se presente, altrimenti verrà creata ex novo. In console sarà possibile monitorare l'avanzamento della fase di inizializzazione del sistema. A questo punto il sistema sarà operativo e verrà avviata l'interfaccia grafica.
L'operazione di creazione dell'ontologia potrebbe richiedere un paio di minuti a causa delle nuomerose richieste necessarie per processare l'intero dataset. È necessario pertanto disporre di una connessione Internet.


## UTILIZZO DEL SISTEMA

Una volta avviata l'interfaccia grafica, l'utente potrà accedere ai seguenti servizi:

- Articles: consultare la lista di articoli relativi alla categoria in esame e accedere ai dettagli di ogni singolo documento nonché filtrare gli articoli per keywords o categoria. Non è possibile specificare più di tre keywords nella barra di ricerca. Inoltre, per avviare la ricerca, è necessario cliccare sull'icona simboleggiante la lente di ingrandimento;

- Text Processing: inserire il testo di un documento da processare al fine di ottenerne la categoria, le keyowrds, le entità e gli eventuali articoli correlati. All'interno della textarea è necessario inserire un testo di lunghezza non inferiore ai 140 caratteri e che rispetta la codifica UTF-8;

- Query Builder: eseguire query SPARQL utilizzando le clausole SELECT e ASK in quanto le uniche due che abbiamo scelto di supportare. 
NB: La libreria owlready2 non permettere di specificare query utilizzando la clausola HAVING;

- About Us: informazioni sul progetto e sugli autori.


## REFACTOR DELL'ONTOLOGIA

I documenti caricati dall'utente vengono salvati all'interno di una cartella chiamata user_docs contenente le stesse cartelle del dataset.
In alcune circostanze potrebbe essere necessario ricreare nuovamente l'ontologia in quanto: 

- Il classificatore non è in grado di riconoscere correttamente i documenti forniti in input. In questo caso sarà a cura dell'utente smistare gli articoli nell'opportuna categoria (qualora presente, ovvero nella relativa cartella all'interno del dataset);
- L'utente potrebbe voler arricchire il dataset. Anche in questo caso si vede necessario un intervento manuale da parte dell'utente il quale dovrà spostare i documenti nella relativa cartella all'interno del dataset.

Dopo aver spostato tutti i documenti, bisognerà cancellare la precedente ontologia e riavviare il sistema. 

**ATTENZIONE: non cancellare o alterare in alcun modo la struttura o i nomi delle cartelle contenente i documenti (dataset, user_docs)!**

**Fantastici 4**
- _D'Amico Stefano_
- _Fusco Laura_
- _Iennaco Umberto_
- _Magna Vincenzo_
