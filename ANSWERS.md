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
