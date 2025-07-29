from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QScrollArea, QPushButton, QFileDialog, QLineEdit)
from PyQt6.QtGui import QFont, QPixmap, QDesktopServices
from PyQt6.QtCore import Qt, QUrl
import os
import pkg_resources
from ..utils.logger import logger

class LinkLabel(QLabel):
    def __init__(self, text, url, parent=None):
        super().__init__(text, parent)
        self.url = url
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QLabel {
                color: #2563EB;
                font-size: 14px;
                padding: 8px 0;
            }
            QLabel:hover {
                color: #1D4ED8;
                text-decoration: underline;
            }
        """)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            QDesktopServices.openUrl(QUrl(self.url))

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(32)
        
        # 左侧区域 - 二维码
        left_column = QVBoxLayout()
        left_column.setSpacing(16)
        
        qr_title = QLabel("添加好友")
        qr_title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        left_column.addWidget(qr_title)
        
        qr_label = QLabel()
        qr_path = pkg_resources.resource_filename('shuke_ai', 'assets/qrcode.jpg')
        qr_pixmap = QPixmap(qr_path)
        if not qr_pixmap.isNull():
            qr_label.setPixmap(qr_pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            logger.error(f"二维码图片未找到: {qr_path}")
            qr_label.setText("二维码图片未找到")
        left_column.addWidget(qr_label)
        left_column.addStretch()
        
        # 右侧区域 - 教程链接
        right_column = QVBoxLayout()
        right_column.setSpacing(16)
        
        tutorial_title = QLabel("教程")
        tutorial_title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        right_column.addWidget(tutorial_title)
        
        # 添加教程链接
        tutorial_link = QLabel('<a href="https://h6vw7qmfq7.feishu.cn/docx/OjUNdtCRxoOn6cxF687cqRLhnRd?from=from_copylink" style="color: #3B82F6; text-decoration: none;">Mimicmotion教程</a>')
        tutorial_link.setOpenExternalLinks(True)
        right_column.addWidget(tutorial_link)
        
        right_column.addStretch()
        
        # 将左右列添加到主布局
        layout.addLayout(left_column, 1)
        layout.addLayout(right_column, 1)
        
        # 设置左右两侧的宽度比例为 1:2
        layout.setStretch(0, 1)
        layout.setStretch(1, 2) 