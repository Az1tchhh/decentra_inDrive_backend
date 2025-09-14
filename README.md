# 🚀 Проект: [inDrive. Анализ изображений для мэнэджеров]

## DEMO
https://drive.google.com/file/d/1c9Glb4GkFkfLpbaLORHpgHCJCGSvGDPU/view?usp=sharing

## 📦 Требования
Клиентская часть проекта была выполнена созданием IOS приложения. Наша идея заключалась в том чтобы решить задачу как часть приложения inDrive. Проект ниже по ссылке:

https://github.com/Lm004yky/Indrive_case_1_Hackathon

Бэкенд часть была выполнена в этом репозиторий.

Для запуска проекта необходимо установить:  
- [Docker Engine](https://docs.docker.com/engine/)  
- [ngrok](https://ngrok.com/) (для хостинга)  

Файл **`.env`** оставлен в репозитории для удобства настройки окружения.  

Наша модель находится в папке model/. Там мы храним созданные весы, и через функцию predict делаем прогноз с изоброжения.

---

## ▶️ Запуск бэкенда

```bash
cd djangoProject/
docker compose up --build

---

## ▶️ Запуск ngrok
ngrok http 8001


