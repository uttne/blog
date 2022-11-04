<!--
blog-meta-data
title: Amazon Linux 2 に PostgreSQL をインストールする
tags: PostgreSQL, AWS, EC2, memo
-->

Amazon Linux 2 に PostgreSQL をインストールして外部のクライアントからアクセスするまでを忘れないようにメモとして残しておく。

## 環境
- AMI
    - Amazon Linux 2 Kernel 5.10 AMI 2.0.20221004.0 x86_64 HVM gp2
- インスタンスタイプ
    - t3a.small
- ストレージ
    - 16GB

## EC2内での手順

```bash
sudo amazon-linux-extras install -y postgresql14
```

```bash
sudo yum install -y postgresql-server postgresql-devel
```

| パッケージ        | 説明                                  |
| ----------------- | ------------------------------------- |
| postgresql-server | initdb や pg_ctl などのユーティリティ |
| postgresql-devel  | ヘッダや pg_config などの開発関連     |

```bash
export PGSETUP_INITDB_OPTIONS="--encoding=UTF8 --locale=ja_JP.UTF-8 --lc-collate=ja_JP.UTF-8 --lc-ctype=ja_JP.UTF-8"
```

| オプション   | 説明                                                                                                             |
| ------------ | ---------------------------------------------------------------------------------------------------------------- |
| --encoding   | initdbでPostgreSQLクラスタのデフォルト文字セット(エンコーディング)                                               |
| --locale     | ロケールのサポートはアルファベット、並び換え、数字の書式など文化的嗜好を配慮したアプリケーションを対象にします。 |
| --lc-collate | 文字列の並び換え順                                                                                               |
| --lc-ctype   | 文字の分類（文字とはどんなもの？大文字小文字を区別しない？）                                                     |

```bash
sudo postgresql-setup --initdb
```

```bash
sudo systemctl start postgresql.service    
sudo systemctl enable postgresql.service   
```

以下のコマンドで PostgreSQL が実行されているかを確認できる。
```bash
systemctl status --no-pager postgresql.service
```

インストールが完了すると `postgres` ユーザーが作成される。

```bash
cat /etc/passwd | grep postgres
```


postgres OS ユーザーの権限で postgres DB に接続をする。
```bash
sudo -u postgres psql
```

以下のような SQL を実行して外部からアクセスするためのパスワードを設定する。

```sql
ALTER ROLE postgres PASSWORD 'Passw0rd';
```

以下のコマンドでパスワードが設定されたことを確認できる。
```sql
SELECT * FROM pg_shadow;
```

psql を抜ける。
```sql
exit
```

コンフィグを設定してIPアドレスを受け入れる。
```bash
sudo vim /var/lib/pgsql/data/postgresql.conf
```

```conf
listen_address = '*'
```

アクセス制御設定ファイルを編集する。
```bash
sudo vim /var/lib/pgsql/data/pg_hba.conf
```

```conf
# TYPE  DATABASE        USER            ADDRESS                 METHOD
# IPv4 local connections:
host    all             all             0.0.0.0/0               md5
```

サービスリロードする。

```
sudo systemctl reload postgresql.service
sudo systemctl restart postgresql.service
```

## EC2のセキュリティグループの設定

EC2 のセキュリティグループにポート `5432` を許可するインバウンドルールを追加する。

## 接続確認

クライアントPCで以下のコマンドを実行して接続

```bash
psql --host=$DB_IP --port=5432 --username=postgres --dbname=postgres
```

## 参考
- [EC2上にPostgreSQL14をインストールしてpgAdmin4と接続するまで](https://zenn.dev/uotohotaru/articles/0730f90dbf7a6d)
- [PostgreSQLインストール・設定 （RedHat／CentOS） : showeryのブログ](http://hxn.blog.jp/archives/26166268.html)
- [文字セットサポート](https://www.postgresql.jp/docs/9.2/multibyte.html)
- [ロケールのサポート](https://www.postgresql.jp/docs/9.4/locale.html)
