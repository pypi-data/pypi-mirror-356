# XiocaAPI Python Client

[![PyPI version](https://badge.fury.io/py/xiocaapi.svg)](https://badge.fury.io/py/xiocaapi)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Асинхронный и синхронный клиент для взаимодействия с [Xioca API](https://xioca.live/).

## Установка

```bash
pip install xiocaapi
```

## Быстрый старт

### 1. Получение API ключа

Для использования библиотеки вам понадобится API ключ.

➡️ Получить его можно бесплатно в Telegram боте: [@xioca_apibot](https://t.me/xioca_apibot)

### 2. Использование

Ключ можно передать напрямую в клиент или использовать переменную окружения `XIOCA_API_KEY`.

### Асинхронное использование

```python
import asyncio
from xiocaapi import AsyncXiocaAPI, APIError

async def main():
    # Передайте ключ напрямую:
    client = AsyncXiocaAPI(api_key="ВАШ_КЛЮЧ")
    try:
        response = await client.chat.create(
            model="deepseek-v3",
            messages=[{"role": "user", "content": "Привет, мир!"}]
        )
        print(response.choices[0].message.content)
    except APIError as e:
        print(f"Ошибка API: {e}")
    finally:
        # Важно закрывать клиент, если он создан не через 'async with'
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### Синхронное использование

```python
from xiocaapi import XiocaAPI, APIError

try:
    # Передайте ключ напрямую:
    client = XiocaAPI(api_key="ВАШ_КЛЮЧ")

    response = client.chat.create(
        model="deepseek-v3",
        messages=[{"role": "user", "content": "Привет, мир!"}]
    )
    print(response.choices[0].message.content)
except APIError as e:
    print(f"Ошибка API: {e}")
```

## Лицензия

Этот проект распространяется под лицензией MIT.