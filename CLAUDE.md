# CLAUDE.md

Этот файл — быстрый брифинг для агента. Прочитай его перед любой правкой кода.

## Что это

Agent Skill + Python CLI `1c-batch` для пакетных операций с 1С:Предприятие 8 (выгрузка/загрузка XML, .cf/.cfe, .epf/.erf, .dt, проверки, сравнения и т.д.).

Это Python-порт PowerShell-проекта https://github.com/vladimir-kharin/1c-batch. На входе у `1cv8`, кроссплатформенно (Linux/macOS/Windows).

## Раскладка

```
/                            ← корень репо
├── src/1c-batch/             ← навык (skill), копируется в .claude/skills/
│   ├── SKILL.md              ← фронтматтер + документация команд
│   ├── assets/               ← пример .1c-devbase.json
│   └── scripts/              ← Python-пакет (он же — install-source)
│       ├── pyproject.toml    ← name="1c-batch", package_dir: onec_batch="."
│       ├── __init__.py       ← __version__ через importlib.metadata
│       ├── cli.py            ← click-команды (entry point: onec_batch.cli:cli)
│       ├── runner.py         ← запуск 1cv8 (subprocess), логирование
│       └── config.py         ← парсер .1c-devbase.json, автоопределение платформы
├── docs/                     ← аналитика, план (не публикуется)
├── tasks/                    ← журнал задач (не публикуется)
├── tests/                    ← фикстуры .cf/.cfe для интеграционных проверок
└── .1c-devbase.json          ← локальная конфигурация (в .gitignore)
```

Пакет ставится как `onec_batch` (исторически), CLI-команда — `1c-batch`.

## Установка / переустановка

Однократно:
```bash
pip install --user -e src/1c-batch/scripts
```

`-e` — editable: правки в `src/1c-batch/scripts/` подхватываются без переустановки. Никаких build/ артефактов или дубликатов `onec_batch/` в корне быть не должно.

Минимум: `pip >= 21.3`, `setuptools >= 77`, `wheel >= 0.40`. Со старым setuptools пакет соберётся как `UNKNOWN-0.0.0` (PEP 621 не парсится).

## Тесты

```bash
pip install --user -e 'src/1c-batch/scripts[dev]'
cd src/1c-batch/scripts && pytest
```

Юнит-тесты лежат в `src/1c-batch/scripts/tests/`. Корневой `/tests` — это 1С-фикстуры, не pytest (gitignored).

## Конвенции

**`subprocess.run` всегда вызывается со списком и без `shell=True`.** Значения в argv передаются **без литеральных кавычек** — квотинг делает ОС (`execvp` на POSIX, `list2cmdline` на Windows). Кавычки нужны только при выводе пользователю — для этого есть `shlex.join` в `runner._echo_command`.

Не возвращайся к старому формату `f"/S{value}"` (concat) или `f'"{value}"'` (литеральные кавычки в argv) — оба ломают передачу значений в `1cv8`. Правильно:

```python
return ["/S", f"{cfg.server}/{cfg.base}"]  # два argv-элемента
```

Исключение — `CREATEINFOBASE`, где сам синтаксис 1С требует одного argv-элемента вида `File="path"`. Это реализовано в `runner.run_create_infobase`.

## Конфигурация

`.1c-devbase.json` ищется от cwd вверх (`config._find_config_file`). Поэтому `1c-batch` нужно запускать из каталога проекта 1С, а не откуда угодно.

Поля: `platform_path`, `connection.{type=file|server, path|server, base}`, `user`, `password`, `cf_dir`, `cfe_dir`, `log_dir`. Пароль в plaintext — не commit'ить.

## Что НЕ делать

- Не создавать `onec_batch/` в корне репо (это был старый layout, теперь shadow-импорт). Если случайно появился — удалить.
- Не править `build/` — это вывод `setup.py build`, сейчас не используется.
- Не править `src/1c-batch/scripts/__pycache__/`.
- Не коммитить `.1c-devbase.json` — там пароль.
