# Async filr upload to S3

## RU

### Способ запуска

> Для начала нужно зайти в ```docker-compose.yml``` и вписать свои ключи от IAM и название Bucket. После прописать ```docker-compose build``` для сбора образа (подгрузка пакетов кэшируется). Запуск проекта будет через ```docker-compose up``` и сервер будет стоять на *localhost:8080* . Выбираем файл и отправляем. В случае чего, можно поиграться с настройками в *config.py* файле. В проекте для многопоточности использовался threading

### Launch method

> First you need to go to ``docker-compose.yml`` and enter your keys from IAM and Bucket name. After that, write ``docker-compose build`` to collect the image (loading packages is cached). The project will be launched via ``docker-compose up`` and the server will be on *localhost:8080* . Select the file and send it. If anything, you can play around with the settings in *config.py * file. In the project, threading was used for multithreading

# Endpoints

-- http://localhost:8080 - Main template (choose file)

-- http://localhost:8000/upload/ - POST (file upload)
