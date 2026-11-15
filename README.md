# 日本建築見積もりワークブック CLI（材料費・労務費・消費税・出典ラベル）

> **関連サイト：[SumaiTools（住まいの建築・リフォーム・DIY 計算器サイト）](https://sumaitools.com/)** — 本リポジトリは、同サイトで公開されている計算器のオフライン版コンパニオン実装です。

## Description

材料価格スナップショットと都道府県別労務単価を組み合わせ、10% 消費税を分離計算し、材料費・送料・労務費を出典ラベル付きで集計するオフライン見積もり CLI。計算器ポータル: https://sumaitools.com/

**Repository topics:** `python` `cli` `construction` `estimating` `japan` `costing` `labor-rate` `renovation`

## 日本語

### このツールについて

ウェブの材料費ツール（[SumaiTools（住まいの建築・リフォーム・DIY 計算器サイト）](https://sumaitools.com/)）は1案件の単価入力向けです。この CLI は明細リストを一括で読み込み、検証済みスナップショット・公的労務単価・利用者入力価格を出典ラベルで区別して見積書を CSV/JSON に出力します。全国平均価格は主張しません。

### 機能

- 同梱の価格スナップショット台帳と労務単価表（20 職種 × 47 都道府県）を参照
- 標準税率 10% を税抜/税込の双方から逆算、消費税を分離表示
- 材料費・送料・労務費を構造的に分離して合計
- 各行に REGISTRY / USER_SUPPLIED の出典ラベルと検証状態を付与
- Python 標準ライブラリのみ

### インストール / Requirements

```bash
# Python 3.10+
git clone https://github.com/anleeylee/jp-material-cost-estimator-cli.git
cd jp-material-cost-estimator-cli
python -m pip install -r requirements.txt
```

### 使い方 / Usage

```bash
python -m jp_cost_estimator.cli --input examples/estimate_sample.csv --output estimate.csv --format csv
```

労務費は所定労働時間内 8 時間当たりの単価で、現場管理費・一般管理費等の諸経費は含みません。

### リポジトリ構成

```
jp-material-cost-estimator-cli/
├── src/jp_cost_estimator/
│   ├── cli.py
│   ├── catalog.py
│   └── costing.py
├── data/
│   ├── price_snapshots.csv
│   └── labor_rates_long.csv
├── examples/estimate_sample.csv
├── tests/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CHANGELOG.md
├── .gitignore
└── sitemap.xml
```

### 注意事項

- 価格スナップショットは特定店舗・特定時点の値で、全国平均・最安値ではありません。
- 労務単価には時間外・休日・深夜割増、現場管理費・一般管理費を含みません。
- 合計には解体費・産廃処分費・仮設材・維持費等は含まれません。

## English

### About

The web material-cost tool ([SumaiTools — Japanese home construction, renovation & DIY calculators](https://sumaitools.com/)) handles one entered unit price. This CLI reads a line-item list, separates verified snapshots, public labor rates and user-entered prices with provenance labels, and exports an estimate CSV/JSON. No national average price is claimed.

### Features

- Bundled price-snapshot catalog and labor rate table (20 occupations x 47 prefectures)
- 10% standard consumption tax computed both ways, shown separately
- Materials, shipping and labor kept structurally separated in totals
- Per-line REGISTRY / USER_SUPPLIED provenance and verification label
- Standard library only

### Usage

See the Japanese command above; the CLI accepts the same arguments and writes CSV / JSON output.

### Notes

- Price snapshots are store- and timestamp-specific, not a national average or lowest price.
- Labor rates exclude overtime and site/general overhead.
- Totals exclude demolition, waste disposal, provisional materials and running costs.

## Source portal

- Calculator web portal: [SumaiTools — Japanese home construction, renovation & DIY calculators](https://sumaitools.com/)
- Open data sets: companion Kaggle datasets published alongside this repository.

## License

MIT — see [LICENSE](LICENSE). Contribution guidelines: [CONTRIBUTING.md](CONTRIBUTING.md).
Release history: [CHANGELOG.md](CHANGELOG.md).
