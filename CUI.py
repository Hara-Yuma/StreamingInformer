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

ORDERS = {
    'show':     u'現在の設定などを表示する',
    'regist':   u'データの登録を行う',
    'delete':   u'登録されたデータの削除を行う',
    'select':   u'登録されたデータから、BOTに適用する設定を選択する',
    'clear':    u'画面の表示をクリアする',
    'help':     u'ヘルプを表示する',
    'quit':     u'終了する'
}

VALID_ARGS_SHOW = {

}

class CUI(StreamingInformer):
    def __init__(self):
        self.__orders = {
            'show':     self.show,
            'regist':   self.regist,
            'delete':   self.delete,
            'select':   self.select,
            'clear':    self.clear,
            'help':     self.help,
            'quit':     self.quit,
        }

    def __check_args(self, args: list, valid_args: dict) -> bool:
        for i, arg in enumerate(args):
            if valid_args is not None:
                if arg in valid_args.keys():
                    valid_args = valid_args[arg]
            else:
                self.show_message(u'無効な引数: ')
                return False
        return True

    def show(self, args) -> None:
        print('show')

    def regist(self, args) -> None:
        print('regist')

    def delete(self, args) -> None:
        print('delete')

    def select(self, args) -> None:
        print('select')

    def clear(self, args) -> None:
        os.system('cls')

    def help(self, args) -> None:
        print('help')

    def quit(self, args) -> None:
        print('See you...')
        quit()

    def show_message(self, message) -> None:
        print(message)

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
            self.execute(input('> ').split())