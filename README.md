
<h1 align = "center"> Nacin pokretanja </h1>

## Requiremets
<p align = "left">

Kako bi preuzeli igru, mozete jednostavno klonirati repozitorijum na vasem racunaru, ili skinuti zipovan projekat. Kako bi instalirali sve biblioteke i pokrenuli igru pomocu nekog od okruzenja koje podrzava Python, morate uraditi sledece.

  - Pozicionirate se gde se nalazi nasa igra, tacnije folder requirements.txt
  - Otvorite tu cmd i ukucate sledece:
  ```sh
$ pip install -r requirements.txt
```

## Pokretanje aplikacije
Potrebno je da se pozicionirate u okvir direktorijuma vas_path/Connect-Four/ koji ste prethodno skinuli/klonovali. A potom na sledeci nacin mozete pokrenuti aplikaciju:
```sh
$ python igra.py
```

 </p>


<h1 align = "center"> Nacin igranja </h1>
<p align = "left">
  
Igranje je vrlo intuitivno, pomeranjem misa levo desno mozete da izaberete kolonu u koju zelite da spustite token(ZETON), klikom na kolonu automatski ce se popuniti prvi slobodan red sa zetonom, zatim je na redu implementirani AI algoritam i tako nazimenicno se smenjujte. Ko ce biti prvi na potezuje AI ili Vi, o tome odlucuje RANDOM generator. 
  
  </p>

<h1 align = "center"> Ukratko o projektu </h1>

Igra sadrži dva moda, pri pokretanju korisniku iskače dialog u kom korisnik bira da li želi da koristi MOD1 ili MOD2 


<p align="center">

  <img width="400" height="200" src="https://user-images.githubusercontent.com/49925421/75761761-e97ca300-5d39-11ea-89d5-49454ecfb2cb.png">

</p>

<p align="center">

  <img width="400" height="750" src="https://user-images.githubusercontent.com/49925421/75762342-cdc5cc80-5d3a-11ea-87c5-acc87e0e2d4d.png">

</p>

Upotpunosti je implementiran MIN-MAX algoritam sa alpha-beta odsecanjem stabla, da bi postigli brze pretraživanje stabla. 

<p align="center">

  <img width="500" height="250" src="https://user-images.githubusercontent.com/49925421/75762813-94da2780-5d3b-11ea-91aa-5d74644278b8.png">

</p>

Ako korisnik izabere MOD1 imaće priliku da iskusi pravu moć MIN-MAX algoritma i da se iskuša protiv skoro nepobedivog algoritma, u tom modu korisnik može da potraži pomoć numerike, tj implementirali smo (***linearnu regresiju sa Ridge and Lasso regularizacijom***)

MOD1 nam ujedno služi i za prikupljanje trening seta podataka koji koristimo da bi napravili što bolje predviđanje uz pomoć regresije. Pamtimo odluke MIN-MAX algoritma i te podatke koristimo za regresiju.
Podaci se čuvaju u .CSV formatu i pri svakom novom pokretanju programa ponovo se učitavaju. Regresiju izvršavamo nad tim podacima.


Ideja projekta je da se regresija koristi kao mali pomoćnik u borbi protiv AI algoritma, svi su svesni da numerika nije ni približno moćna za predviđanje kao MIN MAX algoritam, ali ako iskoristimo tog malog pomoćnika i našu moć razmišljanja možemo vrlo jako da pariramo AI algoritmu. Klikom na dugme "POMOC NUMERIKE" korisnik dobija predlog po predjasnjem iskustvu numerike gde bi bilo najbolje da korisnik odigra sledeci potez.

<p align="center">

  <img width="600" height="750" src="https://user-images.githubusercontent.com/49925421/75765091-3dd65180-5d3f-11ea-815d-a3214310e37a.png">

</p>

Takođe korisnik ako želi može da se oproba u igri protiv numerike, ako pri pokretanju igre izabere MOD2.

Igra sadrži i edukativni sadržaj, tj želeli smo da korisnicima malo približimo regresiju i regularizaciju, klikom na dugme "PRINCIPI NUMERIKE" korisniku isače dialog u kom je u kratkim crtama objašnjena regresija i regularizacija koja šljaka ispod haube.

![image](https://user-images.githubusercontent.com/49925421/75764556-52661a00-5d3e-11ea-96f9-c5a3f5f58f2a.png)

Korisniku je u svakom trenutku dostupan trening set podataka koji se obnavlja pri zavrsetku svake igre u MOD-u 1. Klikom na dugme "TRAINING DATA SET" korisniku dobija prikaz 6 različitih dijagrama, radi demonstracije kako parametar alpha utiče na fitovanje u podatke samim tim i na predviđanje.

![image](https://user-images.githubusercontent.com/49925421/75765528-f4d2cd00-5d3f-11ea-9fa9-1ae395871fca.png)

Igra sadrži i simulaciju fizike. Simuliramo odskakanje tokena, niti se uspavljuju na odredjeno vreme tako da korisniku nije dozvoljeno da odigra sledeci potez dok token ne zavrsi sa simulacijom fizike.

<p align="center">

  <img width="300" height="200" src="https://user-images.githubusercontent.com/49925421/75765882-804c5e00-5d40-11ea-9c14-fb9566f700f8.png">

</p>

