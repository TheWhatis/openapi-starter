
# Table of Contents

1.  [Установка](#org1f5ce26)
2.  [Использование](#org1540d1c)
    1.  [Основное](#org2defc60)
    2.  [`start.sh [--api=apiName] [-p|--port=port] [-c|--config=openapiConfig] ...`](#org1dc4630)
    3.  [`npm start [?name]`](#org572df41)
    4.  [`npm run build [?name]`](#orgda68016)
    5.  [`npm test`](#org63b8af5)
    6.  [`split.sh [openapi.yaml] [outDir]`](#org217a85c)



<a id="org1f5ce26"></a>

# Установка

1.  Установите [Node JS](https://nodejs.org/)
2.  Сделайте клон репозиторий и запустите `npm install` в корневой директории


<a id="org1540d1c"></a>

# Использование


<a id="org2defc60"></a>

## Основное

-   В `redocly.yaml`, в опции `apis` указан список доступных "разделов" которые можно запустить/собрать ([name]).
-   Все шаблоны и вложения находятся в директории docs
-   Все openapi конфиги находятся в директории openapi


<a id="org1dc4630"></a>

## `start.sh [--api=apiName] [-p|--port=port] [-c|--config=openapiConfig] ...`

Создает venv для split, устанавливает requirements.txt в окружение,
декомпозирует большой openapi.yaml, запускает предпросмотр документации
по переданному apiName или первый попавшийся по переданному port или по
порту 8080


<a id="org572df41"></a>

## `npm start [?name]`

Запускает предпросмотр документации


<a id="orgda68016"></a>

## `npm run build [?name]`

Делает сборку документации


<a id="org63b8af5"></a>

## `npm test`

Валидирует конфиги


<a id="org217a85c"></a>

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

