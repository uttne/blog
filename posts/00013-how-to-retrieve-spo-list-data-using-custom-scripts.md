<!--
blog-meta-data
title: SharePoint Online のリストデータをカスタムスクリプトで取得する方法について
tags: SharePoint,備忘録
-->

## データの準備

以下のコードを実行して CSV を生成して実験用のリストを用意する。

```python
import datetime as dt
import pandas as pd
import random as rd
from faker import Faker

title = []
data1 = []
data2 = []
data3 = []
data4 = []
data5 = []

choices_int_data = [i for i in range(100)]
choices_text_data = ["aaaa" + str(i).zfill(4) for i in range(100)]

start_datetime = dt.datetime(
    2024, 1, 1, 0, 0, 0, tzinfo=dt.timezone(offset=dt.timedelta(hours=9))
)

fake = Faker(["en_US", "ja_JP"])

for i in range(100000):
    title.append(i)
    data1.append(rd.choices(choices_int_data)[0])
    data2.append(rd.choices(choices_text_data)[0])
    data3.append((start_datetime + dt.timedelta(seconds=i)).isoformat())

    data5.append(fake.name())


data_1 = [1 for _ in range(1)]
data_10 = [10 for _ in range(10)]
data_100 = [100 for _ in range(100)]
data_1000 = [1000 for _ in range(1000)]
data_4999 = [4999 for _ in range(4999)]
data_5000 = [5000 for _ in range(5000)]
data_5001 = [5001 for _ in range(5001)]
data_10000 = [10000 for _ in range(10000)]
data_numbers = (
    data_1
    + data_10
    + data_100
    + data_1000
    + data_4999
    + data_5000
    + data_5001
    + data_10000
)
data_other = [-1 for _ in range(100000 - len(data_numbers))]

data4 = rd.sample(data_numbers + data_other, len(data_numbers + data_other))

df = pd.DataFrame(
    data={
        "title": title,
        "data1": data1,
        "data2": data2,
        "data3": data3,
        "data4": data4,
        "data5": data5,
    }
)

df.to_csv("test_data_v2.csv", index=None)

```

## SharePoint Online のカスタムスクリプトでリストのデータを取得するための認証

OAuth を使用しない場合、API をコールするときに `X-RequestDigest` ヘッダーを指定する必要があるので以下のようなコードで取得する。

[SharePoint REST エンドポイントを使用して基本的な操作を完了する](https://learn.microsoft.com/ja-jp/sharepoint/dev/sp-add-ins/complete-basic-operations-using-sharepoint-rest-endpoints#writing-data-by-using-the-rest-interface)

```javascript
async function getFdvAsync(siteUrl) {
    const url = `https://${siteUrl}/_api/contextinfo`;
    const res = await fetch(url, {
        method: "POST",
        headers: {
        Accept: "application/json;odata=nometadata",
        },
    });

    if (!res.ok) {
        throw new Error("存在しないサイトです");
    }
    const contextinfo = await res.json();
    let fdv = contextinfo.FormDigestValue;
    return fdv;
}
```

API をリクエストするヘッダーは以下のようなものを共通で用意しておく。

```javascript
let yoursiteurl = "${your-tenant}.sharepoint.com/sites/${your-site-name}"

let fdv =  await getFdvAsync(yoursiteurl);
let headers = { 
    Accept: "application/json;odata=nometadata", 
    "Content-Type": "application/json;odata=verbose", 
    "X-RequestDigest": fdv
}
```

`Accept` で `application/json;odata=nometadata` を指定するのは `Items` でデータを取得するときにメタデータを取得しないようにするため。 `verbose` を指定すると詳細なメタデータを取得することができる。

## Items で取得する場合

[REST を使用してリストとリスト アイテムを操作する](https://learn.microsoft.com/ja-jp/sharepoint/dev/sp-add-ins/working-with-lists-and-list-items-with-rest#retrieve-all-list-items)

シンプルには以下のように指定することで取得ができる。  
この場合、デフォルトでは 100 件のデータが取得できる。

```javascript
let url = `https://${yoursiteurl}/_api/web/lists/GetByTitle('test_data_v2')/Items`;

let res = await fetch(url, {
    method: "GET",
    headers: headers,
    }
).then(r=>r.json());
console.log(res);
```

この時、取得されたデータに `res['odata.nextLink']` があり、そのリンクを使用することで次のページのデータを取得することができる。  
(`odata.nextLink` は `nometadata` を指定したとき取得できるプロパティで `verbose` を指定した場合は `res.d.__next` で取得できる)

`$filter` を指定することでフィルタリングが可能。
```javascript
let url = `https://${yoursiteurl}/_api/web/lists/GetByTitle('test_data_v2')/Items?$filter=field_4 eq 10`;

let res = await fetch(url, {
    method: "GET",
    headers: headers,
    }
).then(r=>r.json());
console.log(res);
```

`$filter` で検索条件に引っかかるアイテムが5000件以下であれば200の応答でデータを取得することができる。
```javascript
let url = `https://${yoursiteurl}/_api/web/lists/GetByTitle('test_data_v2')/Items?$filter=field_4 eq 5000`;

let res = await fetch(url, {
    method: "GET",
    headers: headers,
    }
).then(r=>r.json());
console.log(res);
```

`$filter` で検索条件に引っかかるアイテムが5001件以上の場合5000件問題に抵触しエラーが返る。
```javascript
let url = `https://${yoursiteurl}/_api/web/lists/GetByTitle('test_data_v2')/Items?$filter=field_4 eq 5001`;

let res = await fetch(url, {
    method: "GET",
    headers: headers,
    }
).then(r=>r.json());
console.log(res);
```

```json
{
    "code": "-2147024860, Microsoft.SharePoint.SPQueryThrottledException",
    "message": {
        "lang": "ja-JP",
        "value": "この操作は、リストビューのしきい値を超えているため、実行できません。"
    }
}
```

## RenderListDataAsStream でデータを取得する場合

[REST を使用してリストとリスト アイテムを操作する](https://learn.microsoft.com/ja-jp/sharepoint/dev/sp-add-ins/working-with-lists-and-list-items-with-rest#retrieve-items-as-a-stream)

シンプルな指定では以下のようなリクエストでデータを取得することができる。  
デフォルトでは 30 件のデータを取得することができる。  
次の値を取得する場合は `Paged=TRUE` を指定して得られる `NextHref` を使って次のリクエストを送信する。

```javascript
let url = `https://${yoursiteurl}/_api/web/lists/GetByTitle('test_data_v2')/RenderListDataAsStream`;

let res = await fetch(url, {
    method: "POST",
    headers: headers,
    body: JSON.stringify({
        parameters:{
            "__metadata":{
                "type":"SP.RenderListDataParameters"
                },
            RenderOptions: 0
        }
    })
}).then(r=>r.json());
console.log(res);
```

フィルタリングなどをする場合は URL Parameter で指定する場合と、 ViewXml で指定する方法の 2つがある。

### URL Parameter で指定

[REST を使用してリストとリスト アイテムを操作する](https://learn.microsoft.com/ja-jp/sharepoint/dev/sp-add-ins/working-with-lists-and-list-items-with-rest#renderlistdataasstream-uri-parameters)

シンプルには以下のように指定できる。
```javascript
let url = `https://${yoursiteurl}/_api/web/lists/GetByTitle('test_data_v2')/RenderListDataAsStream?FilterField1=field_4&FilterValue1=10&FilterType1=Number`;

let res = await fetch(url, {
    method: "POST",
    headers: headers,
    body: JSON.stringify({
        parameters:{
            "__metadata":{
                "type":"SP.RenderListDataParameters"
                },
            RenderOptions: 0
        }
    })
}).then(r=>r.json());
console.log(res);
```

5000件までのデータの場合は問題なく 200 でデータの取得ができる。
```javascript
let url = `https://${yoursiteurl}/_api/web/lists/GetByTitle('test_data_v2')/RenderListDataAsStream?FilterField1=field_4&FilterValue1=5000&FilterType1=Number`;

let res = await fetch(url, {
    method: "POST",
    headers: headers,
    body: JSON.stringify({
        parameters:{
            "__metadata":{
                "type":"SP.RenderListDataParameters"
                },
            RenderOptions: 0
        }
    })
}).then(r=>r.json());
console.log(res);
```

`RenderListDataAsStream` は `Items` の場合とは違い、 5001 件以上のデータがヒットした場合でも問題なくデータの取得ができる。

```javascript
let url = `https://${yoursiteurl}/_api/web/lists/GetByTitle('test_data_v2')/RenderListDataAsStream?FilterField1=field_4&FilterValue1=5001&FilterType1=Number`;

let res = await fetch(url, {
    method: "POST",
    headers: headers,
    body: JSON.stringify({
        parameters:{
            "__metadata":{
                "type":"SP.RenderListDataParameters"
                },
            RenderOptions: 0
        }
    })
}).then(r=>r.json());
console.log(res);
```

この場合、以下のようにデータを取得することで対象の全てのデータを取得することができる。

```javascript
let url = `https://${yoursiteurl}/_api/web/lists/GetByTitle('test_data_v2')/RenderListDataAsStream?FilterField1=field_4&FilterValue1=5001&FilterType1=Number`;

let ans = [];

while(true){

    let res = await fetch(url, {
        method: "POST",
        headers: headers,
        body: JSON.stringify({
            parameters:{
                "__metadata":{
                    "type":"SP.RenderListDataParameters"
                    },
                RenderOptions: 0
            }
        })
    }).then(r=>r.json());
    ans = [...ans, ...res.Row];

    if(!res.NextHref)break;
    url = `https://${yoursiteurl}/_api/web/lists/GetByTitle('test_data_v2')/RenderListDataAsStream` + res.NextHref;
}
console.log(ans.length);
```

一度にたくさんのデータを取得する場合は `RowLimit` を指定することになるが、5001 以上を設定すると 500 のエラーが返る。

```javascript
let url = `https://${yoursiteurl}/_api/web/lists/GetByTitle('test_data_v2')/RenderListDataAsStream?RowLimit=5001`;

let res = await fetch(url, {
    method: "POST",
    headers: headers,
    body: JSON.stringify({
        parameters:{
            "__metadata":{
                "type":"SP.RenderListDataParameters"
                },
            RenderOptions: 0
        }
    })
}).then(r=>r.json());
console.log(res);
```

```json
{
    "odata.error": {
        "code": "-2147024860, Microsoft.SharePoint.SPQueryThrottledException",
        "message": {
            "lang": "ja-JP",
            "value": "この操作は、リストビューのしきい値を超えているため、実行できません。"
        }
    }
}
```

`RowLimit` を指定した場合、条件にヒットするデータが 5000 件以内であれば 1 回のリクエストで全て取得することができるが、ヒットするデータが 5001 件以上になる場合は 1 回のリクエストで取得できるデータは分割されてしまう。  
例えば以下のようにパラメータを指定すると 5001 件のデータがヒットするためデータは分割される。  
ただし、注意点として取得されるデータは 5000 件と 1 件に分割されるのではなく、はじめのリクエストで取得されるのは 238 件しか取得されない。  
なぜ 238 件なのかというと全データの先頭 5000 件の中に以下の条件に合致するデータが 238 件しかなかったため。  
つまり、5000 件区切りで検索されその値が返却されるということになる。

```javascript
let url = `https://${yoursiteurl}/_api/web/lists/GetByTitle('test_data_v2')/RenderListDataAsStream?FilterField1=field_4&FilterValue1=5001&FilterType1=Number&RowLimit=5000`;

let res = await fetch(url, {
    method: "POST",
    headers: headers,
    body: JSON.stringify({
        parameters:{
            "__metadata":{
                "type":"SP.RenderListDataParameters"
                },
            RenderOptions: 0
        }
    })
}).then(r=>r.json());
// 238 件のデータ
console.log(res);
```

以下のように条件にヒットするデータが 5000 件以内の場合は 1 回で取得できるので、5001 件を超えるか超えないかによってデータの取得効率にかなり差が出ることになる。

```javascript
let url = `https://${yoursiteurl}/_api/web/lists/GetByTitle('test_data_v2')/RenderListDataAsStream?FilterField1=field_4&FilterValue1=5000&FilterType1=Number&RowLimit=5000`;

let res = await fetch(url, {
    method: "POST",
    headers: headers,
    body: JSON.stringify({
        parameters:{
            "__metadata":{
                "type":"SP.RenderListDataParameters"
                },
            RenderOptions: 0
        }
    })
}).then(r=>r.json());
// 5000 件のデータ
console.log(res);
```

URL パラメータでイコール以外の操作を指定することができるとドキュメントにあるが実際には無視されるらしく、指定を行ってもイコールとしか判定がされない。

[ContentByQueryWebPart.FilterFieldQueryOperator Enumeration (Microsoft.SharePoint.Publishing.WebControls)](https://learn.microsoft.com/en-us/previous-versions/office/developer/sharepoint-2010/ms498236(v=office.14)?redirectedfrom=MSDN)

Reddit ではあるが無視されることが書かれており、実際に指定しても `Leq` などは使えなかった。

[Reddit - Dive into anything](https://www.reddit.com/r/sharepoint/comments/4levk7/url_filter_not_recognizing_filterop1/?rdt=52020)

```javascript
let url = `https://${yoursiteurl}/_api/web/lists/GetByTitle('test_data_v2')/RenderListDataAsStream?FilterField1=field_4&FilterValue1=100&FilterType1=Number&FilterOp1=Leq&RowLimit=5000`;

let res = await fetch(url, {
    method: "POST",
    headers: headers,
    body: JSON.stringify({
        parameters:{
            "__metadata":{
                "type":"SP.RenderListDataParameters"
                },
            RenderOptions: 0
        }
    })
}).then(r=>r.json());
// 100 件のデータが取得されてしまう
console.log(res);
```

そのため、`Leq` などを指定したい場合は `ViewXml` を使用する必要がある。

### ViewXml で指定


ViewXml のリファレンスは以下。  
[View element (List)](https://learn.microsoft.com/en-us/sharepoint/dev/schema/view-element-list)

シンプルに `RowLimit` を指定する場合は以下。

```javascript
let url = `https://${yoursiteurl}/_api/web/lists/GetByTitle('test_data_v2')/RenderListDataAsStream`;

let viewXml = `
<View>
    <RowLimit>5000</RowLimit>
</View>`;

let res = await fetch(url, {
    method: "POST",
    headers: headers,
    body: JSON.stringify({
        parameters:{
            "__metadata":{
                "type":"SP.RenderListDataParameters"
                },
            RenderOptions: 0,
            ViewXml: viewXml
        }
    })
}).then(r=>r.json());
console.log(res);
```

`RenderOptions` を指定することで取得できるデータにメタデータなどを追加することができる。 `0` は最もシンプルなデータを取得する。

[REST を使用してリストとリスト アイテムを操作する](https://learn.microsoft.com/ja-jp/sharepoint/dev/sp-add-ins/working-with-lists-and-list-items-with-rest#sprenderlistdataoptions-options)


フィルターを指定する場合は以下。
```javascript
let url = `https://${yoursiteurl}/_api/web/lists/GetByTitle('test_data_v2')/RenderListDataAsStream`;

let viewXml = `
<View>
    <Query>
        <Where>
            <Eq>
                <FieldRef Name="field_4" />
                <Value Type="Number">100</Value>
            </Eq>
        </Where>
    </Query>
    <RowLimit>5000</RowLimit>
</View>`;

let res = await fetch(url, {
    method: "POST",
    headers: headers,
    body: JSON.stringify({
        parameters:{
            "__metadata":{
                "type":"SP.RenderListDataParameters"
                },
            RenderOptions: 0,
            ViewXml: viewXml
        }
    })
}).then(r=>r.json());
console.log(res);
```

URL Parameter ではできない `Leq` などの設定や複数の条件の設定することができる。
```javascript
let url = `https://${yoursiteurl}/_api/web/lists/GetByTitle('test_data_v2')/RenderListDataAsStream`;

let viewXml = `
<View>
    <Query>
        <Where>
            <And>
                <Leq>
                    <FieldRef Name="field_4" />
                    <Value Type="Number">100</Value>
                </Leq>
                <Geq>
                    <FieldRef Name="field_4" />
                    <Value Type="Number">0</Value>
                </Geq>
            </And>
        </Where>
    </Query>
    <RowLimit>5000</RowLimit>
</View>`;

let res = await fetch(url, {
    method: "POST",
    headers: headers,
    body: JSON.stringify({
        parameters:{
            "__metadata":{
                "type":"SP.RenderListDataParameters"
                },
            RenderOptions: 0,
            ViewXml: viewXml
        }
    })
}).then(r=>r.json());
console.log(res);
```

## 日付と時刻の絞り込みについて

日付の絞り込みはやや特殊なのでメモしておく。

### Items で絞り込み

UTC の ISO フォーマットで日付を指定することでフィルタができる
この時 `2024-01-01T00:00:00%2B09:00` というように `+` はエンコードしておく。  
もちろん `2024-01-01T00:00:00Z` でもよい。  
きちんとタイムゾーンを考慮して絞り込みをしてくれる。

```javascript
let url = `https://${yoursiteurl}/_api/web/lists/GetByTitle('test_data_v2')/Items?$filter=field_3 eq '2024-01-01T00:00:00%2B09:00'`;

let res = await fetch(url, {
    method: "GET",
    headers: headers,
    }
).then(r=>r.json());
console.log(res);
```

### REnderListDataAsStream で絞り込み

時刻まで指定して絞り込みを行うことはできない。  
日単位で絞り込みを行い、取得したデータを Javascript 等でさらに絞り込む必要がある。  

`RowLimit` で `Paged` を指定しない場合 `NextHref` が取得できない場合がある。  

`<Value Type="DateTime">2024-01-01T00:00:00Z</Value>` は `2024/1/1` と解釈されるようで、一番始めに取得される値は以下のようになる。  

```
field_3: "2024/01/01 0:00"
field_3.: "2023-12-31T15:00:00Z"
```


また、日付で以降などの検索をするとデータが5000より多くなる場合がほとんどになると思うので、他のフィールドの値のフィルターと組み合わせるのが無難。  

```javascript
let url = `https://${yoursiteurl}/_api/web/lists/GetByTitle('test_data_v2')/RenderListDataAsStream`;

// このように指定することで表示の 2024/1/1のデータを取得
let viewXml = `
<View>
    <Query>
        <Where>
            <And>
                <Geq>
                    <FieldRef Name="field_3" />
                    <Value Type="DateTime">2024-01-01T00:00:00Z</Value>
                </Geq>
                <Leq>
                    <FieldRef Name="field_3" />
                    <Value Type="DateTime">2024-01-01T00:00:00Z</Value>
                </Leq>
            </And>
        </Where>
    </Query>
    <RowLimit Paged="TRUE">5000</RowLimit>
</View>`;


let ans = [];

while(true){

    let res = await fetch(url, {
        method: "POST",
        headers: headers,
        body: JSON.stringify({
            parameters:{
                "__metadata":{
                    "type":"SP.RenderListDataParameters"
                    },
                RenderOptions: 0,
                ViewXml: viewXml
            }
        })
    }).then(r=>r.json());
    ans = [...ans, ...res.Row];
    console.log(res.Row.length);
    if(!res.NextHref)break;
    url = `https://${yoursiteurl}/_api/web/lists/GetByTitle('test_data_v2')/RenderListDataAsStream` + res.NextHref;
}
console.log(ans.length);

```
