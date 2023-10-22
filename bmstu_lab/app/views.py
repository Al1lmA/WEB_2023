from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.db import connection
from . import models

#Договоры банка. Услуги - набор услуг банка, заявки - заявка на подключение к обслуживанию

def GetOrders(request):
    try:
        input_text = request.GET['txt']
        if input_text:
            orders = [order for order in models.BankServices.objects.filter(service_status='действует') if input_text.lower() in order.title.lower()]
        return render(request, 'orders.html', {'data':{
            'orders':orders,
            'search' : input_text
            }})
    except:
        return render(request, 'orders.html', {'data' : {
            'orders': models.BankServices.objects.filter(service_status='действует'),
        }})

def GetOrder(request, id):
    return render(request, 'order.html', {'data' : {
        'id': id,
        'order' : models.BankServices.objects.filter(bank_service_id=id).first(),
    }})

def ClickRemoveButton(request, id):
    if not CardRemove(id):
        pass
    return redirect(reverse('order_url'))


def CardRemove(id):
    try:
        with connection.cursor() as cursor:    
            quarry = f"UPDATE bank_services SET service_status = 'удалён' WHERE bank_service_id = %s"
            cursor.execute(quarry, [id])
            connection.commit()            
            return True
        
    except Exception as e:
        print(f"Ошибка: {str(e)}")
        return False
