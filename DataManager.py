import copy
import pickle
from pathlib import Path

class PathNotFoundError(Exception):
    '''
    指定されたファイルパスが存在しなかったことを知らせる例外クラス
    '''
    pass

class DataNotFoundError(Exception):
    '''
    指定されたデータがロードされていないことを知らせる例外クラス
    '''
    pass

class DataManager:
    def __init__(self, data_path: str):
        self.__data_path = Path(data_path)

        if not self.__data_path.exists():
            raise PathNotFoundError(u'指定されたパス {data_path} は存在しません。'.format(data_path=str(self.__data_path.resolve())))

        self.__data = {}

    def exist(self, data_name: str, loaded=False):
        if loaded:
            return data_name in self.__data.keys()
        else:
            return (self.__data_path / Path(data_name + '.pickle')).exists()

    def create_data(self, data_name: str, data=None) -> bool:
        file_path = self.__data_path / Path(data_name + '.pickle')

        if '/' in data_name or file_path.exists():
            return False
        else:
            file_path.touch()
            with file_path.open(mode='wb') as f:
                pickle.dump(data, f)
            self.__data[data_name] = data
            return True

    def load_data(self, data_name: str) -> bool:
        file_path = self.__data_path / Path(data_name + '.pickle')

        if not file_path.exists():
            return False
        else:
            with file_path.open(mode='rb') as f:
                self.__data[data_name] = pickle.load(f)
            return True

    def get_data(self, data_name: str, ref=False):
        if data_name not in self.__data.keys():
            raise DataNotFoundError(u'指定されたデータ{data_name}はロードされていません。'.format(data_name=data_name))
        else:
            return self.__data[data_name] if ref else copy.deepcopy(self.__data[data_name])

    def set_data(self, data_name: str, data) -> None:
        if data_name not in self.__data.keys():
            raise DataNotFoundError(u'指定されたデータ{data_name}はロードされていません。'.format(data_name=data_name))
        else:
            with (self.__data_path / Path(data_name + '.pickle')).open(mode='wb') as f:
                pickle.dump(data, f)

    def commit(self, data_name: str) -> None:
        file_path = self.__data_path / Path(data_name + '.pickle')

        if not file_path.exists():
            raise PathNotFoundError(u'指定されたファイルへのパス {data_path} は存在しません。'.format(data_path=str(file_path.resolve())))
        elif data_name not in self.__data.keys():
            raise DataNotFoundError(u'指定されたデータ{data_name}はロードされていません。'.format(data_name=data_name))
        else:
            with file_path.open(mode='wb') as f:
                pickle.dump(self.__data[data_name], f)
