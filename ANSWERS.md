# 穴埋めの答え（答え合わせ用）

手が止まったときは、このページを見ながら `____` の部分を自分でタイピングしてください。
（ノートブックは配布せず、この答えをGitHubで表示して使います）

---

## ② 応用ハンズオン（`02_handson.ipynb`）の穴埋め

### 1. 要約統計量
```python
df.describe()
```
→ `____` に入るのは **`describe`**

### 2. 朝食ごとの平均点（groupby）
```python
grp = df.groupby("breakfast")["test_score"].mean()
print(grp)
```
→ 1つ目の `____` は **`breakfast`**、2つ目の `____` は **`mean`**

### 3. 箱ひげ図で分布を比べる
```python
df.boxplot(column="test_score", by="breakfast", figsize=(6,4))
```
→ `column="test_score"`、`by="breakfast"`

### 4. 散布図（勉強時間と点数）
```python
plt.scatter(df["study_min"], df["test_score"], alpha=0.4)
```
→ 1つ目の `____` は **`study_min`**、2つ目の `____` は **`test_score`**

### 5. 相関係数
```python
print("相関係数：", df["study_min"].corr(df["test_score"]))
```
→ `____` に入るのは **`corr`**

### 6. 「朝食」の行だけ取り出す
```python
asa = g[g["category"] == "朝食"]
```
→ `____` に入るのは **`朝食`**（ダブルクオートの中に日本語で）

---

## ① 基礎編（`01_kiso.ipynb`）の練習問題（セクション6）の解答例

```python
# 1. 人口密度が高い順トップ5
print("■ 人口密度トップ5")
print(df.sort_values("density_per_km2", ascending=False).head(5)[["prefecture","density_per_km2"]])

# 2. 面積が最も大きい都道府県
print("\n■ 面積が最大の都道府県")
print(df.sort_values("area_km2", ascending=False).head(1)[["prefecture","area_km2"]])

# 3. 地方ごとの面積の合計
print("\n■ 地方別の面積合計")
print(df.groupby("region")["area_km2"].sum().sort_values(ascending=False))
```

---

> ヒント：メソッド名（`describe` / `mean` / `corr` など）や列名（`study_min` など）は
> **半角**で、スペルどおりに入力してください。列名の大文字・小文字も区別されます。

---

## ② 応用例集：こんなこともできます（コピペで動きます）

②の内容に慣れたら、下の例を新しいセルに貼って実行してみてください。
すべて `load()` で読み込んだ `df`（`class_sample.csv`）などをそのまま使えます。
※ 都道府県の例は `pref = load("prefecture.csv")`、成長曲線は `sh = load("school_health.csv")`、
　学力データは `g = load("gakuryoku_lifestyle.csv")` を先に読み込んでください。

### A. 集計・絞り込み・データ加工

**件数を数える（value_counts）**
```python
print(df["grade"].value_counts().sort_index())   # 学年ごとの人数
print(df["sex"].value_counts())                   # 男女の人数
```

**割合で見る（normalize）**
```python
print(df["breakfast"].value_counts(normalize=True).round(3))  # 朝食を食べる人の割合
```

**複数の条件で絞り込む**
```python
# 3年生で、勉強時間が90分以上の生徒
jyoken = df[(df["grade"] == 3) & (df["study_min"] >= 90)]
print("該当人数:", len(jyoken))
jyoken.head()
```

**新しい列を作る（BMIを計算）**
```python
df["BMI"] = df["weight_kg"] / (df["height_cm"] / 100) ** 2
print(df[["height_cm", "weight_kg", "BMI"]].head())
```

**学年×性別のクロス集計（pivot_table）**
```python
hyo = df.pivot_table(index="grade", columns="sex", values="test_score", aggfunc="mean").round(1)
print(hyo)
```

**複数の統計量をまとめて（agg）**
```python
print(df.groupby("grade")["test_score"].agg(["count", "mean", "std", "min", "max"]).round(1))
```

**上位・下位を見る（nlargest / nsmallest）**
```python
print("点数トップ5")
print(df.nlargest(5, "test_score")[["student_id", "grade", "test_score"]])
```

**偏差値を計算する**
```python
mu, sd = df["test_score"].mean(), df["test_score"].std()
df["偏差値"] = (df["test_score"] - mu) / sd * 10 + 50
print(df[["test_score", "偏差値"]].head())
```

**欠損値・基本情報の確認**
```python
print(df.info())
print(df.isnull().sum())
```

### B. いろいろなグラフ

**男女で点数のヒストグラムを重ねる**
```python
plt.figure(figsize=(7,4))
for s, sub in df.groupby("sex"):
    plt.hist(sub["test_score"], bins=20, alpha=0.5, label=s)
plt.xlabel("点数"); plt.ylabel("人数"); plt.legend(); plt.title("男女別 点数の分布")
plt.show()
```

**学年ごとの点数を箱ひげ図で比べる**
```python
df.boxplot(column="test_score", by="grade", figsize=(6,4))
plt.title("学年別 点数"); plt.suptitle(""); plt.ylabel("点数")
plt.show()
```

**散布図を性別で色分け**
```python
plt.figure(figsize=(6,5))
for s, sub in df.groupby("sex"):
    plt.scatter(sub["study_min"], sub["test_score"], alpha=0.4, label=s)
plt.xlabel("勉強時間（分）"); plt.ylabel("点数"); plt.legend(); plt.title("勉強時間と点数（男女別）")
plt.show()
```

**相関行列をヒートマップで**
```python
num = df[["height_cm","weight_kg","study_min","sleep_hours","smartphone_hours","test_score"]]
corr = num.corr()
plt.figure(figsize=(6,5))
plt.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1); plt.colorbar()
plt.xticks(range(len(corr.columns)), corr.columns, rotation=45, ha="right")
plt.yticks(range(len(corr.columns)), corr.columns)
plt.title("相関行列"); plt.tight_layout(); plt.show()
print(corr.round(2))
```

**グループの平均を棒グラフに**
```python
m = df.groupby("grade")["test_score"].mean()
plt.figure(figsize=(5,4))
plt.bar(m.index.astype(str), m.values)
plt.xlabel("学年"); plt.ylabel("平均点"); plt.title("学年別 平均点")
plt.show()
```

**並べ替えて上位を横棒グラフに（都道府県）**
```python
t = pref.nlargest(10, "population_2020").sort_values("population_2020")
plt.figure(figsize=(7,4))
plt.barh(t["prefecture"], t["population_2020"]/10000)
plt.xlabel("人口（万人）"); plt.title("人口トップ10"); plt.tight_layout(); plt.show()
```

**成長曲線（学校保健統計・男女別）**
```python
for s, sub in sh.groupby("sex"):
    plt.plot(sub["age"], sub["height_cm"], marker="o", label=s)
plt.xlabel("年齢"); plt.ylabel("平均身長(cm)"); plt.legend(); plt.title("年齢と平均身長")
plt.show()
```

**生活習慣ごとの正答率（学力データ）**
```python
asa = g[g["category"] == "睡眠"]
plt.figure(figsize=(6,4))
plt.bar(asa["group"], asa["japanese_score"])
plt.ylabel("国語 平均正答率(%)"); plt.title("睡眠時間と正答率"); plt.tight_layout(); plt.show()
```

### C. 関係を調べる・予測する

**どの2つが関係が強い？（相関ランキング）**
```python
num = df[["height_cm","weight_kg","study_min","sleep_hours","smartphone_hours","test_score"]]
c = num.corr().abs()
pairs = c.where(~np.eye(len(c), dtype=bool)).stack().sort_values(ascending=False)
print(pairs.head(5).round(3))
```

**単回帰（勉強時間→点数）を数式で**
```python
a, b = np.polyfit(df["study_min"], df["test_score"], 1)
print(f"点数 ≈ {a:.3f} × 勉強時間 + {b:.1f}")
```

**重回帰（複数の要因から予測）**
```python
from sklearn.linear_model import LinearRegression
X = df[["study_min", "sleep_hours", "breakfast", "smartphone_hours"]]
model = LinearRegression().fit(X, df["test_score"])
print(pd.Series(model.coef_, index=X.columns).round(2))
```
