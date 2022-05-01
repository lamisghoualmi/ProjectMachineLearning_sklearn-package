
import numpy as np
import pandas  as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier




###from sklearn.datasets import load_iris
##iris = load_iris()
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


clf = DecisionTreeClassifier()
clf = clf.fit(df, target)
diction=dict(zip(df.columns, clf.feature_importances_))
Scores=pd.DataFrame(list(diction.items()))


Thre_min=Scores[1].min()
Thre_max=Scores[1].max()
walk=(Scores[1].min()+Scores[1].max())/5


cols = ['Threshold', 'Accuracy', 'FeatureSize']
Stock = pd.DataFrame(columns = cols)
BestAccuracy=0
Best_FeatureSize=df.shape[1]
BestThreshold=[]
randEst=[42,10,20,32, 0, 62, 82, 100, 150, 200]
while (Thre_min <= Thre_max):
    
    LabelsSelect=Scores[Scores[1] >= Thre_min]
    Newdf=df[LabelsSelect[0]]

    #----------------------Bootsrapping-------------------------------
    bigy_test=[]
    bigy_pred=[]
    for i in range (0,1):
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
#Stock.to_csv('DT-GSE412-Childhood.tsv',sep='\t')