<!--
blog-meta-data
title: 画像や CSS の参照を GitHub Pages に変更
tags: 雑記,python
-->

この記事は以下の記事の GitHub から画像を参照する話の続きになります。

https://first-step-of-3930.blog.uttne.net/2022/03/blog-post_70.html


## GitHub の画像を参照する方法を変更

記事にも書きましたがこのブログでは本文や画像などのデータを全て GitHub で管理する方向で整備を行っています。  
このため、記事から参照する画像などは GitHub から取得する必要があり、そのための URL を Python で作成しています。  
その URL は GitHub の Raw ファイルを参照するものなのですが以下の StackExchange によるとサービスの悪用と見られかねないらしいので GitHub の静的ホスティングサービスである [GitHub Pages](https://docs.github.com/ja/pages) でレポジトリを公開し、画像や css を取得する方法に変えました。

[CSS file from GitHub pages sent as text/plain, needs to be text/css - StackExchange](https://webapps.stackexchange.com/questions/37097/css-file-from-github-pages-sent-as-text-plain-needs-to-be-text-css)

また、 GitHub Raw で css を取得しようとすると MIME タイプが `text/css` ではなく `text/plain` になってしまうので HTML の head に link を書いても読み込まれないという問題が発生したのでこれを解決するためにも GitHub Pages を使用しました。

## やったこと

やったことは単純で以下の2つです。

1. レポジトリを GitHub Pages で公開
2. URL の生成部分で GitHub Pages の URL を生成するように変更

GitHub Pages でレポジトリを公開する方法は多くの方が説明してくれているのでここでは省きます。  
公式ページにも丁寧な解説があるのでそちらをご確認することをお勧めします。  
すでにあるレポジトリを公開する場合はこの [GitHub Pages サイトの公開元を設定する - GitHub Docs](https://docs.github.com/ja/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) から見るのがいいと思います。

URL を生成する部分の変更は `raw.githubusercontent.com` から `uttne.github.io` というドメインに変更したことと、パスに含まれていたコミットハッシュをなくした所が大きな変更点になります。(uttne の部分はそれぞれのアカウント名が入ります)  
コミットハッシュを省くことができるので以下のようなシンプルな URL になりました。

https://uttne.github.io/blog/posts/00003-upload-images-test/test-image.png

同じファイルの元の GitHub Raw の URL は下のような感じです。

https://raw.githubusercontent.com/uttne/blog/3143021a9a16cb5a66b0125fdd6a77e86039cb87/posts/00003-upload-images-test/test-image.png

また、これで GitHub にコミットした css が参照できるようになったので Blogger のコードハイライトで使用する css の link を以下のように head に追加しました。

```html
<head>
    <!-- ～～～～ここに他のコードがたくさん～～～～ -->
    <link href='https://uttne.github.io/blog/css/code-highlight.css' rel='stylesheet'/>
</head>
```

## 注意点

ただ GitHub Raw で参照をしていたときと違って以下のことを気を付ける必要があります。

- 公開するパスは `/`(ルート) にする
- GitHub Pages で公開するブランチに更新をマージする必要がある

ルートにするのは URL の生成が楽だからです。別に `/docs` でも構いませんがそれに合わせて URL の生成部分を修正する必要があります。

今公開しているブランチは main なので他のブランチで画像などをコミットした場合は必ず main にマージする必要があるので注意したいと思います。

## 変更場所

今回の変更は以下の PR になります。

https://github.com/uttne/blog/pull/5

