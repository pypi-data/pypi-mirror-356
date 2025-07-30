import pytest
import proxly
from proxly import FreeProxy, ProxyError

def test_proxly_import():
    assert proxly is not None
    
def test_proxy_class_creation():
    proxy = FreeProxy()
    assert proxy is not None
    assert proxy.timeout == 30
    assert proxy.max_retries == 3

def test_proxy_class_custom_params():
    proxy = FreeProxy(timeout=10, max_retries=5)
    assert proxy.timeout == 10
    assert proxy.max_retries == 5

def test_context_manager():
    with FreeProxy() as proxy:
        assert proxy is not None

def test_global_functions_exist():
    assert hasattr(proxly, 'get')
    assert hasattr(proxly, 'post')
    assert hasattr(proxly, 'put')
    assert hasattr(proxly, 'delete')
    assert hasattr(proxly, 'head')
    assert hasattr(proxly, 'patch')

def test_proxy_error_exception():
    assert ProxyError is not None
    with pytest.raises(ProxyError):
        raise ProxyError("Test error")
