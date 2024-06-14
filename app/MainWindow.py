import configparser
from datetime import datetime
import pandas as pd
from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QWidget, QVBoxLayout, QLabel, QTableView, QDateTimeEdit, \
    QSpacerItem, QSizePolicy, QCheckBox, QLineEdit, QMessageBox
from PyQt6.QtWidgets import QApplication, QPushButton
from PyQt6.QtCore import Qt, QSize, QAbstractTableModel
from PyQt6.QtGui import QIcon, QCursor, QPalette, QColor, QFont
import requests


class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=None):
        if self._data is None or self._data.empty:
            return 0
        return self._data.shape[0]

    def columnCount(self, parent=None):
        if self._data is None or self._data.empty:
            return 0
        return self._data.shape[1]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.ItemDataRole.DisplayRole:
            if index.row() < 0 or index.row() >= self._data.shape[0]:
                return None
            if index.column() < 0 or index.column() >= self._data.shape[1]:
                return None
            return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if self._data is None or self._data.empty:
                return None
            if orientation == Qt.Orientation.Horizontal:
                if section < 0 or section >= len(self._data.columns):
                    return None
                return str(self._data.columns[section])
            elif orientation == Qt.Orientation.Vertical:
                if section < 0 or section >= len(self._data.index):
                    return None
                return str(self._data.index[section])
        return None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.windowWidth = 740
        self.windowHeight = 400
        self.set_flags()

        self.start_time_label = QLabel("Start Date:")
        self.start_time_label.setProperty("class", "title")
        self.end_time_label = QLabel("End Date:")
        self.end_time_label.setProperty("class", "title")
        self.group_ip_label = QLabel("Group by ip:")
        self.group_ip_label.setProperty("class", "title")
        self.group_ip_check_box = QCheckBox(self)
        self.start_time_picker = QDateTimeEdit(self)
        self.start_time_check_box = QCheckBox(self)
        self.end_time_picker = QDateTimeEdit(self)
        self.end_time_check_box = QCheckBox(self)
        self.get_button = QPushButton("Get")
        self.get_button.setProperty("class", "getButton")
        self.get_button.setFixedSize(80, 30)
        self.get_button.clicked.connect(self.get_data_from_api)
        self.topFrame = QWidget(self)
        self.mainLayout = QVBoxLayout()
        self.mainBox = QHBoxLayout()
        self.start_box = QHBoxLayout()
        self.end_box = QHBoxLayout()
        self.start_box_with_text = QVBoxLayout()
        self.end_box_with_text = QVBoxLayout()
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.centralWidget)
        self.topFrameLayout = QHBoxLayout()
        self.minimizeButton = QPushButton()
        self.closeButton = QPushButton()
        self.mainLabel = QLabel("Apache Log")
        self.table = QTableView(self)

        self.init_style_sheet()
        self.init_top_frame()
        self.dragPos = self.pos()
        self.set_cursor_btn()
        self.get_palette()
        self.get_api_data()

        self.start_time_picker.setPalette(self.palette)
        self.end_time_picker.setPalette(self.palette)

        spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.mainLayout.addItem(spacer)
        self.add_parameters()

        self.init_table()
        self.mainLayout.addWidget(self.table)

    def add_parameters(self):
        self.start_box.addWidget(self.start_time_picker)
        self.start_box.addWidget(self.start_time_check_box)

        self.end_box.addWidget(self.end_time_picker)
        self.end_box.addWidget(self.end_time_check_box)

        self.start_box_with_text.addWidget(self.start_time_label)
        self.start_box_with_text.addLayout(self.start_box)

        self.end_box_with_text.addWidget(self.end_time_label)
        self.end_box_with_text.addLayout(self.end_box)

        self.ip_address_label = QLabel("IP Address:")
        self.ip_address_label.setProperty("class", "title")
        self.ip_address_input = QLineEdit(self)
        self.ip_address_input.setFixedSize(100, 26)
        self.ip_address_check_box = QCheckBox(self)
        self.ip_address_input.setPalette(self.palette)

        self.ip_address_input.setInputMask("000.000.000.000;")

        self.ip_address_layout = QHBoxLayout()
        self.ip_address_layout_with_text = QVBoxLayout()
        self.ip_address_layout.addWidget(self.ip_address_input)
        self.ip_address_layout.addWidget(self.ip_address_check_box)
        self.ip_address_layout_with_text.addWidget(self.ip_address_label)
        self.ip_address_layout_with_text.addLayout(self.ip_address_layout)
        self.mainBox.addLayout(self.ip_address_layout_with_text)
        self.mainBox.addSpacing(10)

        self.status_code_label = QLabel("Status:")
        self.status_code_label.setProperty("class", "title")
        self.status_code_input = QLineEdit(self)
        self.status_code_input.setText("200")
        self.status_code_input.setFixedSize(50, 26)
        self.status_code_check_box = QCheckBox(self)
        self.status_code_input.setPalette(self.palette)

        self.status_code_layout = QHBoxLayout()
        self.status_code_layout_with_text = QVBoxLayout()
        self.status_code_layout.addWidget(self.status_code_input)
        self.status_code_layout.addWidget(self.status_code_check_box)
        self.status_code_layout_with_text.addWidget(self.status_code_label)
        self.status_code_layout_with_text.addLayout(self.status_code_layout)

        self.mainBox.addLayout(self.status_code_layout_with_text)
        self.mainBox.addSpacing(10)

        self.mainBox.addLayout(self.start_box_with_text)
        self.mainBox.addSpacing(10)
        self.mainBox.addLayout(self.end_box_with_text)

        self.mainBox.addSpacing(10)
        self.group_ip_box = QVBoxLayout(self)
        self.group_ip_check_box.setFixedSize(26, 26)
        self.group_ip_box.addWidget(self.group_ip_label)
        self.group_ip_box.addWidget(self.group_ip_check_box)
        self.mainBox.addLayout(self.group_ip_box)

        self.start_time_picker.raise_()
        self.start_time_check_box.raise_()
        self.start_time_picker.setFixedSize(120, 26)
        self.end_time_picker.raise_()
        self.end_time_check_box.raise_()
        self.end_time_picker.setFixedSize(120, 26)
        self.mainBox.addSpacing(10)
        self.mainBox.addWidget(self.get_button)
        self.mainBox.addStretch(0)
        self.mainLayout.addLayout(self.mainBox)

    def get_api_data(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.api_host = config['API']['host']
        self.api_port = config['API']['port']
        self.api_url = config['API']['url']

    def convert_datetime(self, input_datetime_str):
        input_format = "%d.%m.%Y %H:%M"
        output_format = "%Y-%m-%dT%H:%M:%S"

        datetime_obj = datetime.strptime(input_datetime_str, input_format)
        output_datetime_str = datetime_obj.strftime(output_format)

        return output_datetime_str

    def get_data_from_api(self):
        try:
            query_params = []

            if self.ip_address_check_box.isChecked():
                query_params.append(f'ip_address={self.ip_address_input.text()}')

            if self.status_code_check_box.isChecked():
                query_params.append(f'status_code={self.status_code_input.text()}')

            if self.start_time_check_box.isChecked():
                query_params.append(f'start_time={self.convert_datetime(self.start_time_picker.text())}')

            if self.end_time_check_box.isChecked():
                query_params.append(f'end_time={self.convert_datetime(self.end_time_picker.text())}')

            is_group_ip = self.group_ip_check_box.isChecked()

            if is_group_ip:
                query_params.append(f'group_by_ip={str(is_group_ip).lower()}')

            query_string = '&'.join(query_params)
            api_url = f'http://{self.api_host}:{self.api_port}{self.api_url}?{query_string}'

            response = requests.get(api_url)
            response.raise_for_status()

            data = response.json()

            df = pd.DataFrame(data)
            model = PandasModel(df)

            self.table.setModel(model)
            if is_group_ip:
                self.set_column_width_group()
            else:
                self.set_column_width_def()

        except requests.exceptions.RequestException as e:
            self.show_error_dialog(f"Request error: {str(e)}")
        except ValueError as e:
            self.show_error_dialog(f"Value error: {str(e)}")
        except Exception as e:
            self.show_error_dialog(f"An unexpected error occurred: {str(e)}")

    def show_error_dialog(self, message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(message)
        error_dialog.exec()

    def get_palette(self):
        self.palette = QPalette()
        self.palette.setColor(QPalette.ColorRole.Window, QColor(25, 25, 25))
        self.palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        self.palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        self.palette.setColor(QPalette.ColorRole.AlternateBase, QColor(25, 25, 25))
        self.palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
        self.palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
        self.palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
        self.palette.setColor(QPalette.ColorRole.Button, QColor(25, 25, 25))
        self.palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        self.palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        self.palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        self.palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        self.palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))

    def set_column_width_group(self):
        self.table.setColumnWidth(0, 10)
        self.table.setColumnWidth(1, 180)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 180)

    def set_column_width_def(self):
        self.table.setColumnWidth(0, 10)
        self.table.setColumnWidth(1, 90)
        self.table.setColumnWidth(2, 60)
        self.table.setColumnWidth(3, 150)
        self.table.setColumnWidth(4, 80)
        self.table.setColumnWidth(5, 70)
        self.table.setColumnWidth(6, 180)

    def init_table(self):
        self.get_data_from_api()

        self.table.verticalHeader().setVisible(False)

        self.table.setFixedSize(720, 300)
        self.setPalette(self.palette)
        self.table.setPalette(self.palette)
        self.table.verticalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #212121; color: white; border: 1px solid #404040;}"
        )
        self.table.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #212121; color: white; border: 1px solid #404040;}"
        )
        self.table.setStyleSheet("""background-color: #212121;""")
        self.set_column_width_def()

        font = QFont()
        font.setBold(True)
        self.table.horizontalHeader().setFont(font)
        self.table.verticalHeader().setFont(font)

    def set_cursor_btn(self):
        for button in self.findChildren(QPushButton):
            button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def set_flags(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setWindowIcon(QIcon("assets/favicon.ico"))
        self.setFixedSize(self.windowWidth, self.windowHeight)
        self.setWindowTitle('Apache Log')

    def init_top_frame(self):
        self.topFrame.setProperty("class", "topFrame")
        self.topFrame.setFixedHeight(28)
        self.topFrame.setFixedWidth(self.windowWidth)
        self.topFrame.raise_()

        self.mainLabel.setProperty("class", "mainLabel")
        self.topFrameLayout.addWidget(self.mainLabel, Qt.AlignmentFlag.AlignAbsolute)

        # Minimize button
        self.minimizeButton = QPushButton()
        self.setup_top_button(self.minimizeButton, "assets\\minimize.svg", self.showMinimized)

        # Close button
        self.closeButton = QPushButton()
        self.setup_top_button(self.closeButton, "assets\\close.svg", self.close)

        self.topFrameLayout.setContentsMargins(0, 0, 6, 0)
        self.topFrameLayout.setSpacing(0)
        self.topFrame.setLayout(self.topFrameLayout)

    def setup_top_button(self, button, icon_path, click_method):
        button.setIcon(QIcon(icon_path))
        button.setFixedSize(24, 24)
        button.setIconSize(QSize(26, 26))
        button.clicked.connect(click_method)
        button.setProperty("class", "cmButton")
        self.topFrameLayout.addWidget(button)

    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if Qt.MouseButton.LeftButton == event.buttons():
            if (not self.minimizeButton.underMouse() and not self.closeButton.underMouse()
                    and self.topFrame.underMouse()):
                delta = event.globalPosition().toPoint() - self.dragPos
                self.move(self.pos() + delta)
                self.dragPos = event.globalPosition().toPoint()

    def init_style_sheet(self):
        self.setStyleSheet(open('styles/mainwindow.qss').read())
        self.topFrame.setStyleSheet(open('styles/topframe.qss').read())


if __name__ == '__main__':
    app = QApplication([])
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(25, 25, 25))

    app.setPalette(dark_palette)
    window = MainWindow()
    window.show()
    app.exec()
