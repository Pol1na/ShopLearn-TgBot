from botapp import db_manager
from botapp.misc import bot


def user_data_message(user_data):
    msg_text = f"ФИО: {user_data['name']}\n" \
               f"Адрес: {user_data['address']}\n" \
               f"Номер телефона: {user_data['phone']}"
    return msg_text


def order_data_message(user_data):
    print(user_data)
    name = user_data['name'].split(' ')
    msg_text = f"ФИО Плательщика: {name[1]} {name[0]} {name[2]}\n" \
               f"ФИО Получателя: Не указан\n" \
               f"Адрес: {user_data['address']}\n" \
               f"Номер телефона: {user_data['phone']}\n \n" \
               f"Использовать эти данные?"
    return msg_text



def order_newdata_message(user_data):
    name = user_data['name'].split(' ')[0]
    surname = user_data['name'].split(' ')[1]
    patronymic = user_data['name'].split(' ')[2]
    msg_text = f"ФИО Плательщика: {name} {surname} {patronymic}\n" \
               f"ФИО Получателя: Не указан\n" \
               f"Адрес: {user_data['address']}\n" \
               f"Номер телефона: {user_data['phone']}\n \n" \
               f"Сохранить эти данные в профиле для дальнейших заказов?"
    return msg_text


def create_order_message(order_data):
    msg_text = f"Спасибо, ваш заказ {order_data['order_id']} оформлен!\n\n" \
               f"Сумма итого: {order_data['summa']}\n\n" \
               f"Вы получите уведомление о статусе заказа в боте!"
    return msg_text
