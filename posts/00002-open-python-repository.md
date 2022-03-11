<!--
blog-meta-data
title: 投稿スクリプトを公開
tags: 雑記,python
-->

## 投稿の自動化

ブログの投稿を自動化するためにスクリプトを作成してみました。

ソースコードは[ここ](https://github.com/uttne/blog)にあります。

投稿は Markdown で書きたかったので調べてみたら StackEdit という便利そうなツールがありましたが、やっぱり使い慣れている VSCode を使いたいと思ったので Python でスクリプトを書きました。

GitHub で記事の内容も管理できるようになったのでバージョン管理もしやすくなったし、もしも Blogger がサービス終了となっても内容が残るのでいい感じではないかと思ってます。

## つまずいた所

### API の使用方法

Blogger の API を使用しなければならないのでまずは開発者ドキュメントとサンプルコードを探しました。この2つは Google で検索すればすぐに見つかったのですが認証をする所でちょっと躓きました。

とりあえず認証をしなければいけないので GCP の APIとサービスで OAuth 2.0 クライアント ID を作成し、 Google API の Python ライブラリレポジトリにあった [oauth-installed.md](https://github.com/googleapis/google-api-python-client/blob/d1a255fcbeaa36f615cede720692fea2b9f894db/docs/oauth-installed.md) というドキュメントを参考に API にアクセスできるか試して見たのですがなぜかアクセスすることができない。

色々調べると以下のコードに問題があったようでした。

```python
credentials = flow.run_console()
```

Credentials を取得するコードなのですがコンソールに表示される URL にアクセスしても `Error 400: invalid_request` と表示されて code が取得できない。どうも `redirect_uri` に `urn:ietf:wg:oauth:2.0:oob` を設定するとダメなようでした。似たような現象で困っている人が stack overflow に[質問](https://stackoverflow.com/questions/71318804/google-oauth-2-0-failing-with-error-400-invalid-request-for-some-client-id-but)を投稿されていたのでそれを参考にしました。

なぜ `urn:ietf:wg:oauth:2.0:oob` はだめなのかまではよくわからなかったですが、とりあえず以下のようなコードで何とか Credentials を取得できるようになったのでとりあえずはよしとします。どなたかなぜこの urn を設定できないかご存知の方がいらっしゃいましたら教えてください。

```python
credentials = flow.run_local_server(host="localhost", port=28080, open_browser=True)
```

port は適当な値です。 0 でも問題ないらしい。今回は自動でブラウザを開いてほしいので `open_browser` を `True` にしています。

Credentials の取得や次回実行時に使いまわすための方法など Gmail の開発者ドキュメントのほうが参考になるので [こっち](https://developers.google.com/gmail/postmaster/quickstart/python) を見たほうが良かったかもしれません。

### Python のフォルダ構成

つまずいた所ではないかもしれませんが一般的な Python のフォルダ構成というものがどういうものか、ちょっと気になっていたのでこの機会に調べてみました。

「Python」「フォルダ」「構成」というキーワードで検索してみると下のような Qiita の記事があったので参考にさせて頂きました。

- [[python] プロジェクトのディレクトリ推奨構成 - Qiita](https://qiita.com/flcn-x/items/c866eec8824a3cd70fa8)

とりあえず今回は特にライブラリにするわけではないので `setup.py` は作らず以下のような構成にしてみました。

```text
blog(root)
├─blog
│  ├─modules
│  │  └─ classなどのモジュールファイル.py
│  └─ __main__.py
└─posts
　  └─ ブログの記事.md
```

`__main__.py` を作ると `py -m blog` のように実行することができるのは知らなかったです。

今まで何度か Python のスクリプトを書いていましたがフォルダ構成は割と適当になっていたので今後しばらくはこのような構成でやっていこうと思います。

今は自分のブログ管理のためだけのスクリプトですが、いずれライブラリ化して配布出来たらいいなぁと思ってます。

## 今後

ブログなので画像をやっぱり使いたい!!のでそのあたりを API でどうすればいいのか調べたいと思います。

あと GitHub Actions を使って PR をマージしたら自動で投稿してくれる CI/CD のような仕組みができたらいいなと思っているので暇を見つけて調べて見ようと思います。多分 Credentials を取得する所の完全自動化が厳しそうですが...

ちょっとブログっぽくなってきたので三日坊主にならないように頑張るぞ٩( 'ω' )و 

## リンク
- [GitHub - uttne/blog](https://github.com/uttne/blog)
- [StackEdit – In-browser Markdown editor](https://stackedit.io/)
- [google-api-python-client/blogger.py at main · googleapis/google-api-python-client](https://github.com/googleapis/google-api-python-client/blob/main/samples/blogger/blogger.py)
- [Google OAuth 2.0 failing with Error 400: invalid_request for some client_id, but works well for others in the same project](https://stackoverflow.com/questions/71318804/google-oauth-2-0-failing-with-error-400-invalid-request-for-some-client-id-but)
- [Introduction &nbsp;|&nbsp; Blogger &nbsp;|&nbsp; Google Developers](https://developers.google.com/blogger)
- [Blogger API v3](https://developers.google.com/resources/api-libraries/documentation/blogger/v3/python/latest/index.html)
- [Python Quickstart &nbsp;|&nbsp; People API &nbsp;|&nbsp; Google Developers](https://developers.google.com/people/quickstart/python)
- [Python Quickstart &nbsp;|&nbsp; Postmaster Tools API &nbsp;|&nbsp; Google Developers](https://developers.google.com/gmail/postmaster/quickstart/python)
- [[python] プロジェクトのディレクトリ推奨構成 - Qiita](https://qiita.com/flcn-x/items/c866eec8824a3cd70fa8)
