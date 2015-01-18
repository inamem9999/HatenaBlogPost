# HatenaBlogPost
はてなブログにエントリーをポストするSublime-text3プラグイン

## インストール

HatenaBlogPostフォルダをSublime-text3のPackagesフォルダ下にコピーしてください。

## 使い方

1. 後述の設定方法に従って設定ファイルを編集する
1. 後述の書き方に従ってブログエントリを書く
1. ``Tools``メニューの``Hatenablogpost``を選択するか、<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>H</kbd>をタイプします。

## 設定方法

HatenaBlogPost/HatenaBlogPostCommand.sublime-settingを編集してください。

* hatena_id
	* はてなIDを記載します
* api_key
	* AtomPubのAPIキーを記載します
* post_url
	* エントリーポスト用のURLを記載します
	* 形式は「{AtomPubのルートエンドポイント}/entry」です
* draft_mode
	* ``yes``で下書きモード、``no``で公開モードで投稿します

## ブログエントリーの書き方

このプラグインでは、先頭行をタイトル、以降を本文として扱って処理します。
タイトルと本文の間に空行を1行開けてください。

### 例

```
ここはタイトル行

ここからが本文

ここも本文
```

### 悪例

```
ここはタイトル行
ここもタイトル行になっちゃう

ここから本文
```