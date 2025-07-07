<div align="center">
  <img src="./frontend/assets/images/logo.webp" height="100px" alt="BarberManager Logo"/>
  <h1>BarberManager</h1>

[![Deploy to Production](https://github.com/CreepyMemes/barbermanager/actions/workflows/deploy.yml/badge.svg?branch=master)](https://github.com/CreepyMemes/barbermanager/actions/workflows/deploy.yml)
[![BarberManager](https://img.shields.io/badge/BarberManager-Live%20Website-F38020?labelColor=555555&logo=cloudflare&logoColor=white)](https://barbermanager.creepymemes.com/)
[![API Documentation](https://img.shields.io/badge/Swagger%20UI-API%20Documentation-6ec225?labelColor=555555&logo=swagger&logoColor=white)](https://barbermanager.creepymemes.com/api/)

</div>

## Обзор

BarberManager — это контейнеризованная система управления парикмахерской в виде веб-приложения.

Она предоставляет систему бронирования записей для клиентов, управление доступностью для барберов и автоматические напоминания.

Технологический стек использует **React** (Vite) фронтенд, **Django** бэкенд и полагается на **Docker Compose** для удобной кроссплатформенной разработки и развертывания.

## Содержание

- [Обзор](#обзор)
- [Содержание](#содержание)
- [Возможности](#возможности)
- [Архитектура](#архитектура)
- [Документация API](#документация-api)
- [Продакшн развертывание](#продакшн-развертывание)
- [Быстрый старт](#быстрый-старт)
  - [Требования](#требования)
  - [Рабочий процесс разработки](#рабочий-процесс-разработки)
    - [Клонирование репозитория](#клонирование-репозитория)
    - [Сборка и запуск всех контейнеров](#сборка-и-запуск-всех-контейнеров)
    - [(Опционально) Сброс среды разработки](#опционально-сброс-среды-разработки)
- [Руководство по разработке](#руководство-по-разработке)
  - [Бэкенд (Django)](#бэкенд-django)
    - [Конфигурация](#конфигурация)
    - [Зависимости](#зависимости)
    - [Миграции](#миграции)
    - [Суперпользователь](#суперпользователь)
    - [Запуск тестов](#запуск-тестов)
    - [Диаграмма моделей](#диаграмма-моделей)
  - [Фронтенд (React + Vite)](#фронтенд-react--vite)
    - [Зависимости](#зависимости-1)
    - [Запуск тестов](#запуск-тестов-1)
- [Продакшн рабочий процесс](#продакшн-рабочий-процесс)
  - [Развертывание](#развертывание)
    - [Обзор CI/CD процесса](#обзор-cicd-процесса)

## Возможности

- 💇‍♂️ **Доступность барбера**: Администраторы определяют расписание часовых слотов для каждого барбера.
- 📅 **Записи клиентов**: Клиенты могут бронировать доступные слоты с выбранным барбером и услугой(ами).
- ⏰ **Напоминания и автоматизация**: Email напоминания и автоматическое обновление статуса записей через задачи Celery.
- 💬 **Отзывы клиентов**: Разрешены только после завершенных записей; один на пару клиент-барбер.
- 📊 **Статистика панели управления**: Просмотр бизнес-аналитики и обратной связи.
- 🐳 **Портативная разработка**: Контейнеризация через Docker и VSCode Dev Containers для настройки разработки без конфигурации.
- ♾️ **DevOps и CI/CD**: GitHub Actions автоматизирует тестирование, линтинг и развертывание.

## Архитектура

```mermaid
flowchart TD
    US([Пользователь <br> Браузер/Мобильное])

    RP[Обратный прокси: Nginx]

    subgraph FrontendInfra[Инфраструктура фронтенда]
      subgraph frontend[Контейнер: 'frontend']
        SF[Сервер: Nginx]
        BL[Сборщик: Vite]
        FE[Фронтенд: React SPA]
      end
    end

    subgraph BackendInfra[Инфраструктура бэкенда]
      subgraph backend[Контейнер: 'backend']
        SB[WSGI: Gunicorn]
        BE[Бэкенд: Django REST API]
      end

      subgraph celery[Контейнер: 'celery']
          CW[[Воркер: Celery]]
      end

      subgraph celery-beat[Контейнер: 'celery-beat']
          CB[[Beat: Celery]]
      end

      subgraph db[Контейнер: 'db']
        PG[(База данных: Postgres)]
      end

      subgraph redis[Контейнер: 'redis']
        RD[(Брокер: Redis)]
      end
    end

    %% Пользователь
    US -- HTTPS --> RP
    RP -- Маршруты --> SF
    RP -- Маршруты --> SB

    %% Инфраструктура фронтенда
    SF -- Обслуживает --> BL
    BL -- Собирает --> FE

    %% Инфраструктура бэкенда
    SB -- Обслуживает --> BE
    BE -- Доступ ORM --> PG
    CW -- Доступ ORM (для логики задач) --> PG
    CW -- Извлекает задачи --> RD
    CB -- Ставит задачи в очередь --> RD
    BE .-> CW
    BE .-> CB

    style FrontendInfra fill:#0005
    style BackendInfra fill:#0005

    style frontend fill:#2496ED50
    style backend fill:#2496ED50
    style celery fill:#2496ED50
    style celery-beat fill:#2496ED50
    style db fill:#2496ED50
    style redis fill:#2496ED50

    style SF fill:#009639
    style BL fill:#646CFF
    style FE fill:#61DAFB
    style FE color:#000
    style RP fill:#009639
    style BE fill:#092e20
    style SB fill:#499848
    style RD fill:#FF4438
    style PG fill:#4169E1
    style CW fill:#37814A
    style CB fill:#37814A
```

## Документация API

BarberManager предлагает обширную интерактивную документацию API с использованием **Swagger UI**.  
Вы можете изучить все эндпоинты бэкенда, модели, форматы запросов/ответов и попробовать живые запросы прямо в браузере.

➡️ **[Посмотрите документацию API здесь.](https://barbermanager.creepymemes.com/api/)**  
Или нажмите на зеленый бейдж "Swagger UI" в верхней части этого README.

Типичные возможности документации API:

- **Визуальный интерфейс** для изучения всех доступных эндпоинтов и методов.
- **Живая функция "Try it Out"** для аутентификации и тестирования API вызовов.
- **Схемы моделей** и детали обязательных/опциональных полей для каждой операции.

Эта документация всегда актуальна с развернутым бэкендом и является полезным ресурсом для фронтенд разработчиков, интеграторов и тестировщиков.

## Продакшн развертывание

Вы можете попробовать BarberManager самостоятельно на нашем живом продакшн сайте!

➡️ **[Открыть живой сайт](https://barbermanager.creepymemes.com/)**  
Или нажмите на оранжевый бейдж "BarberManager" в верхней части этого README.

Продакшн развертывание включает:

- Последнюю доступную версию, всегда поддерживаемую в актуальном состоянии через автоматизированный CI/CD.
- Полный доступ к основным возможностям веб-приложения, описанным в данной документации.
- Реальную рабочую среду для тестирования, демонстраций или изучения в качестве разработчика, администратора или клиента.

## Быстрый старт

### Требования

- [Docker](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [VSCode](https://code.visualstudio.com/) (+ [Dev Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers))

### Рабочий процесс разработки

Этот раздел о рабочем процессе разработки в программировании и тестировании приложения на локальной машине.

> [!TIP]
> Если вы хотите запустить **VSCode** внутри контейнера бэкенда.
> Когда вы откроете папки проекта `backend` или `frontend` в **VSCode**,
> он должен автоматически обнаружить конфигурации `.devcontainer`.
>
> Если он не обнаружит их или вы проигнорируете уведомление, вы можете:
> Открыть палитру команд (`Ctrl+Shift+P` или `Cmd+Shift+P` на macOS).
> Выбрать `Remote-Containers: Reopen in Container`.

#### Клонирование репозитория

Если репозиторий публичный:

```bash
git clone https://github.com/CreepyMemes/barbermanager.git
cd barbermanager/
```

Если репозиторий приватный:

> [!IMPORTANT]
> Замените **TOKEN** на ваш github токен

```bash
git clone https://CreepyMemes:TOKEN@github.com/CreepyMemes/barbermanager.git
cd barbermanager
```

#### Сборка и запуск всех контейнеров

```bash
docker compose -f docker-compose.dev.yml --env-file .env.dev up --build
```

- Фронтенд: [http://localhost:3000](http://localhost:3000)
- Бэкенд: [http://localhost:8000](http://localhost:8000)

#### (Опционально) Сброс среды разработки

```bash
docker compose -f docker-compose.dev.yml down --volumes --remove-orphans
```

## Руководство по разработке

### Бэкенд (Django)

Django dev сервер автоматически перезагружается при изменении кода.

> [!IMPORTANT]
> Выполните следующие команды _внутри_ контейнера.
> запустив следующую команду:
>
> ```bash
> docker compose -f docker-compose.dev.yml --env-file .env.dev exec -it backend sh
> ```

#### Конфигурация

Создайте новый файл `.env` в корневой директории и введите ваши учетные данные, следуя примеру в `.env.example`:

```sh
# Django конфигурация
SECRET_KEY=your-super-secret-key-here
DJANGO_ALLOWED_HOSTS=*
DJANGO_SETTINGS_MODULE=config.settings.dev # измените .dev или .prod

# Конфигурация базы данных
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=mydb
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword

# Конфигурация email
EMAIL_HOST='smtp.server.com'
EMAIL_PORT=587
EMAIL_HOST_USER='your.stmp@email.com'
EMAIL_HOST_PASSWORD='your stmp pass here'
```

#### Зависимости

Для установки новых зависимостей, для базовых, продакшн или dev:

```bash
pip install <package>
pip freeze > requirements/base.txt
pip freeze > requirements/dev.txt
pip freeze > requirements/prod.txt
```

#### Миграции

Для миграции базы данных:

```bash
python manage.py migrate
```

#### Суперпользователь

Для создания пользователя администратора:

```bash
python manage.py createsuperuser
```

#### Запуск тестов

Для простого запуска всех тестов:

```bash
python manage.py test api
```

Для проверки покрытия тестами мы используем пакет `coverage`, который подсвечивает, какие части кодовой базы тестируются:

```bash
coverage run --source="." manage.py test api
coverage html
```

#### Диаграмма моделей

Для генерации диаграммы моделей мы используем пакет `django-extensions`, который включает генератор диаграмм для всех реализованных моделей, найденных в проекте:

```bash
python manage.py graph_models -a -o models_diagram.png
```

### Фронтенд (React + Vite)

Vite обеспечивает автоматическую горячую перезагрузку при изменении файлов фронтенда.

> [!IMPORTANT]
> Выполните следующие команды _внутри_ контейнера.
> запустив следующую команду:
>
> ```bash
> docker compose -f docker-compose.dev.yml --env-file .env.dev exec -it frontend sh
> ```

#### Зависимости

Для установки новых зависимостей, для продакшн или dev:

```bash
npm install <package> --save-dev
npm install <package>
```

#### Запуск тестов

[TODO]

## Продакшн рабочий процесс

### Развертывание

Процесс развертывания **полностью автоматизирован** через [GitHub Actions](https://github.com/features/actions). CI/CD пайплайн запускается каждым **Pull Request**:

#### Обзор CI/CD процесса

```mermaid
flowchart TD
    PR(🔀 Pull Request)
    Tests{{🧪 Запуск тестов}}
    Passed([✅ Можно сливать])
    Failed([❌ Нельзя сливать])
    Deployment(🚀 Запуск развертывания)
    PR --> Tests
    Tests -- Пройдено --> Passed
    Tests -- Провалено --> Failed
    Passed -- Слияние --> Deployment
```

1. **Сборка и тестирование:**  
   Все pull request'ы запускают автоматические сборки и тесты в продакшн-подобной Docker среде.
2. **Слияние и автоматическое развертывание:**  
   Если тесты проходят, pull request может быть слит.  
   После слияния код автоматически развертывается на сервере через SSH.

- Переменные окружения предоставляются безопасно через GitHub Secrets.
- Развертывания используют кастомный скрипт `deploy.sh` для нулевого времени простоя.
