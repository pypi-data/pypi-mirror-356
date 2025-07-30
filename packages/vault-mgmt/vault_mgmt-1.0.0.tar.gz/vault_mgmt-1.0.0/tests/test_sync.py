import argparse

from vault_mgmt import sync


def test_create_parser():
    parser = argparse.ArgumentParser()
    sync.create_parser(parser)
    assert isinstance(parser, argparse.ArgumentParser)


def test_main_help(capsys):
    parser = argparse.ArgumentParser()
    sync.create_parser(parser)
    try:
        parser.parse_args(['--help'])
    except SystemExit as e:
        assert e.code == 0


def test_main_minimal(monkeypatch):
    parser = argparse.ArgumentParser()
    sync.create_parser(parser)
    args = parser.parse_args([
        '-s', 'http://localhost:8200',
        '-d', 'http://localhost:8201'
    ])
    sync.main(args)
