<!--
blog-meta-data
title: Python の oletools で日本語の VBA を出力する方法
tags: Python,Excel,備忘録
-->

## VBA はどこにある?

以下の記事がとても参考になる。

[実務であまり役に立たないVBAの内部の話 - Qiita](https://qiita.com/mima_ita/items/ad3adaa9c9db658ecdb7)

マクロの実体は `vbaProject.bin` というバイナリファイルの中にあるらしく、これを解析すると VBA を取得することができる。

このファイルは Compound File Binary Format というファイル形式で仕様は効果されているらしい。  
時間があるときに確認してみたい。

[[MS-CFB]: Compound File Binary File Format](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-cfb/53989ce4-7b05-4f8d-829b-d08d6148375b)

## oletools で VBA を出力する方法
`vbaProject.bin` を自分で解析して VBA を出力するのは大変なので `oletools` というライブラリを使用する。  
このライブラリは `olefile` というパーサを使いやすくしたもの。

ただし、このライブラリで VBA を出力すると以下の記事にもあるように日本語は文字化けをしてしまう。

[ExcelマクロのVBAソースコードをAzure DevOpsでバージョン管理する方法](https://medium.com/@saso_33429/excel%E3%83%9E%E3%82%AF%E3%83%AD%E3%81%AEvba%E3%82%BD%E3%83%BC%E3%82%B9%E3%82%B3%E3%83%BC%E3%83%89%E3%82%92azure-devops%E3%81%A7%E3%83%90%E3%83%BC%E3%82%B8%E3%83%A7%E3%83%B3%E7%AE%A1%E7%90%86%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95-d20b751ddc30)

この記事では `extract_macros` を自作することで対応をしていたが、以下のように `bytes2str` を置き換えることでも日本語することができた。  
記述量も少なく手軽に実行できるので記事にしておく。

```python
import os
import oletools.olevba as vba

# ------------------------------------------------------------------
# 定数
OUT_DIR = "./out"
"""出力するフォルダ"""

# ------------------------------------------------------------------
# 日本語出力用の設定
def _bytes2str(bytes_string: bytes, encoding="utf-8"):
    # ShiftJis でデコードする
    return bytes_string.decode("shift_jis", errors="replace")

# VBA を文字列に変換する関数を置き換える
vba.bytes2str = _bytes2str

# ------------------------------------------------------------------
# 処理
vba_parser = vba.VBA_Parser("./assets/sample.xlsm")

vba_modules = vba_parser.extract_all_macros() if vba_parser.detect_vba_macros() else []

for _, _, filename, contents in vba_modules:
    file = os.path.join(OUT_DIR, filename + ".vb")
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, mode="w", encoding="utf-8") as fp:
        fp.write(vba.filter_vba(contents))
```

サンプルコードは以下に置いておく。

[GitHub - uttne/how-to-output-japanese-vba-with-oletools](https://github.com/uttne/how-to-output-japanese-vba-with-oletools)

## その他の参考

- [oletools - python tools to analyze OLE and MS Office files | Decalage](https://www.decalage.info/python/oletools)
- [GitHub - decalage2/oletools: oletools - python tools to analyze MS OLE2 files (Structured Storage, Compound File Binary Format) and MS Office documents, for malware analysis, forensics and debugging.](https://github.com/decalage2/oletools)
- [olefile](https://pypi.org/project/olefile/)
- [oletools](https://pypi.org/project/oletools/)
- [olefile API Reference — olefile 0.47 documentation](https://olefile.readthedocs.io/en/latest/olefile.html)
