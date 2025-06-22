# 📚 Загрузка ZK-Roulette на GitHub

## 🚀 Пошаговая инструкция

### 1. Инициализация Git репозитория

```bash
# Перейди в папку проекта
cd C:\Users\sserg\blockchain_roulette

# Инициализируй Git
git init

# Добавь все файлы (кроме .gitignore)
git add .

# Сделай первый коммит
git commit -m "🎰 Initial commit: ZK-Roulette DEMO готово"
```

### 2. Создание репозитория на GitHub

1. **Открой GitHub**: https://github.com
2. **Нажми "New repository"**  
3. **Название**: `zk-roulette`
4. **Описание**: `Zero-Knowledge Blockchain Roulette с Polygon интеграцией`
5. **Приватность**: Public (чтобы делиться с друзьями)
6. **НЕ добавляй** README.md (у нас уже есть)
7. **Нажми "Create repository"**

### 3. Подключение к GitHub

```bash
# Добавь remote origin (замени YOUR_USERNAME на свой GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/zk-roulette.git

# Проверь что remote добавился
git remote -v

# Отправь код на GitHub
git push -u origin main
```

### 4. Настройка репозитория

После загрузки на GitHub:

1. **Перейди в Settings** → **Pages**
2. **Включи GitHub Pages** (если хочешь хостинг)
3. **Добавь Topics** в About: `blockchain`, `roulette`, `zero-knowledge`, `polygon`, `fastapi`
4. **Добавь описание**: "🎰 Zero-Knowledge Blockchain Roulette"

## 📋 Checklist готовности

- [ ] Git инициализирован
- [ ] Все файлы добавлены
- [ ] Первый коммит сделан  
- [ ] GitHub репозиторий создан
- [ ] Remote origin добавлен
- [ ] Код загружен на GitHub
- [ ] README.md отображается корректно
- [ ] Проект публичный и доступен

## 🔗 Полезные команды

```bash
# Проверить статус Git
git status

# Посмотреть коммиты
git log --oneline

# Проверить remote
git remote -v

# Обновить README
git add README.md
git commit -m "📝 Update README"
git push
```

## 🎯 После загрузки

### Поделись с друзьями:
- **Ссылка на репозиторий**: https://github.com/YOUR_USERNAME/zk-roulette
- **Инструкция запуска**: `git clone` → `cd backend` → `python roulette_server.py`
- **Демо доступно на**: http://localhost:8000

### Следующие шаги:
1. **MetaMask интеграция** 
2. **Polygon смарт-контракт**
3. **React фронтенд**
4. **Production деплой**

## 🛠️ Troubleshooting

### Проблема: "repository not found"
```bash
# Проверь правильность username
git remote set-url origin https://github.com/YOUR_CORRECT_USERNAME/zk-roulette.git
```

### Проблема: "permission denied"
```bash
# Используй personal access token вместо пароля
# Settings → Developer settings → Personal access tokens
```

### Проблема: ".env файл в публичном репозитории"
```bash
# Удали .env из репозитория
git rm --cached backend/.env
git commit -m "🔒 Remove .env from tracking"
git push
```

---

**🎉 Готово! Твой ZK-Roulette теперь на GitHub!** 