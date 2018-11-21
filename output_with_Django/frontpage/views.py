from frontpage.models import Temp
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect

# Create your views here.
def index(request):
    return render(request, 'frontpage/index.html')

def result(request):
    if request.method == "POST":
        return redirect('index')
    else:
        return redirect('index')

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