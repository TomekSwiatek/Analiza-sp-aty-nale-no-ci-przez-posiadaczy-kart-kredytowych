# Databricks notebook source
# MAGIC %md #Analiza spłaty należności przez posiadaczy kart kredytowych.

# COMMAND ----------

# MAGIC %md ###Wstęp
# MAGIC 
# MAGIC Posiadacze kart kredytowych są klientami dużego bank komercyjnego w Tajwanie działającego na rynku kredytów w tym m.in. wydającego karty kredytowe dla swoich klientów. Zadanie polega optymalizacji dochodów banku od obecnych klientów, którzy posiadają kartę kredytową. Firma dysponuje bazą 30 000 klientów. Celem projektu jest wykonanie analizy zbioru danych i zbadanie, którzy kliencie (o jakich cechach) mają największą szanse na niespłacenie kredytu w przyszłym miesiącu co pozwoli wyznaczyć wystąpienie niewypłacalności klienta.
# MAGIC 
# MAGIC Wyniki analizy oprócz samej oceny spłaty przez klientów należności w przyszłym miesiącu na obecnej karcie kredytowej mogą być wykorzystane do oceny wniosku o wydanie nowej karty kredytowej oraz wykorzystane do ogólnej oceny wiarygodności klienta np. przy przyznawaniu kredytu konsumpcyjnego lub przy dostosowaniu ofert innych produktów bankowych. Podczas procesu wydawania karty kredytowej pracownik banku może podjąć decyzje o przyznaniu lub odmowie przyznania karty kredytowej osobie wnioskującej. Za przypadek pozytywny uznajemy zdarzenie niespłacenia zobowiązania przez klienta banku {1}, a brak zdarzenia niespłacenia za zdarzenie negatywne {0}.
# MAGIC 
# MAGIC ###Opis zbioru danych
# MAGIC 
# MAGIC W projekcie zostały użyte dane pochodzące ze strony https://archive.ics.uci.edu/ml/datasets/default+of+credit+card+clients.
# MAGIC 
# MAGIC Autorem danych jest I-Cheng Yeh z Department of Information Management, Chung Hua University, Taiwan.
# MAGIC Dane dotyczą zaległości w spłatach przez klientów banku na Tajwanie.
# MAGIC 
# MAGIC Opis zbioru danych:
# MAGIC 
# MAGIC - Ilość obserwacji: 30000,
# MAGIC - Typy atrybutów: liczby zmiennoprzecinkowe (Real), liczby całkowite (Integer),
# MAGIC - Ilość atrybutów: 24
# MAGIC - Data dodania: 26.01.2016
# MAGIC - Braki w danych: Brak
# MAGIC 
# MAGIC Opis atrybutów:
# MAGIC 
# MAGIC - Y: Zmienna objaśniana określająca zdarzenie pozytywne - brak spłaty zobowiązania w kolejnym miesiącu (październiku 2005) (1=Tak, 0=Nie),
# MAGIC - ID: Kolejny numer wiersza
# MAGIC - LIMIT_BAL: Limit przyznanego kredytu w TWD (dolar tajwański) (uwzględnia daną osobę i jej najbliższą rodzinę),
# MAGIC - SEX: Płeć (1 = mężczyzna; 2 = kobieta),
# MAGIC - EDUCATION: Wykształcenie (1 = wyższe pełne (graduate school); 2 = wyższe; 3 = średnie; 4 = inne),
# MAGIC - MARRIAGE: Stan cywilny (1 = zamężna/żonaty; 2 = wolny; 3 = inny),
# MAGIC - AGE: Wiek (w latach),
# MAGIC - PAY_0 - PAY_6: Historia poprzednich spłat od kwietnia 2005 do września 2005, podana w następujący sposób: PAY_0 = stan spłaty we wrześniu 2005; PAY_2 = stan spłaty w sierpniu 2005 ... PAY_6 = stan spłaty w kwietniu 2005 (-1 = płatność w terminie; 1 = opóźnienie o 1 miesiąc; 2 = opóźnienie o 2 miesiące; ... ; 9 = opóźnienie o 9 miesięcy lub więcej). Dodatkowo występują wartości -2 i 0, których interpretacja podana jest jako: -2 i 0 = nie ma żadnego salda płatności.
# MAGIC - BILL_AMT1 - BILL_AMT6: Wartość na wyciągu w TWD (BILL_AMT1 = wyciąg za wrzesień 2005; BILL_AMT2 = wyciąg za sierpień 2005; ... ; BILL_AMT6 = wyciąg za kwiecień 2005),
# MAGIC - PAY_AMT1 - PAY_AMT6: Wartość poprzednich płatności (PAY_AMT1 = suma płatności we wrześniu 2005, PAY_AMT2 = suma płatności w sierpniu 2005; ... ; PAY_AMT6 = suma płatności w kwietniu 2005).

# COMMAND ----------

# MAGIC %md ####Import bibliotek

# COMMAND ----------

import pyspark.sql.functions as f
from pyspark.sql.types import *
from pyspark.ml.stat import Correlation
from pyspark.ml.feature import VectorAssembler
import matplotlib.pyplot as plt

# COMMAND ----------

# MAGIC %fs
# MAGIC ls /FileStore/tables

# COMMAND ----------

# MAGIC %md ####Import zbioru danych 

# COMMAND ----------

d = spark.read.format('com.databricks.spark.csv')\
  .options(inferSchema="true",header='true', delimiter=';')\
  .load('/FileStore/tables/default_of_credit_card_clients.csv')

# COMMAND ----------

# MAGIC %md ###Wstępna analiza

# COMMAND ----------

d.head(5)

# COMMAND ----------

print ('Ilość obserwacji:')
d.count()

# COMMAND ----------

print('Typy poszczególnych zmiennych:')
d.printSchema()

# COMMAND ----------

print('Ilość braków w danych:')
d.filter(d.ID.isNull() & d.LIMIT_BAL.isNull() & d.SEX.isNull() & d.EDUCATION.isNull() & d.MARRIAGE.isNull() & d.AGE.isNull()\
         & d.PAY_0.isNull() & d.PAY_2.isNull() & d.PAY_3.isNull() & d.PAY_4.isNull() & d.PAY_5.isNull() & d.PAY_6.isNull()\
         & d.BILL_AMT1.isNull() & d.BILL_AMT2.isNull() & d.BILL_AMT3.isNull() & d.BILL_AMT4.isNull() & d.BILL_AMT5.isNull() & d.BILL_AMT6.isNull()\
         & d.PAY_AMT1.isNull() & d.PAY_AMT2.isNull() & d.PAY_AMT3.isNull() & d.PAY_AMT4.isNull() & d.PAY_AMT5.isNull() & d.PAY_AMT6.isNull()\
         & d.Y.isNull())\
         .count()

# COMMAND ----------

# MAGIC %md ###Zmiana nazw atrybutów

# COMMAND ----------

#zmiana nazw atrybutów dla łatwiejszej analizy
d2=d.withColumnRenamed("PAY_0", "PAY_SEP")\
  .withColumnRenamed("PAY_2", "PAY_AUG")\
  .withColumnRenamed("PAY_3", "PAY_JUL")\
  .withColumnRenamed("PAY_4", "PAY_JUN")\
  .withColumnRenamed("PAY_5", "PAY_MAY")\
  .withColumnRenamed("PAY_6", "PAY_APR")\
  .withColumnRenamed("BILL_AMT1", "BILL_AMT_SEP")\
  .withColumnRenamed("BILL_AMT2", "BILL_AMT_AUG")\
  .withColumnRenamed("BILL_AMT3", "BILL_AMT_JUL")\
  .withColumnRenamed("BILL_AMT4", "BILL_AMT_JUN")\
  .withColumnRenamed("BILL_AMT5", "BILL_AMT_MAY")\
  .withColumnRenamed("BILL_AMT6", "BILL_AMT_APR")\
  .withColumnRenamed("PAY_AMT1", "PAY_AMT_SEP")\
  .withColumnRenamed("PAY_AMT2", "PAY_AMT_AUG")\
  .withColumnRenamed("PAY_AMT3", "PAY_AMT_JUL")\
  .withColumnRenamed("PAY_AMT4", "PAY_AMT_JUN")\
  .withColumnRenamed("PAY_AMT5", "PAY_AMT_MAY")\
  .withColumnRenamed("PAY_AMT6", "PAY_AMT_APR")

# COMMAND ----------

d2.display()

# COMMAND ----------

# MAGIC %md ###Analiza wskaźników statystycznych

# COMMAND ----------

d2.describe("Y","ID","LIMIT_BAL","SEX","EDUCATION","MARRIAGE","AGE").show()

# COMMAND ----------

d2.describe("PAY_SEP","PAY_AUG","PAY_JUL","PAY_JUN","PAY_MAY","PAY_APR").show()

# COMMAND ----------

d2.describe("BILL_AMT_SEP","BILL_AMT_AUG","BILL_AMT_JUL","BILL_AMT_JUN","BILL_AMT_MAY","BILL_AMT_APR").show()

# COMMAND ----------

d2.describe("PAY_AMT_SEP","PAY_AMT_AUG","PAY_AMT_JUL","PAY_AMT_JUN","PAY_AMT_MAY","PAY_AMT_APR").show()

# COMMAND ----------

# MAGIC %md ####Rozkłady wartości atrybutów i zmiennej celu

# COMMAND ----------

d2.groupBy("Y")\
  .count()\
  .sort("Y", ascending=False)\
  .display()

# COMMAND ----------

d2.groupBy("SEX")\
  .agg(\
       f.count("Y"),\
       f.sum("Y"))\
  .withColumnRenamed("count(Y)", "Ilość_klientów")\
  .withColumnRenamed("sum(Y)", "Ilość_niewiarygodnych_klientów")\
  .sort("SEX", ascending=True)\
  .display()

# COMMAND ----------

d2.groupBy("EDUCATION")\
  .agg(\
       f.count("Y"),\
       f.sum("Y"))\
  .withColumnRenamed("count(Y)", "Ilość_klientów")\
  .withColumnRenamed("sum(Y)", "Ilość_niewiarygodnych_klientów")\
  .sort("EDUCATION", ascending=True)\
  .display()

# COMMAND ----------

d2.groupBy("MARRIAGE")\
  .agg(\
       f.count("Y"),\
       f.sum("Y"))\
  .withColumnRenamed("count(Y)", "Ilość_klientów")\
  .withColumnRenamed("sum(Y)", "Ilość_niewiarygodnych_klientów")\
  .sort("MARRIAGE", ascending=True)\
  .display()

# COMMAND ----------

d2.groupBy("PAY_SEP")\
  .agg(\
       f.count("Y"),\
       f.sum("Y"))\
  .withColumnRenamed("count(Y)", "Ilość_klientów")\
  .withColumnRenamed("sum(Y)", "Ilość_niewiarygodnych_klientów")\
  .sort("PAY_SEP", ascending=True)\
  .display()

# COMMAND ----------

d2.groupBy("PAY_AUG")\
  .agg(\
       f.count("Y"),\
       f.sum("Y"))\
  .withColumnRenamed("count(Y)", "Ilość_klientów")\
  .withColumnRenamed("sum(Y)", "Ilość_niewiarygodnych_klientów")\
  .sort("PAY_AUG", ascending=True)\
  .display()

# COMMAND ----------

d2.groupBy("PAY_JUL")\
  .agg(\
       f.count("Y"),\
       f.sum("Y"))\
  .withColumnRenamed("count(Y)", "Ilość_klientów")\
  .withColumnRenamed("sum(Y)", "Ilość_niewiarygodnych_klientów")\
  .sort("PAY_JUL", ascending=True)\
  .display()

# COMMAND ----------

d2.groupBy("PAY_JUN")\
  .agg(\
       f.count("Y"),\
       f.sum("Y"))\
  .withColumnRenamed("count(Y)", "Ilość_klientów")\
  .withColumnRenamed("sum(Y)", "Ilość_niewiarygodnych_klientów")\
  .sort("PAY_JUN", ascending=True)\
  .display()

# COMMAND ----------

d2.groupBy("PAY_MAY")\
  .agg(\
       f.count("Y"),\
       f.sum("Y"))\
  .withColumnRenamed("count(Y)", "Ilość_klientów")\
  .withColumnRenamed("sum(Y)", "Ilość_niewiarygodnych_klientów")\
  .sort("PAY_MAY", ascending=True)\
  .display()

# COMMAND ----------

d2.groupBy("PAY_APR")\
  .agg(\
       f.count("Y"),\
       f.sum("Y"))\
  .withColumnRenamed("count(Y)", "Ilość_klientów")\
  .withColumnRenamed("sum(Y)", "Ilość_niewiarygodnych_klientów")\
  .sort("PAY_APR", ascending=True)\
  .display()

# COMMAND ----------

d2.groupBy("AGE")\
  .agg(\
       f.count("Y"),\
       f.sum("Y"))\
  .withColumnRenamed("count(Y)", "Ilość_klientów")\
  .withColumnRenamed("sum(Y)", "Ilość_niewiarygodnych_klientów")\
  .sort("AGE", ascending=True)\
  .display()

# COMMAND ----------

d2.groupBy("LIMIT_BAL")\
  .agg(\
       f.count("Y"),\
       f.sum("Y"))\
  .withColumnRenamed("count(Y)", "Ilość_klientów")\
  .withColumnRenamed("sum(Y)", "Ilość_niewiarygodnych_klientów")\
  .sort("LIMIT_BAL", ascending=True)\
  .display()

# COMMAND ----------

# MAGIC %md ####Atrybuty a zmienna celu

# COMMAND ----------

vector_col = "corr_features"
assembler = VectorAssembler(inputCols=d2.columns, 
                            outputCol=vector_col)
myGraph_vector = assembler.transform(d2).select(vector_col)
matrix = Correlation.corr(myGraph_vector, vector_col)
#matrix.collect()[0]["pearson({})".format(vector_col)].values

matrix = Correlation.corr(myGraph_vector, vector_col).collect()[0][0]
corrmatrix = matrix.toArray().tolist()

df_corr = spark.createDataFrame(corrmatrix,d2.columns)
df_corr.display()

# COMMAND ----------

def plot_corr_matrix(correlations,attr,fig_no):
    fig=plt.figure(fig_no,figsize=(6,6))
    plt.figure(figsize=(200,100))
    ax=fig.add_subplot(111)
    ax.set_title("Correlation Matrix for Specified Attributes")
    ax.set_xticklabels(['']+attr)
    ax.set_yticklabels(['']+attr)
    cax=ax.matshow(correlations,vmax=1,vmin=-1)
    fig.colorbar(cax)
    plt.show()
plot_corr_matrix(corrmatrix, d2.columns, 263)

# COMMAND ----------

d2.corr('AGE', 'Y') 

# COMMAND ----------

d2.groupBy("Y")\
  .agg(\
       f.count("Y"),\
       f.round(f.mean("AGE"),2).alias("Wiek"),\
       f.round(f.mean("LIMIT_BAL"),2).alias("Średni_limit_kredytowy"),\
       f.round(f.mean("PAY_SEP"),2).alias("Średnia_spłata_wrz"),\
       f.round(f.mean("PAY_AUG"),2).alias("Średnia_spłata_sie"),\
       f.round(f.mean("PAY_JUL"),2).alias("Średnia_spłata_lip"),\
       f.round(f.mean("PAY_JUN"),2).alias("Średnia_spłata_cze"),\
       f.round(f.mean("PAY_MAY"),2).alias("Średnia_spłata_maj"),\
       f.round(f.mean("PAY_APR"),2).alias("Średnia_spłata_kwi"),\
       f.round(f.mean("BILL_AMT_SEP"),2).alias("Średni_wyciąg_wrz"),\
       f.round(f.mean("BILL_AMT_AUG"),2).alias("Średni_wyciąg_sie"),\
       f.round(f.mean("BILL_AMT_JUL"),2).alias("Średni_wyciąg_lip"),\
       f.round(f.mean("BILL_AMT_JUN"),2).alias("Średni_wyciąg_cze"),\
       f.round(f.mean("BILL_AMT_MAY"),2).alias("Średni_wyciąg_maj"),\
       f.round(f.mean("BILL_AMT_APR"),2).alias("Średni_wyciąg_kwi"),\
       f.round(f.mean("PAY_AMT_SEP"),2).alias("Średnia_płatność_wrz"),\
       f.round(f.mean("PAY_AMT_AUG"),2).alias("Średnia_płatność_sie"),\
       f.round(f.mean("PAY_AMT_JUL"),2).alias("Średnia_płatność_lip"),\
       f.round(f.mean("PAY_AMT_JUN"),2).alias("Średnia_płatność_cze"),\
       f.round(f.mean("PAY_AMT_MAY"),2).alias("Średnia_płatność_maj"),\
       f.round(f.mean("PAY_AMT_APR"),2).alias("Średnia_płatność_kwi"))\
  .withColumnRenamed("count(Y)", "Ilość_klientów")\
  .sort("Ilość_klientów", ascending=False)\
  .display()

# COMMAND ----------

d2.filter ("AGE<60")\
  .groupBy("Y")\
  .agg(\
       f.count("Y"),\
       f.round(f.mean("AGE"),2).alias("Wiek"),\
       f.round(f.mean("LIMIT_BAL"),2).alias("Średni_limit_kredytowy"),\
       f.round(f.mean("PAY_SEP"),2).alias("Średnia_spłata_wrz"),\
       f.round(f.mean("PAY_AUG"),2).alias("Średnia_spłata_sie"),\
       f.round(f.mean("PAY_JUL"),2).alias("Średnia_spłata_lip"),\
       f.round(f.mean("PAY_JUN"),2).alias("Średnia_spłata_cze"),\
       f.round(f.mean("PAY_MAY"),2).alias("Średnia_spłata_maj"),\
       f.round(f.mean("PAY_APR"),2).alias("Średnia_spłata_kwi"),\
       f.round(f.mean("BILL_AMT_SEP"),2).alias("Średni_wyciąg_wrz"),\
       f.round(f.mean("BILL_AMT_AUG"),2).alias("Średni_wyciąg_sie"),\
       f.round(f.mean("BILL_AMT_JUL"),2).alias("Średni_wyciąg_lip"),\
       f.round(f.mean("BILL_AMT_JUN"),2).alias("Średni_wyciąg_cze"),\
       f.round(f.mean("BILL_AMT_MAY"),2).alias("Średni_wyciąg_maj"),\
       f.round(f.mean("BILL_AMT_APR"),2).alias("Średni_wyciąg_kwi"),\
       f.round(f.mean("PAY_AMT_SEP"),2).alias("Średnia_płatność_wrz"),\
       f.round(f.mean("PAY_AMT_AUG"),2).alias("Średnia_płatność_sie"),\
       f.round(f.mean("PAY_AMT_JUL"),2).alias("Średnia_płatność_lip"),\
       f.round(f.mean("PAY_AMT_JUN"),2).alias("Średnia_płatność_cze"),\
       f.round(f.mean("PAY_AMT_MAY"),2).alias("Średnia_płatność_maj"),\
       f.round(f.mean("PAY_AMT_APR"),2).alias("Średnia_płatność_kwi"))\
  .withColumnRenamed("count(Y)", "Ilość_klientów")\
  .sort("Ilość_klientów", ascending=False)\
  .display()

# COMMAND ----------

d2.select("Y","AGE", "LIMIT_BAL").display()

# COMMAND ----------

d2.select("Y","AGE", "BILL_AMT_SEP").display()

# COMMAND ----------

# MAGIC %md ###Dodatkowe analizy

# COMMAND ----------

d2.groupBy("AGE")\
  .mean()\
  .sort("AGE", ascending=True)\
  .display()

# COMMAND ----------

d2.groupBy("EDUCATION")\
  .agg(\
       f.count("Y"),\
       f.round(f.mean("LIMIT_BAL"),2))\
  .withColumnRenamed("count(Y)", "Ilość_klientów")\
  .withColumnRenamed("round(avg(LIMIT_BAL), 2)", "Średni_limit kredytowy")\
  .sort("EDUCATION", ascending=True)\
  .display()

# COMMAND ----------

d2.groupBy("MARRIAGE")\
  .agg(\
       f.count("Y"),\
       f.round(f.mean("LIMIT_BAL"),2))\
  .withColumnRenamed("count(Y)", "Ilość_klientów")\
  .withColumnRenamed("round(avg(LIMIT_BAL), 2)", "Średni_limit_kredytowy")\
  .sort("MARRIAGE", ascending=True)\
  .display()

# COMMAND ----------

d2.groupBy("SEX")\
  .agg(\
       f.count("Y"),\
       f.round(f.mean("LIMIT_BAL"),2))\
  .withColumnRenamed("count(Y)", "Ilość_klientów")\
  .withColumnRenamed("round(avg(LIMIT_BAL), 2)", "Średni_limit_kredytowy")\
  .sort("SEX", ascending=True)\
  .display()

# COMMAND ----------

# MAGIC %md ###Podsumowanie 
# MAGIC 
# MAGIC Z ogólnego porównania atrybutów wynika, że dla limitu kredytowego odchylenie standardowe jest bardzo duże równe 129748 przy średniej równej 167484. Średni wiek wynosi 35.5 roku przy odchy. standardowym równym 9.2, ale występują także osoby w wieku emerytalnym. Spłaty w większości są w terminie. Średnia wartość wyciągu w kolejnych miesiącach wzrasta i odchy. standardowe jest znaczne np. dla września wynosi 73636 przy średniej równej 51223 (związane jest to z wielkością limitów kredytowych). Podobnie średnia wartość poprzednich płatności z czasem wzrasta, a odchy. standardowe jest bardzo duże np. dla września wynosi 16563 przy średniej 5664.
# MAGIC 
# MAGIC Ilość klientów, którzy nie spłacą zobowiązania w przyszłym miesiącu stanowi ok. 22% wszytkich klientów. Zbiór można uznać za niezbalansowany.
# MAGIC W większości klientami są kobiety i stanowią ok. 60%, osoby z wykształceniem wyższym i wyższym pełnym (łącznie ok. 82% klientów) oraz osoby ze stanem cywilnym kawaler/panna (ok. 53%) ale również dużą liczbę stanowią klienci w związku (ok. 46%).
# MAGIC Większość zadłużenia jest spłacana w terminie (wartość -1). Jednak występują przypadki w których spłata przeciąga się do kilku miesięcy oraz występują dużo przypadków braku salda płatności (wartości -2, 0).
# MAGIC 
# MAGIC Na podstawie zestawienia występowania klientów wiarygodnych/niewiarygodnych dla poszczególnych kategorii atrybutów oraz wspomagając się wykresami proporcji można stwierdzić, że zależność pomiędzy atrybutami a zmienną objaśnianą jest największa dla atrybutów dotyczących terminowej spłaty kredytu. Szczególnie jest to wdoczne dla ostatnich miesięcy (sierpień, wrzesień). Dla pozostałych atrybutów zależność nie jest duża. Największe zróżnicowanie proporcji występuje dla wyksztalcenia (np. dla średniego i wyższego wykształcenia jest duży udział zdarzeń pozytywnych w stosunku do łącznej ilości). Dla płci udział zdarzeń pozytywnych dla mężczyzn jest nieznacznie większy niż dla kobiet. Dla nieznanego stanu cywilnego jest mniej zdarzeń pozytywnych niż dla pozostałych wartości tego atrybutu.
# MAGIC 
# MAGIC Wykorzytując wyznaczone wartości współczynnika korelacji, można stwierdzić, że atrybuty z grupy stan spłaty są najbardziej skorelowane ze zmienną objaśnianą y. Korelacja wzrasta ze zbliżaniem się do października. Limit kredytu i atrybuty z grupy płatności są w niewielkim stopniu skorelowane ze zmienną objaśnianą y. Wiek i atrybuty z grupy wyciąg są tylko nieznacznie skorelowane ze zmienną objaśnianą y. Oczywiste jest wyciąg jest mocno skorelowany z płatnością, a w szczególności wyciąg w danym miesiącu i płatność w kolejnym miesiącu. Wiek praktycznie nie ma korelacji z żadnym z atrybutów (niewielka z limit kredytu). Zależność pomiędzy atrybutami dotyczącymi wykształcenia, płci i  stanu cywilnego jest stosunkowo mała.
# MAGIC 
# MAGIC Warto zauważyć, że ogólnie średnia limitu kredytowy, a co za tym idzie średnia wartości wyciągu i płatności w poszczególnych miesiącach jest mniejsza dla klientów oznaczonych jako niewiarygodni {1} w porównaniu do wiarygodnych {0}. To może oznaczać, że klienci niewiarygodni są raczej w grupie osób o mniejszym przyznanym limicie kredytu. Ponadto średnia wartość opóźnienia spłaty zobowiązania dla klientów niewiarygodnych jest dodatnia, a dla wiarygodnych ujemna, co jest w miarę logiczne - kliencie niespłacający zobowiązania w kolejnych miesiącach wkońcu stają się niewiarygodni. Średni wiek klientów jest podobny dla klientów spłacających i niespłacających zobowiązania. 
# MAGIC 
# MAGIC Dodatkow zgodnie z przedstawionym wykresem widać wzrost limitu kredytowego w zależności od wieku do ok. 30 lat i powolny spadek aż do wieku 60 lat. W tym okresie dla klientów niewiarygodnych wartość limitu kredytowego zachowuje się podobnie jak dla klientów wiarygodnych. Po przekroczenie 60 roku większość ludzi przechodzi na emeryturę i zakres przyznanego limitu kredytowego bardziej się wacha i jest mniej stabilny. Po przekroczeniu 70 roku życia jest mało klientów i wyniki są bardziej losowe.

# COMMAND ----------

# MAGIC %md Na podstawie powyższych danych i wniosków można stwierdzić, że największe znaczenie przy określaniu niewypłacalności klientów w następnym miesiącu ma stan spłaty we wcześniejszych miesiącach, a szczególnie w miesiącach bezpośrednio poprzedzajacych badany mieciąc. Im większe opóźnienie w spłacie tym więcej klientów niewypłacalnych. Znaczenie mają również atrybuty określajace limit kredytowy i powiązany z nim wartości na wyciągu i poprzednich spłat. Okazało się, że klienci niewypłacalni mieli przyznany średnio mniejszy limit kredytowy niż klienci wypłacalni. Dodatkowo klienci o wyższym i średnim wykształceniu stosunkowo częściej nie spłacali zobowiązania niż pozostali.
