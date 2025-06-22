# Быстрый коммит в GitHub

## Проблема: PowerShell завис из-за emoji

## Решение: Команды по шагам

### Шаг 1: Открой новый терминал
- Нажми Win+R
- Введи: cmd
- Нажми Enter

### Шаг 2: Перейди в папку проекта
```
cd C:\Users\sserg\blockchain_roulette
```

### Шаг 3: Настрой Git (если нужно)
```
git init
git remote add origin https://github.com/Azarafel/zk-roulette.git
```

### Шаг 4: Синхронизируйся с GitHub
```
git pull origin master
```

### Шаг 5: Добавь новые файлы
```
git add .
```

### Шаг 6: Сделай коммит
```
git commit -m "Add DEMO roulette server and documentation"
```

### Шаг 7: Отправь на GitHub
```
git push origin master
```

## Если нужна авторизация:
- Используй GitHub username и Personal Access Token
- Создай token: GitHub → Settings → Developer settings → Personal access tokens

## Готово!
После успешного push твой код будет на GitHub: https://github.com/Azarafel/zk-roulette 