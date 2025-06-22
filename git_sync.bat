@echo off
echo Подключаемся к существующему GitHub репозиторию...

REM Инициализируем Git если не инициализирован
git init

REM Добавляем remote origin
git remote remove origin 2>nul
git remote add origin https://github.com/Azarafel/zk-roulette.git

REM Проверяем remote
git remote -v

REM Получаем последние изменения
git pull origin master

REM Добавляем все новые файлы
git add .

REM Делаем коммит с описанием DEMO
git commit -m "Add DEMO roulette server and updated documentation"

REM Отправляем на GitHub
git push origin master

echo Готово! Проект синхронизирован с GitHub.
pause 