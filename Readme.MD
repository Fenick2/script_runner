Сервис на FastAPI, согласно ТЗ.

Настройки путей ко скриптам находятся в файле config.py.

ПРИМЕР:

- Требуется изменить папку со скриптами с "/gtm/management/" на "/other/management":
  1. Открыть config.py текстовым редактором.
  2. В строке с текстом ROOT_PATH= Path(ROOT/'gtm'/'management')ROOT_PATH= Path(ROOT/'gtm'/'management') заменить 'gtm' на 'other'.
  3. Сохранить.

Переменная USER_PATH создана для возможного перехода работы программы с файлами в домашней папке с правами User.
