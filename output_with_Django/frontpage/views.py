from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.core import serializers
from elasticsearch import Elasticsearch
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

es_client = Elasticsearch("localhost:9200")

# 일반 쿼리문
def query(user_input):
    result = es_client.search(index='nnn',
                              doc_type='disease',
                              body={
                                  "query": {
                                      "multi_match": {
                                          "query": user_input,
                                          "fields": ["diseaseko^3", "treatment", "symptom^2"],
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

# 검색결과 내 재검색 쿼리
def re_query(old,new):
    new_result = es_client.search(index='nnn',
                              doc_type='disease',
                              body={
                                  "query": {
                                      "bool": {
                                          "must": {
                                              "multi_match": {
                                                  "query": old,
                                                  "fields": ["diseaseko^3", "treatment", "symptom^2"],
                                                  "type": "best_fields",
                                                  "fuzziness": "auto",
                                                  "minimum_should_match": 2
                                              }
                                          },
                                          "filter": {
                                              "match": {
                                                  "symptom": {
                                                      "query": new,
                                                      "fuzziness": "auto",
                                                      "minimum_should_match": 2
                                                  }
                                              }
                                          }
                                      }
                                  }
                                  ,
                                  "highlight": {
                                      "fragment_size": 2000,
                                      "number_of_fragments": 0,
                                      "fields": [
                                          {"diseaseko": {}},
                                          {"symptom": {}}
                                      ]
                                  }
                              },
                              size=100)
    return new_result


def pagenation_post(request,result):
    count = result['hits']['total']
    disease = result['hits']['hits']
    paginator = Paginator(disease, 10)
    page = request.GET.get('page')
    max_index = len(paginator.page_range)

    try:
        posts = paginator.page(page)
        current_page=int(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
        current_page=1
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
        current_page=int(max_index)

    return count,posts,max_index,current_page


# Create your views here.
def index(request):
    request.session.modified = True
    # 메인화면에서 POST방식일 경우. 사용자 입력받아서 일반 query문으로 던져주면 된다.
    if request.method == "POST":
        test = request
        # Html에서 test.POST.input_Symptom(템플릿 언어일 때)
        # python 코드에서는 접근 방법이 약간 달랐음.
        user_input = test.POST['input_Symptom']
        result = query(user_input)
        count,posts,max_index,current_page=pagenation_post(result)

        request.session['user_input'] = user_input
        request.session['count'] = count

        return render(request, 'frontpage/result.html',
                      {'user_input': user_input, 'posts': posts, 'count': count,
                       'max_index': max_index,'current_page':current_page})
    # 메인화면에서 GET방식일 경우. 이전 검색 내역을 지워주자.
    else:
        try:
            del request.session['user_input']
            del request.session['count']
            return render(request, 'frontpage/index.html')
        except:
            return render(request, 'frontpage/index.html')

def result(request):
    request.session.modified = True
    # 결과 화면에서 POST방식 일 경우.
    ## 결과 내 재검색 체크박스가 False인 경우.
    if request.method == "POST":
        try:
            checkbox_content=request.POST['re-search']
        except:
            checkbox_content=False
        # 결과내 재검색을 체크한 경우
        if checkbox_content:
            request.session['old_input']=request.session['user_input']
            user_input = request.POST['input_Symptom']
            result = query(request.session['old_input'],user_input)
            count, posts, max_index, current_page = pagenation_post(request, result)
            request.session['user_input'] = user_input
            request.session['count'] = count
            return render(request, 'frontpage/more_result.html',
                          {'user_input': user_input, 'posts': posts, 'count': count,
                           'max_index': max_index, 'current_page': current_page})
        # 결과내 재검색을 체크하지 않은 경우
        else:
            user_input = request.POST['input_Symptom']
            result = query(user_input)
            count, posts, max_index,current_page = pagenation_post(request,result)

            # print(posts.object_list[0]['highlight']['symptom'])
            # print(posts.object_list[0]['highlight'])
            # print(re_query('두통 복통', '설사'))
            #print(posts.object_list[0]['_source']['diseaseko'])
            #print(posts.object_list[0])

            request.session['user_input'] = user_input
            request.session['count'] = count
            return render(request, 'frontpage/result.html',
                          {'user_input': user_input, 'posts': posts, 'count': count,
                           'max_index': max_index, 'current_page':current_page})
    # 결과 화면에서 GET방식일 경우.
    else:
        try:
            check = {'user_input': request.session['user_input']}
        except:
            check = False
        # 위의 예외 처리는 Pagination이 POST방식을 활용하는 것이 아니고 GET 방식을 활용하기 때문에 나눠짐.
        ## 결과 화면에서 사용자가 로고를 누를 때와 Pagination의 버튼을 누를 때를 나누기 위해 위의 예외처리를 사용.
        if check:
            user_input = request.session['user_input']
            result = query(user_input)
            count, posts, max_index,current_page = pagenation_post(request,result)

            request.session['user_input'] = user_input
            request.session['count'] = count

            return render(request, 'frontpage/result.html',
                          {'user_input': request.session['user_input'], 'posts': posts,
                           'count': request.session['count'], 'max_index': max_index, 'current_page':current_page})
        # 메인으로 돌아가기.
        else:
            return render(request, 'frontpage/index.html')

def more_result(request):
    request.session.modified = True
    # 결과 화면에서 POST방식 일 경우.
    ## 결과 내 재검색 체크박스가 False인 경우.
    if request.method == "POST":
        user_input = request.POST['input_Symptom']
        result = query(user_input)
        count, posts, max_index, current_page = pagenation_post(request, result)

        #print(posts.object_list[0]['_source']['diseaseko'])
        #print(posts.object_list[0])

        request.session['user_input'] = user_input
        request.session['count'] = count
        # 추가검색을 위해 만들어둔 세션 삭제해야 함.
        del request.session['old_input']
        return render(request, 'frontpage/result.html',
                      {'user_input': user_input, 'posts': posts, 'count': count,
                       'max_index': max_index, 'current_page': current_page})
    else:
        try:
            check = {'user_input': request.session['user_input']}
        except:
            check = False
        # 위의 예외 처리는 Pagination이 POST방식을 활용하는 것이 아니고 GET 방식을 활용하기 때문에 나눠짐.
        ## 결과 화면에서 사용자가 로고를 누를 때와 Pagination의 버튼을 누를 때를 나누기 위해 위의 예외처리를 사용.
        if check:
            user_input = request.session['user_input']
            result = query(user_input)
            count, posts, max_index,current_page = pagenation_post(request,result)

            request.session['user_input'] = user_input
            request.session['count'] = count

            return render(request, 'frontpage/result.html',
                          {'user_input': request.session['user_input'], 'posts': posts,
                           'count': request.session['count'], 'max_index': max_index, 'current_page':current_page})
        # 메인으로 돌아가기.
        else:
            return render(request, 'frontpage/index.html')