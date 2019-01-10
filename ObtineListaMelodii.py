'''
Created on Nov 3, 2017

@author: Pita
'''
maiSuntMelodiiInBazaDate = False

def hammingDistance(hash1,hash2):
    return bin(hash1^hash2).count('1')
def obtineLSV(hashLista1,hashLista2):
    rezervat={}
    rezervatOpus={}
    if len(hashLista1)>len(hashLista2):
        aux=hashLista2[:]
        hashLista2=hashLista1[:]
        hashLista1=aux[:]
    for jt in range(len(hashLista2)):
        minimLocal=10000
        for it in range(len(hashLista1)):
            hD=hammingDistance(hashLista1[it], hashLista2[jt])
            if hD<minimLocal:
                if it not in rezervat and jt not in rezervatOpus:
                    minimLocal=hD
                    rezervat[it]=[jt,hD]
                    rezervatOpus[jt]=[it,hD]
                elif it not in rezervat and jt in rezervatOpus:
                    minimLocal=hD
                    itFolosit=rezervatOpus[jt][0]
                    del rezervat[itFolosit]
                    rezervat[it]=[jt,hD]
                    rezervatOpus[jt]=[it,hD]
                elif it in rezervat and jt not in rezervatOpus:
                    if hD<rezervat[it][1]:
                        minimLocal=hD
                        jtFolosit=rezervat[it][0]
                        del rezervatOpus[jtFolosit]
                        rezervat[it]=[jt,hD]
                        rezervatOpus[jt]=[it,hD]
                elif it in rezervat and jt in rezervatOpus:
                    if hD<rezervat[it][1]:
                        minimLocal=hD
                        itFolosit=rezervatOpus[jt][0]
                        jtFolosit=rezervat[it][0]
                        del rezervat[itFolosit]
                        del rezervatOpus[jtFolosit]
                        rezervat[it]=[jt,hD]
                        rezervatOpus[jt]=[it,hD]       
    nefolosite=[]
    nefolositeOpus=[]
    for it in range(len(hashLista1)):
        if it not in rezervat:
            nefolosite.append(it)
    for jt in range(len(hashLista2)):
        if jt not in rezervatOpus:
            nefolositeOpus.append(jt)
    for it in nefolosite:
        minimLocal=10000
        for jt in nefolositeOpus:
            hD=hammingDistance(hashLista1[it], hashLista2[jt])
            if hD<minimLocal:
                if it not in rezervat and jt not in rezervatOpus:
                        minimLocal=hD
                        rezervat[it]=[jt,hD]
                        rezervatOpus[jt]=[it,hD]
                elif it not in rezervat and jt in rezervatOpus:
                    continue
                elif it in rezervat and jt not in rezervatOpus:
                        minimLocal=hD
                        jtFolosit=rezervat[it][0]
                        del rezervatOpus[jtFolosit]
                        rezervat[it]=[jt,hD]
                        rezervatOpus[jt]=[it,hD]
                elif it in rezervat and jt in rezervatOpus:
                    continue
    factorSimilaritate=0
    for jt in rezervat.values():
        factorSimilaritate+=jt[1]
    return factorSimilaritate
                    
def comparaDouaMelodi(hashMelodie1,hashMelodie2):
    if len(hashMelodie1) > 2 * len(hashMelodie2):
        l1=len(hashMelodie1)
        l2=len(hashMelodie2)
        repet=l1/l2
        minim=100000
        for jt in range(repet):
            hashLista1=hashMelodie1[jt*l2:(jt+1)*l2]
            f1=obtineLSV(hashLista1,hashMelodie2)
            if f1 <minim:
                minim = f1
        return minim
    elif len(hashMelodie2) > 2 * len(hashMelodie1):
        l2=len(hashMelodie2)
        l1=len(hashMelodie1)
        repet=l2/l1
        minim=100000
        for jt in range(repet):
            hashLista2=hashMelodie2[jt*l1:(jt+1)*l1]
            f1=obtineLSV(hashLista2,hashMelodie1)
            if f1 <minim:
                minim = f1
        return minim
    else: 
        return obtineLSV(hashMelodie1,hashMelodie2)
  
def obtineListaMelodii(hashMelodie,listaToateMelodii):
    #try:
        listaMelodiiSimilare=[]
        listaMelodii=listaToateMelodii[:]
        for melodie in listaMelodii:
            print 1
            print melodie
            if melodie[1]!="":
                listaMelodiiSimilare.append([melodie[0],comparaDouaMelodi(hashMelodie,melodie[1])])
        listaMelodiiSimilare.sort(key=lambda x: x[1])
        ids=zip(*listaMelodiiSimilare)[0]
        return 1,ids
    #except Ee:
        return 0,"Nu pot compara melodiile\n"
    
#print obtineListaMelodii([10013364834065278146, 9967859125754084315, 12170243889404886791, 9291901772450860611, 9240473084208896727, 11722086860206387099, 12300539642624332758, 11535822745950318202, 12262616905769282679, 11724491363107331193, 9862111314923587870, 11571606055169849735, 12149897406223110733, 9371973940503719776, 11684565615698308871, 9279688620841409211, 9294631541024479865, 9421028335455308389, 12169123368248695770, 9844078115603014476, 9273934794310144612, 9252532954287340206, 9960627032555353479, 9396662145990405654, 12112217564487236037, 9261374680046532050, 9423986415075296459, 11743588154242733099, 12310914727646495102, 9973776081333222809, 9975060126399418088, 9418939595630878155, 9802075961903693147, 11733898268184694092, 11687277731312130875, 9810768329716162267, 11700339270561040277, 9997232787689039367, 12264339965287930207, 12170339802042768692, 9812425666580286845, 10007779550122673255],[[5, [9839210661711109634, 9389351214501817946, 9995253354549626766, 11579441399051427561, 12135621297420335009, 12176498395595212490, 10002563295665361755, 9816333723181692045, 9998016419525981495, 12164132883917837018, 11729752594223303254, 11684247220519063131, 11714736515771674985, 9277966832660570574, 12158719625694963057, 9389749928186561226, 12165759147652272322, 11683770965569968636, 11536247485421949404, 9418590838437644178, 11739646232798829339, 11569174232363031703, 12170629550670703009, 11546409036121652933, 12113694530727912028, 11532269658515840893, 11731231048829834338, 9870270099455568406, 11547485239388915421, 11731259371804791252, 10003217998375862518, 12113129998355760993, 9382949842887253558, 9867007854276889234, 9260657075226242907, 9250392694577819864, 9437929390404890155, 9290007811707479581, 9233324635040458540, 12131723410790512465, 9868714019297054156, 9994018972797238490, 11584166672636001885, 11598409031483026394, 9401960638693479380, 9820938656979434599, 11541969187344716641, 11716136309368375225, 12266427962652082386, 9291685887768058935, 11585562796794358815, 12156533408873150893]], [8, [11553366837669173044, 11568545304962903330, 9242872130165435623]]])