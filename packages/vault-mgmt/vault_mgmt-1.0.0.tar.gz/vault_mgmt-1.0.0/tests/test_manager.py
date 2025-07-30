import pytest

from vault_mgmt import manager


class FakeSys:
    def list_mounted_secrets_engines(self):
        return {
            'data': {
                'secret/': {
                    'type': 'kv',
                    'options': {'version': '2'}
                }
            }
        }


class FakeOIDC:
    def oidc_authorization_url_request(self, role, redirect_uri):
        return {"data": {"auth_url": "http://localhost:8250/oidc/callback?nonce=abc&state=xyz"}}

    def oidc_callback(self, code, path, nonce, state):
        return {"auth": {"client_token": "token123"}}


class FakeAuth:
    def __init__(self):
        self.oidc = FakeOIDC()


class FakeClient:
    def __init__(self, url=None):
        self.auth = FakeAuth()
        self.sys = FakeSys()
        self.token = None


def test_manager_init():
    m = manager.VaultManager('http://localhost:8200')
    assert m.vault_addr == 'http://localhost:8200'


def test_is_authenticated_false():
    m = manager.VaultManager('http://localhost:8200')
    assert not m.is_authenticated()


def test_get_kv_version(monkeypatch):
    m = manager.VaultManager('http://localhost:8200')
    m.client = FakeClient()  # type: ignore
    m.is_authenticated = lambda: True
    assert m.get_kv_version('secret') == 2


# Patch hvac.Client and webbrowser.open for the test
def test_authenticate_with_oidc_success(monkeypatch):
    m = manager.VaultManager('http://localhost:8200')
    monkeypatch.setattr(manager, 'hvac', type('hvac', (), {'Client': lambda url: FakeClient(url)}))
    monkeypatch.setattr(manager.webbrowser, 'open', lambda url: None)
    monkeypatch.setattr(m, '_login_oidc_get_token', lambda: 'dummy_code')
    client = m.authenticate_with_oidc(oidc_role='test-role')
    assert client.token == 'token123'  # type: ignore
    assert m.client.token == 'token123'  # type: ignore


def test_authenticate_with_oidc_failure(monkeypatch):
    m = manager.VaultManager('http://localhost:8200')

    class FailingOIDC:
        def oidc_authorization_url_request(self, role, redirect_uri):
            raise Exception('fail')

    class FailingAuth:
        def __init__(self):
            self.oidc = FailingOIDC()

    class FailingClient:
        def __init__(self, url=None):
            self.auth = FailingAuth()
    monkeypatch.setattr(manager, 'hvac', type('hvac', (), {'Client': lambda url: FailingClient(url)}))
    monkeypatch.setattr(manager.webbrowser, 'open', lambda url: None)
    with pytest.raises(Exception) as excinfo:
        m.authenticate_with_oidc(oidc_role='test-role')
    assert str(excinfo.value) == 'fail'
