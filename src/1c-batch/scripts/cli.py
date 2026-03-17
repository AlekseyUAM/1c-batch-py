"""CLI точка входа — команда 1c-batch."""

import sys

import click

from .config import load_config as _load_config
from .runner import run_batch, run_interactive


@click.group()
@click.pass_context
def cli(ctx: click.Context) -> None:
    """1c-batch — пакетные операции с 1С:Предприятие 8."""
    ctx.ensure_object(dict)
    cfg = _load_config()
    ctx.obj["config"] = cfg


# ── Запуск ──────────────────────────────────────────────────────────

@cli.command()
@click.argument("epf", required=False)
@click.pass_context
def run_enterprise(ctx: click.Context, epf: str | None) -> None:
    """Запуск в режиме предприятия."""
    cfg = ctx.obj["config"]
    extra: list[str] = []
    if epf:
        extra.append(f"/Execute{epf}")
    extra.extend(["/DisableStartupDialogs", "/DisableStartupMessages"])
    run_interactive(cfg, "ENTERPRISE", extra)


@cli.command()
@click.pass_context
def run_designer(ctx: click.Context) -> None:
    """Запуск конфигуратора."""
    cfg = ctx.obj["config"]
    run_interactive(cfg, "DESIGNER")


# ── Конфигурация ────────────────────────────────────────────────────

@cli.command()
@click.argument("directory")
@click.option("--update", is_flag=True, help="Инкрементальная выгрузка (-update -force)")
@click.option("--extension", default=None, help="Имя расширения (-Extension)")
@click.option("--all-extensions", is_flag=True, help="Все расширения (-AllExtensions)")
@click.option("--format", "fmt", type=click.Choice(["Plain", "Hierarchical"]), default=None, help="Формат выгрузки (-Format)")
@click.pass_context
def dump_config(ctx: click.Context, directory: str, update: bool, extension: str | None, all_extensions: bool, fmt: str | None) -> None:
    """Выгрузка конфигурации в XML."""
    cfg = ctx.obj["config"]
    args = [f"/DumpConfigToFiles{directory}"]
    if extension:
        args.append(f"-Extension{extension}")
    if all_extensions:
        args.append("-AllExtensions")
    if update:
        args.extend(["-update", "-force"])
    if fmt:
        args.extend(["-Format", fmt])
    sys.exit(run_batch(cfg, "dump-config", args))


@cli.command()
@click.argument("directory")
@click.option("--files", default=None, help="Список файлов через запятую для частичной загрузки (-files)")
@click.option("--list-file", default=None, help="Путь к файлу-списку (-listFile)")
@click.option("--format", "fmt", type=click.Choice(["Plain", "Hierarchical"]), default=None, help="Формат (-Format)")
@click.option("--partial", is_flag=True, help="Частичная загрузка (-partial)")
@click.option("--extension", default=None, help="Имя расширения (-Extension)")
@click.option("--skip-db-update", is_flag=True, help="Не обновлять конфигурацию БД")
@click.pass_context
def load_config(ctx: click.Context, directory: str, files: str | None, list_file: str | None,
                fmt: str | None, partial: bool, extension: str | None, skip_db_update: bool) -> None:
    """Загрузка конфигурации из XML."""
    cfg = ctx.obj["config"]
    args = [f"/LoadConfigFromFiles{directory}"]
    if extension:
        args.append(f"-Extension{extension}")
    if files:
        args.append(f"-files{files}")
    if list_file:
        args.append(f"-listFile{list_file}")
    if fmt:
        args.extend(["-Format", fmt])
    if partial:
        args.append("-partial")
    args.append("-updateConfigDumpInfo")
    if not skip_db_update:
        args.append("/UpdateDBCfg")
        if extension:
            args.append(f"-Extension{extension}")
    sys.exit(run_batch(cfg, "load-config", args))


@cli.command()
@click.argument("filepath")
@click.option("--extension", default=None, help="Имя расширения (-Extension)")
@click.pass_context
def dump_cfg(ctx: click.Context, filepath: str, extension: str | None) -> None:
    """Сохранение конфигурации в файл .cf."""
    cfg = ctx.obj["config"]
    args = [f"/DumpCfg{filepath}"]
    if extension:
        args.append(f"-Extension{extension}")
    sys.exit(run_batch(cfg, "dump-cfg", args))


@cli.command()
@click.argument("filepath")
@click.option("--extension", default=None, help="Имя расширения (-Extension)")
@click.pass_context
def load_cfg(ctx: click.Context, filepath: str, extension: str | None) -> None:
    """Загрузка конфигурации из файла .cf."""
    cfg = ctx.obj["config"]
    args = [f"/LoadCfg{filepath}"]
    if extension:
        args.append(f"-Extension{extension}")
    sys.exit(run_batch(cfg, "load-cfg", args))


@cli.command()
@click.option("--dynamic", type=click.Choice(["+", "-"]), default=None, help="Динамическое обновление (-Dynamic+|-)")
@click.option("--server", is_flag=True, help="Серверный режим (-Server)")
@click.option("--extension", default=None, help="Имя расширения (-Extension)")
@click.pass_context
def update_db_cfg(ctx: click.Context, dynamic: str | None, server: bool, extension: str | None) -> None:
    """Обновление конфигурации БД."""
    cfg = ctx.obj["config"]
    args = ["/UpdateDBCfg"]
    if dynamic:
        args.append(f"-Dynamic{dynamic}")
    if server:
        args.append("-Server")
    if extension:
        args.append(f"-Extension{extension}")
    sys.exit(run_batch(cfg, "update-db-cfg", args))


# ── Расширения ──────────────────────────────────────────────────────

@cli.command()
@click.argument("directory")
@click.option("--name", required=True, help="Имя расширения")
@click.option("--update", is_flag=True, help="Инкрементальная выгрузка")
@click.option("--format", "fmt", type=click.Choice(["Plain", "Hierarchical"]), default=None, help="Формат выгрузки")
@click.pass_context
def dump_extension(ctx: click.Context, directory: str, name: str, update: bool, fmt: str | None) -> None:
    """Выгрузка расширения в XML."""
    cfg = ctx.obj["config"]
    args = [f"/DumpConfigToFiles{directory}", f"-Extension{name}"]
    if update:
        args.extend(["-update", "-force"])
    if fmt:
        args.extend(["-Format", fmt])
    sys.exit(run_batch(cfg, "dump-extension", args))


@cli.command()
@click.argument("directory")
@click.option("--name", required=True, help="Имя расширения")
@click.option("--skip-db-update", is_flag=True, help="Не обновлять конфигурацию БД")
@click.pass_context
def load_extension(ctx: click.Context, directory: str, name: str, skip_db_update: bool) -> None:
    """Загрузка расширения из XML."""
    cfg = ctx.obj["config"]
    args = [
        f"/LoadConfigFromFiles{directory}",
        f"-Extension{name}",
        "-updateConfigDumpInfo",
    ]
    if not skip_db_update:
        args.extend(["/UpdateDBCfg", f"-Extension{name}"])
    sys.exit(run_batch(cfg, "load-extension", args))


@cli.command()
@click.argument("filepath")
@click.option("--name", required=True, help="Имя расширения")
@click.pass_context
def dump_cfg_extension(ctx: click.Context, filepath: str, name: str) -> None:
    """Сохранение расширения в .cfe."""
    cfg = ctx.obj["config"]
    args = [f"/DumpCfg{filepath}", f"-Extension{name}"]
    sys.exit(run_batch(cfg, "dump-cfg-extension", args))


@cli.command()
@click.argument("filepath")
@click.option("--name", required=True, help="Имя расширения")
@click.pass_context
def load_cfg_extension(ctx: click.Context, filepath: str, name: str) -> None:
    """Загрузка расширения из .cfe."""
    cfg = ctx.obj["config"]
    args = [f"/LoadCfg{filepath}", f"-Extension{name}"]
    sys.exit(run_batch(cfg, "load-cfg-extension", args))


@cli.command()
@click.option("--name", default=None, help="Имя расширения")
@click.option("--all", "all_ext", is_flag=True, help="Удалить все расширения (-AllExtensions)")
@click.pass_context
def delete_extension(ctx: click.Context, name: str | None, all_ext: bool) -> None:
    """Удаление расширения."""
    cfg = ctx.obj["config"]
    args = ["/DeleteCfg"]
    if name:
        args.append(f"-Extension{name}")
    if all_ext:
        args.append("-AllExtensions")
    sys.exit(run_batch(cfg, "delete-extension", args))


@cli.command()
@click.pass_context
def list_extensions(ctx: click.Context) -> None:
    """Список расширений."""
    cfg = ctx.obj["config"]
    args = ["/DumpDBCfgList", "-AllExtensions"]
    sys.exit(run_batch(cfg, "list-extensions", args))


# ── Обработки (EPF/ERF) ────────────────────────────────────────────

@cli.command()
@click.argument("xml_dir")
@click.argument("epf_file")
@click.option("--format", "fmt", type=click.Choice(["Plain", "Hierarchical"]), default=None, help="Формат выгрузки (-Format)")
@click.pass_context
def dump_epf(ctx: click.Context, xml_dir: str, epf_file: str, fmt: str | None) -> None:
    """Разборка обработки/отчёта в XML."""
    cfg = ctx.obj["config"]
    args = [f"/DumpExternalDataProcessorOrReportToFiles{xml_dir}", epf_file]
    if fmt:
        args.extend(["-Format", fmt])
    sys.exit(run_batch(cfg, "dump-epf", args))


@cli.command()
@click.argument("xml_dir")
@click.argument("epf_file")
@click.pass_context
def build_epf(ctx: click.Context, xml_dir: str, epf_file: str) -> None:
    """Сборка обработки/отчёта из XML."""
    cfg = ctx.obj["config"]
    args = [f"/LoadExternalDataProcessorOrReportFromFiles{xml_dir}", epf_file]
    sys.exit(run_batch(cfg, "build-epf", args))


# ── База данных ─────────────────────────────────────────────────────

@cli.command()
@click.argument("filepath")
@click.pass_context
def dump_ib(ctx: click.Context, filepath: str) -> None:
    """Выгрузка ИБ в .dt."""
    cfg = ctx.obj["config"]
    args = [f"/DumpIB{filepath}"]
    sys.exit(run_batch(cfg, "dump-ib", args))


@cli.command()
@click.argument("filepath")
@click.option("--jobs-count", type=int, default=None, help="Количество фоновых заданий (-JobsCount)")
@click.pass_context
def restore_ib(ctx: click.Context, filepath: str, jobs_count: int | None) -> None:
    """Загрузка ИБ из .dt."""
    cfg = ctx.obj["config"]
    args = [f"/RestoreIB{filepath}"]
    if jobs_count is not None:
        args.append(f"-JobsCount{jobs_count}")
    sys.exit(run_batch(cfg, "restore-ib", args))


@cli.command()
@click.option("--path", required=True, help="Путь к каталогу новой файловой базы")
@click.option("--add-to-list", default=None, help="Имя для добавления в список баз (/AddToList)")
@click.option("--use-template", default=None, help="Путь к шаблону (/UseTemplate)")
@click.pass_context
def create_infobase(ctx: click.Context, path: str, add_to_list: str | None, use_template: str | None) -> None:
    """Создание информационной базы."""
    cfg = ctx.obj["config"]
    if not cfg.platform_path:
        click.echo("Ошибка: Не задан путь к платформе 1С.", err=True)
        sys.exit(1)
    import subprocess
    cmd = [cfg.platform_path, "CREATEINFOBASE", f'File="{path}"']
    if add_to_list:
        cmd.append(f"/AddToList{add_to_list}")
    if use_template:
        cmd.append(f"/UseTemplate{use_template}")
    click.echo(f"Запуск: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


@cli.command()
@click.pass_context
def ib_restore_integrity(ctx: click.Context) -> None:
    """Восстановление структуры ИБ."""
    cfg = ctx.obj["config"]
    args = ["/IBRestoreIntegrity"]
    sys.exit(run_batch(cfg, "ib-restore-integrity", args))


@cli.command()
@click.option("--reindex", is_flag=True, help="Реиндексация таблиц (-ReIndex)")
@click.option("--log-integrity", is_flag=True, help="Проверка логической целостности (-LogIntegrity)")
@click.option("--recalc-totals", is_flag=True, help="Пересчёт итогов (-RecalcTotals)")
@click.option("--ib-compression", is_flag=True, help="Сжатие таблиц ИБ (-IBCompression)")
@click.option("--rebuild", is_flag=True, help="Пересоздание таблиц (-Rebuild)")
@click.pass_context
def ib_check_and_repair(ctx: click.Context, reindex: bool, log_integrity: bool,
                        recalc_totals: bool, ib_compression: bool, rebuild: bool) -> None:
    """Тестирование и исправление ИБ."""
    cfg = ctx.obj["config"]
    args = ["/IBCheckAndRepair"]
    if reindex:
        args.append("-ReIndex")
    if log_integrity:
        args.append("-LogIntegrity")
    if recalc_totals:
        args.append("-RecalcTotals")
    if ib_compression:
        args.append("-IBCompression")
    if rebuild:
        args.append("-Rebuild")
    sys.exit(run_batch(cfg, "ib-check-and-repair", args))


# ── Проверки ────────────────────────────────────────────────────────

@cli.command()
@click.option("--config-log-integrity", is_flag=True, help="Проверка логической целостности конфигурации (-ConfigLogIntegrity)")
@click.option("--incorrect-references", is_flag=True, help="Поиск некорректных ссылок (-IncorrectReferences)")
@click.option("--thin-client", is_flag=True, help="Проверка для тонкого клиента (-ThinClient)")
@click.option("--server", is_flag=True, help="Проверка для сервера (-Server)")
@click.option("--extension", default=None, help="Имя расширения (-Extension)")
@click.option("--all-extensions", is_flag=True, help="Все расширения (-AllExtensions)")
@click.pass_context
def check_config(ctx: click.Context, config_log_integrity: bool, incorrect_references: bool,
                 thin_client: bool, server: bool, extension: str | None, all_extensions: bool) -> None:
    """Проверка конфигурации."""
    cfg = ctx.obj["config"]
    args = ["/CheckConfig"]
    if config_log_integrity:
        args.append("-ConfigLogIntegrity")
    if incorrect_references:
        args.append("-IncorrectReferences")
    if thin_client:
        args.append("-ThinClient")
    if server:
        args.append("-Server")
    if extension:
        args.append(f"-Extension{extension}")
    if all_extensions:
        args.append("-AllExtensions")
    sys.exit(run_batch(cfg, "check-config", args))


@cli.command()
@click.option("--thin-client", is_flag=True, help="Проверка для тонкого клиента (-ThinClient)")
@click.option("--server", is_flag=True, help="Проверка для сервера (-Server)")
@click.option("--extension", default=None, help="Имя расширения (-Extension)")
@click.option("--all-extensions", is_flag=True, help="Все расширения (-AllExtensions)")
@click.pass_context
def check_modules(ctx: click.Context, thin_client: bool, server: bool, extension: str | None, all_extensions: bool) -> None:
    """Проверка модулей."""
    cfg = ctx.obj["config"]
    args = ["/CheckModules"]
    if thin_client:
        args.append("-ThinClient")
    if server:
        args.append("-Server")
    if extension:
        args.append(f"-Extension{extension}")
    if all_extensions:
        args.append("-AllExtensions")
    sys.exit(run_batch(cfg, "check-modules", args))


# ── Сравнение ───────────────────────────────────────────────────────

@cli.command()
@click.argument("filepath")
@click.option("--settings", default=None, help="Файл настроек объединения (-Settings)")
@click.option("--force", is_flag=True, help="Принудительное объединение (-force)")
@click.pass_context
def merge_cfg(ctx: click.Context, filepath: str, settings: str | None, force: bool) -> None:
    """Объединение конфигураций."""
    cfg = ctx.obj["config"]
    args = [f"/MergeCfg{filepath}"]
    if settings:
        args.append(f"-Settings{settings}")
    if force:
        args.append("-force")
    sys.exit(run_batch(cfg, "merge-cfg", args))


@cli.command()
@click.option("--first-type", required=True, help="Тип первой конфигурации (-FirstConfigurationType)")
@click.option("--second-type", required=True, help="Тип второй конфигурации (-SecondConfigurationType)")
@click.option("--report-format", default=None, help="Формат отчёта (-ReportFormat)")
@click.option("--report-file", default=None, help="Файл отчёта (-ReportFile)")
@click.pass_context
def compare_cfg(ctx: click.Context, first_type: str, second_type: str,
                report_format: str | None, report_file: str | None) -> None:
    """Сравнение конфигураций."""
    cfg = ctx.obj["config"]
    args = ["/CompareCfg", f"-FirstConfigurationType{first_type}", f"-SecondConfigurationType{second_type}"]
    if report_format:
        args.append(f"-ReportFormat{report_format}")
    if report_file:
        args.append(f"-ReportFile{report_file}")
    sys.exit(run_batch(cfg, "compare-cfg", args))


# ── Свойства конфигурации ──────────────────────────────────────────

@cli.command()
@click.argument("directory")
@click.option("--module", is_flag=True, help="Выгрузить модули (-Module)")
@click.option("--template", is_flag=True, help="Выгрузить макеты (-Template)")
@click.option("--help-flag", is_flag=True, help="Выгрузить справку (-Help)")
@click.option("--all-writable", is_flag=True, help="Все редактируемые свойства (-AllWritable)")
@click.option("--picture", is_flag=True, help="Выгрузить картинки (-Picture)")
@click.option("--right", is_flag=True, help="Выгрузить права (-Right)")
@click.option("--extension", default=None, help="Имя расширения (-Extension)")
@click.pass_context
def dump_config_files(ctx: click.Context, directory: str, module: bool, template: bool,
                      help_flag: bool, all_writable: bool, picture: bool, right: bool,
                      extension: str | None) -> None:
    """Выгрузка свойств конфигурации (модули, макеты, права)."""
    cfg = ctx.obj["config"]
    args = [f"/DumpConfigFiles{directory}"]
    if module:
        args.append("-Module")
    if template:
        args.append("-Template")
    if help_flag:
        args.append("-Help")
    if all_writable:
        args.append("-AllWritable")
    if picture:
        args.append("-Picture")
    if right:
        args.append("-Right")
    if extension:
        args.append(f"-Extension{extension}")
    sys.exit(run_batch(cfg, "dump-config-files", args))


@cli.command()
@click.argument("directory")
@click.option("--module", is_flag=True, help="Загрузить модули (-Module)")
@click.option("--template", is_flag=True, help="Загрузить макеты (-Template)")
@click.option("--help-flag", is_flag=True, help="Загрузить справку (-Help)")
@click.option("--all-writable", is_flag=True, help="Все редактируемые свойства (-AllWritable)")
@click.option("--picture", is_flag=True, help="Загрузить картинки (-Picture)")
@click.option("--right", is_flag=True, help="Загрузить права (-Right)")
@click.option("--extension", default=None, help="Имя расширения (-Extension)")
@click.pass_context
def load_config_files(ctx: click.Context, directory: str, module: bool, template: bool,
                      help_flag: bool, all_writable: bool, picture: bool, right: bool,
                      extension: str | None) -> None:
    """Загрузка свойств конфигурации."""
    cfg = ctx.obj["config"]
    args = [f"/LoadConfigFiles{directory}"]
    if module:
        args.append("-Module")
    if template:
        args.append("-Template")
    if help_flag:
        args.append("-Help")
    if all_writable:
        args.append("-AllWritable")
    if picture:
        args.append("-Picture")
    if right:
        args.append("-Right")
    if extension:
        args.append(f"-Extension{extension}")
    sys.exit(run_batch(cfg, "load-config-files", args))


# ── Обслуживание ────────────────────────────────────────────────────

@cli.command()
@click.argument("date", required=True)
@click.pass_context
def reduce_event_log(ctx: click.Context, date: str) -> None:
    """Сокращение журнала регистрации. DATE — дата в формате YYYYMMDD."""
    cfg = ctx.obj["config"]
    args = [f"/ReduceEventLogSize{date}"]
    sys.exit(run_batch(cfg, "reduce-event-log", args))
