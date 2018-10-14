import requests
from django.shortcuts import render
from django.http import HttpResponse
from .forms import ContactForm
from .models import Greeting
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
from nltk.tokenize import RegexpTokenizer
import json
from eventregistry import *
from dandelion import DataTXT

def db(request):

    #greeting = Greeting()
    #greeting.save()

    greetings = Greeting.objects.all()


    return render(request, 'db.html', {'greetings': greetings})

def index(request):
    li={}
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            msg=request.POST.get('message')
            li=tok1(msg)
            print(li)
            return render(request, 'db.html',{'dict1':li})                      # reuqest--> specifies the request for which this response is genertaed
                                                                                #'db.html' templated to render
                                                                                # '{'dic1': li}' dictionary to be send to template
    else:
        form = ContactForm()
    return render(request, 'index.html',{'form':form})

def tok1(msg):
    lis=[]
    #li=[]
    li=[]
    returnList=[]
    articlesDict={}
    datatxt = DataTXT(app_id='5d504312af124377bac2f69c908dc20b',app_key='5d504312af124377bac2f69c908dc20b')
    repnews=['news.google.co.in','nytimes.com','timesofindia.indiatimes.com','wsj.com','washingtonpost.com','bbc.com','moneycontrol.com','economist.com','newyorker.com','economictimes.indiatimes.com','ndtv.com','indiatoday.in','indianexpress.com','thehindu.com','news18.com','firstpost.com','dnaindia.com','apnews.com','brief.news','npr.org','scroll.in','reuters.com']
    tokenizer = RegexpTokenizer(r'\w+')
    a=tokenizer.tokenize(msg)
    stop = stopwords.words('english') + list(string.punctuation)
    a=[i for i in a if i not in stop]                                           #removed stop words from user query
    er = EventRegistry(apiKey = "e010e4f7-343c-49d5-893d-63d4c2cfd487")
    q = QueryArticlesIter(keywords= QueryItems.OR(a),lang=["eng"],keywordsLoc="title")
    b=q.execQuery(er, sortBy = "rel", maxItems =50 )
    # for articles in b:
    #      articlesDict['id']=[articles['title'],articles['source']]
    #      # print(articlesDict)                                                      #query is executed on EventRegistry
    for article in b:
        if(article['source']['uri'] in repnews and (datatxt.sim(msg,article['title'])['similarity']>=0.60)): 
            print(article['title'])
            articlesDict[article['uri']]={'id':article['uri'],'title':article['title'],'source':article['source'],'url':article['url'],'date':article['date']}                        #filtered outed articals from reputed source
    #         articlesDict[article['uri']]={'title':article['title'],'source':article['source']}
    # print(articlesDict)

            # if article['title'] not in li:
            #     print(article['title'],article['source']['uri'])
            #     li.append(article['title'])
            #     # li.append(article['uri'])
    # for i in articlesDict:                                                   #find similarity of user's query and filtered out articals
    #     a=datatxt.sim(msg,articlesDict[i]['title'])
    #     if a['similarity'] >= 0.60 :                                            #if similarity greated than 0.6 then add that artical to list else ignore
    #             print(a['similarity'])
    #             returnList.append(articlesDict[i])
    return(articlesDict)
