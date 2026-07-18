#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
e-Stat 公式API から実データを取得して CSV に保存する再現用スクリプト。

使い方:
    export ESTAT_APP_ID=あなたのアプリケーションID
    python3 scripts/fetch_estat.py

取得するもの:
  1) 令和2年(2020)国勢調査 人口等基本集計（statsDataId=0003445099）
     → 都道府県別 人口・面積・人口密度
     生JSON : data_official/raw/census2020_pref_0003445099.json
     整形CSV: data_official/prefecture_estat2020.csv

  2) 学校保健統計調査 平成27年度以降 全国表（statsDataId=0003146500）
     → 年齢別(5〜17歳)・男女別 平均身長・平均体重（最新年度=2019年度）
     生JSON : data_official/raw/school_health_0003146500.json
     整形CSV: data_official/school_health_estat2019.csv

出典: 政府統計の総合窓口(e-Stat) https://www.e-stat.go.jp/
      総務省統計局「令和2年国勢調査」/ 文部科学省「学校保健統計調査」
"""
import os
import re
import csv
import json
import datetime
import urllib.parse
import urllib.request

APP_ID = os.environ.get("ESTAT_APP_ID")
API = "https://api.e-stat.go.jp/rest/3.0/app/json"

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(HERE, "data_official", "raw")
OUT_DIR = os.path.join(HERE, "data_official")

# 既存 prefecture.csv から region(地方区分) を引き継ぐ
PREF_CSV = os.path.join(HERE, "data", "prefecture.csv")


def get(endpoint, params):
    params = dict(params)
    params["appId"] = APP_ID
    url = f"{API}/{endpoint}?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=120) as r:
        return r.read()


def load_region_map():
    region = {}
    if os.path.exists(PREF_CSV):
        with open(PREF_CSV, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                region[row["prefecture"]] = row.get("region", "")
    return region


def fetch_census_prefecture():
    """令和2年国勢調査 都道府県別 人口・面積・人口密度"""
    stats_data_id = "0003445099"
    # tab: 2020_03=2015人口(組替), 2020_34=5年間の人口増減数,
    #      2020_47=面積(参考), 2020_48=人口密度(公表値)
    raw = get("getStatsData", {
        "statsDataId": stats_data_id,
        "cdTab": "2020_03,2020_34,2020_47,2020_48",
    })
    os.makedirs(RAW_DIR, exist_ok=True)
    raw_path = os.path.join(RAW_DIR, f"census2020_pref_{stats_data_id}.json")
    with open(raw_path, "wb") as f:
        f.write(raw)

    d = json.loads(raw)
    sd = d["GET_STATS_DATA"]
    status = sd["RESULT"]["STATUS"]
    if status != 0:
        raise RuntimeError(f"e-Stat error: {sd['RESULT'].get('ERROR_MSG')}")

    # 地域コード -> 名称
    names = {}
    for cls in sd["STATISTICAL_DATA"]["CLASS_INF"]["CLASS_OBJ"]:
        if cls["@id"] == "area":
            objs = cls["CLASS"]
            objs = [objs] if isinstance(objs, dict) else objs
            for o in objs:
                names[o["@code"]] = o["@name"]

    pref_re = re.compile(r"^(0[1-9]|[1-4][0-9])000$")  # 都道府県コード(全国00000を除く)
    rows = {}
    for v in sd["STATISTICAL_DATA"]["DATA_INF"]["VALUE"]:
        area = v["@area"]
        if not pref_re.match(area):
            continue
        rows.setdefault(area, {})[v["@tab"]] = v["$"]

    region_map = load_region_map()
    out = []
    for area in sorted(rows):
        r = rows[area]
        code = int(area[:2])
        name = names[area]
        pop2015 = int(r["2020_03"])
        delta = int(r["2020_34"])
        pop2020 = pop2015 + delta          # 2020総人口 = 2015人口 + 5年間の増減数
        area_km2 = float(r["2020_47"])     # 面積(参考)
        density = float(r["2020_48"])      # 人口密度(公表値)
        out.append({
            "code": code,
            "prefecture": name,
            "region": region_map.get(name, ""),
            "population_2020": pop2020,
            "area_km2": area_km2,
            "density_per_km2": density,
        })

    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, "prefecture_estat2020.csv")
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "code", "prefecture", "region",
            "population_2020", "area_km2", "density_per_km2",
        ])
        w.writeheader()
        w.writerows(out)

    return out_path, raw_path, len(out)


def fetch_school_health():
    """学校保健統計調査 年齢別・男女別 平均身長・平均体重（最新年度）"""
    stats_data_id = "0003146500"
    # cat01: 60=男(計), 110=女(計)
    # cat02: 10..130 = 計[各年齢 5〜17歳]（設置者=計）
    # cat03: 0000010=平均値
    # cat04: 0000010=身長(cm), 0000020=体重(kg)
    age_codes = [str(c) for c in range(10, 131, 10)]  # 10,20,...,130
    raw = get("getStatsData", {
        "statsDataId": stats_data_id,
        "cdCat01": "60,110",
        "cdCat02": ",".join(age_codes),
        "cdCat03": "0000010",
        "cdCat04": "0000010,0000020",
    })
    os.makedirs(RAW_DIR, exist_ok=True)
    raw_path = os.path.join(RAW_DIR, f"school_health_{stats_data_id}.json")
    with open(raw_path, "wb") as f:
        f.write(raw)

    d = json.loads(raw)
    sd = d["GET_STATS_DATA"]
    if sd["RESULT"]["STATUS"] != 0:
        raise RuntimeError(f"e-Stat error: {sd['RESULT'].get('ERROR_MSG')}")

    # コード -> 名称の辞書
    meta = {}
    latest_time = None
    for cls in sd["STATISTICAL_DATA"]["CLASS_INF"]["CLASS_OBJ"]:
        objs = cls["CLASS"]
        objs = [objs] if isinstance(objs, dict) else objs
        meta[cls["@id"]] = {o["@code"]: o["@name"] for o in objs}
        if cls["@id"] == "time":
            # 最新年度（コードが最大）
            latest_time = max(o["@code"] for o in objs)

    sex_map = {"60": "male", "110": "female"}
    age_re = re.compile(r"\((\d+)歳\)")

    # (age, sex) -> {height, weight}
    rows = {}
    for v in sd["STATISTICAL_DATA"]["DATA_INF"]["VALUE"]:
        if v.get("@time") != latest_time:
            continue
        sex = sex_map.get(v["@cat01"])
        if sex is None:
            continue
        m = age_re.search(meta["cat02"].get(v["@cat02"], ""))
        if not m:
            continue
        age = int(m.group(1))
        kind = v["@cat04"]  # 0000010=身長, 0000020=体重
        key = (age, sex)
        rows.setdefault(key, {})
        if kind == "0000010":
            rows[key]["height_cm"] = float(v["$"])
        elif kind == "0000020":
            rows[key]["weight_kg"] = float(v["$"])

    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, "school_health_estat2019.csv")
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["age", "sex", "height_cm", "weight_kg"])
        w.writeheader()
        for (age, sex) in sorted(rows, key=lambda k: (k[0], k[1])):
            r = rows[(age, sex)]
            w.writerow({
                "age": age, "sex": sex,
                "height_cm": r.get("height_cm"),
                "weight_kg": r.get("weight_kg"),
            })

    year_label = latest_time[:4] if latest_time else "?"
    return out_path, raw_path, len(rows), year_label


def main():
    if not APP_ID:
        raise SystemExit("環境変数 ESTAT_APP_ID を設定してください。")
    stamp = datetime.date.today().isoformat()
    print(f"[{stamp}] e-Stat 取得開始")

    out_path, raw_path, n = fetch_census_prefecture()
    print("1) 国勢調査 都道府県")
    print(f"   raw : {raw_path}")
    print(f"   csv : {out_path}  ({n} 都道府県)")

    out_path, raw_path, n, year = fetch_school_health()
    print(f"2) 学校保健統計調査（{year}年度）")
    print(f"   raw : {raw_path}")
    print(f"   csv : {out_path}  ({n} 行 = 年齢×男女)")


if __name__ == "__main__":
    main()
