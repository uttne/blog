<!--
blog-meta-data
title: Windows 11対応のためにサブPCをアップグレードしたらいろいろ大変だった...
tags: 自作PC,Ryzen
-->

## はじめに

今年の秋に Windows 10 のサポートが終了するので、自宅のサブPCを Windows 11 に対応させるために今週の土日は頑張った。  
もともと Window 11 の要件を満たしていなかったので Linux を入れていたが、結局あまり使わなかったので、それならゲームができるようにしたほうがまだ使うだろうと頑張ってアップグレードすることにした。  
最近必要なパーツがちょっと安くなっていたので買い集め、ついでにメインPCの構成も見直してメインもアップグレードしつつサブPCもパーツ流用で Window 11 化を目指したがいろいろと大変だったので教訓として記録を残しておく。  

---

## 当初の計画

メインPCには Ryzen 2700X を使用していたので、以下のような構成変更を計画した。

- サブPC用に新しい **AM4マザーボード** を購入
- **Ryzen 5700X** を新たに購入し、これをメインPCに装着
- 2700X はサブPCに移植して、両方のPCをアップグレード

ソケットも AM4 で揃え問題なく行くだろと考えていたが見積もりが甘かった...

---

## トラブルその1：マザーボードがRyzen 2700X非対応だった

新しく購入したAM4マザーボードは以下で AM4 だから 2700X も問題ないなと思っていたが、2700Xを装着しても BIOS が表示されず...  
いろいろ調べて最終的に製品のページを改めて確認したら「Ryzen 3000番台以降のみ対応」のマザーボードという落ちだった。

<table border="0" cellpadding="0" cellspacing="0"><tr><td><div style="border:1px solid #95a5a6;border-radius:.75rem;background-color:#FFFFFF;width:504px;margin:0px;padding:5px;text-align:center;overflow:hidden;"><table><tr><td style="width:240px"><a href="https://hb.afl.rakuten.co.jp/ichiba/4876edf0.a5ce10dd.4876edf1.fb97a283/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fdospara-r%2Fic513644%2F&link_type=picttext&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJwaWN0dGV4dCIsInNpemUiOiIyNDB4MjQwIiwibmFtIjoxLCJuYW1wIjoicmlnaHQiLCJjb20iOjEsImNvbXAiOiJkb3duIiwicHJpY2UiOjEsImJvciI6MSwiY29sIjoxLCJiYnRuIjoxLCJwcm9kIjowLCJhbXAiOmZhbHNlfQ%3D%3D" target="_blank" rel="nofollow sponsored noopener" style="word-wrap:break-word;"><img src="https://hbb.afl.rakuten.co.jp/hgb/4876edf0.a5ce10dd.4876edf1.fb97a283/?me_id=1407733&item_id=10003361&pc=https%3A%2F%2Fthumbnail.image.rakuten.co.jp%2F%400_gold%2Fdospara-r%2Fimg%2Fitem%2F513644.jpg%3F_ex%3D240x240&s=240x240&t=picttext" border="0" style="margin:2px" alt="[商品価格に関しましては、リンクが作成された時点と現時点で情報が変更されている場合がございます。]" title="[商品価格に関しましては、リンクが作成された時点と現時点で情報が変更されている場合がございます。]"></a></td><td style="vertical-align:top;width:248px;display: block;"><p style="font-size:12px;line-height:1.4em;text-align:left;margin:0px;padding:2px 6px;word-wrap:break-word"><a href="https://hb.afl.rakuten.co.jp/ichiba/4876edf0.a5ce10dd.4876edf1.fb97a283/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fdospara-r%2Fic513644%2F&link_type=picttext&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJwaWN0dGV4dCIsInNpemUiOiIyNDB4MjQwIiwibmFtIjoxLCJuYW1wIjoicmlnaHQiLCJjb20iOjEsImNvbXAiOiJkb3duIiwicHJpY2UiOjEsImJvciI6MSwiY29sIjoxLCJiYnRuIjoxLCJwcm9kIjowLCJhbXAiOmZhbHNlfQ%3D%3D" target="_blank" rel="nofollow sponsored noopener" style="word-wrap:break-word;">ASRock B550M WiFi (B550 AM4 MicroATX) ドスパラ限定モデル</a><br><span >価格：9,880円（税込、送料無料)</span> <span style="color:#BBB">(2025/5/25時点)</span></p><div style="margin:10px;"><a href="https://hb.afl.rakuten.co.jp/ichiba/4876edf0.a5ce10dd.4876edf1.fb97a283/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fdospara-r%2Fic513644%2F&link_type=picttext&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJwaWN0dGV4dCIsInNpemUiOiIyNDB4MjQwIiwibmFtIjoxLCJuYW1wIjoicmlnaHQiLCJjb20iOjEsImNvbXAiOiJkb3duIiwicHJpY2UiOjEsImJvciI6MSwiY29sIjoxLCJiYnRuIjoxLCJwcm9kIjowLCJhbXAiOmZhbHNlfQ%3D%3D" target="_blank" rel="nofollow sponsored noopener" style="word-wrap:break-word;"><img src="https://static.affiliate.rakuten.co.jp/makelink/rl.svg" style="float:left;max-height:27px;width:auto;margin-top:0" ></a><a href="https://hb.afl.rakuten.co.jp/ichiba/4876edf0.a5ce10dd.4876edf1.fb97a283/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fdospara-r%2Fic513644%2F%3Fscid%3Daf_pc_bbtn&link_type=picttext&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJwaWN0dGV4dCIsInNpemUiOiIyNDB4MjQwIiwibmFtIjoxLCJuYW1wIjoicmlnaHQiLCJjb20iOjEsImNvbXAiOiJkb3duIiwicHJpY2UiOjEsImJvciI6MSwiY29sIjoxLCJiYnRuIjoxLCJwcm9kIjowLCJhbXAiOmZhbHNlfQ==" target="_blank" rel="nofollow sponsored noopener" style="word-wrap:break-word;"><div style="float:right;width:41%;height:27px;background-color:#bf0000;color:#fff!important;font-size:12px;font-weight:500;line-height:27px;margin-left:1px;padding: 0 12px;border-radius:16px;cursor:pointer;text-align:center;"> 楽天で購入 </div></a></div></td></tr></table></div><br><p style="color:#000000;font-size:12px;line-height:1.4em;margin:5px;word-wrap:break-word"></p></td></tr></table>

### 解決策

泣く泣く予定を変更し、Ryzen 5700X をサブPCに使うことにしメインPCの性能アップはお見送りした ( ´･ω･`)

### 教訓

- **同じソケットでも世代が違えば動かない！**
- 購入前に **対応CPUリスト** を必ず確認するべし

---

## トラブルその2：CPUクーラーが外れない

Ryzen 2700X のリテールクーラーを外そうとしたところ、まったく外れない。  
確かリテールクーラーに付属していたグリスをそのまま使っており、それの品質があまりよくなかったのかカチカチに固まって接着剤のようになっていた。

### 解決策

- CPU に負荷をかけてとにかく温めた
- クーラーをぐりぐりと結構強めにねじりながら30分ぐらい格闘して、ようやく外した

### 教訓

- リテールクーラーのグリスは信用しない。
- 評判のグリスを使用するべし！
- 今回は **ARCTIC MX-4** を新たに購入して塗りました。(多分下のものが一番安いはず。QRコードで確認しても本物だったので正規品...のはず...)

<table border="0" cellpadding="0" cellspacing="0"><tr><td><div style="border:1px solid #95a5a6;border-radius:.75rem;background-color:#FFFFFF;width:504px;margin:0px;padding:5px;text-align:center;overflow:hidden;"><table><tr><td style="width:240px"><a href="https://hb.afl.rakuten.co.jp/ichiba/4876b411.fa3b5c2a.4876b412.26b9620d/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Ffivestarshop%2Farctic-mx4-spatula%2F&link_type=picttext&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJwaWN0dGV4dCIsInNpemUiOiIyNDB4MjQwIiwibmFtIjoxLCJuYW1wIjoicmlnaHQiLCJjb20iOjEsImNvbXAiOiJkb3duIiwicHJpY2UiOjEsImJvciI6MSwiY29sIjoxLCJiYnRuIjoxLCJwcm9kIjowLCJhbXAiOmZhbHNlfQ%3D%3D" target="_blank" rel="nofollow sponsored noopener" style="word-wrap:break-word;"><img src="https://hbb.afl.rakuten.co.jp/hgb/4876b411.fa3b5c2a.4876b412.26b9620d/?me_id=1419149&item_id=10000267&pc=https%3A%2F%2Fthumbnail.image.rakuten.co.jp%2F%400_mall%2Ffivestarshop%2Fcabinet%2Fcompass1679143145.jpg%3F_ex%3D240x240&s=240x240&t=picttext" border="0" style="margin:2px" alt="[商品価格に関しましては、リンクが作成された時点と現時点で情報が変更されている場合がございます。]" title="[商品価格に関しましては、リンクが作成された時点と現時点で情報が変更されている場合がございます。]"></a></td><td style="vertical-align:top;width:248px;display: block;"><p style="font-size:12px;line-height:1.4em;text-align:left;margin:0px;padding:2px 6px;word-wrap:break-word"><a href="https://hb.afl.rakuten.co.jp/ichiba/4876b411.fa3b5c2a.4876b412.26b9620d/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Ffivestarshop%2Farctic-mx4-spatula%2F&link_type=picttext&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJwaWN0dGV4dCIsInNpemUiOiIyNDB4MjQwIiwibmFtIjoxLCJuYW1wIjoicmlnaHQiLCJjb20iOjEsImNvbXAiOiJkb3duIiwicHJpY2UiOjEsImJvciI6MSwiY29sIjoxLCJiYnRuIjoxLCJwcm9kIjowLCJhbXAiOmZhbHNlfQ%3D%3D" target="_blank" rel="nofollow sponsored noopener" style="word-wrap:break-word;">ARCTIC MX-4 4g ヘラ スパチュラ付き アークティック MX4 グリス グリース 熱伝導グリス 低熱抵抗 低粘性 長期不硬化 非導電性 サーマルコンパウンド ペースト シリコングリス カーボンベース ヒートシンクペースト CPU 冷却グリス 冷却 冷却グリース</a><br><span >価格：980円（税込、送料無料)</span> <span style="color:#BBB">(2025/5/25時点)</span></p><div style="margin:10px;"><a href="https://hb.afl.rakuten.co.jp/ichiba/4876b411.fa3b5c2a.4876b412.26b9620d/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Ffivestarshop%2Farctic-mx4-spatula%2F&link_type=picttext&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJwaWN0dGV4dCIsInNpemUiOiIyNDB4MjQwIiwibmFtIjoxLCJuYW1wIjoicmlnaHQiLCJjb20iOjEsImNvbXAiOiJkb3duIiwicHJpY2UiOjEsImJvciI6MSwiY29sIjoxLCJiYnRuIjoxLCJwcm9kIjowLCJhbXAiOmZhbHNlfQ%3D%3D" target="_blank" rel="nofollow sponsored noopener" style="word-wrap:break-word;"><img src="https://static.affiliate.rakuten.co.jp/makelink/rl.svg" style="float:left;max-height:27px;width:auto;margin-top:0" ></a><a href="https://hb.afl.rakuten.co.jp/ichiba/4876b411.fa3b5c2a.4876b412.26b9620d/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Ffivestarshop%2Farctic-mx4-spatula%2F%3Fscid%3Daf_pc_bbtn&link_type=picttext&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJwaWN0dGV4dCIsInNpemUiOiIyNDB4MjQwIiwibmFtIjoxLCJuYW1wIjoicmlnaHQiLCJjb20iOjEsImNvbXAiOiJkb3duIiwicHJpY2UiOjEsImJvciI6MSwiY29sIjoxLCJiYnRuIjoxLCJwcm9kIjowLCJhbXAiOmZhbHNlfQ==" target="_blank" rel="nofollow sponsored noopener" style="word-wrap:break-word;"><div style="float:right;width:41%;height:27px;background-color:#bf0000;color:#fff!important;font-size:12px;font-weight:500;line-height:27px;margin-left:1px;padding: 0 12px;border-radius:16px;cursor:pointer;text-align:center;"> 楽天で購入 </div></a></div></td></tr></table></div><br><p style="color:#000000;font-size:12px;line-height:1.4em;margin:5px;word-wrap:break-word"></p></td></tr></table>

---

## トラブルその3：BIOSが映らず焦る

当初の予定ではメインPCに Ryzen 5700X 装着する予定だったのでそちらの作業を先に行っていたが、CPUを取り付けたあと電源を入れても画面がつかず BIOS にも入れなくなってしまった。  
BIOSすら表示されず、「これは壊してしまったか...」と肝が冷えました。  

### 原因は2つ

1. **マザーボードのBIOSが古く、Ryzen 5000番台に対応していなかった**
2. **Ryzen 5700X はグラフィック機能非搭載。GPUを挿さないと映像が出ない**

### 解決策

- 古いマザーボードであったため、公式サイトを確認し対応するファームウェアをダウンロードしアップデートを行ったことできちんと起動をした
- GPU を取り付け HDMI を GPU に接続して画面に出力をした

### 教訓

- **Ryzen はソケットが同じでもマザーボードによって対応が異なる**。BIOSの対応状況を必ず確認！
- **iGPU（内蔵GPU）なしCPU** には要注意。グラフィック機能がない場合はマザーボードの HDMI に接続しても意味がないので GPU はめんどくさがらずにきちんとつけること！

---

## 最終的な構成と結果

結果的には当初の計画とは変わり以下の構成となった。

- **サブPC**
    - Ryzen 5700X
    - 新 AM4 マザーボード
- **メインPC**
    - Ryzen 2700X 継続使用

予定していた構成にはならなかったが何とか起動ができてよかったです。

---

## おわりに

「パーツの流用でメインもサブもお得にアップグレード！」と思ったら、予定外の出費や手間がかかってしまった。  
やはり事前の調査は大事なので次の更新ではちゃんとメーカーページの確認をします。

次は AM6 がでてからかなぁ

---
