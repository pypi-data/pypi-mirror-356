# Kenat / ቀናት [![PyPI Version](https://img.shields.io/pypi/v/kenat)](https://pypi.org/project/kenat/)

![banner](https://raw.githubusercontent.com/MelakuDemeke/kenat_py/master/assets/img/py_banner.png)

![GitHub issues](https://img.shields.io/github/issues/MelakuDemeke/kenat_py)
![GitHub Repo stars](https://img.shields.io/github/stars/MelakuDemeke/kenat_py?logo=github&style=flat)
![GitHub forks](https://img.shields.io/github/forks/MelakuDemeke/kenat_py?logo=github&style=falt)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/MelakuDemeke/kenat_py?logo=github)


**A complete Ethiopian Calendar & Bahire Hasab toolkit for Python**

---

## 📌 Overview

**Kenat** (Amharic: ቀናት) is a powerful and authentic Ethiopian calendar library for Python. It offers full support for date conversion, holiday computation (including Bahire Hasab), localized formatting, Geez numerals, and more — all without external dependencies.

> 🚀 Ported from the original [kenat JS library](https://github.com/MelakuDemeke/kenat).

---

## ✨ Features

* 🔄 **Bidirectional Conversion**: Ethiopian ↔ Gregorian calendars
* 📅 **Full Holiday System**: Christian, Muslim, cultural, and public holidays
* ⛪ **Bahire Hasab**: Accurate movable feast calculations (e.g. Fasika, Tsome Nebiyat)
* 🏷️ **Holiday Filtering**: Filter holidays by type (`public`, `christian`, `muslim`, etc.)
* 📆 **Date Arithmetic**: Add/subtract days, months, years (13-month calendar support)
* 🔠 **Localized Formatting**: Amharic and English support
* 🔢 **Geez Numerals**: Convert integers to ግዕዝ numeral strings
* ⏰ **Ethiopian Time Support**: 12-hour Ethiopian ↔ 24-hour Gregorian
* 🗓️ **Calendar Grids**: Monthly/yearly calendar generation

---

## 🚀 Installation

Install the library from source:

```bash
pip install kenat
```

For development/testing:

```bash
pip install -e ".[test]"
```

---

## 🟢 Quick Start

```python
from kenat import Kenat

today = Kenat.now()

print(today.get_ethiopian())
# → {'year': 2017, 'month': 9, 'day': 26}

print(today.format({'lang': 'english', 'show_weekday': True}))
# → "Tuesday, Ginbot 26 2017"
```

---

## ⛪ Bahire Hasab & Holiday System

### Get All Holidays in a Year

```python
from kenat import get_holidays_for_year

holidays = get_holidays_for_year(2017)

# Example: Find Fasika (Easter)
fasika = next(h for h in holidays if h['key'] == 'fasika')
print(fasika['ethiopian'])  # → {'year': 2017, 'month': 8, 'day': 21}
```

### Filter Holidays by Type

```python
from kenat import get_holidays_for_year, HolidayTags

# Public only
get_holidays_for_year(2017, filter_by=HolidayTags.PUBLIC)

# Christian and Muslim holidays
get_holidays_for_year(2017, filter_by=[HolidayTags.CHRISTIAN, HolidayTags.MUSLIM])
```

### Check if a Date is a Holiday

```python
from kenat import Kenat

meskel = Kenat("2017/1/17")
print(meskel.is_holiday())  # → [Holiday object]

non_holiday = Kenat("2017/1/18")
print(non_holiday.is_holiday())  # → []
```

### Access Bahire Hasab Calculations

```python
from kenat import Kenat

bh = Kenat("2017/1/1").get_bahire_hasab()

print(bh['evangelist'])  # → {'name': 'ማቴዎስ', 'remainder': 1}
print(bh['movableFeasts']['fasika']['ethiopian'])
# → {'year': 2017, 'month': 8, 'day': 21}
```

---

## ➕ More API Examples

### Date Arithmetic

```python
from kenat import Kenat

date = Kenat("2017/2/10")
print(date.add(days=10))     # → Add days
print(date.add(months=-1))   # → Subtract a month
```

### Date Difference

```python
from kenat import Kenat

a = Kenat("2015/5/15")
b = Kenat("2012/5/15")

print((a - b).days)         # → 1095 days
print(a.diff_in_days(b))    # → 1095
```

### Geez Numerals

```python
from kenat import to_geez

print(to_geez(2017))  # → ፳፻፲፯
```

---

## 🧱 Contributing

1. Fork & clone the repo
2. Create a new branch: `git checkout -b feature/your-feature`
3. Make your changes, add tests in `/tests/`
4. Run `pytest` to ensure everything passes
5. Submit a pull request 🚀

---

## 👨‍💻 Author

**Melaku Demeke**
GitHub: [@melakud](https://github.com/melakud)

---

## 📄 License

**MIT License** — see [LICENSE](./LICENSE) for details.

---

Let me know if you want to:

* add badges (PyPI, license, tests)
* include an animated GIF demo (e.g. calendar grid or console output)
* or generate this as a `README.md` file automatically.
