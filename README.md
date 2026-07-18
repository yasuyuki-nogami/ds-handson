# 3時間データサイエンス・ハンズオン教材（岡山県 高校教員向け）

Chromebook + Google Colab だけで動く、日本の公開データを使ったハンズオン一式です。

## 中身
```
notebooks/
  01_kiso.ipynb              ① 座学：Python/pandas/可視化の基礎（写経）
  02_handson.ipynb           ② 応用ハンズオン（穴埋め・受講者用）
  02_handson_solution.ipynb  ②' 解答版（講師用）
  03_group_starter.ipynb     ③ グループ自由演習スターター
data/
  prefecture.csv             47都道府県 人口・面積（国勢調査2020・実データ）
  school_health.csv          年齢別 平均身長・体重（学校保健統計・実データ整理）
  gakuryoku_lifestyle.csv    生活習慣×平均正答率（全国学力調査・整理）
  class_sample.csv           生徒360人の練習用サンプル（架空データ）
DATA_GUIDE.md                データ説明書＋配布方法
FACILITATION_GUIDE.md        3時間の進行台本（講師用）
slide_prompt.txt             発表スライドをAIで作るためのプロンプト
```

## Colabで開く（オーナー向け・ワンクリック）
> privateリポなので、初回はColabのGitHub連携の認可が必要です（リポにアクセスできるアカウントで）。
- ① 座学: https://colab.research.google.com/github/yasuyuki-nogami/ds-handson/blob/main/notebooks/01_kiso.ipynb
- ② 演習: https://colab.research.google.com/github/yasuyuki-nogami/ds-handson/blob/main/notebooks/02_handson.ipynb
- ②' 解答: https://colab.research.google.com/github/yasuyuki-nogami/ds-handson/blob/main/notebooks/02_handson_solution.ipynb
- ③ グループ: https://colab.research.google.com/github/yasuyuki-nogami/ds-handson/blob/main/notebooks/03_group_starter.ipynb

## 使い方（かんたん）
1. Google Colab（https://colab.research.google.com/ ）を開く。
2. `notebooks/` の .ipynb をアップロード（または上の「Colabで開く」リンク）。
3. 上のセルから順に **Shift+Enter** で実行。
4. データは各ノート最初の `load()` が読み込みます（既定は手動アップロード。`DATA_GUIDE.md` 参照）。

## 受講者への配布（Chromebook）
privateリポの raw URL はトークンが必要なため、受講者への自動ダウンロードには不向きです。
当日は **`data/` のCSVを配って手動アップロード**、または **Google Drive共有** が確実です。

## 3時間の流れ
- 1時間目：基礎を写経で（`01_kiso.ipynb`）
- 2時間目：自分で手を動かす演習（`02_handson.ipynb`）
- 3時間目：グループで自由分析＆発表（`03_group_starter.ipynb`）

詳細は `FACILITATION_GUIDE.md` を参照。
