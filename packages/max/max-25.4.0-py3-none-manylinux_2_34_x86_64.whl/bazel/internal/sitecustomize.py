# ===----------------------------------------------------------------------=== #
#
# This file is Modular Inc proprietary.
#
# ===----------------------------------------------------------------------=== #

import os


def __absolutize_path(value: str) -> str:
    if os.path.exists(value):
        return os.path.abspath(value)

    if execroot := os.getenv("BUILD_EXECROOT"):
        rebased = os.path.join(execroot, value)
        if os.path.exists(rebased):
            return os.path.abspath(rebased)

    return value


def __absolutize_env():
    for key in sorted(os.environ.keys()):
        value = os.environ[key]
        if key == "MODULAR_MOJO_MAX_IMPORT_PATH":
            value = ",".join(
                sorted(__absolutize_path(x) for x in value.split(","))
            )
        else:
            value = __absolutize_path(value)

        os.environ[key] = value


if os.getenv("MODULAR_USE_SITECUSTOMIZE") == "True":
    __absolutize_env()
