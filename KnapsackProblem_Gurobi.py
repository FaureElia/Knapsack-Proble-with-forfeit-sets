from mip import *;
import winsound
import time

m=Model("Knapsack problem",solver_name=GRB)
start=time.process_time()
#Lettura da file
input=open("C:/python/TesiKnapSackProblem/example_intance_2.txt")
dati_iniziali=input.readline().split()

items=range(int(dati_iniziali[0]))
dati_iniziali[0]=int(dati_iniziali[0])
subset=range(int(dati_iniziali[1]))
subset_number=int(dati_iniziali[1])
capacity=int(dati_iniziali[2])
threshold=round(dati_iniziali[0]/15,0)
#threshold per scenario 1-2
#if ((int)(dati_iniziali[0])==300):
 #   threshold=round(dati_iniziali[0]/15,0)
#if ((int)(dati_iniziali[0])==500):
 #   threshold=round(dati_iniziali[0]/25,0)
#if ((int)(dati_iniziali[0])==700):
 #   threshold=round(dati_iniziali[0]/35,0)
#if ((int)(dati_iniziali[0])==800):
 #   threshold=round(dati_iniziali[0]/45,0)
#if ((int)(dati_iniziali[0])==1000):
 #   threshold=round(dati_iniziali[0]/55,0)


#leggo profitti
profits=input.readline().split()
for i in items:
    profits[i]=int(profits[i])

#leggo pesi
weights=input.readline().split()
for i in items:
    weights[i]=int(weights[i])

#leggo subset
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

print("---- STAMPO A VIDEO DIZIONARI---")
print("-- proprietà (hmax,penalità,cardinalità)--")
print (dizionario_proprietaSubset)
print("-- composizione (items presenti in ogni subset)--")
print(dizionario_composizioneSubset)
print()
input.close()

#inserisco variabili nel modello.

#creo delle variabili binarie a 2 indici che mi permettono di capire se un dato item è stato preso
#inserisco le variabili in un dizionario che mi permette di contare tutte le variabili

#DIZIONARIO PER L'ACCESSO AGLI ITEMS
x={}
for i in items:
    x[i]=m.add_var(var_type=BINARY,name="x[%d]"%(i))

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


m.objective=maximize(xsum(profits[i]*x[i] for i in items)
                     -xsum(dizionario_proprietaSubset[s][1]*viol[s] for s in subset))

start=time.perf_counter()
m.optimize(max_seconds=300)
end=time.perf_counter()
print("tempo:",end-start)



winsound.MessageBeep()

# stampo a video la soluzione ottenuta
print("\n---STAMPO SOLUZIONE OTTENUTA---")
#for i in items:
   #print(x[i]," valore ",x[i].x)
count_tot_violazioni=0
for s in subset:
    #print(viol[s], "numero violazioni", viol[s].x)
    if (viol[s].x>=1):
       count_tot_violazioni+=viol[s].x


finale=xsum(profits[i]*x[i].x for i in items)-xsum(dizionario_proprietaSubset[s][1]*viol[s].x for s in subset)
print("valore funzione obiettivo: ", finale,"| con ",count_tot_violazioni," violazioni totali con un limite di ",threshold,"violazioni")
spazio_occupato=0
profitto=0
lista_test=[]
for i in items:
    if (x[i].x==1):
        lista_test.append(i)
        spazio_occupato+=weights[i]
        profitto+=profits[i]
print("---STAMPO A VIDEO PARAMETRI DEFINITIVI---")
print("tot_violazioni: %d | spazio_occupato: %d | profitto: %d "%(count_tot_violazioni,spazio_occupato,profitto))
print("limite_violazioni: %d | capacita: %d "%(threshold ,capacity))

print(lista_test)

