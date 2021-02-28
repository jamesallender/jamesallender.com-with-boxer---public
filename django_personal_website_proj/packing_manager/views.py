from django.shortcuts import render
from .models import Box
from .forms import GetCreateUpdateBox
from django.http import HttpResponse
from django.db.models import Max
from generate_label import download_box_label


def home (request):
    context = {
        'boxes': Box.objects.all(),
    }
    return render(request=request, template_name='packing_manager/home.html', context=context)


def about (request):
    context = {
        'boxes': Box.objects.all(),
    }
    return render(request=request, template_name='packing_manager/about.html', context=context)


def packing_manager_box_lookup(request):
    min_box_id = 100000000
    min_box_num = 0

    # Post requests
    if request.method == 'POST':
        form = request.POST
        print(repr(form))

        try:
            box_warn = form.getlist('box_warnings')
            box_warn = ', '.join(box_warn)
        except Exception:
            box_warn = ""
        box_qr_val = f"http://www.jamesallender.com/packing_manager/box-lookup/?box_id={form['box_id']}"

        contents = form['contents'].replace(', ', ',')
        contents = contents.replace(',', ', ')

        print(f"box_num = {form['box_num']}")
        print(f"box_dest = {form['box_dest']}")
        print(f"contents = {contents}")
        print(f"box_warnings = {box_warn}")
        print(f"box_id = {form['box_id']}")
        print(f"box_qr_val = {box_qr_val}")

        new_box = Box(box_num=form['box_num'], box_dest=form['box_dest'], contents=contents,
                      box_id=form['box_id'], box_warnings=box_warn, box_qr_val=box_qr_val)
        new_box.save()

        if form.__contains__('submit'):
            print('submit clicked')

        elif form.__contains__('submit_and_download'):
            print('submit and download clicked')
            return download_box_label(box_qr_val, form['box_num'], form['box_dest'], contents, form['box_id'],
                                      box_warn)
        # else:
        #     raise ValueError(f"unexpected post request type: {repr(form)}")

    # GET requests
    elif request.method == 'GET':
        form = request.GET
        print(repr(form))

        if form.get('box_id', None):
            # Get Box
            print(f"getting: {form.get('box_id')}")
            box = Box.objects.get(box_id=form.get('box_id'))

            context = {
                'boxes': Box.objects.all(),
                'box': box
            }

            return render(request=request, template_name='packing_manager/box-lookup.html',
                          context=context)

    else:
        raise Exception(f"packing_manager_box_lookup got neiter a get or post request, got: {request}")

    # Get min box id
    max_box_id = Box.objects.aggregate(Max('box_id'))['box_id__max']
    if not max_box_id:
        max_box_id = min_box_id
    elif max_box_id:
        max_box_id = int(max_box_id)
    if max_box_id < min_box_id:
        max_box_id = min_box_id

    # Get min box num
    max_box_num = Box.objects.aggregate(Max('box_num'))['box_num__max']
    if not max_box_num:
        max_box_num = min_box_num
    elif max_box_num:
        max_box_num = int(max_box_num)
    if max_box_num < min_box_num:
        max_box_num = min_box_num

    box = Box(box_num=str(max_box_num+1), box_dest="", contents="", box_id=str(max_box_id+1),
              box_warnings="", box_qr_val="")
    context = {
        'boxes': Box.objects.all(),
        'box': box
    }
    return render(request=request, template_name='packing_manager/box-lookup.html', context=context)

