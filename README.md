# ブログ管理

## Usage

```bash
pipenv install --dev
```

```bash
py -m blog
```

## style

コードハイライトを使用するために Python-Markdown の [Fenced Code Blocks](https://python-markdown.github.io/extensions/fenced_code_blocks/) と [CodeHilite](https://python-markdown.github.io/extensions/code_hilite/index.html) を使用する。

CodeHilite で使用する css は以下の出力することができるので Blogger のテーマを編集してこの css を head に書き込む。

```bash
py -m pygments -S default -f html -a .codehilite > styles.css
```

## API リファレンス

- [Blogs: listByUser &nbsp;|&nbsp; Blogger &nbsp;|&nbsp; Google Developers](https://developers.google.com/blogger/docs/3.0/reference/blogs/listByUser)
