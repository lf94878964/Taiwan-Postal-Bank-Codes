# Taiwan Postal & Bank Codes

台灣三碼郵遞區號與金融機構代碼的 CSV / JSON 對照表。

- **Postal codes:** 371 筆（368 個不同的三碼）
- **Bank codes:** 105 筆（三碼機構代號）

## Files

| File | Description |
| --- | --- |
| `postal_codes.csv` / `.json` | 三碼郵遞區號、縣市、鄉鎮市區（含英文） |
| `bank_codes.csv` / `.json` | 三碼金融機構代號、名稱、類別、資料來源 |
| `data/banks_source.csv` | 銀行代碼的原始人工整理檔 |
| `scripts/build.py` | 產生上述檔案並驗證資料 |

## Usage

```
# 查郵遞區號
grep "^330," postal_codes.csv

# 查銀行代碼
grep "^822," bank_codes.csv
```

```python
import json
banks = {b["code"]: b["name"] for b in json.load(open("bank_codes.json", encoding="utf-8"))}
print(banks["012"])  # 台北富邦商業銀行
```

## Notes

- 同一個三碼可對應多個行政區：`300`（新竹市東區／北區／香山區）、`600`（嘉義市東區／西區）、`290`（釣魚臺）、`817`／`819`（東沙／南沙群島）。
- 這裡只收三碼郵遞區號，不含後三碼投遞區段碼。
- 銀行代碼是轉帳時填的三碼，即中央銀行機構代號（四碼）去掉開頭的 `0`。
- `sources` 欄位：`cbc_2020` 是中央銀行金融機構代碼一覽表（2020-10-06 版），`money101` 是 Money101 整理的轉帳代碼表（含純網銀與電子支付）。**只有單一來源的項目請自行確認，部分機構可能已合併或更名。**
- 電子支付代碼（390–398）取自 Money101，與央行表中的四碼編號（如 0791–0796）不同，轉帳以 390–398 為準。
- 農會、漁會（`M` 開頭代號）不在範圍內。

## Sources

- 郵遞區號：中華郵政三碼郵遞區號，經由 [donma/TaiwanAddressCityAreaRoadChineseEnglishJSON](https://github.com/donma/TaiwanAddressCityAreaRoadChineseEnglishJSON) 取得，`build.py` 會自動抓取並驗證。
- 銀行代碼：中央銀行金融資料網路申報系統「金融機構代碼一覽表」、Money101「銀行代碼/代號查詢一覽表」。

## Disclaimer

非官方整理，資料僅供參考，轉帳或寄送重要郵件前請再向官方確認。發現錯誤歡迎開 issue。
