
# Table of Contents

1.  [Установка](#org2d1f942)
2.  [Использование](#orgc897257)
    1.  [Основное](#orgd8b23cf)
    2.  [`start.sh [--api=apiName] [-p|--port=port] [-c|--config=openapiConfig] ...`](#org9da3f1d)
    3.  [`npm start [?name]`](#orga6ea073)
    4.  [`npm run build [?name]`](#org173f01e)
    5.  [`npm test`](#orgb90d16c)
    6.  [`split.sh [openapi.yaml] [outDir]`](#orgcd67ece)



<a id="org2d1f942"></a>

# Установка

1.  Установите [Node JS](https://nodejs.org/)
2.  Сделайте клон репозиторий и запустите `npm install` в корневой директории


<a id="orgc897257"></a>

# Использование


<a id="orgd8b23cf"></a>

## Основное

-   В `redocly.yaml`, в опции `apis` указан список доступных "разделов" которые можно запустить/собрать ([name]).
-   Все шаблоны и вложения находятся в директории docs
-   Все openapi конфиги находятся в директории openapi


<a id="org9da3f1d"></a>

## `start.sh [--api=apiName] [-p|--port=port] [-c|--config=openapiConfig] ...`

Создает venv для split, устанавливает requirements.txt в окружение,
декомпозирует большой openapi.yaml, запускает предпросмотр документации
по переданному apiName или первый попавшийся по переданному port или по
порту 8080


<a id="orga6ea073"></a>

## `npm start [?name]`

Запускает предпросмотр документации


<a id="org173f01e"></a>

## `npm run build [?name]`

Делает сборку документации


<a id="orgb90d16c"></a>

## `npm test`

Валидирует конфиги


<a id="orgcd67ece"></a>

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
    на внешние (#/components/schema/asd станет refs/somehash.yaml
    или somehash.yaml)

2.  Собирает и группирует полученные из 1го пункта пути по тегам.
3.  Генерирует разделенные по тегам данные.
    
    по-сути если есть тэг Address, то в файле Address.yaml
    будет не полноценный конфиг openapi, а список путей

