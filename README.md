# 配信通知BOT
## 概要
指定したYouTubeチャンネルにおける以下の情報を一定時間毎に取得して、
指定したDiscordチャンネルに通知するBOTを稼働させる。

- 配信の予約
- 配信の開始
- 動画の投稿 (アーカイブの投稿)

## 使用方法
- GUIモード

    現在準備中

- CUIモード

    以下のコマンドで起動

    `
    $ python main.py -m cui
    `

    起動後は指示に従って操作してください。

## 設定可能な項目
- Google APIキー

- YouTubeチャンネルID

- Discordトークン

- DiscordチャンネルID

- 更新間隔

- BOT稼働時の挨拶文