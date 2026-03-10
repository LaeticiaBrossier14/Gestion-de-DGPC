import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SERVER_PATH = ROOT / "verification_tool" / "server.py"

spec = importlib.util.spec_from_file_location("verification_server", SERVER_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)

module.AUDIO_DIRS[0].mkdir(exist_ok=True)
module.load_csv()
module.load_progress()
module.app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
