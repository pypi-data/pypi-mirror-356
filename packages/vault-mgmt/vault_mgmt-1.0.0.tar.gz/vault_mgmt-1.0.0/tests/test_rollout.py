import argparse

from vault_mgmt import rollout


def test_create_parser():
    parser = argparse.ArgumentParser()
    rollout.create_parser(parser)
    assert isinstance(parser, argparse.ArgumentParser)


def test_main_help(capsys):
    parser = argparse.ArgumentParser()
    rollout.create_parser(parser)
    try:
        parser.parse_args(['--help'])
    except SystemExit as e:
        assert e.code == 0


def test_main_minimal(monkeypatch):
    parser = argparse.ArgumentParser()
    rollout.create_parser(parser)
    args = parser.parse_args([
        'vault', '--vault-addr', 'http://localhost:8200'
    ])
    rollout.main(args)
