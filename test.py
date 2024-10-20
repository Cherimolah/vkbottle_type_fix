from vkbottle.bot import Bot, Message
from vkbottle.framework.labeler.bot import BotLabeler
from vkbottle.dispatch.rules.base import AttachmentTypeRule

from type_fix import BotMessageViewExtended


bot = Bot('group_token',
          labeler=BotLabeler(message_view=BotMessageViewExtended()))


@bot.on.message(AttachmentTypeRule('poll'))
async def poll_message(m: Message):
    await m.answer('Опрос интересный!')


if __name__ == '__main__':
    bot.run_forever()
