# Google Cloud Helpers

Набор прослоек для работы с сервисами Google Cloud Platform с использованием библиотеки [Google Cloud](https://googleapis.github.io/google-cloud-python/latest/index.html
)

## Начало работы 

```bash
git clone https://github.com/ArticsIS/Google-Cloud-Helpers.git
cd Google-Cloud-Helpers
python3 -m pip install -r requirements.txt
python3 example.py
```

Авторизация API может происходить как в автоматическом режиме (например, если авторизационная информация содержится в переменных среды), так и в ручном (с использованием ключей сервисного аккаунта) - поведение в данном случае контролируется параметром `local`

## Google Cloud Datastore

Класс `DataStoreObject` содержит только базовые методы работы с объектами в хранилище. В настоящий момент при помощи класса можно:

1. Получить список объектов DataStore *по типу и пространству имен*.
2. Получить список объектов DataStore по значению какого-либо атрибута объекта.
3. Получить объект из DataStore по его названию.
4. Создать или обновить объект в DataStore с заданным названием и значением.

# Google Cloud Tasks

Для работы доступны 2 класса - `CloudTasks` и `CloudQueue` (часть функций наследует от первого класса). В настоящий момент классы позволяют:

1. Получить список очередей App Engine (`CloudTasks`).
2. Создать новую очередь App Engine (`CloudTasks`).
3. Удалить очередь из App Engine (`CloudTasks`).
4. Получить статус работы очереди (`CloudQueue`).
5. Получить список задач в очереди (`CloudQueue`).
6. Приостановить работу очереди (`CloudQueue`).
7. Возобновить работу очереди (`CloudQueue`).
8. Очистить очередь (`CloudQueue`).
9. Добавить новую задачу в очередь (`CloudQueue`).