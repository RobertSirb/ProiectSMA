# ProiectSMA
Algoritmul de recunoastere a melodie a fost implementat conform descrierii gasite in la : coding-geek.com/how-shazam-works


In linii mari acesta functioneaza in felul urmator:

	1.Pentru fiecare aprox. 0.1 secunde de melodie inregistreaza se aplica FastFourierTransform , se creaza astfel spectrul aplitudinii raportat la frecventa.
  
	2.Pentru fiecare 0.1 secunde de melodie se alege frecventa cu aplitudinea cea mai mare si se face media tuturor astfel de frecvente pentru toata melodia
  
	3.Pentru fiecare spectru se tin minte doar frecventele si momentul in timp al acelor frecvnete ce au aplitudinea mai mare decat o constanca c1 * media tuturor frecventelor.
  
	4.Cu lista de puncte (frecventa,moment de timp ) se creaza zone tinte formata din 5 asemenea puncte consecutive  ( ordonate dupa timp si dupa frecventa). Fiecare zona tinta are o ancora , si anume punctul ce are indexul = indexul primului punct in zona -3
  
	5.Pentru fiecare zona tinta si pentru fiecare punct din acea zona tinta se creaza o adresa de forma :
  
						[frecventa ancorei; frecventa punctului , diferenta de timp intre ancora si  punct]  -> [timpul absolut a ancorei in inregistrare]
            
	6.Baza de date este de forma :
  
						[frecventa ancorei; frecventa punctului , diferenta de timp intre ancora si  punct] -> [timpul absolut al ancorei in melodie, indexulMelodiei]
            
	7.Petru fiecare adresa din inregistreaza , aceasta se foloseste drept cheie pentru a gasi toate tuplurile [timp absolut al ancorei in melodie, indexulMelodiei] ce corespun acelei adrese
  
	8.Fiind folosit un dictionare, cautarea se face in O(n) unde n reprezita numarul de adrese din inregistrare. Astfel e deosebit de eficient, si chiar pentru un numar foarte mare de adrese in care se cauta, ( peste 600.000)timpul cel mai mare e consumat tot de transformata Fourieri
  
	9.Se tin minte doar melodiile al caror index apare de mai mult decat o constanta c2 * numarul total de adrese din inregistrare
  
  10.Pentru fiecare melodie cu index ce se gaseste in cele gasite si pentru fiecare adresa se calculeaza delta = timpul absolut al ancorei in inregistrare - timpul absolut al ancorei in melodie
  
  11.Melodia recunoscuta va fi cea pentru care apare valoarea delta cel mai des .
  
  
Algoritmul de similirite functioneaza in felul urmator :

	1. Pentru fiecare aprox 0.1 secunde de melodie se alica transforamata fourier si se obtine astfel spectrul
  
	2. Pentru fiecare spectru se tine minte doar frecventa cea mai dominanta din intervalul :
  
	3. Cu lista de frecvente domintante se creza o imagine alb negru , ce are pixel colorat negru la coordonatele(t,f) unde e t e momentul de timp al frecventei in melodie , si f e valoarea frecventei
  
	4. Pe imaginea creata se aplica metoda de perceptualHash pentru a returna o lista de hash-uri ce caracterizeaza melodia
  
	5. Pentru fiecare melodie din baza de data  , se compara lista  hashuri acelei melodii cu lista de hashuri tuturor celorlalte melodii din baza de data
  
	6. Compatia se face folosind dinstanta Hamming , pentru a da un factor de similaritate intre cele doua hashuri .
  
	7. Valoarea de similaritate va fi suma acelei permutari de hashuri care genereaza valoarea cea mai mare
  
	8. Melodiile se ordoneaza descrescator dupa valoarea factorului de similairate si se tin minte cele mai mari 3 valori
	
  
Baza de data e formata din 3 parti:

	1. Lista de [frecventa ancorei; frecventa punctului , diferenta de timp intre ancora si  punct] -> [timpul absolut al ancorei in melodie, indexulMelodiei]
  
	2. Lista [index Melodie] -> [numele melodiei]
  
	3. Lista [indexul Melodiei]->[Index Melodie similara1; Index Melodie similara2; Index Melodie similara3]
  
	
Fisiere folosite :

	1.BazaDeDateRefractor.py : Incarca din memorie la pornirea server-ului cele 3 liste , si are functii de get si set pentru indexul/numele melodiei , respectiv functii ce implementeaza algoritmul de recunoastere de la pasul 7-10
  
	2.BazaDeDateCreator.py : Adauga in baza de date o melodie noua, creaza pentru ea lista de adrese , si index
  
	3.codRefractor.py  : Simuleaza un mini server. Asculta constant modificari in firebase si cand se adauga o melodie noua , citeste bytes inregistrati si returneaza numele melodiei respectiv melodiile similare
  
	4.ExecutaFFT.py : Pntru o lista de short-s ce reprezinta inregistrarea melodiei executa transformata Fouriere
  
	5.ObtineHash.py : Ia spectrele unei melodii si le transforma in imagini si genereaza perceptualHash pe ele
  
	

	
	
