from frontpage.models import Temp
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect

from elasticsearch import Elasticsearch
es_client = Elasticsearch("localhost:9200")

# Create your views here.
def index(request):
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
        count = result['hits']['total']
        disease = result['hits']['hits']
        print(count)
        print(disease)
        return render(request, 'frontpage/result.html',
                      {'user_input': user_input, 'disease': disease, 'count': count})
    else:
        return render(request, 'frontpage/index.html')


    '''    
    elif request.method == "POST":
        form = GallaryForm(request.POST)
        formset = ImageFormset(request.POST or None, request.FILES or None)
        if form.is_valid() and formset.is_valid():
            gallary = form.save(commit=False)
            gallary.origin_date = timezone.now()
            gallary.final_date = timezone.now()
            gallary.writer_name = check['name']
            gallary.writer_id = check['id']
            gallary.save()

            for f in formset:
                try:
                    photo = Images(post=gallary, image=f.cleaned_data['image'])
                    photo.save()

                except Exception as e:
                    break
            return redirect('album')
    return render(request, 'blog/album_edit.html',
                  {'form': form, 'formset': formset, 'check': check})
    '''