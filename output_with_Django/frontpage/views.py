from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .query import *


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

    re_search_check=False
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
        request.session['posts'] = posts

        return render(request, 'frontpage/result.html',
                      {'user_input': user_input, 'posts': posts, 'count': count,
                       'max_index': max_index,'current_page':current_page,'re_search_check':re_search_check})
    # 메인화면에서 GET방식일 경우. 이전 검색 내역을 지워주자.
    else:
        try:
            del request.session['user_input']
            del request.session['count']
            del request.session['posts']
        except:
            print('no data')
        return render(request, 'frontpage/index.html')

def result(request):
    request.session.modified = True
    try:
        re_search_check = request.session['re_search']
    except:
        re_search_check = False
    # 결과 화면에서 POST방식 일 경우.
    if request.method == "POST":
        try:
            checkbox_content=request.POST['re-search']
        except:
            checkbox_content=False

        # 결과내 재검색을 체크한 경우
        print(checkbox_content)
        if checkbox_content:
            request.session['old_input']=request.session['user_input']
            old_input = request.session['old_input']
            request.session['re_search']=checkbox_content
            user_input = request.POST['input_Symptom']

            result = re_query(request.session['old_input'],user_input)
            count, posts, max_index, current_page = pagenation_post(request, result)
            request.session['user_input'] = user_input
            request.session['count'] = count
            request.session['posts'] = posts.object_list
            print(old_input)
            print(user_input)
            return render(request, 'frontpage/result.html',
                          {'user_input': user_input, 'posts': posts, 'count': count,'old_input':old_input,
                           'max_index': max_index, 'current_page':current_page,'re_search_check':checkbox_content})
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
            request.session['posts'] = posts.object_list
            #print(posts.object_list[0]['_source']['diseaseko'])
            # 추가검색을 위해 만들어둔 세션 삭제해야 함.
            print("-------------------------------------------")
            print(current_page)
            print("-------------------------------------------")
            try:
                del request.session['old_input']
                del request.session['re_search']
            except:
                print("not re_query")
            return render(request, 'frontpage/result.html',
                          {'user_input': user_input, 'posts': posts, 'count': count,
                           'max_index': max_index, 'current_page':current_page,'re_search_check':checkbox_content})
    # 결과 화면에서 GET방식일 경우.
    else:
        # 예외 처리는 Pagination이 POST방식을 활용하는 것이 아니고 GET 방식을 활용하기 때문에 나눠짐.
        ## 결과 화면에서 사용자가 로고를 누를 때와 Pagination의 버튼을 누를 때를 나누기 위해 예외처리를 사용.
        try:
            search_check = request.session['user_input']
        except:
            search_check = False
        try:
            old_input = request.session['old_input']
        except:
            old_input = False

        if re_search_check:
            user_input = request.session['user_input']
            result = re_query(old_input,user_input)
            count, posts, max_index,current_page = pagenation_post(request,result)

            request.session['user_input'] = user_input
            request.session['count'] = count

            return render(request, 'frontpage/result.html',
                          {'user_input': request.session['user_input'], 'posts': posts, 'old_input':old_input,
                           'count': request.session['count'], 'max_index': max_index, 'current_page':current_page,'re_search_check':re_search_check})

        # Pagination 이용할 때
        elif search_check:
            user_input = request.session['user_input']
            result = query(user_input)
            count, posts, max_index,current_page = pagenation_post(request,result)

            request.session['user_input'] = user_input
            request.session['count'] = count
            request.session['posts'] = posts.object_list
            print("-------------------------------------------")
            print(current_page)
            print("-------------------------------------------")
            return render(request, 'frontpage/result.html',
                          {'user_input': request.session['user_input'], 'posts': posts,'old_input':old_input,
                           'count': request.session['count'], 'max_index': max_index, 'current_page':current_page,'re_search_check':re_search_check})
        # 메인으로 돌아가기.
        else:
            try:
                del request.session['user_input']
                del request.session['count']
            except:
                print('no data')
            try:
                del request.session['old_input']
                del request.session['re_search']
            except:
                print('no data')
            return render(request, 'frontpage/index.html')


def result_detail(request,query):
    temp=request.session['posts']
    request.session.modified = True
    if request.method == "GET":
        return render(request, 'frontpage/result_detail.html',{'temp':temp[int(query)]})