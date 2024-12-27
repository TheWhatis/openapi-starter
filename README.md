
# Table of Contents

1.  [Установка](#orgda6af3b)
2.  [Использование](#org0cb8bcb)
    1.  [Основное](#orgb549a1a)
    2.  [`npm start [?name]`](#org485fcae)
    3.  [`npm run build [?name]`](#org2fbd8c6)
    4.  [`npm test`](#org2b4cb08)
    5.  [`split.sh [openapi.yaml] [outDir]`](#org5d1f299)



<a id="orgda6af3b"></a>

# Установка

1.  Установите [Node JS](https://nodejs.org/)
2.  Сделайте клон репозиторий и запустите `npm install` в корневой директории


<a id="org0cb8bcb"></a>

# Использование


<a id="orgb549a1a"></a>

## Основное

-   В `redocly.yaml`, в опции `apis` указан список

доступных "разделов" которые можно запустить/собрать ([name]).

-   Все шаблоны и вложения находятся в директории docs
-   Все openapi конфиги находятся в директории openapi


<a id="org485fcae"></a>

## `npm start [?name]`

Запускает предпросмотр документации


<a id="org2fbd8c6"></a>

## `npm run build [?name]`

Делает сборку документации


<a id="org2b4cb08"></a>

## `npm test`

Валидирует конфиги


<a id="org5d1f299"></a>

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

