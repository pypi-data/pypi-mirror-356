import nqs_pycore


def activate_log() -> None:
    try:
        nqs_pycore.activate_log()
    except Exception:
        pass
