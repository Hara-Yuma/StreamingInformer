import os
from StreamingInformer import StreamingInformer

GREETING_PHRASE = u'''
=============================
Streaming Informer (CUI MODE)
=============================

Hello!
各設定やBOTの起動を行うには、コマンドを入力して下さい。
詳しい使い方を見るには、helpと入力してください。
'''

HELP_GENERALLY = u'''
各コマンドの詳細は、-h もしくは --help オプションを使用することで見ることができます。
'''

SETTINGS = u'''
{selected}

登録済みのデータ:
\tYouTube:
\t\tAPIキー:
{youtube_api_keys}

\t\tチャンネルID:
{youtube_channel_ids}

\tDiscord:
\t\tトークン:
{discord_tokens}

\t\tチャンネルID:
{discord_channel_ids}
'''

SELECTED = u'''
現在適用されているデータ:
\tYouTube:
\t\tAPIキー:        {youtube_api_key}
\t\tチャンネルID:   {youtube_channel_id}

\tDiscord:
\t\tトークン:       {discord_token}
\t\tチャンネルID:   {discord_channel_id}

\tApplication:
\t\t更新間隔:       {update_interval}(秒)
\t\t挨拶文:
\t\t\t{greeting_active}
\t\t\t{greeting_phrase}
'''

ORDERS = {
    'show':     u'現在の設定などを表示する',
    'regist':   u'データの登録を行う',
    'set':      u'値の変更を行う',
    'delete':   u'登録されたデータの削除を行う',
    'select':   u'登録されたデータから、BOTに適用する設定を選択する',
    'start':    u'設定した内容でBOTを起動させる',
    'clear':    u'画面の表示をクリアする',
    'help':     u'ヘルプを表示する',
    'quit':     u'終了する'
}

VALID_ARGS_SHOW = {
    '-h': None,
    '--help': None,
    'settings': None,
    'selected': None,
    'youtube_api_key': None,
    'youtube_channel_id': None,
    'discord_token': None,
    'discord_channel_id': None,
    'update_interval': None,
    'greeting_active': None,
    'greeting_phrase': None
}

VALID_ARGS_REGIST = {
    '-h': None,
    '--help': None,
    'youtube_api_key': {'*': {'*': None}},
    'youtube_channel_id': {'*': {'*': None}},
    'discord_token': {'*': {'*': None}},
    'discord_channel_id': {'*': {'*': None}}
}

VALID_ARGS_SET = {
    '-h': None,
    '--help': None,
    'update_interval': {'*': None},
    'greeting_active': {'*': None},
    'greeting_phrase': {'*': None}
}

VALID_ARGS_DELETE = {
    '-h': None,
    '--help': None,
    'youtube_api_key': {'*': None},
    'youtube_channel_id': {'*': None},
    'discord_token': {'*': None},
    'discord_channel_id': {'*': None}
}

VALID_ARGS_SELECT = {
    '-h': None,
    '--help': None,
    'youtube_api_key': {'*': None},
    'youtube_channel_id': {'*': None},
    'discord_token': {'*': None},
    'discord_channel_id': {'*': None}
}

VALID_ARGS_START = {
    '-h': None,
    '--help': None,
    '--restart': None,
    'NO_ARG': None
}

VALID_ARGS_CLEAR = {
    '-h': None,
    '--help': None,
    'NO_ARG': None
}

VALID_ARGS_HELP = {
    '-h': None,
    '--help': None,
    'NO_ARG': None
}

VALID_ARGS_QUIT = {
    '-h': None,
    '--help': None,
    'NO_ARG': None
}

DATA_NAMES = {
    'youtube_api_key': 'config_youtube.api_key',
    'youtube_channel_id': 'config_youtube.channel_id',
    'discord_token': 'config_discord.token',
    'discord_channel_id': 'config_discord.channel_id',
    'update_interval': 'config_application.update_interval',
    'greeting_active': 'config_application.greeting.active',
    'greeting_phrase': 'config_application.greeting.phrase'
}

class CUI(StreamingInformer):
    def __init__(self):
        super().__init__()

        self.__orders = {
            'show':     self.show,
            'regist':   self.regist,
            'set':      self.set,
            'delete':   self.delete,
            'select':   self.select,
            'start':    self.start,
            'clear':    self.clear,
            'help':     self.help,
            'quit':     self.quit,
        }

    def __check_args(self, args: list, valid_args: dict) -> bool:
        for i, arg in enumerate(args):
            if valid_args is not None:
                if arg in valid_args.keys():
                    valid_args = valid_args[arg]
                elif '*' in valid_args.keys():
                    valid_args = valid_args['*']
                else:
                    self.show_message(u'無効な引数: {}'.format(', '.join([a for a in args[i:]])))
                    return False
            else:
                self.show_message(u'無効な引数: {}'.format(', '.join([a for a in args[i:]])))
                return False
        if valid_args is None:
            return True
        elif len(args) == 0 and 'NO_ARG' in valid_args.keys():
            return True
        else:
            return False

    def __exclude_none(self, v, sub):
        return v if v is not None else sub

    def show(self, args) -> None:
        if not self.__check_args(args, VALID_ARGS_SHOW):
            return

        if args[0] == 'settings':
            print(
                SETTINGS.format(
                    selected=SELECTED.format(
                        youtube_api_key=self.__exclude_none(super().get_data('config_youtube.api_key')['selected'], '---'),
                        youtube_channel_id=self.__exclude_none(super().get_data('config_youtube.channel_id')['selected'], '---'),
                        discord_token=self.__exclude_none(super().get_data('config_discord.token')['selected'], '---'),
                        discord_channel_id=self.__exclude_none(super().get_data('config_discord.channel_id')['selected'], '---'),
                        update_interval=super().get_data('config_application.update_interval'),
                        greeting_active=u'有効' if super().get_data('config_application.greeting.active') else u'無効',
                        greeting_phrase=super().get_data('config_application.greeting.phrase')
                    ),
                    youtube_api_keys='\n'.join(['\t\t\t{tag} ({value})'.format(tag=k, value=v) for k, v in super().get_data('config_youtube.api_key')['registed'].items()]),
                    youtube_channel_ids='\n'.join(['\t\t\t{tag} ({value})'.format(tag=k, value=v) for k, v in super().get_data('config_youtube.channel_id')['registed'].items()]),
                    discord_tokens='\n'.join(['\t\t\t{tag} ({value})'.format(tag=k, value=v) for k, v in super().get_data('config_discord.token')['registed'].items()]),
                    discord_channel_ids='\n'.join(['\t\t\t{tag} ({value})'.format(tag=k, value=v) for k, v in super().get_data('config_discord.channel_id')['registed'].items()])
                )
            )
        elif args[0] == 'selected':
            print(
                SELECTED.format(
                    youtube_api_key=self.__exclude_none(super().get_data('config_youtube.api_key')['selected'], '---'),
                    youtube_channel_id=self.__exclude_none(super().get_data('config_youtube.channel_id')['selected'], '---'),
                    discord_token=self.__exclude_none(super().get_data('config_discord.token')['selected'], '---'),
                    discord_channel_id=self.__exclude_none(super().get_data('config_discord.channel_id')['selected'], '---'),
                    update_interval=super().get_data('config_application.update_interval'),
                    greeting_active=u'有効' if super().get_data('config_application.greeting.active') else u'無効',
                    greeting_phrase=super().get_data('config_application.greeting.phrase')
                )
            )
        else:
            data = super().get_data(DATA_NAMES[args[0]])
            print(u'''
適用されている設定: {} ({})

登録されている設定:
{}
            '''.format(
                self.__exclude_none(data['selected'], '---'),
                data['registed'][data['selected']] if data['selected'] is not None else '---',
                '\n'.join(['\t{tag} ({value})'.format(tag=k, value=v) for k, v in data['registed'].items()])
            ))

    def regist(self, args) -> None:
        if not self.__check_args(args, VALID_ARGS_REGIST):
            return

        super().regist_data(DATA_NAMES[args[0]], args[1], args[2])

    def set(self, args) -> None:
        if not self.__check_args(args, VALID_ARGS_SET):
            return

        super().set_data(DATA_NAMES[args[0]], args[1])

    def delete(self, args) -> None:
        if not self.__check_args(args, VALID_ARGS_DELETE):
            return

        super().delete_data(DATA_NAMES[args[0]], args[1])

    def select(self, args) -> None:
        if not self.__check_args(args, VALID_ARGS_SELECT):
            return

        super().select_data(DATA_NAMES[args[0]], args[1])

    def start(self, args) -> None:
        if not self.__check_args(args, VALID_ARGS_START):
            return

        super().start(restart=(len(args) == 1 and args[0] == '--restart'))

    def clear(self, args) -> None:
        if not self.__check_args(args, VALID_ARGS_CLEAR):
            return

        os.system('clear')

    def help(self, args) -> None:
        if not self.__check_args(args, VALID_ARGS_HELP):
            return

        print(u'''
コマンド一覧:
{}
'''.format('\n\n'.join(['{command}\t\t{explain}'.format(command=k, explain=v) for k, v in ORDERS.items()])))
        print(HELP_GENERALLY)

    def quit(self, args) -> None:
        if not self.__check_args(args, VALID_ARGS_QUIT):
            return

        print('See you...')
        quit()

    def show_message(self, message) -> None:
        print(message)
        print(HELP_GENERALLY)

    def execute(self, args) -> None:
        argc = len(args)

        if argc == 0:
            return
        elif args[0] not in ORDERS.keys():
            return
        else:
            self.__orders[args[0]](args[1:])

    def run(self):
        print(GREETING_PHRASE)

        while True:
            self.execute(input(' > ').split())
