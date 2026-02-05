# Sprint_7 — API tests (Yandex Scooter)

## Установка
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Запуск тестов
```bash
pytest
```

## Allure
1) Запуск тестов с генерацией результатов:
```bash
pytest --alluredir=target/allure-results
```

2) Сгенерировать HTML-отчёт локально:
```bash
allure generate target/allure-results -o target/allure-report --clean
allure open target/allure-report
```
