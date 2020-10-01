import requests
from googleapiclient.discovery import build

class UnexpectedResponseStatusError(Exception):
    '''
    チャンネルへのアクセス時に、予期せぬHTTPレスポンスステータスコードが観測された事を知らせる例外クラス
    '''
    pass

class NetworkUnreachedError(Exception):
    '''
    ネットワークに接続されていないことを知らせる例外クラス
    '''
    pass

class ChannelNotFoundError(Exception):
    '''
    指定されたチャンネルが存在しなかったことを知らせる例外クラス
    '''
    pass

class YouTubeConnector:
    def __init__(self, developer_key: str):
        self.__youtube = build('youtube', 'v3', developerKey=developer_key)

    @classmethod
    def channel_exist(cls, target_channel_id: str) -> bool:
        try:
            status = requests.get('https://www.youtube.com/channel/{channel_id}'.format(channel_id=target_channel_id))
        except:
            raise NetworkUnreachedError(u'ネットワークに接続されていません。')

        if status == 200:
            return True
        elif status == 404:
            return False
        else:
            raise UnexpectedResponseStatusError(u'''https://www.youtube.com/channel/{channel_id}へ正しくアクセス出来ませんでした。
        YouTubeサービスに何らかの異常が発生している可能性があります。''')

    def get_movie_items(self, target_channel_id: str) -> list:
        if YouTubeConnector.channel_exist(target_channel_id):
            return self.__youtube.search().list(
                part='id,snippet',
                channelId=target_channel_id,
                order='date',
                type='video'
            ).execute()["items"]
        else:
            raise ChannelNotFoundError(u'チャンネルID: {channel_id} のようなチャンネルは見つかりませんでした。'.format(channel_id=target_channel_id))