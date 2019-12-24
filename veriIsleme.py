# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 11:00:50 2019

@author: sefa
"""

import pandas as pd
import numpy as np
import re
import nltk
#nltk.download("stopwords")      
from nltk.corpus import stopwords
from TurkishStemmer import TurkishStemmer
import tkinter as tk
from tkinter import filedialog

Response=pd.read_json("1.json",encoding="UTF-8")                        
commentList=Response["result"]["reviews"]
df=pd.DataFrame(commentList)

for each in range(2,102): 
    Response=pd.read_json(str(each)+".json",encoding="UTF-8")                        
    commentList=Response["result"]["reviews"]
    df2=pd.DataFrame(commentList)
    df=np.concatenate((df, df2), axis=0)
    df=pd.DataFrame(df)
       
df.columns=[each for each in df2.columns]
df.drop(columns=['createdDate', 'gender','id','isVerifiedPurchase','userAge','userLocation','userName','title','agreeCount','disagreeCount'],inplace=True)
df=df[df.rating!='3']
df.rating=["Olumlu" if each>=4 else "Olumsuz" for each in df.rating]

comment_list = []
for comment in df.reviewText:
    comment = re.sub("\W"," ",comment)
    comment = re.sub("[0-9]"," ",comment)
    comment = comment.lower()   # buyuk harftan kucuk harfe cevirme
    comment = nltk.word_tokenize(comment)
    comment = [ word for word in comment if not word in set(stopwords.words("turkish"))]
    kokbul = TurkishStemmer()
    comment = [ kokbul.stem(word) for word in comment]
    comment = " ".join(comment)
    comment_list.append(comment)
    
df.reviewText=[each for each in comment_list]

root= tk.Tk()
canvas1 = tk.Canvas(root, width = 300, height = 300, bg = 'lightsteelblue2', relief = 'raised')
canvas1.pack()

def exportCSV ():
    global df
    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
    df.to_csv (export_file_path, index = None, header=True)

saveAsButton_CSV = tk.Button(text='Export CSV', command=exportCSV, bg='green', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(150, 150, window=saveAsButton_CSV)
root.mainloop()