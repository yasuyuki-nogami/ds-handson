# 3時間データサイエンス・ハンズオン教材（岡山県 高校教員向け）

Chromebook + Google Colab だけで動く、日本の公開データを使ったハンズオン一式です。

## 中身
```
notebooks/
  01_kiso.ipynb              ① 座学：Python/pandas/可視化の基礎（入力して実行）
  02_handson.ipynb           ② 応用ハンズオン（穴埋め・受講者用）
  02_handson_solution.ipynb  ②' 解答版（穴埋めをすべて埋めた講師用）
  03_group_starter.ipynb     ③ グループ自由演習スターター
  03_group_example.ipynb     ③' 模範グループワーク例（完成サンプル）
  04_advanced.ipynb          ④ 発展デモ（③の別案・実行するだけ）：クラスタリング/主成分分析(PCA)/回帰予測/因果推論
ANSWERS.md                   ①②の穴埋めの答え＋②の応用例集（コピペで動く事例集）
data/
  prefecture.csv             47都道府県 人口・面積（国勢調査2020・実データ）
  school_health.csv          年齢別 平均身長・体重（学校保健統計・実データ整理）
  gakuryoku_lifestyle.csv    生活習慣×平均正答率（全国学力調査・整理）
  class_sample.csv           生徒360人の練習用サンプル（架空データ）
data_official/               e-Stat公式APIから実際にDLした実データ（別ファイル名で保存）
  prefecture_estat2020.csv   47都道府県 人口・面積・人口密度（令和2年国勢調査）
  school_health_estat2019.csv 年齢別・男女別 平均身長・体重（学校保健統計 2019年度）
  raw/*.json                 APIの生レスポンス（記録用）
scripts/fetch_estat.py       上記を再取得する再現スクリプト（要 ESTAT_APP_ID）
text/                        読み物版テキスト（全4章のmd）
  README.md                  テキストの目次
  01_基礎編.md / 02_応用ハンズオン.md / 03_グループワーク.md / 04_発展編.md
DATA_GUIDE.md                データ説明書＋配布方法＋公式実データの出典
FACILITATION_GUIDE.md        3時間の進行台本（講師用）
slide_prompt.txt             発表スライドをAIで作るためのプロンプト
```

## Colabで開く（オーナー向け・ワンクリック）
> privateリポなので、初回はColabのGitHub連携の認可が必要です（リポにアクセスできるアカウントで）。
- ① 座学: https://colab.research.google.com/github/yasuyuki-nogami/ds-handson/blob/main/notebooks/01_kiso.ipynb
- ② 演習: https://colab.research.google.com/github/yasuyuki-nogami/ds-handson/blob/main/notebooks/02_handson.ipynb
- ②' 解答（講師用）: https://colab.research.google.com/github/yasuyuki-nogami/ds-handson/blob/main/notebooks/02_handson_solution.ipynb
- ③ グループ: https://colab.research.google.com/github/yasuyuki-nogami/ds-handson/blob/main/notebooks/03_group_starter.ipynb
- ③' 完成例: https://colab.research.google.com/github/yasuyuki-nogami/ds-handson/blob/main/notebooks/03_group_example.ipynb
- ④ 発展デモ（③の別案）: https://colab.research.google.com/github/yasuyuki-nogami/ds-handson/blob/main/notebooks/04_advanced.ipynb

### 穴埋めの答え（手が止まった人向け）
**受講者向け**：下のページをGitHubで表示し、穴埋めの答えを見ながら自分で入力してください。
- 穴埋めの答え＋応用例集: https://github.com/yasuyuki-nogami/ds-handson/blob/main/ANSWERS.md

**講師向け**：穴埋めをすべて埋めた②'解答ノート（上の「②' 解答（講師用）」リンク）を手元に。

> ②は穴埋め式です。`____` を自分で埋めるまでエラーになります（仕様）。埋め方がわからないときは ANSWERS.md を参照。

## 使い方（かんたん）
1. Google Colab（https://colab.research.google.com/ ）を開く。
2. `notebooks/` の .ipynb をアップロード（または上の「Colabで開く」リンク）。
3. 上のセルから順に **Shift+Enter** で実行。
4. データは各ノート最初の `load()` が読み込みます（既定は手動アップロード。`DATA_GUIDE.md` 参照）。

## 受講者への配布（Chromebook）
各ノートの `BASE_URL` は、このリポの raw URL を指すよう設定済みです。

- **当日だけ public にする運用（おすすめ）**：リポを Public にしている間は、`load()` が
  raw URL から自動でデータを読み込みます（受講者はアップロード不要・「Colabで開く→実行」だけ）。
  終わったら Private に戻せばOK。
- **private のまま運用**：raw URL はトークンが必要なため自動DLは失敗し、`load()` は
  自動的に「手動アップロード」に切り替わります。`data/` のCSVを配布してください。

### 公開/非公開の切り替え方
GitHubのリポ → **Settings → General → 一番下 Danger Zone → Change repository visibility**。
（このリポのデータは公開統計・架空データのみで、秘密情報は含みません）

## 3時間の流れ
- 1時間目：基礎を入力しながら（`01_kiso.ipynb`）
- 2時間目：自分で手を動かす演習（`02_handson.ipynb`）
- 3時間目：グループで自由分析＆発表（`03_group_starter.ipynb`）

詳細は `FACILITATION_GUIDE.md` を参照。
