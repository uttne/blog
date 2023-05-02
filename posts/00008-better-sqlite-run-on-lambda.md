<!--
blog-meta-data
title: better-sqlite3 を AWS の Lambda で動かす
tags: aws, lambda, nodejs, sqlite
-->

# 動かない...

AWS の Lambda 上で Sqlite を動かしたいと思ったので試してみたが、素直に動かせなかったので動かせるようになるまでの記録を残しておく。

# 現象

nodejs で Sqlite を動かすために `better-sqlite3` をインストールし、 AWS の Lambda にデプロイして実行すると以下のようなエラーが発生し実行ができなかった。

```text
/lib64/libm.so.6: version `GLIBC_2.29' not found
```

どうも nodejs 18 が動いている Amazon Linux 2 の `/lib64/libm.so.6` に `GLIBC_2.29` が入っていないが、 `better-sqlite3` では 2.29 を使っているため実行エラーになってしまっている様子。

ちなみに Amazon Linux 2 の `/lib64/libm.so.6` の確認は以下のように行った。

```bash
# Amazon Linux 2 のコンテナを起動
> docker run -it --rm --entrypoint "bash" public.ecr.aws/lambda/nodejs:18-x86_64
```

以下をコンテナ内で実行

```bash
> yum install binutils
> strings /lib64/libm.so.6 | grep GLIBC_
GLIBC_2.2.5
GLIBC_2.4
GLIBC_2.15
GLIBC_2.18
GLIBC_2.23
GLIBC_2.24
GLIBC_2.25
GLIBC_2.26
GLIBC_PRIVATE
GLIBC_2.15
...
```

# 解決方法

AWS Lambda の nodejs 18.X ランタイムが動いている Amazon Linux 2 用に `better-sqlite3` をビルドし直した。

# ビルド方法

AWS Lambda nodejs 18.X の実行コンテナイメージは公開されているので、それを使ってビルドした。

今回対象としている `better-sqlite3` のバージョンは 8.3.0。  
Amazon Linux 2 が更新されない限り、これ以降のバージョンを使う場合でも同様にビルドが必要だと思われる。

とりあえず以下のようなシェルを作成する。

build.bash

```bash
#!/bin/bash

# 作業ディレクトリに移動
cd /work

# ビルドに必要なパッケージをインストール
yum install git python3 make gcc gcc-c++ -y

# ビルド結果があったときはクリアしておく
if [ -d ./better-sqlite3 ]; then
    rm -fr ./better-sqlite3
fi

# better-sqlite3 のソースをダウンロードする
git clone https://github.com/WiseLibs/better-sqlite3.git -b v8.3.0 --depth=1

# ソースのフォルダに移動する
cd better-sqlite3

# ビルドコマンドを実行する
npm install

# テストを実行して動くことを確認する
npm test
```

`build.bash` を指定のディレクトリに配置し、以下のコマンドで Docker を使いビルドする。

```bash
# ./better-sqlite3/build.bash のように配置したときのコマンド
docker run -it --rm -v "$(pwd)/better-sqlite3:/work" --entrypoint "/work/build.bash" public.ecr.aws/lambda/nodejs:18-x86_64
```

これを実行すると `./better-sqlite3/better-sqlite3/build/Release/better_sqlite3.node` が生成されるので、これを AWS Lambda の Layer にデプロイして関数から参照して実行すればいい。

# サンプル

-   [GitHub - uttne/node-lambda-sample](https://github.com/uttne/node-lambda-sample)
