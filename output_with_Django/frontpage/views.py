from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.core import serializers
from elasticsearch import Elasticsearch
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

es_client = Elasticsearch("localhost:9200")

def query(user_input):
    result = es_client.search(index='nnn',
                                  doc_type='disease',
                                  body={
                                      "query": {
                                          "multi_match": {
                                              "query": user_input,
                                              "fields": ["diseaseko^5", "treatment", "symptom^3"],
                                              "type": "best_fields",
                                              "fuzziness": "auto",
                                              "minimum_should_match": 2
                                          }
                                      },
                                      "highlight": {
                                          "fragment_size": 2000,
                                          "number_of_fragments": 0,
                                          "fields": [
                                              {"diseaseko": {}},
                                              {"symptom": {}}
                                          ]
                                      }
                                  },
                                  size = 100)
    return result

def pagenation_post(request,result):
    count = result['hits']['total']
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

    return count,posts,max_index


# Create your views here.
def index(request):
    request.session.modified = True
    if request.method == "POST":
        test = request
        # Html에서 test.POST.input_Symptom(템플릿 언어일 때)
        # python 코드에서는 접근 방법이 약간 달랐음.
        user_input = test.POST['input_Symptom']
        result = query(user_input)
        count,posts,max_index=pagenation_post(result)

        request.session['user_input'] = user_input
        request.session['count'] = count

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
        result = query(user_input)
        count, posts, max_index = pagenation_post(request,result)

        # print(posts.object_list[0]['highlight']['symptom'])
        print(posts.object_list[0]['highlight'])

        request.session['user_input'] = user_input
        request.session['count'] = count
        return render(request, 'frontpage/result.html',
                      {'user_input': user_input, 'posts': posts, 'count': count, 'max_index': max_index, })

    else:
        try:
            check = {'user_input': request.session['user_input']}
        except:
            check = False
        if check:
            user_input = request.session['user_input']
            result = query(user_input)
            count, posts, max_index = pagenation_post(request,result)

            request.session['user_input'] = user_input
            request.session['count'] = count

            print(posts.object_list)

            return render(request, 'frontpage/result.html',
                          {'user_input': request.session['user_input'], 'posts': posts,
                           'count': request.session['count'], 'max_index': max_index, })
        else:
            return render(request, 'frontpage/index.html')