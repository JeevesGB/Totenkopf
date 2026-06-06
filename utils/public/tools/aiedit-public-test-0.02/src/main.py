import sys
sys.dont_write_bytecode = True
import os

_SRC_DIR = os.path.dirname(os.path.abspath(__file__))
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("RTCW AI Editor")
    app.setStyle("Fusion")

    win = MainWindow()
    win.show()

    # Load any .ai files passed on the command line
    ai_args = [a for a in sys.argv[1:] if a.endswith('.ai') and os.path.isfile(a)]
    for path in ai_args:
        win._load_file(path)
    if ai_args:
        win._rebuild_map_list()
        win._refresh_all_tree()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()