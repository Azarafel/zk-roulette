# 🎰 ZK-Roulette Development Version

## 📋 Статус разработки

✅ **Backend (Python/FastAPI)** - Работает  
✅ **Frontend (React)** - Работает  
⚠️ **Блокчейн интеграция** - В разработке  

## 🚀 Быстрый запуск

### Вариант 1: PowerShell скрипты (рекомендуется)

```powershell
# Запуск Backend (в первом терминале)
.\start_backend.ps1

# Запуск Frontend (во втором терминале)  
.\start_frontend.ps1
```

### Вариант 2: Ручной запуск

#### Backend (порт 8000)
```powershell
cd backend
venv\Scripts\activate
python main_v2.py
```

#### Frontend (порт 3000)
```powershell
cd frontend
npm start
```

## 🔗 URL'ы

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

## 🛠️ Установка зависимостей

### Backend
```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements_v2_light.txt
```

### Frontend
```powershell
cd frontend
npm install
```

## 🔧 Возможности текущей версии

### Backend API
- ✅ ZK-proof система (базовая)
- ✅ Байесовский анализатор мошенничества
- ✅ Rate limiting и безопасность
- ✅ Swagger документация
- ⚠️ Web3 подключение (mock данные)

### Frontend
- ✅ Современный React интерфейс
- ✅ Проверка статуса backend
- ✅ Тестирование API
- ✅ Responsive дизайн
- ⚠️ Полная интеграция с блокчейном

## 🐛 Известные ограничения

1. **Web3 Warning:** Backend показывает ошибки Web3 - это нормально, т.к. блокчейн не подключен
2. **Mock данные:** ZK-proofs генерируются локально без реального блокчейна
3. **Pydantic Warning:** Используется deprecated validator - не критично

## 🔄 Следующие шаги

1. **Интеграция с Ethereum/Polygon**
2. **Подключение к MetaMask**
3. **Развертывание смарт-контрактов**
4. **Полноценная 3D рулетка**
5. **Real-time мультиплеер**

## 📊 Тестирование

### API тесты
```bash
# Проверка здоровья
curl http://localhost:8000/health

# Тест подготовки ставки
curl -X POST http://localhost:8000/bet/prepare \
  -H "Content-Type: application/json" \
  -d '{"number": 7, "amount": 0.1, "player_address": "0x1234567890123456789012345678901234567890"}'
```

### Frontend тесты
- Откройте http://localhost:3000
- Нажмите "Обновить статус" - должно показать зеленый статус
- Нажмите "Тест ставки" - должно сгенерировать ZK-proof

## 🌟 Особенности архитектуры

- **Zero-Knowledge Proofs** - Приватность ставок
- **Байесовская статистика** - ИИ-анализ подозрительной активности  
- **FastAPI + React** - Современный tech stack
- **Модульная архитектура** - Легко расширяемая

---

**🔗 GitHub:** https://github.com/Azarafel/zk-roulette/tree/development-version 