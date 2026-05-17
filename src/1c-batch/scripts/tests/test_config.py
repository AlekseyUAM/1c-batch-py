"""Тесты загрузки .1c-devbase.json и автоопределения платформы."""

import json
from pathlib import Path

from onec_batch.config import Config, _find_config_file, load_config


def test_validate_ok_file_mode():
    cfg = Config(
        platform_path=__file__,  # любой существующий файл
        connection_type="file",
        connection_path="/tmp/base",
    )
    assert cfg.validate() == []


def test_validate_missing_platform():
    cfg = Config(connection_type="file", connection_path="/tmp/base")
    errors = cfg.validate()
    assert any("platform" in e.lower() for e in errors)


def test_validate_server_requires_server_and_base():
    cfg = Config(platform_path=__file__, connection_type="server")
    errors = cfg.validate()
    assert any("сервер" in e.lower() for e in errors)
    assert any("базы" in e.lower() for e in errors)


def test_validate_unknown_connection_type():
    cfg = Config(platform_path=__file__, connection_type="cloud")
    errors = cfg.validate()
    assert any("cloud" in e for e in errors)


def test_find_config_walks_up(tmp_path: Path):
    cfg_file = tmp_path / ".1c-devbase.json"
    cfg_file.write_text("{}", encoding="utf-8")
    deep = tmp_path / "a" / "b" / "c"
    deep.mkdir(parents=True)
    assert _find_config_file(deep) == cfg_file


def test_find_config_returns_none_when_absent(tmp_path: Path):
    assert _find_config_file(tmp_path) is None


def test_load_config_server(tmp_path: Path):
    (tmp_path / ".1c-devbase.json").write_text(
        json.dumps({
            "platform_path": "/fake/1cv8",
            "connection": {"type": "server", "server": "host:1541", "base": "ref"},
            "user": "Админ",
            "password": "p@ss",
        }),
        encoding="utf-8",
    )
    cfg = load_config(tmp_path)
    assert cfg.platform_path == "/fake/1cv8"
    assert cfg.connection_type == "server"
    assert cfg.server == "host:1541"
    assert cfg.base == "ref"
    assert cfg.user == "Админ"
    assert cfg.password == "p@ss"


def test_load_config_file_mode_defaults(tmp_path: Path):
    (tmp_path / ".1c-devbase.json").write_text(
        json.dumps({
            "platform_path": "/fake/1cv8",
            "connection": {"type": "file", "path": "/tmp/base"},
        }),
        encoding="utf-8",
    )
    cfg = load_config(tmp_path)
    assert cfg.connection_type == "file"
    assert cfg.connection_path == "/tmp/base"
    assert cfg.cf_dir == "src/cf"  # дефолт
    assert cfg.log_dir == "logs"   # дефолт
