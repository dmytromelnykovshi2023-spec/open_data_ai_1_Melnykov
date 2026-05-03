# Open Data AI Analytics - DevOps & Infrastructure

## Архітектура та Інфраструктура
Цей проєкт налаштований для розгортання в хмарі Azure з використанням Kubernetes (K3s). 
Локальна розробка на ARM64 (macOS/M1) підтримується завдяки використанню крос-компіляції у Docker (`platform: linux/amd64`).

## Інструкція із запуску системи

### Локально через Docker Compose
1. Переконайтесь, що Docker Desktop запущено.
2. В корені проєкту запустіть:
   ```bash
   docker compose up --build
   ```
   Усі образи зберуться для архітектури `linux/amd64` незалежно від вашої машини, імітуючи продакшн-середовище.
3. Веб-інтерфейс буде доступний на порту `5001`.

### Через Kubernetes (k3s)
Застосунок упаковано у формат K8s маніфестів (папка `k8s/`). 
Логіка конвеєра реалізована через `initContainers` у файлі `app.yaml`.
Всі сервіси (`data_load`, `data_quality_analysis`, `data_research`, `visualization`) виконуються послідовно перед стартом веб-сервера.

## Моніторинг (Prometheus + Grafana)
Моніторинг розгортається у неймспейсі `monitoring` через файл `k8s/monitoring.yaml`.
- **Prometheus** автоматично збирає метрики з подів, які мають анотацію `prometheus.io/scrape: "true"`.
- **Grafana** підключена для візуалізації метрик.

### Доступ до інтерфейсів:
- **Web App:** `<VM-IP>:30001` (NodePort K8s) або локально на `5001`
- **Grafana:** `<VM-IP>:30000` (NodePort K8s). Логін: `admin`, пароль: `admin`
- **Prometheus:** `<VM-IP>:30090` (NodePort K8s)
- **SSH / K8s API:** 22, 6443

### Як додати дашборди у Grafana:
1. Зайдіть у Grafana за адресою `http://<VM-IP>:30000`
2. Перейдіть у **Connections -> Data Sources** і додайте Prometheus з URL `http://prometheus.monitoring.svc:9090`
3. У розділі **Dashboards** ви можете імпортувати стандартні шаблони (наприклад, ID: `315` для Kubernetes).
