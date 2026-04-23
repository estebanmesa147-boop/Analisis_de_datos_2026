import pandas as pd
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import numpy as np 

datos= pd.read_csv("https://archive.ics.uci.edu/static/public/186/data.csv")

print(datos.head)

subconjunto =datos[datos['quality'].isin([5,7])]

X=subconjunto.iloc[:,0:11]
y= subconjunto['quality']

X_train,X_test,y_train,y_test = train_test_split(
    X,y,test_size=0.3,random_state=42
)

print(subconjunto)

clasificacion=datos.groupby('quality')['pH'].agg('max')

print(clasificacion)

mlp=MLPClassifier(
    hidden_layer_sizes=(10,10),
    random_state=42,
    activation='logistic',
    max_iter=1000
)
mlp.fit(X_train,y_train)

score=mlp.score(X_test,y_test)

print(score)

vino= [[8.5,0.49,0.11,2.3,0.084,9,67,0.9968,3.17,0.53,9.4],[7.4,0.62,0.05,1.9,0.068,24,42,0.9961,3.42,0.57,11.5],
       [6.9,1.09,0.06,2.1,0.061,12,31,0.9948,3.51,0.43,11.4],[5.2,0.48,0.04,1.6,0.054,19,106,0.9927,3.54,0.62,12.2]]
y_pred=mlp.predict(vino)

print(y_pred)