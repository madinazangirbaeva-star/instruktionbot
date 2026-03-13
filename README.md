# 🤖 Бот для канала @instruktionforlife

Telegram-бот на Python (aiogram 3) + Claude AI.

## Что умеет
- Отвечает на вопросы по темам канала: финансы, быт, карьера, отношения
- Поддерживает, когда пользователю тяжело
- Рекомендует статьи из канала
- Запоминает контекст диалога (последние 20 сообщений)

---

## Быстрый старт

### 1. Получи токены

**Telegram Bot Token:**
1. Напиши @BotFather в Telegram
2. `/newbot` → введи имя и username бота
3. Скопируй токен вида `1234567890:ABC...`

**Anthropic API Key:**
1. Зайди на https://console.anthropic.com
2. API Keys → Create Key
3. Скопируй ключ вида `sk-ant-...`

### 2. Установи зависимости

```bash
pip install -r requirements.txt
```

### 3. Настрой переменные окружения

```bash
cp .env.example .env
# Открой .env и вставь свои токены
```

### 4. Запусти бота

```bash
python bot.py
```

---

## Деплой (бесплатно)

### Railway (рекомендуется)
1. https://railway.app → New Project → Deploy from GitHub
2. Загрузи код в репозиторий GitHub
3. В Railway добавь переменные окружения из `.env`
4. Готово — бот работает 24/7

### Render
1. https://render.com → New Web Service
2. Тип: Worker (не Web)
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `python bot.py`
5. Добавь Environment Variables

### Локально (для теста)
Просто запусти `python bot.py` — бот работает пока открыт терминал.

---

## Команды бота
- `/start` — приветствие и главное меню
- `/help` — помощь
- `/clear` — сбросить историю диалога

---

## Структура файлов
```
instruktionbot/
├── bot.py          # Основной код бота
├── config.py       # Настройки и переменные окружения
├── requirements.txt
├── .env.example    # Пример .env файла
└── README.md
```
