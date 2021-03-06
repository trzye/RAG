NAZWA
     rag – rozproszony algorytm genetyczny

WYWOŁANIE

     rag [-f funkcja][-o liczba_osobników][-p liczba_pokoleń]
         [-w sposób_wyboru][-m współczynnik_mutacji]
         [-k współczynnik_krzyżowania][-x serwer]
         [-t liczba wątków]
OPIS

     rag to rozproszony program wykorzystujący bibliotekę parall-
     el python(http://www.parallelpython.com) do wykonywania alg-
     orytmu genetycznego z wykorzystaniem wielu maszyn jednocześ-
     nie

WYMAGANE ARGUMENTY

     -f funkcja
          do wyboru jedna z dwóch funkcji, których minimum będzie
          poszukiwane
          f1:
            f(a,b,c) = 4a + 6c – 15a^2 – 20b^2 – 6a^3 – 70
            a<-5; 10>, b<-15;8>, c<-1;7>
          f2:
            f(a,b,c) = 4cos(a) + 6cos(c) – 20b^2 + 3a^3 – 70
            a<-5; 10>, b<-2; 4>, c<-3; 7>

     -o liczba_osobników
          liczba osobników, którzy zostaną wylosowani w początko-
          wej generacji

     -p liczba_pokoleń
          liczba pokoleń, ilość iteracji algorytmu w poszukiwaniu
          optymalnego rozwiązania

     -w sposób_wyboru
          sposób wyboru osobników do następnego przetwarzania:
          wlp – wybór losowy z powtórzeniami
          wlr – wybór losowy według reszt bez powtórzeń
          wd  – wybór deterministyczny

     -m współczynnik_mutacji
          Wartość w przedziale <0,1> określająca jaki procent os-
          obników będzie podlegał mutacji przed kolejnym przetwa-
          rzaniem

     -k współczynnik_krzyżowania
          Wartość w przedziale <0,1> określająca jaki procent os-
          obników będzie podlegał operacji krzyżowania przed kol-
          ejnym przetwarzaniem

 DODATKOWE ARGUMENTY
 
     -s sposób_skalowania
          jeżeli opcja nie zostanie wybrana wyniki funkcji przys-
          stosowania nie będą skalowane. Możliwe skalowania:
          lin – skalowanie liniowe
          pot – potęgowe
          log - logarytmiczne

     -n nazwa_pliku
          nazwa pliku, do którego zostaną zapisane informacje o
          wyniku przetwarzania (jeżeli nie, to na stdout zostanie
          wypisane krótkie podsumowanie przetwarzania

     -x serwer
          adres serwera, na którym uruchomiony jest ppserver.py
          np. 192.168.0.1 lub 192.168.0.1:60123

     -t liczba wątków
          liczba wątków, z którymi chcemy uruchomić program
          domyślnie 1
