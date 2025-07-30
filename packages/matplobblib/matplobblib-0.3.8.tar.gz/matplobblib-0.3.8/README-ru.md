<center>
    <img src="icon.png" alt="icon" width="400" />
</center>

# matplobblib

Замечательная библиотека разных структур для реализации на языке python

[![PyPI version](https://badge.fury.io/py/matplobblib.svg)](https://badge.fury.io/py/matplobblib)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/pypi/pyversions/matplobblib.svg)](https://pypi.org/project/matplobblib/)

## Выберите язык:

- [English README](README.md) 🇬🇧
- [Русский README](README-ru.md) 🇷🇺

## Краткое описание

Библиотека `mdatplobblib` предоставляет набор инструментов и функций для различных предметных областей, включая анализ и структуры данных (АИСД), теорию вероятностей и математическую статистику (ТВиМС), машинное обучение (ML) и численные методы (NM).

## Оглавление

- Установка
- Быстрый старт
- Модули
- Зависимости
- Участие в разработке
- Лицензия
- Контакты

## Установка

Для установки библиотеки `matplobblib` выполните следующую команду:

```bash
pip install matplobblib
```

Убедитесь, что у вас установлен Python версии 3.6 или выше.

## Быстрый старт

Импортируйте необходимые модули и начните использовать функции:

```python
# Пример импорта модулей
import matplobblib.aisd as aisd
import matplobblib.tvims as tvims
import matplobblib.ml as ml
import matplobblib.nm as nm

# Пример использования функции из модуля tvims для отображения доступных тем
tvims.description()

# Для получения подробной информации о функциях каждого модуля,
# обратитесь к соответствующим README файлам модулей.
```

## Модули

Библиотека включает следующие основные модули:

* ### **[aisd](https://github.com/Ackrome/matplobblib/tree/master/matplobblib/aisd)**: Реализации различных алгоритмов и структур данных.
* ### **[tvims](https://github.com/Ackrome/matplobblib/tree/master/matplobblib/tvims#readme)**: Функции и инструменты для теории вероятностей и математической статистики. Включает в себя теоретические материалы, расчеты для случайных величин, проверку гипотез и многое другое.
* ### **[ml](https://github.com/Ackrome/matplobblib/tree/master/matplobblib/ml#readme)**: Инструменты и алгоритмы для задач машинного обучения.
* ### **[nm](https://github.com/Ackrome/matplobblib/tree/master/matplobblib/nm#readme)**: Реализации численных методов для решения математических задач.

Каждый модуль имеет собственный `README.md` с более подробным описанием его содержимого и примерами использования.

## Зависимости

Основные зависимости проекта:

* numpy
* sympy
* pandas
* scipy
* pyperclip
* pymupdf
* graphviz
* statsmodels
* fitz
* cvxopt

Полный список зависимостей можно найти в файле `setup.py`.

## Участие в разработке

Мы приветствуем вклад в развитие проекта! Если вы хотите предложить улучшения, исправить ошибки или добавить новые функции, пожалуйста, создайте Issue/Pull Request в репозитории.

## Лицензия

Проект распространяется под лицензией MIT. Подробнее см. файл [LICENSE.txt](https://github.com/Ackrome/matplobblib/blob/master/LICENSE.txt)

## Контакты

* **Автор:** Ackrome
* **Email:** ivansergeyevicht@gmail.com
* **GitHub:** https://github.com/Ackrome/matplobblib
