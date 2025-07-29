
from pathlib import Path
from hatchling.builders.hooks.plugin.interface import BuildHookInterface
import subprocess

class CustomBuildHook(BuildHookInterface):
    PLUGIN_NAME = "betaflight-sitl"

    def initialize(self, version, build_data):
        project_root = Path(self.root)
        firmware_dir = project_root / "betaflight" / "firmware"

        if self.target_name == "sdist":
            return

        subprocess.run(["make", "TARGET=SITL"], cwd=firmware_dir, check=True)
        build_data.setdefault("artifacts", []).append(
            str(firmware_dir / "obj")
        )
