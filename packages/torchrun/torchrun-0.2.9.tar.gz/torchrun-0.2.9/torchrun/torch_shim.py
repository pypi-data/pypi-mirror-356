import torch
import types
import builtins
import os

SHIM_LOG_PATH = "/workspace/shim.log"
SHIM_VERBOSE = os.environ.get("SHIM_VERBOSE", "0") == "1"

def log(message: str):
    if SHIM_VERBOSE:
        print(message)
        try:
            with open(SHIM_LOG_PATH, "a") as f:
                f.write(message + "\n")
        except Exception:
            pass

class FakeCuda:
    def is_available(self):
        log("[torch_shim] torch.cuda.is_available() → True")
        return True

    def device(self, *args, **kwargs):
        log(f"[torch_shim] torch.cuda.device({args}, {kwargs}) → torch.device('cuda')")
        return torch.device("cuda")

    def current_device(self):
        log("[torch_shim] torch.cuda.current_device() → 0")
        return 0

    def get_device_name(self, device=None):
        log(f"[torch_shim] torch.cuda.get_device_name({device}) → 'ROCm Compatible Device'")
        return "ROCm Compatible Device"

    def manual_seed(self, seed):
        log(f"[torch_shim] torch.cuda.manual_seed({seed}) → no-op")

    def empty_cache(self):
        log("[torch_shim] torch.cuda.empty_cache() → no-op")

    def synchronize(self, device=None):
        log(f"[torch_shim] torch.cuda.synchronize({device}) → no-op")

    def set_device(self, device):
        log(f"[torch_shim] torch.cuda.set_device({device}) → no-op")

    def memory_allocated(self, device=None):
        log(f"[torch_shim] torch.cuda.memory_allocated({device}) → 0")
        return 0

    def memory_reserved(self, device=None):
        log(f"[torch_shim] torch.cuda.memory_reserved({device}) → 0")
        return 0

    def memory_cached(self, device=None):
        log(f"[torch_shim] torch.cuda.memory_cached({device}) → 0")
        return 0

    def get_device_capability(self, device=None):
        log(f"[torch_shim] torch.cuda.get_device_capability({device}) → (7, 0)")
        return (7, 0)

    def stream(self, *args, **kwargs):
        log(f"[torch_shim] torch.cuda.stream({args}, {kwargs}) → None")
        return None

    def __getattr__(self, name):
        # Catch any other method and return no-op
        def fallback(*args, **kwargs):
            log(f"[torch_shim] torch.cuda.{name}({args}, {kwargs}) → no-op fallback")
            return None
        return fallback

# Replace torch.cuda with shim
torch.cuda = FakeCuda()

# Replace torch.backends.cuda if accessed
if hasattr(torch.backends, "cuda"):
    torch.backends.cuda = types.SimpleNamespace(
        is_built=True,
        is_available=True,
        version="ROCm Shim"
    )
    log("[torch_shim] torch.backends.cuda replaced with ROCm stub")

# Override import system to return shim when 'torch.cuda' is requested
_orig_import = builtins.__import__
def patched_import(name, globals=None, locals=None, fromlist=(), level=0):
    if name == "torch.cuda":
        log("[torch_shim] patched import: torch.cuda")
        return torch.cuda
    if name == "torch.backends.cuda":
        log("[torch_shim] patched import: torch.backends.cuda")
        return torch.backends.cuda
    return _orig_import(name, globals, locals, fromlist, level)

builtins.__import__ = patched_import

# Patch known torch.ops.cuda.* kernel calls to no-op
try:
    if hasattr(torch.ops, "cuda"):
        for op_name in dir(torch.ops.cuda):
            if not op_name.startswith("_"):
                log(f"[torch_shim] monkey-patching torch.ops.cuda.{op_name}")
                setattr(torch.ops.cuda, op_name, lambda *args, **kwargs: log(f"[torch_shim] 🚫 torch.ops.cuda.{op_name}() was called → no-op"))
except Exception as e:
    log(f"[torch_shim] failed to patch torch.ops.cuda ops: {e}")