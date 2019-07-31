from flask import Flask,render_template, request, send_file
from flask_pymongo import PyMongo
from pymongo import MongoClient
from operator import itemgetter
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as bar
import matplotlib.pyplot as pl
import matplotlib.pyplot as pl1
from matplotlib.pyplot import figure
import numpy as np
from io import BytesIO
import base64
import math


app = Flask(__name__)
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client.videogame
vg = db.vg
a = []
b = []
c = []
result = ""
r2 = ""
r3 = ""
conteggio= []
byplat = None



@app.route("/")
def home_page():
    allv = db.vg.find({})
    global b
    global c
    b = []
    c = []
    for document in allv:
          a.append(document)
    platform=[]
    for i in a:
        if pd.isna(i.get("Platform"))!= True:
           exist = False
           for c in platform:
               if c == i.get("Platform") :
                  exist = True
           if exist == False  :
              platform.append(i.get("Platform"))
    genere=[]
    for i in a:
        if pd.isna(i.get("Genre"))!= True:
           exist = False
           for c in genere:
               if c == i.get("Genre") :
                  exist = True
           if exist == False  :
              genere.append(i.get("Genre"))
    return render_template("index.html", p=a, e = platform,g = genere)

@app.route('/result1',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      global result
      global r2
      result = str(request.form['platform'])
      r2 = str(request.form['genre'])
      if result!="All":
         if r2!="All":
            myquery = { "Platform": result,"Genre": r2  }
         else:            
            myquery = { "Platform": result}
      elif r2!="All":
         myquery = { "Genre": r2 }
      else:
         myquery = {}
      byplat = None
      byplat = db.vg.find(myquery)
      global b
      b = []
      for document in byplat:
          b.append(document)
      editori=[]
      for i in b:
          if pd.isna(i.get("Publisher"))!= True:
             exist = False
             for c in editori:
                 if c == i.get("Publisher") :
                    exist = True
             if exist == False  :
                 editori.append(i.get("Publisher"))
      sales = []
      for a in editori:
          sales.append(0)
      for x in b:
          m = 0
          for z in editori:
              if x.get("Publisher") == editori[m]:
                 sales[m] = sales[m] + x.get("NA_Sales") + x.get("EU_Sales") + x.get("JP_Sales") + x.get("Other_Sales")
              m = m+1
      migliori = [] 
      for n in range(0,len(editori)):
          a = [editori[n],sales[n]]
          migliori.append(a)
      newlist = sorted(migliori,key = lambda k:k[1], reverse=True)
      editori1 = []
      sales1 = []
      for be in newlist:
          if len(editori1)<11:
             editori1.append(be[0])
             sales1.append(be[1])
      pl.figure(figsize=(16,9))
      pl.barh(editori1,sales1)
      pl.xlabel("Vendite in mln")
      pl.ylabel("Editori")
      pl.savefig("static/grafico1.png")
      global img
      img = BytesIO()
      pl.savefig(img)
      pl.clf()
      if result!="All" and r2!="All":
         cont=db.vg.aggregate([
                               {"$match":
                                 {"Publisher":{ "$exists": "true"},
                                  "Platform": result,
                                  "Genre": r2, 
                                  } 
                               },
                               {"$group":
                                 {"_id": "$Publisher",
                                  "count":{ "$sum": 1}}}
                              ])
      elif result!="All" and r2=="All":
         cont=db.vg.aggregate([
                               {"$match":
                                 {"Publisher":{ "$exists": "true"},
                                  "Platform": result,
                                  } 
                               },
                               {"$group":
                                 {"_id": "$Publisher",
                                  "count":{ "$sum": 1}}}
                              ])
      elif result=="All" and r2!="All":
         cont=db.vg.aggregate([
                               {"$match":
                                 {"Publisher":{ "$exists": "true"},
                                  "Genre": r2, 
                                  } 
                               },
                               {"$group":
                                 {"_id": "$Publisher",
                                  "count":{ "$sum": 1}}}
                              ])
      else :
          cont=db.vg.aggregate([
                               {"$match":
                                 {"Publisher":{ "$exists": "true"}, 
                                  } 
                               },
                               {"$group":
                                 {"_id": "$Publisher",
                                  "count":{ "$sum": 1}}}
                              ]) 
      global conteggio
      conteggio = []
      for document in cont:
          conteggio.append(document)
      pub=[]
      conte=[]
      for gr in conteggio:
          if pd.isna(gr.get("_id"))!= True:
             pub.append(gr.get("_id"))
             conte.append(gr.get("count"))
      migliori1 = [] 
      for ny in range(0,len(pub)):
          a = [pub[ny],conte[ny]]
          migliori1.append(a)
      newlist1 = sorted(migliori1,key = lambda k:k[1], reverse=True)
      pub1 = []
      conte1 = []
      for be1 in newlist1:
          if len(pub1)<11:
             pub1.append(be1[0])
             conte1.append(be1[1])
      bar.figure(figsize=(16,9))
      bar.barh(pub1,conte1)
      bar.xlabel("Videogiochi pubblicati")
      bar.ylabel("Editori")
      bar.savefig("static/graficocount.png")
      global imgcount
      imgcount = BytesIO()
      bar.savefig(imgcount)
      bar.clf()
      return render_template("result1.html",result1 = b, edit = editori)
      


@app.route('/result2',methods = ['POST', 'GET'])
def result2():
   if request.method == 'POST':
      global r3
      r3 = request.form['publisher']
      global img2
      img2 = BytesIO()
      if str(r3)!="All":
          global c
          c = []
          global result
          global r2
          if result!="All" and r2!="All":
             cont1=db.vg.aggregate([
                                    {"$match":
                                     {"Year":{ "$exists": "true"},
                                      "Publisher": str(r3),
                                      "Platform": result,
                                      "Genre": r2, 
                                     } 
                                    },
                                    {"$group":
                                      {"_id": "$Year",
                                       "sales0":{ "$sum": "$NA_Sales" },
                                       "sales1":{ "$sum": "$EU_Sales" },
                                       "sales2":{ "$sum": "$JP_Sales" },
                                       "sales3":{ "$sum": "$Other_Sales"}}}
                               ])
             gnr=r2
             plt=result
          elif result!="All" and r2=="All":
             cont1=db.vg.aggregate([
                                    {"$match":
                                     {"Year":{ "$exists": "true"},
                                      "Publisher": str(r3),
                                      "Platform": result,
                                     } 
                                    },
                                    {"$group":
                                      {"_id": "$Year",
                                       "sales0":{ "$sum": "$NA_Sales" },
                                       "sales1":{ "$sum": "$EU_Sales" },
                                       "sales2":{ "$sum": "$JP_Sales" },
                                       "sales3":{ "$sum": "$Other_Sales"}}}
                               ])
             gnr=""
             plt=result
          elif result=="All" and r2!="All":
             cont1=db.vg.aggregate([
                                    {"$match":
                                     {"Year":{ "$exists": "true"},
                                      "Publisher": str(r3),
                                      "Genre": r2, 
                                     } 
                                    },
                                    {"$group":
                                      {"_id": "$Year",
                                       "sales0":{ "$sum": "$NA_Sales" },
                                       "sales1":{ "$sum": "$EU_Sales" },
                                       "sales2":{ "$sum": "$JP_Sales" },
                                       "sales3":{ "$sum": "$Other_Sales"}}}
                               ])
             gnr=r2
             plt="qualsiasi piattaforma"
          else:
             cont1=db.vg.aggregate([
                                    {"$match":
                                     {"Year":{ "$exists": "true"},
                                      "Publisher": str(r3), 
                                     } 
                                    },
                                    {"$group":
                                      {"_id": "$Year",
                                       "sales0":{ "$sum": "$NA_Sales" },
                                       "sales1":{ "$sum": "$EU_Sales" },
                                       "sales2":{ "$sum": "$JP_Sales" },
                                       "sales3":{ "$sum": "$Other_Sales"}}}
                               ])
             gnr=""
             plt="qualsiasi piattaforma"
          line = []
          for docum in cont1:
              if pd.isna(docum.get("_id"))!= True:
                 line.append(docum)
          newline = sorted(line,key = itemgetter("_id"))
          anni=[]
          sales = []
          for u in newline:
              if pd.isna(u.get("_id"))!= True:
                 anni.append(int(u.get("_id")))
                 a = u.get("sales0") + u.get("sales1") + u.get("sales2") + u.get("sales3")
                 sales.append(a)
          pl1.plot(anni,sales)
          pl1.xlabel("Anni")
          pl1.ylabel("Vendite in mln")
          pl1.savefig("static/grafico2.png")
          pl1.savefig(img2)
          pl1.clf()  
          return render_template("result2.html", result2 = newline,publi=str(r3),gnr=gnr,plt=plt)

@app.route('/image',methods = ['POST', 'GET'])
def image():
   if request.method == 'POST':
      global img
      img.seek(0)
      return send_file(img, mimetype='image/png')

@app.route('/imagetwo',methods = ['POST', 'GET'])
def imagetwo():
   if request.method == 'POST':
      global img2
      img2.seek(0)
      return send_file(img2, mimetype='image/png')

@app.route('/imagecount',methods = ['POST', 'GET'])
def imagecount():
   if request.method == 'POST':
      global imgcount
      imgcount.seek(0)
      return send_file(imgcount, mimetype='image/png')

if __name__ == "__main__":
    app.run()