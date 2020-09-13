from DataManager import DataManager
from DiscordInformer import DiscordInformer
from YouTubeConnector import YouTubeConnector

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

class StreamingInformer:
    def __init__(self):
        self.__data_manager = DataManager('./data')

        for dn in ['config_youtube', 'config_discord', 'config_application', 'movie_data']:
            if self.__data_manager.exist(dn):
                self.__data_manager.load_data(dn)
            else:
                self.__data_manager.create_data(dn, DATA_TEMPLATE[dn])

    def get_data(self, data_name: str):
        return self.__data_manager.get_data(data_name)

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
                    self.__data_manager.get_data(l[0])[l[1]] = int(value)
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
                        data['selected'] = data['registed'].keys()[0]
                self.__data_manager.commit(l[0])
                return True

    def start(self):
        pass
