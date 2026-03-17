---
name: 1c-batch
description: "Пакетные операции с платформой 1С:Предприятие 8. Выгрузка/загрузка конфигураций и расширений в XML, сборка/разборка внешних обработок (.epf/.erf), выгрузка/загрузка ИБ, создание баз, проверка конфигурации, объединение/сравнение конфигураций, работа со свойствами конфигурации. Используй когда нужно: работать с конфигурацией или расширениями 1С, собрать или разобрать обработку/отчёт, выгрузить или загрузить ИБ, запустить 1С:Предприятие или конфигуратор."
---

# 1c-batch

Кроссплатформенный Python-инструмент для пакетных операций с платформой 1С:Предприятие 8.

## Запуск

Команда `1c-batch` устанавливается через pip. Запускать **из корня проекта** (где лежит `.1c-devbase.json`):

```bash
1c-batch <команда> [аргументы] [опции]
```

---

## Работа с обработками (EPF/ERF)

### dump-epf — разборка обработки в XML

```bash
1c-batch dump-epf <XML_DIR> <EPF_FILE> [--format Plain|Hierarchical]
```

- `XML_DIR` — каталог для выгрузки XML
- `EPF_FILE` — путь к исходной обработке `.epf` или `.erf`
- `--format` — формат выгрузки (Plain или Hierarchical)

### build-epf — сборка обработки из XML

```bash
1c-batch build-epf <XML_DIR> <EPF_FILE>
```

- `XML_DIR` — каталог с XML-исходниками
- `EPF_FILE` — путь к результирующему файлу `.epf` или `.erf`

---

## Работа с конфигурацией

### dump-config — выгрузка конфигурации в XML

```bash
1c-batch dump-config <DIRECTORY> [--update] [--extension ИМЯ] [--all-extensions] [--format Plain|Hierarchical]
```

- `DIRECTORY` — каталог для выгрузки
- `--update` — инкрементальная выгрузка (только изменения, с -force)
- `--extension` — выгрузить конкретное расширение
- `--all-extensions` — выгрузить все расширения
- `--format` — формат выгрузки

### load-config — загрузка конфигурации из XML

```bash
1c-batch load-config <DIRECTORY> [--files СПИСОК] [--list-file ФАЙЛ] [--format Plain|Hierarchical] [--partial] [--extension ИМЯ] [--skip-db-update]
```

- `DIRECTORY` — каталог с XML-файлами
- `--files` — список файлов через запятую для частичной загрузки
- `--list-file` — путь к файлу-списку
- `--format` — формат (Plain или Hierarchical)
- `--partial` — частичная загрузка
- `--extension` — загрузить в расширение
- `--skip-db-update` — не обновлять конфигурацию БД (по умолчанию обновляется)

Примеры:
```bash
# Полная загрузка
1c-batch load-config src/cf

# Частичная загрузка одного модуля
1c-batch load-config src/cf --files "CommonModules/МойМодуль/Ext/Module.bsl"

# Загрузка без обновления БД
1c-batch load-config src/cf --skip-db-update
```

### dump-cfg — сохранение конфигурации в .cf

```bash
1c-batch dump-cfg <FILEPATH> [--extension ИМЯ]
```

### load-cfg — загрузка конфигурации из .cf

```bash
1c-batch load-cfg <FILEPATH> [--extension ИМЯ]
```

### update-db-cfg — обновление конфигурации БД

```bash
1c-batch update-db-cfg [--dynamic +|-] [--server] [--extension ИМЯ]
```

---

## Работа с расширениями

### dump-extension — выгрузка расширения в XML

```bash
1c-batch dump-extension <DIRECTORY> --name ИМЯ [--update] [--format Plain|Hierarchical]
```

### load-extension — загрузка расширения из XML

```bash
1c-batch load-extension <DIRECTORY> --name ИМЯ [--skip-db-update]
```

По умолчанию после загрузки выполняется обновление расширения в БД.

### dump-cfg-extension — сохранение расширения в .cfe

```bash
1c-batch dump-cfg-extension <FILEPATH> --name ИМЯ
```

### load-cfg-extension — загрузка расширения из .cfe

```bash
1c-batch load-cfg-extension <FILEPATH> --name ИМЯ
```

### delete-extension — удаление расширения

```bash
1c-batch delete-extension --name ИМЯ
1c-batch delete-extension --all
```

### list-extensions — список расширений

```bash
1c-batch list-extensions
```

---

## Запуск 1С

### run-enterprise — запуск предприятия

```bash
1c-batch run-enterprise [EPF_FILE]
```

- `EPF_FILE` — обработка для автозапуска (опционально)

### run-designer — запуск конфигуратора

```bash
1c-batch run-designer
```

---

## База данных

### dump-ib — выгрузка ИБ в .dt

```bash
1c-batch dump-ib <FILEPATH>
```

### restore-ib — загрузка ИБ из .dt

```bash
1c-batch restore-ib <FILEPATH> [--jobs-count N]
```

### create-infobase — создание информационной базы

```bash
1c-batch create-infobase --path /путь/к/базе [--add-to-list ИМЯ] [--use-template ШАБЛОН]
```

### ib-restore-integrity — восстановление структуры ИБ

```bash
1c-batch ib-restore-integrity
```

### ib-check-and-repair — тестирование и исправление ИБ

```bash
1c-batch ib-check-and-repair [--reindex] [--log-integrity] [--recalc-totals] [--ib-compression] [--rebuild]
```

---

## Проверки

### check-config — проверка конфигурации

```bash
1c-batch check-config [--config-log-integrity] [--incorrect-references] [--thin-client] [--server] [--extension ИМЯ] [--all-extensions]
```

### check-modules — проверка модулей

```bash
1c-batch check-modules [--thin-client] [--server] [--extension ИМЯ] [--all-extensions]
```

---

## Сравнение и объединение

### merge-cfg — объединение конфигураций

```bash
1c-batch merge-cfg <FILEPATH> [--settings ФАЙЛ_НАСТРОЕК] [--force]
```

### compare-cfg — сравнение конфигураций

```bash
1c-batch compare-cfg --first-type ТИП --second-type ТИП [--report-format ФОРМАТ] [--report-file ФАЙЛ]
```

---

## Свойства конфигурации

### dump-config-files — выгрузка свойств

```bash
1c-batch dump-config-files <DIRECTORY> [--module] [--template] [--help-flag] [--all-writable] [--picture] [--right] [--extension ИМЯ]
```

### load-config-files — загрузка свойств

```bash
1c-batch load-config-files <DIRECTORY> [--module] [--template] [--help-flag] [--all-writable] [--picture] [--right] [--extension ИМЯ]
```

---

## Обслуживание

### reduce-event-log — сокращение журнала регистрации

```bash
1c-batch reduce-event-log <ДАТА>
```

- `ДАТА` — дата в формате YYYYMMDD

---

## Сценарии использования

### Исправить ошибку в обработке

1. Разобрать: `1c-batch dump-epf src/epf/МояОбработка.xml Исходная.epf`
2. Отредактировать BSL-файлы в `src/epf/МояОбработка/`
3. Собрать: `1c-batch build-epf src/epf/МояОбработка.xml build/МояОбработка.epf`
4. Проверить: `1c-batch run-enterprise build/МояОбработка.epf`

### Загрузка изменённого модуля

```bash
1c-batch load-config src/cf --files "CommonModules/МойМодуль/Ext/Module.bsl"
```

### Обновить расширение

1. Выгрузить: `1c-batch dump-extension src/cfe/МоёРасширение --name МоёРасширение`
2. Внести изменения в XML-файлы
3. Загрузить: `1c-batch load-extension src/cfe/МоёРасширение --name МоёРасширение`

### Выгрузка/загрузка ИБ (резервная копия)

1. Выгрузить: `1c-batch dump-ib backup.dt`
2. Загрузить: `1c-batch restore-ib backup.dt`

### Сохранение конфигурации в .cf

```bash
1c-batch dump-cfg backup.cf
1c-batch load-cfg backup.cf
```

---

## Правила использования

**При выгрузке конфигурации или расширения:** если пользователь явно не указал тип выгрузки (полная или инкрементальная), спросить его перед выполнением:
- Полная выгрузка — выгружает все объекты заново
- Инкрементальная (`--update`) — выгружает только изменённые объекты (быстрее)

---

## Важно

- **Обработки:** первый аргумент — XML-каталог, второй — файл .epf/.erf
- **Конфигурация/расширения:** первый аргумент — каталог
- При ошибке — ненулевой код возврата
- Логи сохраняются в каталоге `logs/`
- Конфигурация подключения — в файле `.1c-devbase.json` в корне проекта
