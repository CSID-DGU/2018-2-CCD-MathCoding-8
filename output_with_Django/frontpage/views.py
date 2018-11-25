from frontpage.models import Temp
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect

# Create your views here.
def index(request):
    print("hihi")
    if request.method == "POST":
        test=request
        # Html에서 test.POST.input_Symptom
        # python 코드에서는 접근 방법이 약간 달랐음.
        user_input=test.POST['input_Symptom']
        result=Temp.objects.filter(origin=user_input)
        #for i in result:
            #print(i.synonym)
        return render(request, 'frontpage/result.html',
                      {'test': test,'result':result})
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