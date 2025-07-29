from PyQt6.QtWidgets import QApplication
from .view.main_window import MainWindow
from .utils.logger import logger
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(
        description='舒克AI工具集 - 一个强大的AI工具箱',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--gui', action='store_true', help='启动图形界面')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1.1')
    
    args = parser.parse_args()

    if args.gui:
        try:
            app = QApplication(sys.argv[:1])  # 只传递程序名，避免Qt解析其他参数
            window = MainWindow()
            window.show()
            return app.exec()
        except Exception as e:
            logger.error(f"启动GUI时发生错误: {str(e)}")
            return 1
    else:
        parser.print_help()
        return 0

if __name__ == "__main__":
    sys.exit(main())

