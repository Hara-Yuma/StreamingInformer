from pathlib import Path
from DataManager import *
from DiscordInformer import *
from YouTubeConnector import *

DATA_TEMPLATE = {
    'config_youtube': {
        'api_key': {
            'selected': None,
            'registed': {}
        },
        'channel_id': {
            'selected': None,
            'registed': {}
        }
    },
    'config_discord': {
        'token': {
            'selected': None,
            'registed': {}
        },
        'channel_id': {
            'selected': None,
            'registed': {}
        }
    },
    'config_application': {
        'update_interval': 1200,
        'greeting': {
            'active': False,
            'phrase': ''
        }
    },
    'movie_data': []
}

REGISTABLE_DATA = [
    'config_youtube.api_key',
    'config_youtube.channel_id',
    'config_discord.token',
    'config_discord.channel_id'
]

SETABLE_DATA = [
    'config_application.update_interval',
    'config_application.greeting.active',
    'config_application.greeting.phrase'
]

EXPLAIN_OF_DATA = {
    'config_youtube.api_key':       u'YouTube APIキー',
    'config_youtube.channel_id':    u'YouTubeチャンネルID',
    'config_discord.token':         u'Discordトークン',
    'config_discord.channel_id':    u'DiscordチャンネルID'
}

class StreamingInformer:
    def __init__(self):
        Path('./data').mkdir(exist_ok=True)
        self.__data_manager = DataManager('./data')
        self.__youtube_connector = None

        for dn in ['config_youtube', 'config_discord', 'config_application', 'movie_data']:
            if self.__data_manager.exist(dn):
                self.__data_manager.load_data(dn)
            else:
                self.__data_manager.create_data(dn, DATA_TEMPLATE[dn])

    def get_data(self, data_name: str):
        if data_name not in REGISTABLE_DATA + SETABLE_DATA:
            self.show_message(u'指定されたデータが正しくありません。')
            return None
        else:
            l = data_name.split('.')
            if len(l) == 2:
                return self.__data_manager.get_data(l[0])[l[1]]
            elif len(l) == 3:
                return self.__data_manager.get_data(l[0])[l[1]][l[2]]
            else:
                return None

    def show_message(self, message: str):
        pass

    def select_data(self, data_name: str, data_tag: str) -> bool:
        if data_name not in REGISTABLE_DATA:
            self.show_message(u'指定されたデータ名が正しくありません。')
            return False
        else:
            l = data_name.split('.')
            data = self.__data_manager.get_data(l[0], ref=True)[l[1]]

            if data_tag not in data['registed'].keys():
                self.show_message(u'指定されたデータは存在しません。')
                return False
            else:
                data['selected'] = data_tag
                self.__data_manager.commit(l[0])
                return True

    def regist_data(self, data_name: str, data_tag: str, value: str) -> bool:
        if data_name not in REGISTABLE_DATA:
            self.show_message(u'指定されたデータ名が正しくありません。')
            return False
        else:
            l = data_name.split('.')
            data = self.__data_manager.get_data(l[0], ref=True)[l[1]]

            if data_tag in data['registed'].keys():
                self.show_message(u'タグ名{data_tag}は既に使用されています。'.format(data_tag=data_tag))
                return False
            else:
                if data_name == 'config_discord.channel_id':
                    if not value.isdigit():
                        self.show_message(u'DiscordチャンネルのIDは整数で指定される必要があります。')
                        return False
                    else:
                        value = int(value)
                data['registed'][data_tag] = value

                if data['selected'] is None:
                    data['selected'] = data_tag

                self.__data_manager.commit(l[0])
                return True

    def set_data(self, data_name: str, value: str) -> bool:
        if data_name not in SETABLE_DATA:
            self.show_message(u'指定されたデータ名が正しくありません。')
            return False
        else:
            l = data_name.split('.')

            if len(l) == 2:
                if not value.isdigit():
                    self.show_message(u'更新間隔は整数で指定される必要があります。')
                    return False
                else:
                    self.__data_manager.get_data(l[0], ref=True)[l[1]] = int(value)
                    self.__data_manager.commit(l[0])
                    return True
            else:
                value = value.upper()

                if l[2] == 'active':
                    if value == 'TRUE':
                        value = True
                    elif value == 'FALSE':
                        value = False
                    else:
                        self.show_message(u'挨拶の有効化の指定はTrueかFalseで行う必要があります。')
                        return False

                self.__data_manager.get_data(l[0], ref=True)[l[1]][l[2]] = value
                self.__data_manager.commit(l[0])
                return True

    def delete_data(self, data_name: str, data_tag: str) -> bool:
        if data_name not in REGISTABLE_DATA:
            self.show_message(u'指定されたデータ名が正しくありません。')
            return False
        else:
            l = data_name.split('.')
            data = self.__data_manager.get_data(l[0], ref=True)[l[1]]

            if data_tag not in data['registed'].keys():
                self.show_message(u'指定されたデータは存在していません。')
                return False
            else:
                del data['registed'][data_tag]
                if data['selected'] == data_tag:
                    if len(data['registed']) == 0:
                        data['selected'] = None
                    else:
                        data['selected'] = list(data['registed'].keys())[0]
                self.__data_manager.commit(l[0])
                return True

    def get_movie_data(self) -> dict:
        try:
            movie_items = self.__youtube_connector.get_movie_items(self.get_data('config_youtube.channel_id'))

            movie_data = {}

            for item in movie_items:
                movie_data[item['etag']] = {
                    'title': item['snippet']['title'],
                    'url':  'https://www.youtube.com/v?={}'.format(item['id']['videoId']),
                    'liveBroadcastContent': item['snippet']['liveBroadcastContent']
                }

            return movie_data
        except UnexpectedResponseStatusError:
            self.show_message(u'YouTubeサービスへの接続に失敗しました。')
            return None
        except NetworkUnreachedError:
            self.show_message(u'ネットワークに接続できませんでした。')
            return None
        except ChannelNotFoundError:
            self.show_message(u'指定されたYouTubeチャンネルが見つかりません。')
            return None

    def check_update(self) -> list:

        updated_contents = []

        movie_data = self.__data_manager.get_data('movie_data', ref=True)
        current = self.get_movie_data(self.__data_manager.get_data('movie_data'))

        if current is not None:
            for etag, data in current.items():
                if etag in movie_data:
                    continue
                else:
                    movie_data.append(etag)
                    updated_contents.append(u'''

                    ''')

        return updated_contents

    def start(self, restart=False):
        readied = True
        l = []

        for data_name in REGISTABLE_DATA:
            if self.get_data(data_name)['selected'] is None:
                readied = False
                l.append(data_name)

        if not readied:
            self.show_message(u'未設定のデータ： {}'.format(
                ', '.join([EXPLAIN_OF_DATA[data_name] for data_name in l])
            ))
            return

        self.__youtube_connector = YouTubeConnector(self.get_data('config_youtube.api_key'))

        if not restart:
            movie_data = self.__data_manager.get_data('movie_data', ref=True)
            for data in self.get_movie_data():
                movie_data.append(data)

        try:
            DiscordInformer().activate(
                self.get_data('config_discord.token'),
                self.get_data('config_discord.channel_id'),
                self.check_update,
                self.get_data('config_application.update_interval'),
                greeting_phrase=self.get_data('config_application.greeting.phrase') if self.get_data('config_application.greeting.active') else None
            )
        except DiscordChannelConnectionError:
            self.show_message(u'Discordチャンネルに正しく接続できませんでした。\n設定が正しく行われているか確認して、もう一度実行してください。')
            return
