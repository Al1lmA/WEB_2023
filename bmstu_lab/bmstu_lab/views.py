from django.shortcuts import render
from datetime import date

#Договоры банка. Услуги - набор услуг банка, заявки - заявка на подключение к обслуживанию

database = [
    {'id' : 1, 
     'title' : 'Кредиты', 
     'button_text' : 'Оформить кредит', 
     'short_text': 'Оформи кредит на любые цели', 
     'description' : 'Кредит — сумма средств, которая передаётся банком своему клиенту во временное пользование с условием своевременного возврата и уплаты процента за их использование.',
     'img' : 'https://ggo.ismcdn.jp/mwimgs/2/2/-/img_228fa19c34db8f44cb3e90437606c043105422.jpg',
     'order_img' : 'https://polinka.top/uploads/posts/2023-05/thumbs/1684801387_polinka-top-p-bankovskie-kartinki-dlya-prezentatsii-kras-18.jpg',
     },
    {'id' : 2, 
     'title' : 'Вклады', 
     'button_text' : 'Оформить вклад', 
     'short_text': 'Самые выгодные вклады по стране', 
     'description' : 'Банковский вклад (депозит) — денежная сумма, которую гражданин передаёт в банк с условием обратного её возврата через определённый срок или по первому требованию вкладчика, а также начисления банком процентов на всю сумму депозита.',
     'img' : 'https://catherineasquithgallery.com/uploads/posts/2021-02/1613631468_110-p-fon-dlya-prezentatsii-po-ekonomike-122.jpg',
     'order_img' : 'https://trafaret-decor.ru/sites/default/files/2023-03/Банк%20%289%29.jpg',
     },
    {'id' : 3, 
     'title' : 'Карты', 
     'button_text' : 'Оформить карту', 
     'short_text': 'Пользоваться нашими картами - выгодно!', 
     'description' : 'Банковская карта — пластиковая карта стандартного размера, на которой хранится информация в электронном виде о банковском счёте держателя карты.',
     'img' : 'https://cdn.newswire.com/files/x/3b/27/534c5fdad46d06908f61f33c6232.jpg',
     'order_img' : 'https://klike.net/uploads/posts/2023-03/1679029773_3-129.jpg',
     },
    # {'id' : 4, 'title' : 'Инвестиции', 'button-text' : 'Открыть брокерский счёт', 'description' : ''},
    # {'id' : 5, 'title' : 'Инвестиции', 'button-text' : 'Открыть брокерский счёт', 'description' : ''},
    # {'id' : 6, 'title' : 'Инвестиции', 'button-text' : 'Открыть брокерский счёт', 'description' : ''},
    # {'id' : 7, 'title' : 'Инвестиции', 'button-text' : 'Открыть брокерский счёт', 'description' : ''},
]

def GetOrders(request):
    try:
        input_text = request.GET['txt']
        if input_text:
            orders = [order for order in database if input_text.lower() in order['title'].lower()]
        return render(request, 'orders.html', {'data':{
            'orders':orders,
            'search' : input_text
            }})
    except:
        return render(request, 'orders.html', {'data' : {
            'orders': database,
            'search' : input_text
        }})

def GetOrder(request, id):
    for item in database:
        if item['id'] == id:
            current_data = item
    return render(request, 'order.html', {'data' : {
        'id': id,
        'order' : current_data
    }})

