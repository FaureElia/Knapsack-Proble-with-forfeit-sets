#Lettura da file
from builtins import sorted
import time
from mip import *
import winsound

#PROVO A DEFINIRE LE FUNZIONI PRINCIPALI
#-----------------------------------------------------------------------------------------------------------#
def ordino_in_rapporti(indice):
    #ordino gli items per rapporti profitti*somma/numeroSubset delle soglie dei subset in cui è. In questo caso
    #un item che è presente in pochi items con soglia molto alta è preferibile!
    lista_rapporti=[]
    for i in items:
        somma=0
        count=0
        for s in subset:
            if (i in dizionario_composizioneSubset[s]):
                somma=somma+dizionario_proprietaSubset[s][indice]
        if(indice==0):#algoritmo somma_limiti
            lista_rapporti.append(profits[i]*somma/(weights[i]))
        elif (indice==1):#algoritmo somma_penalita
            lista_rapporti.append(profits[i]/(weights[i]*somma))
        else: #algoritmo profitto/peso
            lista_rapporti.append(profits[i]/(weights[i]))

    lista_rapporti_ordinati=sorted(lista_rapporti,reverse=True)
    dizionario_rapporti={}

    for element in lista_rapporti_ordinati:
        if(lista_rapporti.count(element)==1):
            indice=lista_rapporti.index(element)
            dizionario_rapporti[indice]=element
        elif(lista_rapporti.count(element)>1):
            lista_posizioni=[]
            for i in range(len(lista_rapporti)):
                if (lista_rapporti[i]==element):
                    lista_posizioni.append(i)
            for pos in lista_posizioni:
                dizionario_rapporti[pos]=element
    print("verifica lunghezza dizionario: ",len(dizionario_rapporti))
    return dizionario_rapporti

#-----------------------------------------------------------------------------------------------------------------------
#definisco una funzione che valuta se conviene inserire l'item oppure no. Decido che conviene inserire l'item se il profitto che si ottiene
# è maggiore della penalita che sarebbe causata dal suo inserimento
def conviene(item):
    profitto=profits[item]
    possibile_perdita=0;
    presence_subsets=[]
    for s in subset:
        if (item in dizionario_composizioneSubset[s]):
            presence_subsets.append(s)
    for set in presence_subsets:
        if (viol[set]>=dizionario_proprietaSubset[set][0]):
            possibile_perdita=possibile_perdita+dizionario_proprietaSubset[set][1]
    if (profitto>possibile_perdita):
        #print("potrei prendere l'item ", item," perchè profitto=%d e perdita_stimata:%d"%(profitto,possibile_perdita))
        return True;
    else:
        #print("NON prendo l'item ", item," perchè profitto=%d e perdita_stimata:%d"%(profitto,possibile_perdita))
        #print(presence_subsets)
        return False;
#--------------------------------------------------------------------------------------------------------------------
#definisco una funzione che controlla il valore delle violazioni totali!

def limite_superato(item,violazioi_totali):
    violazioni_causate=0
    violazioni_disponibili=threshold-violazioni_totali
    presence_subsets=[]
    for s in subset:
        if (item in dizionario_composizioneSubset[s]):
            presence_subsets.append(s)
    for set in presence_subsets:
        if (viol[set]>=dizionario_proprietaSubset[set][0]):
            violazioni_causate=violazioni_causate+1
    if (violazioni_causate>violazioni_disponibili):
        return -1;
    else:
        #print("l'item ",item," si potrebbe prendere perchè %d violazioni causate e %d violazioni disponibili"%(violazioni_causate,violazioni_disponibili))
        return violazioni_causate;
#------------------------------------------------------------------------------------------------------------------------------------------
#INIZIO ADESSO CON LA LETTURA DA FILE

input=open("")





dati_iniziali=input.readline().split()

items=range(int(dati_iniziali[0]))
subset=range(int(dati_iniziali[1]))
subset_number=int(dati_iniziali[1])
capacity=int(dati_iniziali[2])
dati_iniziali[0]=int(dati_iniziali[0])
#threshold per scenario 1-2
#if ((int)(dati_iniziali[0])==300):
 #   threshold=round(dati_iniziali[0]/15,0)
#elif ((int)(dati_iniziali[0])==500):
#    threshold=round(dati_iniziali[0]/25,0)
#elif ((int)(dati_iniziali[0])==700):
#    threshold=round(dati_iniziali[0]/35,0)
#elif ((int)(dati_iniziali[0])==800):
#   threshold=round(dati_iniziali[0]/45,0)
#elif ((int)(dati_iniziali[0])==1000):
 #   threshold=round(dati_iniziali[0]/55,0)
#else:
 #   threshold=6;
threshold=round(dati_iniziali[0]/15,0)

risultati=[]#creo lista dove memorizzo tutti i risultati

#leggo profitti
profits=input.readline().split()
for i in items:
    profits[i]=int(profits[i])

#leggo pesi
weights=input.readline().split()
for i in items:
    weights[i]=int(weights[i])

#LEGGO SUBSET
## in particolare sto creando 2 dizionari, uno che mi fornisce le proprietà del subset, l'altro che contiene tutti gli elementi contenuti nel subset
## le chiavi sono uguali per entrambi i dizionari

dizionario_composizioneSubset={}
dizionario_proprietaSubset={}
count_subset=-1
for i in range(subset_number*2):
    if (i%2==0):
        count_subset=count_subset+1
        prop=input.readline().split()
        for i in range(3):
            prop[i]=int(prop[i])
        dizionario_proprietaSubset[count_subset]=prop
    else:
        elements=input.readline().split()
        for j in range(dizionario_proprietaSubset[count_subset][2]):
            elements[j]=int(elements[j])
        dizionario_composizioneSubset[count_subset]=elements

#print("---- STAMPO A VIDEO DIZIONARI---")
#print("-- proprietà (hmax,penalità,cardinalità)--")
#print (dizionario_proprietaSubset)
#print("-- composizione (items presenti in ogni subset)--")
#print(dizionario_composizioneSubset)
print()
input.close()
start=time.perf_counter()
print("*****************************")
print("---ALGORITMO SOMMA_LIMITI---")
print("*****************************")
dizionario_rapporti=ordino_in_rapporti(0)

#print("---- STAMPO A VIDEO LISTA DEI RAPPORTI ORDINATA IN ORDINE CRESCENTE---")
#print(dizionario_rapporti)

#DIZIONARIO PER L'ACCESSO AGLI ITEMS
x={}
for i in items:
    x[i]=0

#creo delle variabili che contano il numero di violazioni all'interno di un singolo subset.
#il numero di variabili di questo tipo sarà pari al numero di subset.

#DIZIONARIO PER L'ACCESSO AL SUBSET
viol={}
for i in subset:
    viol[i]=0


somma_pesi=0
funzione_obiettivo=0
profitto=0
violazioni_totali=0
for item in dizionario_rapporti.keys():
    violazioni_aggiunte=limite_superato(item,violazioni_totali)
    conv=conviene(item)
    if (weights[item]<=capacity-somma_pesi and conv and violazioni_aggiunte!=-1):
        #print("item preso, aggiorno valore delle violazioni totali")
        violazioni_totali=violazioni_totali+violazioni_aggiunte
        print(violazioni_totali)
        somma_pesi=somma_pesi+weights[item]
        x[item]=1
        profitto=profitto+profits[item]
        #conto l'incremento di violazione in ogni subset
        for i in subset:
            if (item in dizionario_composizioneSubset[i]):
                viol[i]=viol[i]+1;

penalita=0
for i in subset:
    if (dizionario_proprietaSubset[i][0]<viol[i]):
        penalita=penalita+dizionario_proprietaSubset[i][1]*(viol[i]-dizionario_proprietaSubset[i][0])
lista_violazioni=[]
for s in subset:
    lista_violazioni.append(max(dizionario_proprietaSubset[s][0]-viol[s],0))

lista_SL=[]
spazio_occupato=0
for i in items:
    if (x[i]==1):
        lista_SL.append(i)
        spazio_occupato+=weights[i]

print("LISTA_SL")
print(lista_SL)

risultato_SL =profitto-penalita;
risultati.append(risultato_SL)
print("---STAMPO A VIDEO LA FUNZIONE OBIETTIVO E I VALORI TROVATI---")
print("valore funzione obiettivo: ", risultato_SL)
#print("valore penalità: ",penalita)
#print("valore profitto: ",profitto)
#print("---VALORI BINARI DELLE VARIABILI---")
#print(x)
#print("---VALORI INTERI DELLE VIOLAZIONI PER OGNI SUBSET---")
#print(lista_violazioni)
print("---VALORI DELLE VIOLAZIONI TOTALI---")
print(violazioni_totali, " vs ",threshold," ammesse")
print("---CAPACITA OCCUPATA---")
print(spazio_occupato, " vs ",capacity," disponibile")

print("*****************************")
print("---ALGORIMTO SOMMA PENALITA---")
print("*****************************")
dizionario_rapporti=ordino_in_rapporti(1)

#DIZIONARIO PER L'ACCESSO AGLI ITEMS
x={}
for i in items:
    x[i]=0

#creo delle variabili che contano il numero di violazioni all'interno di un singolo subset.
#il numero di variabili di questo tipo sarà pari al numero di subset.

#DIZIONARIO PER L'ACCESSO AL SUBSET
viol={}
for i in subset:
    viol[i]=0


somma_pesi=0
profitto=0
violazioni_totali=0
for item in dizionario_rapporti.keys():
    violazioni_aggiunte=limite_superato(item,violazioni_totali)
    conv=conviene(item)
    if (weights[item]<=capacity-somma_pesi and conv and violazioni_aggiunte!=-1):
        #print("item preso, aggiorno valore delle violazioni totali")
        violazioni_totali=violazioni_totali+violazioni_aggiunte
        #print(violazioni_totali)
        somma_pesi=somma_pesi+weights[item]
        x[item]=1
        profitto=profitto+profits[item]
        #conto l'incremento di violazione in ogni subset
        for i in subset:
            if (item in dizionario_composizioneSubset[i]):
                viol[i]=viol[i]+1;

penalita=0
for i in subset:
    if (dizionario_proprietaSubset[i][0]<viol[i]):
        penalita=penalita+dizionario_proprietaSubset[i][1]*(viol[i]-dizionario_proprietaSubset[i][0])

lista_violazioni=[]
for s in subset:
    lista_violazioni.append(max(viol[s]-dizionario_proprietaSubset[s][0],0))

lista_SP=[]
spazio_occupato=0
for i in items:
    if (x[i]==1):
        lista_SP.append(i)
        spazio_occupato+=weights[i]

print("LISTA_SP")
print(lista_SP)

risultato_SP =profitto-penalita;
risultati.append(risultato_SP)
print("---STAMPO A VIDEO LA FUNZIONE OBIETTIVO E I VALORI TROVATI---")
print("valore funzione obiettivo: ", risultato_SP)
#print("valore penalità: ",penalita)
#print("valore profitto: ",profitto)
#print("---VALORI BINARI DELLE VARIABILI---")
#print(x)
#print("---VALORI INTERI DELLE VIOLAZIONI PER OGNI SUBSET---")
#print(lista_violazioni)
print("---VALORI DELLE VIOLAZIONI TOTALI---")
print(violazioni_totali, " vs ",threshold," ammesse")
print("---CAPACITA OCCUPATA---")
print(spazio_occupato, " vs ",capacity," disponibile")

print("*****************************")
print("---ALGORIMTO PROFITTO/PESO---")
print("*****************************")
dizionario_rapporti=ordino_in_rapporti(-1)

#DIZIONARIO PER L'ACCESSO AGLI ITEMS
x={}
for i in items:
    x[i]=0

#creo delle variabili che contano il numero di violazioni all'interno di un singolo subset.
#il numero di variabili di questo tipo sarà pari al numero di subset.

#DIZIONARIO PER L'ACCESSO AL SUBSET
viol={}
for i in subset:
    viol[i]=0


somma_pesi=0
profitto=0
violazioni_totali=0
for item in dizionario_rapporti.keys():
    violazioni_aggiunte=limite_superato(item,violazioni_totali)
    conv=conviene(item)
    if (weights[item]<=capacity-somma_pesi and conv and violazioni_aggiunte!=-1):
        #print("item preso, aggiorno valore delle violazioni totali")
        violazioni_totali=violazioni_totali+violazioni_aggiunte
        #print(violazioni_totali)
        somma_pesi=somma_pesi+weights[item]
        x[item]=1
        profitto=profitto+profits[item]
        #conto l'incremento di violazione in ogni subset
        for i in subset:
            if (item in dizionario_composizioneSubset[i]):
                viol[i]=viol[i]+1;

penalita=0
for i in subset:
    if (dizionario_proprietaSubset[i][0]<viol[i]):
        penalita=penalita+dizionario_proprietaSubset[i][1]*(viol[i]-dizionario_proprietaSubset[i][0])

lista_violazioni=[]
for s in subset:
    lista_violazioni.append(max(viol[s]-dizionario_proprietaSubset[s][0],0))

lista_PP=[]
spazio_occupato=0
for i in items:
    if (x[i]==1):
        lista_PP.append(i)
        spazio_occupato+=weights[i]

print("LISTA_PP")
print(lista_PP)

risultato_PP =profitto-penalita;
risultati.append(risultato_PP)
print("---STAMPO A VIDEO LA FUNZIONE OBIETTIVO E I VALORI TROVATI---")
print("valore funzione obiettivo: ", risultato_PP)
#print("valore penalità: ",penalita)
#print("valore profitto: ",profitto)
#print("---VALORI BINARI DELLE VARIABILI---")
#print(x)
#print("---VALORI INTERI DELLE VIOLAZIONI PER OGNI SUBSET---")
#print(lista_violazioni)
print("---VALORI DELLE VIOLAZIONI TOTALI---")
print(violazioni_totali, " vs ",threshold," ammesse")
print("---CAPACITA OCCUPATA---")
print(spazio_occupato, " vs ",capacity," disponibile")

#CONTROLLO ALGORITMO MIGLIORE:
if (risultato_SL==max(risultati)):
    print("miglior risultato dato da somma_limiti, ", risultato_SL)
    miglior_risultato=risultato_SL
    miglior_soluzione=lista_SL
elif (risultato_SP==max(risultati)):
    print("miglior risultato dato da somma_penalita, ", risultato_SP)
    miglior_risultato=risultato_SP
    miglior_soluzione=lista_SP
else:
    print("miglior risultato dato da profitto/peso ", risultato_PP)
    miglior_risultato=risultato_PP
    miglior_soluzione=lista_PP

rimanenti=[]
for i in items:
    if (i not in miglior_soluzione):
        rimanenti.append(i)

#AGGIORNO I VALORI FINALI
x={}
for i in items:
    if (i in miglior_soluzione):
        x[i]=1
    else:
        x[i]=0

viol={}

for s in subset:
    viol[s]=0
    for element in miglior_soluzione:
        if (element in dizionario_composizioneSubset[s]):
            viol[s]+=1


#EFFETTUO RICERCA LOCALE DELLA SOLUZIONE, PROVANDO A PERTURBARE!

print("--- TENTATIVO MIGLIORARE SOLUZIONE---")

print("---STAMPO A VIDEO LISTA DEGLI ELEMENTI CHE VOGLIO PROVARE AD AGGIUNGERE ORDINAT0 SECONDO IL CRITERIO INIZIALE ---")
print(rimanenti)

#provo adesso a fare un ulteriore passo.
#---------------------------------------------------------------------------------------------------------------------------
# devo creare una funzione che mi calcola in fretta lo spazio occupato

def calcolaSpazioOccupato(lista_elementi):
    spazio_occupato=0
    for i in lista_elementi:
        spazio_occupato+=weights[i]
    return spazio_occupato



#ed ho inoltre bisogno di una funzione che conta le violazioni totali di un item

def aggiornoViolazioni(lista):
    daTogliere=lista[0]
    daMettere=lista[1]
    for s in subset:
        if (daTogliere in dizionario_composizioneSubset[s]):
            viol[s]-=1;
        if (daMettere in dizionario_composizioneSubset[s]):
            viol[s]+=1







def funzioneObiettivoFinale(lista):
    profitto=0
    penalita=0
    spazio_occupato=0
    tot_violazioni=0
    for s in subset:
        violazioni_subset=max(viol[s]-dizionario_proprietaSubset[s][0],0)
        if(violazioni_subset!=0):
            penalita+=violazioni_subset*dizionario_proprietaSubset[s][1]
            tot_violazioni+=violazioni_subset
    for oggetto in lista:
            profitto+=profits[oggetto]
    print("rsultato_finale: ",profitto-penalita)
    print("tot violazioni: ", tot_violazioni," vs ",threshold,"(limite)")









def calcolaFunzioneObiettivo(daMigliorare,daTogliere,daMettere,funzione_obiettivo):
    profitto=0
    penalita=0
    spazio_occupato=0
    tot_violazioni=0
    #prendo tutti i sottoset in cui è presente il mio item che volgio togliere e tolgo una violazione se l'it3m esce,
    # ne aggiungo una se l'item entra
    for s in subset:
        if (daTogliere in dizionario_composizioneSubset[s]):
            viol[s]-=1;
        if (daMettere in dizionario_composizioneSubset[s]):
            viol[s]+=1
        violazioni_subset=max(viol[s]-dizionario_proprietaSubset[s][0],0) # SE VIOLAZIONI< LIMITE--> PENALITA' NULLA
        if(violazioni_subset!=0):
            penalita+=violazioni_subset*dizionario_proprietaSubset[s][1]
            tot_violazioni+=violazioni_subset
    spazio_occupato=capacity-spazio_libero+weights[daMettere]-weights[daTogliere]
    #backtracking
    for s in subset:
            if (daTogliere in dizionario_composizioneSubset[s]):
                viol[s]+=1;
            if (daMettere in dizionario_composizioneSubset[s]):
                viol[s]-=1
    if (tot_violazioni>threshold):
        #print("troppe violazioni")
        return -1;
    elif(spazio_occupato>capacity):
       # print("troppo spazio")
        return -1;
    else:
        #print("sol accettabile")
        profitto=0
        for oggetto in daMigliorare:
            if (oggetto!= daTogliere):
                profitto+=profits[oggetto]
        profitto+=profits[daMettere]
        risultato=profitto-penalita

    if (risultato>funzione_obiettivo):
            return risultato
    else:
            return -1
#-------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------
#ALGORITMO PER IL MIGLIORAMENTO DELLA SOLUZIONE TROVATA
best_bound=miglior_risultato
miglior_soluzione_trovata=list(miglior_soluzione)
flagStop=False
soluzioni_provate=set()#CREO SET PER EVITARE DI PROVARE PIU' VOLTE LA STESSA SOLUZIONE
spazio_libero=capacity-calcolaSpazioOccupato(miglior_soluzione_trovata)
ultimo_cambiamento=list()
# A QUESTO PUNTO VOGLIO PORVARE A SOSTITUIRE GLI ITEMS!
while(flagStop!=True and time.perf_counter()-start<400 ):#il ciclo procede fino a quando si trovano soluzioni migliori
    #print("PROVA MIGLIORAMENTO ",miglior_soluzione_trovata)
    lista_possibili_soluzioni=[]
    for item in miglior_soluzione_trovata: #PROVO A SOSTITUIRE OGNI ITEM CON TUTTI GLI ALTRI
        if(time.perf_counter()-start>400):
                break;
        for r in rimanenti:
            if(time.perf_counter()-start>400):
                break;
            migliorato=list(miglior_soluzione_trovata) #COPIO LA MIGLIOR SOLUZIONE TROVATA
            #print("prova tolgo %d metto %d"%(item,r))
            if (weights[r]<=spazio_libero+weights[item]):#ci sta l'item!!

                risultato=calcolaFunzioneObiettivo(miglior_soluzione_trovata,item,r,best_bound)

                if (risultato!=-1):
                    best_bound=risultato;
                    migliorato.remove(item)
                    migliorato.append(r)
                    lista_possibili_soluzioni.append([migliorato,risultato])
                    ultimo_cambiamento=[item,r] #tolto,messo-> SALVO IN UN VETTORE L'ULTIMO SCAMBIO EFFETTUATO
                    print("SOLUZIONE MIGLIORATA",risultato)
                    print("---SPAZIO_OCCUPATO: ",capacity-spazio_libero)

    if(len(lista_possibili_soluzioni)!=0):# SIAMO ANCORA ALL'INTERNO DEL WHILE
        rimanenti=[]
        #partirò da quesa soluzione, aggiorno  i valori
        aggiornoViolazioni(ultimo_cambiamento)# SARA' SICURAMENTE IL MIGLIOR RISULTATO TROVATO FINORA
        spazio_libero=spazio_libero+weights[ultimo_cambiamento[0]]-weights[ultimo_cambiamento[1]]
        miglior_soluzione_trovata=lista_possibili_soluzioni[len(lista_possibili_soluzioni)-1][0]
        #devo aggiornare le violazioni
        print("miglior_soluzione_trovata aggiornata!",miglior_soluzione_trovata)
        for i in items:
            if (i not in miglior_soluzione_trovata):
                rimanenti.append(i)
    else:#SE NON HO MIGLIORATO LA SOLUZIONE MI FERMO!
        flagStop=True; #vincolo di uscita!
end=time.perf_counter()

print("lista_finale_da_testare:",miglior_soluzione_trovata)
print("****************************************************************")
print("---RISULTATI FINALI---")
if(miglior_soluzione_trovata!=miglior_soluzione):
    print("Soluzione migliorata DEFINITIVAMENTE")
    print(funzioneObiettivoFinale(miglior_soluzione_trovata)," VS ", miglior_risultato )
    print(" TEMPO impiegato: ",(end-start))
    print("totale spazio occupato: ", capacity-spazio_libero,"vs capacità di:",capacity)



#introduco controllo con gurobi

#DIZIONARIO PER L'ACCESSO AGLI ITEMS
m=Model("Knapsack problem",solver_name=GRB)
lista_da_testare=miglior_soluzione_trovata

x={}
for i in items:
    if (i in lista_da_testare):
        x[i]=m.add_var(var_type=BINARY,name="x[%d]"%(i),lb=0.9)
    else:
        x[i]=m.add_var(var_type=BINARY,name="x[%d]"%(i),ub=0.9)

#creo delle variabili che contano il numero di violazioni all'interno di un singolo subset.
#il numero di variabili di questo tipo sarà pari al numero di subset.

#DIZIONARIO PER L'ACCESSO AL SUBSET
viol={}
for i in subset:
    #il numero di violazioni può essere al massimo capacita_subset-numero_massimo_items_prelevabili
    uBound=dizionario_proprietaSubset[i][2]-dizionario_proprietaSubset[i][0]
    viol[i]=m.add_var(var_type=INTEGER, name="v[%d]"%(i), lb=0, ub=uBound)

#posso adesso scrivere i vincoli

#vincolo budget dello zaino ∑𝑤𝑗𝑥𝑗 ≤b
m+=xsum(weights[i]*x[i] for i in items)<=capacity, "vincolo_capacità_zaino"

#vincolo soglia di violazioni massime ∑𝑣𝑖 ≤k
m+= xsum(viol[i] for i in subset)<=threshold, "vincolo_violazioni_totali"

#vincolo che conta il numero di violazioni per ogni subset
#sum(xj-vi)<=hi per ogni subset
#in altre parole sum(xj-hi)<=vi, cioè se il numero di items presi dal subset è minore del numero massimo
#di violazioni, allora vi sarà inizializzata a 0( nessuna violazione). In caso contrario il numero di
#violazioni sarà pari alla differenza tra gli items presi dal subset e il numero di item prelevabili senza
#creare una violazione

#devo creare un vincolo per ogni subset.
for s in subset:
    somma=0
    v=viol[s]
    listaItems=dizionario_composizioneSubset[s]
    h=dizionario_proprietaSubset[s][0]

    m+=(xsum(x[i] for i in items if (i in listaItems)))-v<=h, "vincolo_violazioni_subset_%d"%(s)

#creo la funzione obiettivo
#  max ∑ 𝑝𝑗𝑥𝑗 − ∑di𝑣i
#in altre parole sto massimizzando la differenza tra il profitto ottenuto e la penale totale da pagare ( data dalla somma delle singole penali)


m.optimize(max_seconds=300)



winsound.MessageBeep()

# stampo a video la soluzione ottenuta
print("\n---STAMPO SOLUZIONE OTTENUTA---")
#for i in items:
   #print(x[i]," valore ",x[i].x)
count_tot_violazioni=0
for s in subset:
    #print(viol[s], "numero violazioni", viol[s].x)
    if (viol[s].x!=0):
       count_tot_violazioni+=viol[s].x


finale=xsum(profits[i]*x[i].x for i in items)-xsum(dizionario_proprietaSubset[s][1]*viol[s].x for s in subset)
print("valore funzione obiettivo: ", finale,"| con ",count_tot_violazioni," violazioni totali con un limite di ",threshold,"violazioni")

spazio_occupato=0
profitto=0
lista_risultato=[]
for i in items:
    if (x[i].x==1):
        lista_risultato.append(i)
        spazio_occupato+=weights[i]
        profitto+=profits[i]
print(lista_risultato)
print("---STAMPO A VIDEO PARAMETRI DEFINITIVI---")
print("tot_violazioni: %d | spazio_occupato: %d | profitto: %d "%(count_tot_violazioni,spazio_occupato,profitto))
print("limite_violazioni: %d | capacita: %d "%(threshold ,capacity))

print("STAMPO FUNZIONE OBIETTIVO")
funzione_obb=""
for i in items:
    if (x[i].x==1):
        funzione_obb+="+"+str(profits[i])+"("+str(i)+")"
print(funzione_obb)
print("*************************************************************************************************")
print("RISULTATO CORRETTO")
print("valore trovato: ", best_bound, "gurobi: ",finale)
print("count tot violazioni", count_tot_violazioni, " vs ",threshold)
print("spazio occupato: ", capacity-spazio_libero,",gurobi ",spazio_occupato)
print("tempo impiegato: ", end-start)

