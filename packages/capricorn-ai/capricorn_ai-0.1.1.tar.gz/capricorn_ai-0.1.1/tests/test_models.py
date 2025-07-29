import sys
import types
import pytest

# Stub out heavy dependencies before importing the package
numpy_stub = types.ModuleType('numpy')
numpy_stub.ndarray = object
sys.modules.setdefault('numpy', numpy_stub)

pil_stub = types.ModuleType('PIL')
image_stub = types.ModuleType('PIL.Image')
pil_stub.Image = image_stub
sys.modules.setdefault('PIL', pil_stub)
sys.modules.setdefault('PIL.Image', image_stub)

from capricorn_ai.models import list_models, get_model_path


def test_list_models_contains_capricorn():
    assert 'capricorn0.1' in list_models()


def test_get_model_path_invalid():
    with pytest.raises(ValueError):
        get_model_path('unknown-model')
