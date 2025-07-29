import glob
import os
import platform
from importlib import resources
from pathlib import Path


class Assets:
    assets_folder = str(resources.files('nikassets.helper').joinpath('assets'))
    if not os.path.exists(assets_folder):
        assets_folder = os.path.join(os.getcwd(), 'assets')
    if not os.path.exists(assets_folder):
        pwd = Path(os.getcwd()).parent
        for folders in pwd.iterdir():
            if folders.is_dir():
                if folders.name == "assets":
                    assets_folder = str(folders)
                    break
    cwd = assets_folder + os.path.sep
    system_name = platform.system()
    aapt_path = "aapt2"
    adb_path = "adb"
    gofile_path = os.path.join(assets_folder, 'gofile.sh')
    if system_name == "Windows":
        aapt_path = os.path.join(assets_folder, 'bin', system_name, 'aapt2.exe')
        adb_path = os.path.join(assets_folder, 'bin', system_name, 'adb.exe')
    elif system_name == "Linux":
        aapt_path = os.path.join(assets_folder, 'bin', system_name, 'aapt2')
    elif system_name == "Darwin":
        aapt_path = os.path.join(assets_folder, 'bin', system_name, 'aapt2')
        if not os.path.exists(aapt_path):
            sdk_path = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT")
            if not sdk_path:
                raise EnvironmentError("Android SDK path not found. "
                                       "Set ANDROID_HOME or ANDROID_SDK_ROOT environment variable.")
            search_pattern = os.path.join(sdk_path, "build-tools", "*", "aapt")
            aapt_paths = glob.glob(search_pattern)
            if aapt_paths:
                aapt_path = str(max(aapt_paths, key=os.path.getmtime))

    @staticmethod
    def get(file_name):
        return Assets.cwd + file_name
