# furusato_crawler
## What is this?
ふるさと納税の納税先を決定する上での判断材料を提供するツールです。
ふるさとチョイスで検索したい任意の文字列を引数として渡すと、その引数での検索結果のうち必要最低限な情報をまとめてCSV出力します。
出力は値段の安い順となっています。
ふるさとチョイスのURLは以下。
https://www.furusato-tax.jp/

## How to use on Mac

```
$ python furusato_crawler.py <search string>
```

### example
実行は以下のような感じ

```
$ python furusato_crawler.py ステーキ 神戸牛
  -> 出力ファイルは "./result/ステーキ_神戸牛_201709100000.csv"
```

出力ファイルの中身は以下のような感じ

```
title, price, content
神戸牛A4等級MBS6以上, 10000, 200g（1枚）
神戸牛（加古川育ち）ステーキ, 20000, 200g x 2枚
```

## Remarks
このツールは私の妻が私のMac上で使うことのみを想定しているため、作りが雑なことこの上ないです。
ご注意下さい。
