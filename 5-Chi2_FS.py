# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 14:21:14 2020

@author: Benk
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 11:59:49 2020

@author: Benk
"""


import numpy as np
import pandas  as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
from sklearn import svm
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2



#from sklearn.datasets import load_iris
#iris = load_iris()
#df= pd.DataFrame(iris.data, columns=['sepal_length', 'sepal_width', 'petal_length', 'petal_width'])
#target=iris.target


from sklearn.datasets import load_digits
digits = load_digits()
df=digits.data
df = pd.DataFrame(df)
target=digits.target

#from sklearn.datasets import fetch_olivetti_faces
#f = fetch_olivetti_faces()
#df=f.data
#df=pd.DataFrame(df)
#target=f.target

#df=pd.read_csv("BCGSE349_350.tab",sep="\t",index_col=0)
#df.drop(df.index[:2], inplace=True)
#df["class"]= df["class"].replace('resistant', 0) 
#df["class"]= df["class"].replace('sensitive', 1) 
#target=df["class"]
#df=df.drop(["class"], axis=1)
#df=df.drop(["sample"], axis=1)

FeatSelector = SelectKBest(chi2, k='all')
fitData = FeatSelector.fit(df, target)
MapData=pd.DataFrame(fitData.scores_, df.columns.values)

MapData=MapData.fillna(0)
Thre_min=MapData.values.min()
Thre_max=MapData.values.max()
walk=(MapData.values.min()+MapData.values.max())/5
walk=100
cols = ['Threshold', 'Accuracy', 'FeatureSize', 'MSE', 'R2']
Stock = pd.DataFrame(columns = cols)
BestAccuracy=0
Best_FeatureSize=df.shape[1]
BestThreshold=[]
randEst=[42,10,20,32, 0, 62, 82, 100, 150, 200]
while (Thre_min <= Thre_max):
    LabelsSelect=MapData[MapData.values>=Thre_min]
    Newdf=df[LabelsSelect.index]
    
     #----------------------Bootsrapping-------------------------------
    bigy_test=[]
    bigy_pred=[]
    for i in range (0,9):
        X_train,X_test,y_train,y_test = train_test_split(Newdf,target,test_size=0.5,random_state=randEst[i])
        clf = svm.SVC(kernel='linear') 
        clf.fit(X_train, y_train)
        y_pred= clf.predict(X_test)
        bigy_test.append(y_test)
        bigy_pred.append(y_pred)
        
    bigy_test = [j for sub in bigy_test for j in sub]
    bigy_pred = [jj for subj in bigy_pred for jj in subj]
    Accuracy=accuracy_score(bigy_test, bigy_pred)
#----------------------------------------------------------------
    
    Stock = Stock.append({'Threshold': Thre_min, 'Accuracy':Accuracy, 'FeatureSize': Newdf.shape[1]},ignore_index=True)
    if (Accuracy >=  BestAccuracy and  Newdf.shape[1] <= Best_FeatureSize):
        BestAccuracy=Accuracy
        Best_FeatureSize=Newdf.shape[1]
        BestThreshold=Thre_min
    Thre_min=Thre_min+walk
    
print('BestAccuracy; ', BestAccuracy, 'BestFeatureSize: ', Best_FeatureSize, 'BestThreshold: ', BestThreshold)
    
#Stock.to_csv('Chi2-GSE93992-CardiogenicShock.tsv',sep='\t')