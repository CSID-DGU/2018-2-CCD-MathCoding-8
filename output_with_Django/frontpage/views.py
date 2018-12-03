from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.core import serializers
from elasticsearch import Elasticsearch
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

es_client = Elasticsearch("localhost:9200")

# Create your views here.
def index(request):
    request.session.modified = True
    if request.method == "POST":
        test = request
        # Html에서 test.POST.input_Symptom
        # python 코드에서는 접근 방법이 약간 달랐음.
        user_input = test.POST['input_Symptom']
        print(user_input)
        result = es_client.search(index='nonono',
                                  doc_type='doc',
                                  body={
                                      "query": {
                                          "multi_match": {
                                              "query": user_input,
                                              "analyzer" : "nori",
                                              "fields": ["diseaseko^5", "treatment", "symptom^3"]
                                          }
                                      }
                                  },
                                  size = 100
                                  )
        print(type(result))
        count = result['hits']['total']
        disease = result['hits']['hits']
        #print(count)
        #print(disease)
        #print(type(count))
        #print(type(disease))
        paginator = Paginator(disease, 10)
        page = request.GET.get('page')

        request.session['user_input'] = user_input
        request.session['count'] = count
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            posts = paginator.page(paginator.num_pages)

        max_index = len(paginator.page_range)
        return render(request, 'frontpage/result.html',
                      {'user_input': user_input, 'posts': posts, 'count': count,'max_index': max_index,})
    else:
        try:
            del request.session['user_input']
            del request.session['count']
            return render(request, 'frontpage/index.html')
        except:
            return render(request, 'frontpage/index.html')

def result(request):
    request.session.modified = True
    if request.method == "POST":
        test = request
        user_input = test.POST['input_Symptom']
        print(user_input)
        result = es_client.search(index='nonono',
                                  doc_type='doc',
                                  body={
                                      "query": {
                                          "multi_match": {
                                              "query": user_input,
                                              "analyzer": "nori",
                                              "fields": ["diseaseko^5", "treatment", "symptom^3"]
                                          }
                                      }
                                  },
                                  size=100
                                  )

        count = result['hits']['total']
        disease = result['hits']['hits']

        paginator = Paginator(disease, 10)
        page = request.GET.get('page')

        request.session['user_input'] = user_input
        request.session['count'] = count
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            posts = paginator.page(paginator.num_pages)

        max_index = len(paginator.page_range)
        return render(request, 'frontpage/result.html',
                      {'user_input': user_input, 'posts': posts, 'count': count, 'max_index': max_index, })

    else:
        try:
            check = {'user_input': request.session['user_input']}
        except:
            check = False
        if check:
            user_input = request.session['user_input']
            result = es_client.search(index='nonono',
                                      doc_type='doc',
                                      body={
                                          "query": {
                                              "multi_match": {
                                                  "query": user_input,
                                                  "analyzer": "nori",
                                                  "fields": ["diseaseko^5", "treatment", "symptom^3"]
                                              }
                                          }
                                      },
                                      size=100
                                      )
            disease = result['hits']['hits']
            paginator = Paginator(disease, 10)
            page = request.GET.get('page')
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                posts = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                posts = paginator.page(paginator.num_pages)

            max_index = len(paginator.page_range)

            return render(request, 'frontpage/result.html',
                          {'user_input': request.session['user_input'], 'posts': posts,
                           'count': request.session['count'], 'max_index': max_index, })
        else:
            return render(request, 'frontpage/index.html')