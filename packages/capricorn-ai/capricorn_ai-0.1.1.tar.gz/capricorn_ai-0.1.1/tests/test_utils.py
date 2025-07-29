import sys
import types

# Stub out heavy dependencies so the module can import without them installed
numpy_stub = types.ModuleType('numpy')
numpy_stub.ndarray = object
sys.modules.setdefault('numpy', numpy_stub)

pil_stub = types.ModuleType('PIL')
image_stub = types.ModuleType('PIL.Image')
pil_stub.Image = image_stub
sys.modules.setdefault('PIL', pil_stub)
sys.modules.setdefault('PIL.Image', image_stub)

from capricorn_ai.utils import _categorize


def test_categorize_mapping():
    assert _categorize('mucus') == 'Colon Histology'
    assert _categorize('melanoma') == 'Skin Bathology'
    assert _categorize('platelet') == 'Blood Smear'
    assert _categorize('not-a-label') == 'Unknown'
