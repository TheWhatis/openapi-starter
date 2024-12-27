
# Table of Contents

1.  [Установка](#org07351b4)
2.  [Использование](#orgfa7dbef)
    1.  [Основное](#orgce9a79b)
    2.  [`start.sh [--api=apiName] [-p|--port=port] [-c|--config=openapiConfig] ...`](#orgc0e68ee)
    3.  [`npm start [?name]`](#org39ea6fb)
    4.  [`npm run build [?name]`](#org5646de7)
    5.  [`npm test`](#org527363b)
    6.  [`split.sh [openapi.yaml] [outDir]`](#org3573b43)



<a id="org07351b4"></a>

# Установка

1.  Установите [Node JS](https://nodejs.org/)
2.  Сделайте клон репозиторий и запустите `npm install` в корневой директории


<a id="orgfa7dbef"></a>

# Использование


<a id="orgce9a79b"></a>

## Основное

-   В `redocly.yaml`, в опции `apis` указан список доступных "разделов" которые можно запустить/собрать ([name]).
-   Все шаблоны и вложения находятся в директории docs
-   Все openapi конфиги находятся в директории openapi

1.  `npm install`
2.  `./start.sh`


<a id="orgc0e68ee"></a>

## `start.sh [--api=apiName] [-p|--port=port] [-c|--config=openapiConfig] ...`

Создает venv для split, устанавливает requirements.txt в окружение,
декомпозирует большой openapi.yaml, запускает предпросмотр документации
по переданному apiName или первый попавшийся по переданному port или по
порту 8080


<a id="org39ea6fb"></a>

## `npm start [?name]`

Запускает предпросмотр документации


<a id="org5646de7"></a>

## `npm run build [?name]`

Делает сборку документации


<a id="org527363b"></a>

## `npm test`

Валидирует конфиги


<a id="org3573b43"></a>

## `split.sh [openapi.yaml] [outDir]`

Подбробнее об аргументах можно посмотреть:
`split.sh -h`.

Разбирает большой openapi yaml на составные
части. На текущий момент разделяет только по
тегам:

1.  Ищет все пути, обрабатывает ссылки
    
    Выносит все внутренние ссылки ($ref) в
    поддиректорию refs ({outDir}/refs).
    
    Заменяет соответственно пути ссылок из внутренних
    на внешние (`#/components/schema/asd` станет `refs/somehash.yaml`
    или `somehash.yaml`)

2.  Собирает и группирует полученные из 1го пункта пути по тегам.
3.  Генерирует разделенные по тегам данные.
    
    По-сути если есть тэг Address, то в файле Address.yaml
    будет не полноценный конфиг openapi, а список путей

