# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 12:50:50 2023

@author: Bernd Ebenhoch
"""


"""
In diesem Beispiel wollen wir vorhersagen wie viele Schnittblumen in der 
Zukunft verkauft werden 
Die Porgnose basiert hierbei auf den verkauften Schnittblumen in den
vergangenen Tagen, sowie dem Wetter und möglichen anstehenden Feiertagen
Wir betachten, wie wir einen lagen Datensatz in einzelne kurze Sequenzen aufteilen 
können und insbesondere wie zukünftige Events wie anstehende Feiertage
berücksichtigt werden können.



"CashierData.csv" (angepasst von https://github.com/grimmlab/HorticulturalSalesPredictions/blob/master/Data/ - es wurden Angaben für Muttertag und Valentinstag hinzugefügt) vom Datenaustausch herunterladen und mit Pandas laden
Spalte "Public Holiday" onehotencoden, z. B. mit Pandas getdummies
Spalten entfernen: Date, PotOwn, PotPurchased, Wholesale, FruitsVegs, Commodity, mean_humid, mean_prec_height_mm mean_prec_flag, total_prec_flag, mean_sun_dur_min, school_holiday 
Spalten behalten: CutFlowers, mean_temp, total_prec_height_mm, total_sun_dur_h, public_holiday (onehotencoded)
Alle verbleibenden Daten spaltenweise minmax-skalieren
Optional: Alle Merkmale um die Forecastlength nach hinten zurück versetzen (Z. B. Erster Weihnachtstag in Zeile 15 -> Zeile 10), um dem Modell schon im voraus anzukündigen ob ein Feiertag ansteht und wie das Wetter die nächsten Tage wird
Daten in einzelne Sequenzen aufteilen, ein Fenster mit einer For-Schleife über die Daten iterieren und: 
Zu einer Liste x alle Merkmale (inklusive CutFlowers) über eine Sequencelength (z. B. 50) hinzufügen
Zu einer Liste y das Label CutFlowers über eine Forecastlength (z. B. 5) hinzufügen
Die Listen x und y in NumPy-arrays umwandeln und zufällig in Trainings- und Validationdaten aufteilen
Alle Sequenzen mit Missing Values (NaN-Values) entfernen
Das Modell designen mit LSTM-Schichten und Dense-Schichten. Anzahl der Ausgabeneuronen entsprechend der Forecastlength
Modell kompilieren für eine Multilabelregression
Modell trainieren
Für eine Prognose in die Zukunft die letztmögliche Sequenz aus den Daten bilden
Eine Prognose durchführen und wieder auf ursprünglichen Zahlenbereich zurückskalieren
Die Prognose zusammen mit den Originaldaten in einer Grafik darstellen

"""


# Daten mit pandas laden


from sklearn.multioutput import RegressorChain
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge, Lasso
from sklearn.neighbors import KNeighborsRegressor
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import r2_score
import pandas as pd
data = pd.read_csv(r"C:\Users\alfa\Downloads\CashierData (github.com grimmlab HorticulturalSalesPredictions MIT-Lizenz).csv",
                   delimiter=';')


# Daten ausgeben
print(data)


def convert_date(x):
    a = x.split('.')
    a.reverse()
    return '-'.join(a)


data['Date'] = data['Date'].map(convert_date)
date = data['Date'].to_numpy()
date = date.astype('datetime64[D]').reshape(-1, 1)

# In pandas Datetime Datentyp umwandeln
date_pd = pd.to_datetime(date[:, 0])


weekday = date_pd.strftime('%A')
weekday = np.array(weekday)
data['weekday'] = weekday

month = date_pd.strftime('%m')
month = np.array(month, dtype='int')
data['month'] = month
# data['month'] = np.sin(month/12 + 0.5/12)

day = date_pd.strftime('%d')
day = np.array(day, dtype='int')
data['day'] = day/31

# Das Label (CutFlowers) als Funktion der Zeit darstellen
plt.plot(date, data['CutFlowers'])
plt.xlabel('Time')
plt.ylabel('CutFlowers')
plt.xticks(rotation=25)
plt.show()


# Spalte "public_holiday" onehotencoden
data = pd.get_dummies(data, columns=['public_holiday'])
data = pd.get_dummies(data, columns=['weekday'])
data = pd.get_dummies(data, columns=['month'])


# Unnötige Spalten entfernen
data = data.drop(columns=["Date", "PotOwn", "PotPurchased", "Wholesale", "FruitsVegs", "Commodity", "mean_humid",
                          "mean_prec_height_mm", "mean_prec_flag", "total_prec_flag", "mean_sun_dur_min",
                          "school_holiday"])


print(data.columns)

columns = data.columns

# Data in ein NumPy-Array umwandeln
data = data.to_numpy()
data = data.astype('float32')


# Alle Daten skalieren
scaler = MinMaxScaler()
data = scaler.fit_transform(data)


# %%

# Daten in einzelne Sequenzen aufteilen
# Wir halten die Forcastlength eher kurz, da Schnittblumen eh schnell verwelken
# Es macht keinen Sinn die Verkaufszahlen sehr lange in die Zukunft zu planen
# Wenn wir die Prognose vom Wetter abhängig machen, müssen wir berücksichtigen,
# dass eine gute Wettervorhersage nur für wenige Tage gewährleistet ist
sequence_length = 15
forecast_length = 5
sequence_step = 1

# Die Wetterdaten um 5 Tage (Forecastlength) nach hinten verschieben
data[:-forecast_length, 1:] = data[forecast_length:, 1:]

# Die Feiertage um weitere 5 Tage nach hinten schieben
# Da das Einkaufsverhalten vermutlich schon geprägt ist, wenn zukünftig ein Feiertag ansteht
data[:-forecast_length, 4:] = data[forecast_length:, 4:]
data = data[:-forecast_length]
