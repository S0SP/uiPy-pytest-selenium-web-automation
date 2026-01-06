# pytest-selenium-web-automation

> **Production-grade Selenium UI test automation framework built with Python, Pytest & Page Object Model**
> — Login · Inventory · Cart · Full E2E Checkout · Screenshot-on-failure · CI/CD

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![Pytest](https://img.shields.io/badge/Pytest-8.1-green)](https://pytest.org)
[![Selenium](https://img.shields.io/badge/Selenium-4.20-orange)](https://selenium.dev)
[![CI](https://github.com/S0SP/uiPy-pytest-selenium-web-automation/actions/workflows/test.yml/badge.svg)](https://github.com/S0SP/uiPy-pytest-selenium-web-automation/actions)

---

## 📌 Project Overview

End-to-end UI test automation framework targeting **[SauceDemo](https://www.saucedemo.com/)** — the industry-standard demo e-commerce site used for automation practice — built using patterns from real enterprise QA teams:

- **Page Object Model (POM)** — zero Selenium code inside test files, all selectors live in page classes
- **Auto-screenshot on failure** — every failed test saves a timestamped screenshot, embedded in the HTML report
- **Headless execution** — runs in CI/CD with no display server required
- **Cross-browser** — Chrome and Firefox via `webdriver-manager` (no manual driver downloads)
- **Parallel execution** — `pytest-xdist` cuts suite runtime by running tests concurrently
- **Full E2E coverage** — Login → Add to cart → Checkout → Order confirmation

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.11 |
| Test Runner | Pytest 8.1 |
| Browser Automation | Selenium 4.20 |
| Driver Management | webdriver-manager 4.0 |
| Design Pattern | Page Object Model (POM) |
| Reporting | pytest-html 4.1 |
| Parallel Execution | pytest-xdist |
| CI/CD | GitHub Actions |
| Env Management | python-dotenv |

---

## 📂 Folder Structure

```
pytest-selenium-web-automation/
├── tests/
│   ├── test_login.py           # Login: valid, invalid, locked, logout
│   ├── test_inventory.py       # Product listing, sorting, add-to-cart
│   └── test_cart_checkout.py   # Cart management + full E2E checkout
├── pages/
│   ├── base_page.py            # BasePage: all Selenium helpers, explicit waits
│   ├── login_page.py           # Login page actions + locators
│   ├── inventory_page.py       # Products page actions + locators
│   ├── cart_page.py            # Cart page actions + locators
│   └── checkout_page.py        # Checkout step 1, 2, confirmation
├── utils/
│   ├── driver_factory.py       # Chrome/Firefox driver setup with headless support
│   ├── screenshot.py           # Screenshot capture utility
│   └── logger.py               # File + console logging
├── config/
│   └── settings.py             # Env-var-driven config
├── reports/                    # Auto-generated HTML report + screenshots
├── .github/
│   └── workflows/
│       └── test.yml            # GitHub Actions CI pipeline
├── conftest.py                 # Driver fixture, auto-screenshot hook
├── pytest.ini                  # Markers, HTML report path, log config
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## ⚡ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/S0SP/uiPy-pytest-selenium-web-automation.git
cd uiPy-pytest-selenium-web-automation
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
# No changes needed — works against saucedemo.com out of the box
```

> **Chrome/Firefox** is auto-downloaded by `webdriver-manager` on first run.

---

## ▶️ Running Tests

### Run all tests (headless Chrome)
```bash
pytest
```

### Run smoke tests only
```bash
pytest -m smoke -v
```

### Run specific test file
```bash
pytest tests/test_login.py -v
pytest tests/test_cart_checkout.py -v
```

### Run with Firefox
```bash
pytest --browser=firefox
```

### Run in headed mode (visible browser)
```bash
pytest --headless=false
```

### Run in parallel (4 workers)
```bash
pytest -n 4
```

### Run with HTML report
```bash
pytest --html=reports/report.html --self-contained-html
```

---

## 📊 Sample Output

```
tests/test_login.py::TestLogin::test_valid_login_redirects_to_inventory PASSED
tests/test_login.py::TestLogin::test_invalid_password_shows_error PASSED
tests/test_login.py::TestLogin::test_locked_user_shows_error PASSED
tests/test_login.py::TestLogin::test_logout_returns_to_login PASSED
tests/test_inventory.py::TestInventory::test_inventory_shows_six_products PASSED
tests/test_inventory.py::TestInventory::test_add_single_product_updates_cart_badge PASSED
tests/test_inventory.py::TestInventory::test_sort_products_by_name_a_to_z PASSED
tests/test_cart_checkout.py::TestCartAndCheckout::test_full_checkout_flow_completes_successfully PASSED
tests/test_cart_checkout.py::TestCartAndCheckout::test_each_product_can_be_added_to_cart[...] PASSED

====== 18 passed in 42.7s ======
```

On test failure, a screenshot is automatically saved to `reports/screenshots/` and embedded into `reports/report.html`.

---

## 🔁 CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/test.yml`) automatically:

1. Triggers on push to `main`/`develop`, PRs, and daily at 7 AM UTC
2. Installs Google Chrome on the Ubuntu runner
3. Runs smoke tests first — fast feedback gate
4. Runs full suite with headless Chrome
5. Uploads HTML report + screenshots as artifacts (retained 14 days)

---

## 🏗️ Architecture Decisions

| Decision | Why it matters |
|---|---|
| **Page Object Model** | Locator changes require edits in ONE place only |
| `BasePage` superclass | All pages inherit waits/click/type — DRY principle |
| `DriverFactory` | Swap browsers via CLI flag — no code changes |
| Auto-screenshot hook | Failure evidence captured without any test code |
| `autouse` login fixture | No repeated login boilerplate in every test |
| Parametrized cart tests | Multiple products tested from one function |
| `.env` config | Works locally and in CI with zero hardcoding |

---

## 🌍 Why This Matters

UI automation breaks when developers rename selectors, change page flows, or restructure layouts. A strong framework accounts for this by:

- Isolating all locators in page classes — **one change, all tests fixed**
- Using **explicit waits** instead of `time.sleep` — tests don't flake on slow loads
- Capturing **failure screenshots** — QA team immediately sees what broke and where
- Running in **CI on every push** — regressions caught before they merge

This mirrors how QA automation works in production engineering teams.

---

*Built to demonstrate production-quality Selenium + Pytest automation engineering.*
