from PyQt6.QtWidgets import QApplication
from .view.main_window import MainWindow
from .utils.logger import logger
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='舒克AI工具集')
    parser.add_argument('--gui', action='store_true', help='启动图形界面')
    args = parser.parse_args()

    if args.gui:
        app = QApplication(sys.argv[:1])  # 只传递程序名，避免QT解析其他参数
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

