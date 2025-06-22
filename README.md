# �� ZK-Roulette v2.0

**Zero-Knowledge Blockchain Roulette с Polygon интеграцией и байесовской аналитикой**

![Demo Status](https://img.shields.io/badge/Status-DEMO%20Ready-brightgreen)
![Blockchain](https://img.shields.io/badge/Blockchain-Polygon-8247E5)
![Python](https://img.shields.io/badge/Python-3.11+-blue)

## 🚀 Быстрый старт

### 🎮 DEMO версия (готова к игре!)

```bash
# Клонируй репозиторий
git clone https://github.com/your-username/zk-roulette.git
cd zk-roulette/backend

# Активируй виртуальное окружение  
.\venv\Scripts\Activate.ps1

# Запусти демо сервер
python roulette_server.py
```

**🌐 Открой http://localhost:8000 и играй!**

### ⚙️ Полная версия (в разработке)

1. **Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements_v2_light.txt
python main_v2.py
```

2. **Frontend:**
```bash
cd frontend
npm install
npm start
```

## 🔥 Особенности

### ✅ DEMO (готово):
- 🎰 **Рулетка с анимацией** - Красивое колесо с плавным вращением
- 💰 **Система ставок** - Ставки на числа 0-36 с выплатами 35:1
- 📊 **Live статистика** - Баланс, выигрыши, статистика в реальном времени
- 🎨 **Современный UI** - Адаптивный дизайн с градиентами
- 🚀 **FastAPI сервер** - Готовый к продакшену API

### 🔄 В разработке:
- 🔒 **Zero-Knowledge Proof** - Математически доказуемая честность
- 💎 **MetaMask интеграция** - Подключение кошельков
- 📜 **Polygon смарт-контракты** - Реальные MATIC ставки
- 🤖 **Байесовская аналитика** - ИИ-анализ паттернов игры

## 📁 Структура проекта

```
zk-roulette/
├── backend/
│   ├── roulette_server.py     # 🎰 DEMO сервер (ГОТОВ!)
│   ├── main_v2.py             # 🔧 Основной сервер
│   ├── zk_system.py           # 🔐 ZK-proof система
│   ├── bayesian_analyzer.py   # 📊 Байесовская аналитика
│   └── .env                   # 🔑 Polygon настройки
├── frontend/                   # React UI (в разработке)
├── contracts/                  # Solidity контракты
└── scripts/                    # Deployment утилиты
```

## 🎮 Как играть

1. **💰 Сделай ставку**: Введи число (0-36) и сумму
2. **🎲 Крути колесо**: Нажми красную кнопку
3. **🎉 Получай выигрыш**: x35 за точное попадание!
4. **📈 Следи за статистикой**: Баланс обновляется в реальном времени

## 🛣️ Roadmap

### Phase 1: DEMO ✅ 
- [x] Рулетка с анимацией
- [x] Система ставок 35:1
- [x] FastAPI сервер
- [x] Красивый UI

### Phase 2: Blockchain 🔄
- [ ] MetaMask подключение  
- [ ] Polygon смарт-контракт
- [ ] Реальные MATIC ставки
- [ ] React фронтенд

### Phase 3: ZK-Proof 📋
- [ ] Circom схемы честности
- [ ] Zero-Knowledge валидация
- [ ] Публичная верификация

### Phase 4: Advanced 🚀
- [ ] Байесовская аналитика
- [ ] Турниры и бонусы
- [ ] Mobile app
- [ ] DAO управление

## 🔧 Технический стек

- **FastAPI** - веб-фреймворк
- **Uvicorn** - ASGI сервер  
- **Web3.py** - блокчейн интеграция
- **Polygon** - Layer 2 для Ethereum
- **React** - фронтенд (планируется)
- **Solidity** - смарт-контракты (планируется)

## 💡 Экономическая модель

- 🎯 **Ставки**: 0.1-1000 MATIC (демо: виртуальные монеты)
- 💰 **Выплаты**: 35:1 за точное попадание  
- 🏠 **House Edge**: 2.7% (европейская рулетка)
- 📈 **Проекции**: $10-10,800/день при запуске

## 📖 Документация

- [DEVELOPMENT_README.md](DEVELOPMENT_README.md) - Техническая документация
- [GITHUB_SETUP.md](GITHUB_SETUP.md) - Развертывание на GitHub
- [API Docs](http://localhost:8000/docs) - FastAPI документация

## 🎯 Статус: DEMO ГОТОВО! 🚀

**Попробуй демо прямо сейчас:** `python roulette_server.py` 