# See http://peak.telecommunity.com/DevCenter/setuptools#namespace-packages
try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:  # pragma: no cover
    from pkgutil import extend_path  # pragma: no cover
    __path__ = extend_path(__path__, __name__)  # pragma: no cover
