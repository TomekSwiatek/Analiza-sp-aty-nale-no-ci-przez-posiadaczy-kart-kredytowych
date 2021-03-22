# Analysis-of-debt-repayment-by-credit-card-holders
Project made in Databricks using PySpark.

The actual main file with the extension .py.

### Wstęp

Posiadacze kart kredytowych są klientami dużego bank komercyjnego w Tajwanie działającego na rynku kredytów w tym m.in. wydającego karty kredytowe dla swoich klientów. Zadanie polega optymalizacji dochodów banku od obecnych klientów, którzy posiadają kartę kredytową. Firma dysponuje bazą 30 000 klientów. Celem projektu jest wykonanie analizy zbioru danych i zbadanie, którzy kliencie (o jakich cechach) mają największą szanse na niespłacenie kredytu w przyszłym miesiącu co pozwoli wyznaczyć wystąpienie niewypłacalności klienta.

Wyniki analizy oprócz samej oceny spłaty przez klientów należności w przyszłym miesiącu na obecnej karcie kredytowej mogą być wykorzystane do oceny wniosku o wydanie nowej karty kredytowej oraz wykorzystane do ogólnej oceny wiarygodności klienta np. przy przyznawaniu kredytu konsumpcyjnego lub przy dostosowaniu ofert innych produktów bankowych. Podczas procesu wydawania karty kredytowej pracownik banku może podjąć decyzje o przyznaniu lub odmowie przyznania karty kredytowej osobie wnioskującej. Za przypadek pozytywny uznajemy zdarzenie niespłacenia zobowiązania przez klienta banku {1}, a brak zdarzenia niespłacenia za zdarzenie negatywne {0}.

###Opis zbioru danych

W projekcie zostały użyte dane pochodzące ze strony https://archive.ics.uci.edu/ml/datasets/default+of+credit+card+clients.

Autorem danych jest I-Cheng Yeh z Department of Information Management, Chung Hua University, Taiwan. Dane dotyczą zaległości w spłatach przez klientów banku na Tajwanie.

Opis zbioru danych:

- Ilość obserwacji: 30000,
- Typy atrybutów: liczby zmiennoprzecinkowe (Real), liczby całkowite (Integer),
- Ilość atrybutów: 24,
- Data dodania: 26.01.2016,
- Braki w danych: Brak.

Opis atrybutów:

- Y: Zmienna objaśniana określająca zdarzenie pozytywne - brak spłaty zobowiązania w kolejnym miesiącu (październiku 2005) (1=Tak, 0=Nie),
- ID: Kolejny numer wiersza
- LIMIT_BAL: Limit przyznanego kredytu w TWD (dolar tajwański) (uwzględnia daną osobę i jej najbliższą rodzinę),
- SEX: Płeć (1 = mężczyzna; 2 = kobieta),
- EDUCATION: Wykształcenie (1 = wyższe pełne (graduate school); 2 = wyższe; 3 = średnie; 4 = inne),
- MARRIAGE: Stan cywilny (1 = zamężna/żonaty; 2 = wolny; 3 = inny),
- AGE: Wiek (w latach),
- PAY_0 - PAY_6: Historia poprzednich spłat od kwietnia 2005 do września 2005, podana w następujący sposób: PAY_0 = stan spłaty we wrześniu 2005; PAY_2 = stan spłaty w sierpniu 2005 ... PAY_6 = stan spłaty w kwietniu 2005 (-1 = płatność w terminie; 1 = opóźnienie o 1 miesiąc; 2 = opóźnienie o 2 miesiące; ... ; 9 = opóźnienie o 9 miesięcy lub więcej). Dodatkowo występują wartości -2 i 0, których interpretacja podana jest jako: -2 i 0 = nie ma żadnego salda płatności.
- BILL_AMT1 - BILL_AMT6: Wartość na wyciągu w TWD (BILL_AMT1 = wyciąg za wrzesień 2005; BILL_AMT2 = wyciąg za sierpień 2005; ... ; BILL_AMT6 = wyciąg za kwiecień 2005),
- PAY_AMT1 - PAY_AMT6: Wartość poprzednich płatności (PAY_AMT1 = suma płatności we wrześniu 2005, PAY_AMT2 = suma płatności w sierpniu 2005; ... ; PAY_AMT6 = suma płatności w kwietniu 2005).


