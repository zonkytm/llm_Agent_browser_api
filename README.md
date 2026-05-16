# DeepSeek Code Agent

Локальный AI-агент, который использует веб-интерфейс [DeepSeek](https://chat.deepseek.com/) как языковую модель и выполняет команды прямо на вашей машине — читает, создаёт и редактирует файлы по инструкции модели.

## Как это работает

1. Запускает Chrome с отдельным профилем и открывает chat.deepseek.com
2. Подключается к браузеру через Selenium
3. Отправляет системный промпт, превращая DeepSeek в Code Agent
4. Принимает ваши запросы, передаёт их модели и выполняет её команды на локальной файловой системе

## Структура проекта

```
deepseek_agent/
├── main.py              # точка входа
├── config.py            # настройки и system prompt
├── logger.py            # цветной вывод
│
├── browser/
│   ├── launcher.py      # запуск и подготовка Chrome
│   ├── driver.py        # Selenium, ввод текста, отправка сообщений
│   └── response.py      # потоковое чтение ответа
│
├── agent/
│   └── agent.py         # инициализация и цикл диалога
│
└── tools/
    ├── fs.py            # LIST_DIR, READ_FILE, WRITE_FILE
    └── dispatcher.py    # парсинг вызовов инструментов из ответа модели
```

## Требования

- Python 3.10+
- Google Chrome
- Аккаунт на [chat.deepseek.com](https://chat.deepseek.com/)

## Установка Зависимостей

```bash
pip install -r requirements.txt
```

## Запуск

```bash
python main.py
```

При первом запуске Chrome откроется автоматически. Если вы ещё не авторизованы на DeepSeek — войдите вручную, затем перезапустите агента.

## Конфигурация

Все настройки в `config.py`:

| Параметр | По умолчанию | Описание |
|---|---|---|
| `CHROME_PATH` | `C:\Program Files\...` | Путь к исполняемому файлу Chrome |
| `DEBUG_PROFILE_ROOT` | `C:\chrome_debug` | Папка для отдельного профиля агента |
| `DEBUG_PORT` | `9222` | Порт remote debugging |
| `DEEPSEEK_URL` | `https://chat.deepseek.com/` | URL чата |

## Инструменты агента

Модель может вызывать три инструмента:

- **LIST_DIR** — список файлов в директории
- **READ_FILE** — чтение содержимого файла (до 6000 символов)
- **WRITE_FILE** — запись файла (создаёт папки при необходимости)

## Лицензия

MIT — см. [LICENSE](LICENSE)
