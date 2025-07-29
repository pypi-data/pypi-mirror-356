from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QLineEdit, QFileDialog, QTableWidget, 
                            QTableWidgetItem, QHeaderView, QProgressBar)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QFont
import os
import pkg_resources
from ..mimicmotion_comfyui import MimicMotionComfyUI
from ..utils.logger import logger

class PathSelectWidget(QWidget):
    file_selected = pyqtSignal(str)
    
    def __init__(self, placeholder_text, file_type="file", parent=None):
        super().__init__(parent)
        self.file_type = file_type
        
        # 创建水平布局
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # 创建输入框
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText(placeholder_text)
        self.path_input.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                border: 1px solid #E5E7EB;
                border-radius: 4px;
                background: white;
                font-size: 14px;
            }
            QLineEdit:hover {
                border-color: #3B82F6;
            }
            QLineEdit:focus {
                border-color: #3B82F6;
                outline: none;
            }
        """)
        layout.addWidget(self.path_input)
        
        # 创建选择按钮
        select_btn = QPushButton("选择")
        select_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                background-color: #F3F4F6;
                border: 1px solid #E5E7EB;
                border-radius: 4px;
                color: #374151;
                font-size: 14px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #E5E7EB;
                border-color: #D1D5DB;
            }
        """)
        select_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        select_btn.clicked.connect(self.on_select_click)
        layout.addWidget(select_btn)

    def on_select_click(self):
        if self.file_type == "folder" or self.file_type == "image":
            path = QFileDialog.getExistingDirectory(
                self,
                "选择文件夹",
                "",
                QFileDialog.Option.ShowDirsOnly
            )
        elif self.file_type == "video":
            path, _ = QFileDialog.getOpenFileName(
                self,
                "选择视频文件",
                "",
                "Video Files (*.mp4 *.avi *.mov);;All Files (*)"
            )
        else:
            path, _ = QFileDialog.getOpenFileName(
                self,
                "选择文件",
                "",
                "All Files (*)"
            )
            
        if path:
            self.path_input.setText(path)
            self.file_selected.emit(path)

class ProcessThread(QThread):
    progress_updated = pyqtSignal(int, str)  # row, status
    
    def __init__(self, log_items, server_url, output_dir):
        super().__init__()
        self.log_items = log_items
        self.is_running = True
        self.server_url = server_url
        self.output_dir = output_dir
    
    def run(self):
        for row, item in enumerate(self.log_items):
            if not self.is_running:
                break
                
            # 更新状态为"处理中"
            self.progress_updated.emit(row, "处理中")
            
            logger.info(f"开始执行: {item['video_path']}, {item['image_path']}, {self.output_dir}")
            # 开始执行 
            MimicMotionComfyUI.generate_mimicmotion(self.server_url, item["image_path"], item["video_path"], self.output_dir)
            
            # 更新状态为"已完成"
            self.progress_updated.emit(row, "已完成")
    
    def stop(self):
        self.is_running = False

class MimicMotionPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.process_thread = None
        self.log_items = []
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(32)
        
        # 左侧区域
        left_column = QVBoxLayout()
        left_column.setSpacing(24)
        
        # 对标视频选择
        video_group = QWidget()
        video_layout = QVBoxLayout(video_group)
        video_layout.setContentsMargins(0, 0, 0, 0)
        video_layout.setSpacing(8)
        
        video_title = QLabel("对标视频选择")
        font = QFont("Arial", 14)
        font.setBold(True)
        video_title.setFont(font)
        video_layout.addWidget(video_title)
        
        self.video_select = PathSelectWidget("请选择视频文件", "video")
        self.video_select.file_selected.connect(self.on_video_selected)
        video_layout.addWidget(self.video_select)
        
        left_column.addWidget(video_group)
        
        # 图片文件夹
        image_group = QWidget()
        image_layout = QVBoxLayout(image_group)
        image_layout.setContentsMargins(0, 0, 0, 0)
        image_layout.setSpacing(8)
        
        image_title = QLabel("图片文件夹")
        image_title.setFont(font)
        image_layout.addWidget(image_title)
        
        self.image_select = PathSelectWidget("请选择图片文件夹", "image")
        self.image_select.file_selected.connect(self.on_image_selected)
        image_layout.addWidget(self.image_select)
        
        left_column.addWidget(image_group)
        
        # 输出目录
        output_group = QWidget()
        output_layout = QVBoxLayout(output_group)
        output_layout.setContentsMargins(0, 0, 0, 0)
        output_layout.setSpacing(8)
        
        output_title = QLabel("输出目录")
        output_title.setFont(font)
        output_layout.addWidget(output_title)
        
        self.output_select = PathSelectWidget("请选择输出目录", "folder")
        self.output_select.file_selected.connect(self.on_output_selected)
        output_layout.addWidget(self.output_select)
        
        left_column.addWidget(output_group)
        
        # 服务器设置
        server_group = QWidget()
        server_layout = QVBoxLayout(server_group)
        server_layout.setContentsMargins(0, 0, 0, 0)
        server_layout.setSpacing(8)
        
        server_title = QLabel("服务器设置")
        server_title.setFont(font)
        server_layout.addWidget(server_title)
        
        self.server_input = QLineEdit()
        self.server_input.setPlaceholderText("请输入服务器地址")
        self.server_input.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                border: 1px solid #E5E7EB;
                border-radius: 4px;
                background: white;
                font-size: 14px;
            }
            QLineEdit:hover {
                border-color: #3B82F6;
            }
            QLineEdit:focus {
                border-color: #3B82F6;
                outline: none;
            }
        """)
        server_layout.addWidget(self.server_input)
        
        left_column.addWidget(server_group)
        left_column.addStretch()
        
        # 右侧日志区域
        right_column = QVBoxLayout()
        
        log_group = QWidget()
        log_layout = QVBoxLayout(log_group)
        log_layout.setContentsMargins(0, 0, 0, 0)
        log_layout.setSpacing(8)
        
        log_title = QLabel("运行日志")
        log_title.setFont(font)
        log_layout.addWidget(log_title)
        
        self.log_table = QTableWidget()
        self.log_table.setStyleSheet("""
            QTableWidget {
                background: white;
                border: 1px solid #E5E7EB;
                border-radius: 4px;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background: #F9FAFB;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #E5E7EB;
            }
        """)
        self.log_table.setColumnCount(3)
        self.log_table.setHorizontalHeaderLabels(["视频", "图片", "状态"])
        
        # 设置表格列宽
        header = self.log_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # 视频列自适应
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # 图片列自适应
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)    # 状态列固定宽度
        
        # 设置固定列的宽度
        self.log_table.setColumnWidth(2, 100)  # 状态列宽度
        
        log_layout.addWidget(self.log_table)
        
        # 添加执行按钮
        self.execute_btn = QPushButton("执行")
        self.execute_btn.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                padding: 8px 24px;
                border-radius: 4px;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
        """)
        self.execute_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.execute_btn.clicked.connect(self.on_execute)
        log_layout.addWidget(self.execute_btn, alignment=Qt.AlignmentFlag.AlignRight)
        
        right_column.addWidget(log_group)
        
        # 将左右列添加到主布局
        layout.addLayout(left_column, 1)
        layout.addLayout(right_column, 1)

    def on_video_selected(self, path):
        print(f"选择的视频文件: {path}")
        
    def on_image_selected(self, path):
        print(f"选择的图片文件夹: {path}")
        
    def on_output_selected(self, path):
        print(f"选择的输出目录: {path}")
        
    def on_execute(self):
        # 获取视频文件路径
        video_path = self.video_select.path_input.text()
        if not video_path or not os.path.isfile(video_path):
            return
            
        # 获取图片文件夹路径
        image_dir = self.image_select.path_input.text()
        if not image_dir or not os.path.isdir(image_dir):
            return
            
        # 获取输出目录
        output_dir = self.output_select.path_input.text()
        if not output_dir or not os.path.isdir(output_dir):
            return
            
        # 获取服务器地址
        server_url = self.server_input.text()
        if not server_url:
            return
            
        # 清空日志表格和日志项列表
        self.log_table.setRowCount(0)
        self.log_items.clear()
        
        # 获取所有图片文件
        image_files = [f for f in os.listdir(image_dir) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
        
        # 添加所有图片处理任务到日志
        for image_name in image_files:
            image_path = os.path.join(image_dir, image_name)
            self.add_log_item(video_path, image_path, "待执行")
                
        # 禁用执行按钮
        self.execute_btn.setEnabled(False)
        self.execute_btn.setText("处理中...")
        
        # 启动处理线程
        if self.process_thread and self.process_thread.isRunning():
            self.process_thread.stop()
            self.process_thread.wait()
            
        self.process_thread = ProcessThread(self.log_items, server_url, output_dir)
        self.process_thread.progress_updated.connect(self.update_log_status)
        self.process_thread.finished.connect(self.on_process_finished)
        self.process_thread.start()
    
    def add_log_item(self, video_path, image_path, status):
        row = self.log_table.rowCount()
        self.log_table.insertRow(row)
        
        # 添加视频路径
        video_item = QTableWidgetItem(video_path)
        video_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.log_table.setItem(row, 0, video_item)
        
        # 添加图片路径
        image_item = QTableWidgetItem(image_path)
        image_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.log_table.setItem(row, 1, image_item)
        
        # 添加状态
        status_item = QTableWidgetItem(status)
        status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.log_table.setItem(row, 2, status_item)
        
        # 保存日志项信息
        self.log_items.append({
            "video_path": video_path,
            "image_path": image_path,
            "status": status,
            "row": row
        })
        
        # 滚动到最新的行
        self.log_table.scrollToBottom()
    
    def update_log_status(self, row, status):
        if 0 <= row < self.log_table.rowCount():
            status_item = QTableWidgetItem(status)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # 根据状态设置不同的样式
            if status == "处理中":
                status_item.setForeground(Qt.GlobalColor.blue)
            elif status == "已完成":
                status_item.setForeground(Qt.GlobalColor.green)
            elif status == "失败":
                status_item.setForeground(Qt.GlobalColor.red)
                
            self.log_table.setItem(row, 2, status_item)
            self.log_items[row]["status"] = status
    
    def on_process_finished(self):
        # 恢复执行按钮
        self.execute_btn.setEnabled(True)
        self.execute_btn.setText("执行")
        
        # 清理线程
        if self.process_thread:
            self.process_thread.deleteLater()
            self.process_thread = None 