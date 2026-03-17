"""Запуск процессов 1cv8 — интерактивный и пакетный режимы."""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

import click

from .config import Config


def build_connection_args(cfg: Config) -> list[str]:
    """Формирование аргументов подключения к ИБ."""
    if cfg.connection_type == "server":
        return [f"/S{cfg.server}\\{cfg.base}"]
    return [f"/F{cfg.connection_path}"]


def build_auth_args(cfg: Config) -> list[str]:
    """Формирование аргументов аутентификации."""
    args: list[str] = []
    if cfg.user:
        args.append(f"/N{cfg.user}")
    if cfg.password:
        args.append(f"/P{cfg.password}")
    return args


def build_base_command(cfg: Config, mode: str) -> list[str]:
    """Формирование базовой командной строки 1cv8 с общими параметрами подключения.

    mode: "ENTERPRISE", "DESIGNER" или "CREATEINFOBASE"
    """
    cmd = [cfg.platform_path, mode]
    cmd.extend(build_connection_args(cfg))
    cmd.extend(build_auth_args(cfg))
    return cmd


def build_log_path(cfg: Config, command_name: str) -> Path:
    """Формирование пути к лог-файлу для пакетной команды."""
    log_dir = Path(cfg.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return log_dir / f"{command_name}_{timestamp}.log"


def read_log(log_path: Path) -> str | None:
    """Чтение и возврат содержимого лог-файла (/Out)."""
    if not log_path.exists():
        return None
    try:
        # 1С может писать в разных кодировках
        for encoding in ("utf-8-sig", "utf-8", "cp1251", "cp866"):
            try:
                return log_path.read_text(encoding=encoding)
            except (UnicodeDecodeError, ValueError):
                continue
        return log_path.read_bytes().decode("utf-8", errors="replace")
    except OSError:
        return None


def run_interactive(cfg: Config, mode: str, extra_args: list[str] | None = None) -> None:
    """Запуск 1С в интерактивном режиме (без ожидания завершения).

    mode: "ENTERPRISE" или "DESIGNER"
    """
    errors = cfg.validate()
    if errors:
        for e in errors:
            click.echo(f"Ошибка: {e}", err=True)
        sys.exit(1)

    cmd = build_base_command(cfg, mode)
    if extra_args:
        cmd.extend(extra_args)

    click.echo(f"Запуск: {' '.join(cmd)}")
    subprocess.Popen(cmd)


def run_batch(cfg: Config, command_name: str, extra_args: list[str]) -> int:
    """Запуск 1С в пакетном режиме (DESIGNER с /DisableStartupDialogs).

    Возвращает код возврата процесса.
    Логирует вывод (/Out) в файл и выводит содержимое при ошибке.
    """
    errors = cfg.validate()
    if errors:
        for e in errors:
            click.echo(f"Ошибка: {e}", err=True)
        return 1

    log_path = build_log_path(cfg, command_name)

    cmd = build_base_command(cfg, "DESIGNER")
    cmd.append("/DisableStartupDialogs")
    cmd.append(f"/Out{log_path}")
    cmd.extend(extra_args)

    click.echo(f"Запуск: {' '.join(cmd)}")
    result = subprocess.run(cmd)

    # Чтение и вывод содержимого лога
    log_content = read_log(log_path)

    if result.returncode != 0:
        click.echo(f"Ошибка (код {result.returncode}). Лог: {log_path}", err=True)
        if log_content:
            click.echo("--- Содержимое лога ---", err=True)
            click.echo(log_content, err=True)
            click.echo("--- Конец лога ---", err=True)
    else:
        click.echo(f"Готово. Лог: {log_path}")
        if log_content and log_content.strip():
            click.echo(log_content)

    return result.returncode
