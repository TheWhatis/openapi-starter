
# Table of Contents

1.  [Установка](#org357649d)
2.  [Использование](#org6e03dd7)
    1.  [Основное](#orgca2bd77)
    2.  [`start.sh [--api=apiName] [-p|--port=port] [-c|--config=openapiConfig] ...`](#org86cb3ba)
    3.  [`npm start [?name]`](#orgf7de386)
    4.  [`npm run build [?name]`](#orgcfac6b7)
    5.  [`npm test`](#orgb0f6429)
    6.  [`split.sh [openapi.yaml] [outDir]`](#org030cceb)



<a id="org357649d"></a>

# Установка

1.  Установите [Node JS](https://nodejs.org/)
2.  Сделайте клон репозиторий и запустите `npm install` в корневой директории


<a id="org6e03dd7"></a>

# Использование


<a id="orgca2bd77"></a>

## Основное

-   В `redocly.yaml`, в опции `apis` указан список

доступных "разделов" которые можно запустить/собрать ([name]).

-   Все шаблоны и вложения находятся в директории docs
-   Все openapi конфиги находятся в директории openapi


<a id="org86cb3ba"></a>

## `start.sh [--api=apiName] [-p|--port=port] [-c|--config=openapiConfig] ...`

Создает venv для split, устанавливает requirements.txt в окружение,
декомпозирует большой openapi.yaml, запускает предпросмотр документации
по переданному apiName или первый попавшийся по переданному port или по
порту 8080


<a id="orgf7de386"></a>

## `npm start [?name]`

Запускает предпросмотр документации


<a id="orgcfac6b7"></a>

## `npm run build [?name]`

Делает сборку документации


<a id="orgb0f6429"></a>

## `npm test`

Валидирует конфиги


<a id="org030cceb"></a>

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

