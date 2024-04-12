git config --global user.name "Ваше имя"
git config --global user.email "ваш-email@example.com"
Инициализация локального репозитория Git:
Откройте терминал, перейдите в директорию вашего проекта и выполните:

csharp
Copy code
git init
git add .
git commit -m "Initial commit"
Добавление удаленного репозитория:

csharp
Copy code
git remote add origin URL_вашего_репозитория
Push вашего проекта:

perl
Copy code
git push -u origin master