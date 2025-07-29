import sys
import argparse
from PyQt6.QtWidgets import QApplication
from .view.main_window import MainWindow
from .utils.logger import logger

VERSION = "0.2.2"

def main():
    parser = argparse.ArgumentParser(description="舒克AI工具集")
    parser.add_argument("--gui", action="store_true", help="启动图形界面")
    parser.add_argument("--version", action="store_true", help="显示版本号")
    args = parser.parse_args()
    
    if args.version:
        print(f"shuke-ai {VERSION}")
        return
    
    if args.gui:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

