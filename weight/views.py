# TODO График среднего
# TODO ! Удаление веса из таблицы
# TODO примечание и правка его в таблице

from django.shortcuts import render,HttpResponseRedirect,render_to_response
from .forms import *
from .models import *
from chartit import DataPool, Chart
from django.http import JsonResponse

from django.db import IntegrityError,InterfaceError

from django.utils.dateparse import parse_date

def edit_desc_weight(request):
    print("edit")
    return_dict = dict()
    weight_id = request.POST.get('weight_id')
    desc= request.POST.get('desc')
    weightObject=Weight.objects.filter(id=weight_id).update(description=desc)
    return JsonResponse(return_dict)


def remove_weight(request):
    return_dict = dict()
    weight_id = request.POST.get('weight_id')
    weightObject=Weight.objects.filter(id=weight_id).first()
    weightObject.is_deleted=True
    weightObject.save(force_update=True)
    return JsonResponse(return_dict)

def add_weight(request):
    return_dict = dict()

    date_str = request.POST.get('date')
    date = parse_date(date_str)
    weight = int(request.POST.get('weight'))

    if Weight.objects.filter(date=date,is_deleted=False).count():
        return_dict['error'] = "Запись за " + date.strftime('%d.%m.%Y') + " уже введена"
    else:
        Weight.objects.create(date=date, weight=weight)

    return JsonResponse(return_dict)

def async_weight_table(request):
    weight_list = Weight.objects.filter(is_deleted=False).order_by('-date')
    return render_to_response('table.html', {'weight_list': weight_list})

def async_weight_chart(request):
    cht = create_weight_chart()
    return render_to_response('chart.html', {'cht': cht})

def home(request):
    weight_list = Weight.objects.filter(is_deleted=False).order_by('-date')
    cht = create_weight_chart()
    form = WeightForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        print(form)
        form.save()
        return HttpResponseRedirect("/")
    return render(request, 'weight/home.html', locals())

def create_weight_chart():
    data = \
        DataPool(
            series=
            [{'options': {
                'source': Weight.objects.filter(is_deleted=False)},
                'terms': [
                    'date',
                    'weight',
                    ]}
            ])

    cht = Chart(
        datasource=data,
        series_options=
        [{'options': {
            'type': 'line',
            'stacking': False},
            'terms': {
                'date': [
                    'weight'
                    ]
            }}],
        chart_options=
        {
            'title': {
                'text': 'вес Викули по дням'
            },
            'legend': {
                'enabled': 'false'
            },
            'credits': {
                'enabled': 'false',
                'text':''
            },
            'xAxis': {
                'title': {
                    'text': 'Дни'}},
            'yAxis': {
                'title': {
                    'text': 'Вес'}},
            'chart':{
                'backgroundColor':'#f0f7f7',
                'borderWidth':'0'
            }
        }
    )
    return cht