from PyQt6.QtWidgets import (QMainWindow, QLabel, QVBoxLayout, QWidget, 
                            QPushButton, QHBoxLayout, QFrame, QStackedWidget, QSizePolicy, QTabWidget)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
import os
import pkg_resources
from .mimicmotion_page import MimicMotionPage
from .settings_page import SettingsPage

class DrawerNav(QWidget):
    def __init__(self, on_nav):
        super().__init__()
        self.on_nav = on_nav
        self.setFixedWidth(220)
        self.setStyleSheet("background: #fff;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # LOGO区
        logo_frame = QFrame()
        logo_frame.setStyleSheet("background: #fff;")
        logo_layout = QVBoxLayout(logo_frame)
        logo_layout.setContentsMargins(0, 36, 0, 12)
        logo_label = QLabel("TK舒克")
        logo_label.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        logo_label.setStyleSheet("color: #3B6EF6; letter-spacing: 2px; background: transparent;")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(logo_label)
        subtitle_label = QLabel("AI工具箱")
        subtitle_label.setFont(QFont("Arial", 12))
        subtitle_label.setStyleSheet("color: #B0B3B8; background: transparent;")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(subtitle_label)
        layout.addWidget(logo_frame)

        # 菜单按钮
        self.btns = []
        navs = ["MimicMotion", "设置"]
        for idx, name in enumerate(navs):
            btn = QPushButton(name)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            btn.setFixedHeight(44)
            btn.setFont(QFont("Arial", 15))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    color: #222;
                    background: #fff;
                    text-align: left;
                    padding-left: 32px;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background: #F0F6FF;
                }
            """)
            btn.clicked.connect(lambda checked, i=idx: self.on_nav(i))
            layout.addWidget(btn)
            self.btns.append(btn)
        layout.addStretch(1)
        self.set_active(0)

    def set_active(self, idx):
        for i, btn in enumerate(self.btns):
            if i == idx:
                btn.setStyleSheet("""
                    QPushButton {
                        color: #3B6EF6;
                        background: #F0F6FF;
                        text-align: left;
                        padding-left: 32px;
                        border: none;
                        border-radius: 8px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background: #F0F6FF;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        color: #222;
                        background: #fff;
                        text-align: left;
                        padding-left: 32px;
                        border: none;
                        border-radius: 8px;
                    }
                    QPushButton:hover {
                        background: #F0F6FF;
                    }
                """)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TK舒克 - AI工具箱")
        self.setMinimumSize(1200, 700)
        
        # 创建主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # 创建主布局
        layout = QHBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 添加左侧导航栏
        self.drawer = DrawerNav(self.on_nav)
        layout.addWidget(self.drawer)
        
        # 添加主要内容区域
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background: #F7F9FB;")
        
        # 添加页面
        self.mimic_motion_page = MimicMotionPage()
        self.settings_page = SettingsPage()
        self.stack.addWidget(self.mimic_motion_page)
        self.stack.addWidget(self.settings_page)
        
        layout.addWidget(self.stack)
        
        # 设置样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F7F9FB;
            }
        """)
        
        # 默认显示第一个页面
        self.stack.setCurrentIndex(0)
        self.drawer.set_active(0)

    def on_nav(self, index):
        self.stack.setCurrentIndex(index)
        self.drawer.set_active(index) 