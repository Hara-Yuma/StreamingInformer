import discord
from discord.ext import tasks
from typing import Callable

class DiscordChannelConnectionError(Exception):
    '''
    正常にチャンネル接続出来なかったことを知らせる例外クラス
    '''
    pass

class DiscordInformer:
    def activate(self, token: str, target_channel_id: int, callback: Callable[[], list], interval: int, greeting_phrase: str=None) -> None:
        self.__client = discord.Client()
        self.__readied = False

        async def wait_for_ready() -> None:
            while not self.__readied:
                pass
            return

        @self.__client.event
        async def on_ready() -> None:
            self.__target_channel = self.__client.get_channel(target_channel_id)

            if self.__target_channel is None:
                raise DiscordChannelConnectionError(u'正常にチャンネル接続出来ませんでした')

            if greeting_phrase is not None:
                await self.__target_channel.send(greeting_phrase)
            print(u'Discord Informer: チャンネルに接続しました')
            self.__readied = True

        @tasks.loop(seconds=interval)
        async def loop() -> None:
            await wait_for_ready()

            items = callback()

            if len(items) == 0:
                print(u'更新はありませんでした')

            for item in callback():
                await self.__target_channel.send(item)
                print(u'【　送信済みアイテム　】')
                print(item)
                print('--------------------------------------------------')
                print(u'送信先: {channel}'.format(channel=self.__target_channel))
                print('')

        loop.start()
        self.__client.run(token)
