# define PY_SSIZE_T_CLEAN
from manager import log_manager
from manager.command_manager import CommandManager
from manager.stt_manager import SpeechToTextManager


if __name__ == '__main__':
    log_manager.hide_logs()
    cmd_manager = CommandManager()
    stt_manager = SpeechToTextManager()
    try:
        while True:
            value = stt_manager.listen()
            if value is not None:
                cmd_manager.manage(value)
    except KeyboardInterrupt:
        pass
