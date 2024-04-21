# ブログ管理

## ブログのURL

[3930kmのいっぽめ(https://first-step-of-3930.blog.uttne.net/)](https://first-step-of-3930.blog.uttne.net/)

## Secret の保存と暗号化について

client_secret.json をそのまま持たなくてもいいように暗号化を実施する。  

1. .env に暗号化のためのパスフレーズを設定

```ini
# これに暗号化のためのパスフレーズを設定する
BLOGGER_SECRET_ENCRYPT_PASSPHRASE=
```

2. Client Secret を保存する

Google Cloud の API とサービスにある認証情報に登録されているクライアントIDを選択し、クライアントシークレットをダウンロードし `client_secret.json` という名前で保存する。

![](readme_img/2024-04-21-22-46-46.png)

3. 暗号化ファイルを作成する

以下を実行する。

```bash
pipenv run encrypt
```

これを実行することで `client_secret.json.enc` が作成される。


## Usage

```bash
pipenv install --dev
```

```bash
# 新しい記事を作成する
pipenv run new

# 記事をアップロードする
pipenv run up
```

## style

コードハイライトを使用するために Python-Markdown の [Fenced Code Blocks](https://python-markdown.github.io/extensions/fenced_code_blocks/) と [CodeHilite](https://python-markdown.github.io/extensions/code_hilite/index.html) を使用する。

CodeHilite で使用する css は以下の出力することができるので Blogger のテーマを編集してこの css を head に書き込む。

```bash
py -m pygments -S default -f html -a .codehilite > styles.css
```

## API リファレンス

- [Blogs: listByUser &nbsp;|&nbsp; Blogger &nbsp;|&nbsp; Google Developers](https://developers.google.com/blogger/docs/3.0/reference/blogs/listByUser)
