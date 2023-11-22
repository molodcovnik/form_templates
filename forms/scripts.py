import datetime

import requests
import random
import string

url = 'http://127.0.0.1:8000/api/get_form/?'

fields = ['user_name', 'user_email', 'user_phone', 'order_date', 'gender', 'lead_email', 'name',
          'mobile', 'mail']

dates = ['01.01.2022', '12.01.2022', '21.11.2023', '011.01.222', '01.13.2022',
        '2022-01-11', '2023-12-31', '2022-15-11', 'mail@mail.ru', 'mail@.mail.ru', 'mail.mail.ru', 'mail@mail.com',
        '89056621267', '8-903-111-11-11', '+7-903-111-11-11', '79152221199', '+89152221199', 'nik', 'sda', 'andrei', 'dmitriy', 'olga',
         'elena', 'inna', 'petr', 'igor', 'alex', 'tim']

# url_test = f'{url}{random.choices(fields)[0]}={random.choices(dates)[0]}&{random.choices(fields)[0]}={random.choices(dates)[0]}'

for i in range(150):
    field1 = random.choices(fields)[0]
    field2 = random.choices(fields)[0]
    value1 = random.choices(dates)[0]
    value2 = random.choices(dates)[0]
    print(f'{field1} -- {value1}, {field2} -- {value2}')
    # res = requests.get(f'{url}{random.choices(fields)[0]}={random.choices(dates)[0]}&{random.choices(fields)[0]}={random.choices(dates)[0]}')
    res = requests.get(f'{url}{field1}={value1}&{field2}={value2}')
    # if res.status_code == 200:
    #     print(res.text)
    for r in res:
        print(res.status_code, r)
    print('________________')