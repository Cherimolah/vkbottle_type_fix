# VKBottle Type Fix
Так как разработчики замечательного фреймворка обновляют типы только тогда, когда они появляются в официальном репозитории ВК 
https://github.com/VKCOM/vk-api-schema, а они в свою очередь не ососбо торопятся публиковать обновления, 
создан этот репозиторий

**Отправляйте какие ещё типы не работают в vkbottle**


# Использование
Скачиваем файл `type_fix.py` к себе в проект

Пример использования (больше примеров в `test.py`)

```python
from vkbottle.bot import Bot, Message
from vkbottle.framework.labeler.bot import BotLabeler
from vkbottle.dispatch.rules.base import AttachmentTypeRule

from type_fix import BotMessageViewExtended


bot = Bot('group_token',
          labeler=BotLabeler(message_view=BotMessageViewExtended()))


@bot.on.message(AttachmentTypeRule('narrative'))
async def poll_message(m: Message):
    # Access: m.attachments[0].narrative
    await m.answer('Классный сюжет!')


if __name__ == '__main__':
    bot.run_forever()

```

# Исправленные/добавленные типы

 - Опросы
 - Сюжеты
 - Кружочки (вк откатили тип, вместо него обычный video)
