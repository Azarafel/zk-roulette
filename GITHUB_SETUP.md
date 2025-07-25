# 🎰 ZK-Roulette - GitHub Setup Guide

## 🚀 Быстрый запуск

### 1. Клонирование и установка

```bash
git clone https://github.com/Azarafel/zk-roulette.git
cd zk-roulette
```

### 2. Backend (Python FastAPI)

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements_v2_light.txt
python test_zk_system.py  # Тесты
python main_v2.py         # Запуск сервера
```

### 3. Frontend (React)

```bash
cd frontend
npm install
npm start
```

### 4. Доступ

- **API:** http://localhost:8000
- **Docs:** http://localhost:8000/docs
- **UI:** http://localhost:3000

## 🔥 Особенности

- **🔒 Zero-Knowledge Proof** - Математически доказуемая честность
- **🤖 ИИ-анализ** - Байесовская детекция мошенничества
- **⚡ Real-time** - Мгновенная аналитика
- **🛡️ Безопасность** - Многоуровневая защита

## 📁 Структура

```
backend/          # Python FastAPI + ZK система
frontend/         # React + 3D рулетка  
contracts/        # Solidity смарт-контракты
```

## 🧪 Тестирование

```bash
cd backend
python test_zk_system.py
```

## 🔧 Конфигурация

Создайте `.env` файл в папке backend:

```env
DEBUG=True
PORT=8000
SECRET_KEY=your-secret-key
```

**Готово к запуску! 🎉**
