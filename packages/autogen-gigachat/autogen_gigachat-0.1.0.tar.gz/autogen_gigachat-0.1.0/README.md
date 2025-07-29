# О autogen-gigachat

autogen-gigachat — это Python-библиотека для подключения модели Gigachat в [autogen](https://github.com/microsoft/autogen)

## Установка

Для установки библиотеки можно использовать менеджер пакетов pip:

```sh
pip install autogen-gigachat
```

## Настройка

В autogen-studio добавить новую модель c 'provider = autogen_gigachat.GigachatChatCompletionClient'

Пример конфигурации:

```json
{
  "provider": "autogen_gigachat.GigachatChatCompletionClient",
  "component_type": "model",
  "version": 1,
  "component_version": 1,
  "description": "Gigachat Lite",
  "label": "Gigachat Lite",
  "config": {
    "model": "GigaChat-2",
    "verify_ssl_certs": false,
    "verbose": true
  }
}
```

Необходимо указать данные для авторизации.

Можно записать в переменную окружения `GIGACHAT_API_KEY` или в параметр `api_key` в json-конфигурации один из вариантов значения:

- `giga-cred-<credentials>:<scope>` — для авторизации credentials + scope
- `giga-user-<user>:<password>` — для авторизации через имя пользователя и пароль
- `giga-auth-<access_token>` — для передачи access_token (который получается одним из первых двух способов)

Также можно использовать переменные, которые поддерживает [библиотека GigaChat](https://github.com/ai-forever/gigachat#%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0-%D0%BF%D0%B5%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%BD%D1%8B%D1%85-%D0%BE%D0%BA%D1%80%D1%83%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F):

- `GIGACHAT_USER` и `GIGACHAT_PASSWORD` — для авторизации с помощью с помощью логина и пароля.
- `GIGACHAT_CREDENTIALS` — для авторизации с помощью ключа авторизации.
- `GIGACHAT_ACCESS_TOKEN` — для авторизации с помощью токен доступа, полученного в обмен на ключ.
- `GIGACHAT_VERIFY_SSL_CERTS` — для того, что бы проверять SSL сертификаты, по умолчанию `False`.

## Разработка

 Для сборки применяется пакетный менеджер `uv`. Установка описана тут: [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/).

  Установка зависимостей:
  
  ```bash
  uv sync
  ```

## Лицензия

Проект распространяется под лицензией MIT.
Подробная информация — в файле [LICENSE](LICENSE).
