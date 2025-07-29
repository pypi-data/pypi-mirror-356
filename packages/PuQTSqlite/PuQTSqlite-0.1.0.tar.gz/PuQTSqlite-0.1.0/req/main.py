import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
                            QDialog, QLabel, QLineEdit, QComboBox, QSpinBox, 
                            QMessageBox, QHeaderView, QFrame, QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont, QPixmap, QPalette, QColor
from database import Database

class StyledButton(QPushButton):
    def __init__(self, text, is_primary=False):
        super().__init__(text)
        self.setFont(QFont("Segoe UI", 10))
        if is_primary:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #67BA80;
                    color: white;
                    border: none;
                    padding: 5px 15px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #5AA873;
                }
                QPushButton:pressed {
                    background-color: #4D9666;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #F4E8D3;
                    color: black;
                    border: none;
                    padding: 5px 15px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #E5D9C4;
                }
                QPushButton:pressed {
                    background-color: #D6CAB5;
                }
            """)

class StyledTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #F4E8D3;
                border: 1px solid #F4E8D3;
            }
            QHeaderView::section {
                background-color: #F4E8D3;
                padding: 5px;
                border: 1px solid #F4E8D3;
                font-family: 'Segoe UI';
                font-size: 10pt;
            }
            QTableWidget::item {
                padding: 5px;
                font-family: 'Segoe UI';
                font-size: 10pt;
            }
        """)

class PartnerDialog(QDialog):
    def __init__(self, parent=None, partner_data=None):
        super().__init__(parent)
        self.partner_data = partner_data
        self.db = Database()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Добавление/редактирование партнера")
        self.setMinimumWidth(600)
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                font-family: 'Segoe UI';
                font-size: 10pt;
            }
            QLineEdit, QComboBox, QSpinBox {
                font-family: 'Segoe UI';
                font-size: 10pt;
                padding: 5px;
                border: 1px solid #F4E8D3;
                border-radius: 3px;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Тип партнера
        type_layout = QHBoxLayout()
        type_label = QLabel("Тип партнера:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["ООО", "ИП", "ОАО", "АО", "ПАО", "ЗАО"])
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_combo)
        layout.addLayout(type_layout)
        
        # Наименование компании
        company_layout = QHBoxLayout()
        company_label = QLabel("Наименование компании:")
        self.company_edit = QLineEdit()
        company_layout.addWidget(company_label)
        company_layout.addWidget(self.company_edit)
        layout.addLayout(company_layout)
        
        # ФИО директора
        director_layout = QHBoxLayout()
        director_label = QLabel("ФИО директора:")
        self.director_edit = QLineEdit()
        director_layout.addWidget(director_label)
        director_layout.addWidget(self.director_edit)
        layout.addLayout(director_layout)
        
        # Email
        email_layout = QHBoxLayout()
        email_label = QLabel("Email:")
        self.email_edit = QLineEdit()
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_edit)
        layout.addLayout(email_layout)
        
        # Телефон
        phone_layout = QHBoxLayout()
        phone_label = QLabel("Телефон:")
        self.phone_edit = QLineEdit()
        phone_layout.addWidget(phone_label)
        phone_layout.addWidget(self.phone_edit)
        layout.addLayout(phone_layout)
        
        # Адрес
        address_layout = QHBoxLayout()
        address_label = QLabel("Адрес:")
        self.address_edit = QLineEdit()
        address_layout.addWidget(address_label)
        address_layout.addWidget(self.address_edit)
        layout.addLayout(address_layout)
        
        # ИНН
        inn_layout = QHBoxLayout()
        inn_label = QLabel("ИНН:")
        self.inn_edit = QLineEdit()
        inn_layout.addWidget(inn_label)
        inn_layout.addWidget(self.inn_edit)
        layout.addLayout(inn_layout)
        
        # Рейтинг
        rating_layout = QHBoxLayout()
        rating_label = QLabel("Рейтинг:")
        self.rating_spin = QSpinBox()
        self.rating_spin.setRange(0, 100)
        rating_layout.addWidget(rating_label)
        rating_layout.addWidget(self.rating_spin)
        layout.addLayout(rating_layout)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        self.save_button = StyledButton("Сохранить", is_primary=True)
        self.cancel_button = StyledButton("Отмена")
        self.save_button.clicked.connect(self.save_partner)
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
        
        if self.partner_data:
            self.load_partner_data()
    
    def load_partner_data(self):
        self.type_combo.setCurrentText(self.partner_data[1])
        self.company_edit.setText(self.partner_data[2])
        self.director_edit.setText(self.partner_data[3])
        self.email_edit.setText(self.partner_data[4])
        self.phone_edit.setText(self.partner_data[5])
        self.address_edit.setText(self.partner_data[6])
        self.inn_edit.setText(self.partner_data[7])
        self.rating_spin.setValue(self.partner_data[8])
    
    def validate_data(self):
        if not self.company_edit.text():
            QMessageBox.warning(self, "Ошибка", "Введите наименование компании")
            return False
        if not self.director_edit.text():
            QMessageBox.warning(self, "Ошибка", "Введите ФИО директора")
            return False
        if not self.email_edit.text() or '@' not in self.email_edit.text():
            QMessageBox.warning(self, "Ошибка", "Введите корректный email")
            return False
        if not self.phone_edit.text() or not self.phone_edit.text().startswith('+7'):
            QMessageBox.warning(self, "Ошибка", "Введите корректный номер телефона")
            return False
        if not self.address_edit.text():
            QMessageBox.warning(self, "Ошибка", "Введите адрес")
            return False
        if not self.inn_edit.text() or not self.inn_edit.text().isdigit() or len(self.inn_edit.text()) not in [10, 12]:
            QMessageBox.warning(self, "Ошибка", "ИНН должен содержать 10 или 12 цифр")
            return False
        return True
    
    def save_partner(self):
        if not self.validate_data():
            return
        
        partner_data = (
            self.type_combo.currentText(),
            self.company_edit.text(),
            self.director_edit.text(),
            self.email_edit.text(),
            self.phone_edit.text(),
            self.address_edit.text(),
            self.inn_edit.text(),
            self.rating_spin.value()
        )
        
        if self.partner_data:
            self.db.update_partner(self.partner_data[0], partner_data)
        else:
            self.db.add_partner(partner_data)
        
        self.accept()

class HistoryDialog(QDialog):
    def __init__(self, parent=None, partner_data=None):
        super().__init__(parent)
        self.partner_data = partner_data
        self.db = Database()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle(f"История продаж {self.partner_data[2]}")
        self.setMinimumWidth(800)
        self.setMinimumHeight(400)
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
        """)
        layout = QVBoxLayout()
        # Таблица истории
        self.history_table = StyledTable()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels([
            "Продукт", "Артикул", "Количество", "Дата", "Сумма"
        ])
        header = self.history_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.history_table)
        # Кнопка закрытия
        close_button = StyledButton("Закрыть")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
        self.setLayout(layout)
        self.load_history()

    def load_history(self):
        history = self.db.get_partner_history(self.partner_data[0])
        self.history_table.setRowCount(len(history))
        for row, record in enumerate(history):
            self.history_table.setItem(row, 0, QTableWidgetItem(record[0]))
            self.history_table.setItem(row, 1, QTableWidgetItem(record[1]))
            self.history_table.setItem(row, 2, QTableWidgetItem(str(record[2])))
            self.history_table.setItem(row, 3, QTableWidgetItem(record[3]))
            self.history_table.setItem(row, 4, QTableWidgetItem(str(record[4])))

class MaterialCalcDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Расчет количества материала")
        self.setMinimumWidth(500)
        layout = QVBoxLayout()

        # Выбор типа продукции
        prod_layout = QHBoxLayout()
        prod_label = QLabel("Тип продукции:")
        self.prod_combo = QComboBox()
        for prod in self.db.get_product_types():
            self.prod_combo.addItem(prod[1], prod[0])
        prod_layout.addWidget(prod_label)
        prod_layout.addWidget(self.prod_combo)
        layout.addLayout(prod_layout)

        # Выбор типа материала
        mat_layout = QHBoxLayout()
        mat_label = QLabel("Тип материала:")
        self.mat_combo = QComboBox()
        for mat in self.db.get_material_types():
            self.mat_combo.addItem(mat[1], mat[0])
        mat_layout.addWidget(mat_label)
        mat_layout.addWidget(self.mat_combo)
        layout.addLayout(mat_layout)

        # Количество продукции
        qty_layout = QHBoxLayout()
        qty_label = QLabel("Количество продукции:")
        self.qty_spin = QSpinBox()
        self.qty_spin.setRange(1, 1000000)
        qty_layout.addWidget(qty_label)
        qty_layout.addWidget(self.qty_spin)
        layout.addLayout(qty_layout)

        # Параметры продукции
        param1_layout = QHBoxLayout()
        param1_label = QLabel("Параметр 1:")
        self.param1_edit = QLineEdit()
        param1_layout.addWidget(param1_label)
        param1_layout.addWidget(self.param1_edit)
        layout.addLayout(param1_layout)

        param2_layout = QHBoxLayout()
        param2_label = QLabel("Параметр 2:")
        self.param2_edit = QLineEdit()
        param2_layout.addWidget(param2_label)
        param2_layout.addWidget(self.param2_edit)
        layout.addLayout(param2_layout)

        # Кнопка расчета
        calc_button = StyledButton("Рассчитать", is_primary=True)
        calc_button.clicked.connect(self.calculate)
        layout.addWidget(calc_button)

        # Результат
        self.result_label = QLabel("")
        self.result_label.setFont(QFont('Segoe UI', 12))
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def calculate(self):
        try:
            prod_id = self.prod_combo.currentData()
            mat_id = self.mat_combo.currentData()
            qty = self.qty_spin.value()
            param1 = float(self.param1_edit.text())
            param2 = float(self.param2_edit.text())
            result = self.db.calc_material(prod_id, mat_id, qty, param1, param2)
            if result == -1:
                self.result_label.setText("Ошибка: некорректные данные!")
            else:
                self.result_label.setText(f"Необходимое количество материала: {result}")
        except Exception:
            self.result_label.setText("Ошибка: введите корректные параметры!")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Система управления партнерами")
        self.setMinimumWidth(1000)
        self.setMinimumHeight(600)
        
        # Установка иконки приложения
        if os.path.exists("resources/icon.ico"):
            self.setWindowIcon(QIcon("resources/icon.ico"))
        
        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                font-family: 'Segoe UI';
            }
        """)
        
        # Основной layout
        layout = QVBoxLayout(central_widget)
        
        # Логотип
        if os.path.exists("Мастер пол.png"):
            logo_label = QLabel()
            logo_pixmap = QPixmap("Мастер пол.png")
            logo_pixmap = logo_pixmap.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(logo_pixmap)
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(logo_label)
        
        # Заголовок
        title_label = QLabel('Система управления партнёрами')
        title_label.setFont(QFont('Segoe UI', 20))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Кнопка добавления партнера
        add_button = StyledButton("Добавить партнера", is_primary=True)
        add_button.clicked.connect(self.add_partner)
        layout.addWidget(add_button)
        
        # Кнопка расчета материала
        calc_button = StyledButton("Расчет материала")
        calc_button.clicked.connect(self.open_material_calc)
        layout.addWidget(calc_button)
        
        # Создаем область прокрутки для карточек
        self.cards_scroll = QScrollArea()
        self.cards_scroll.setWidgetResizable(True)
        self.cards_scroll.setFixedHeight(500)  # Можно изменить по желанию
        layout.addWidget(self.cards_scroll)
        self.cards_container = QWidget()
        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setSpacing(10)
        self.cards_scroll.setWidget(self.cards_container)

        self.load_partners()
    
    def load_partners(self):
        # --- Очистка layout карточек перед повторным заполнением ---
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        partners = self.db.get_partners()
        for partner in partners:
            card = QFrame()
            card.setFrameShape(QFrame.Shape.Box)
            card.setStyleSheet("QFrame { background: white; border: 1px solid #bbb; border-radius: 5px; }")
            card_layout = QHBoxLayout(card)

            # --- Левая часть карточки: информация о партнере ---
            info_layout = QVBoxLayout()
            title = QLabel(f"{partner[1]} | {partner[2]}")
            title.setFont(QFont('Segoe UI', 12, QFont.Weight.Bold))
            title.setStyleSheet("border: none;")
            info_layout.addWidget(title)
            director_label = QLabel(f"{partner[3]}")
            director_label.setStyleSheet("border: none;")
            info_layout.addWidget(director_label)
            phone_label = QLabel(f"{partner[5]}")
            phone_label.setStyleSheet("border: none;")
            info_layout.addWidget(phone_label)
            rating_label = QLabel(f"Рейтинг: {partner[8]}")
            rating_label.setStyleSheet("border: none;")
            info_layout.addWidget(rating_label)
            info_layout.setSpacing(2)
            card_layout.addLayout(info_layout)

            # --- Правая часть карточки: процент скидки и кнопка истории ---
            right_layout = QVBoxLayout()
            # Получаем скидку по общему количеству реализованной продукции (см. database.py)
            percent = self.db.get_partner_discount(partner[0])
            percent_label = QLabel(f"{percent}%")
            percent_label.setFont(QFont('Segoe UI', 14))
            percent_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
            percent_label.setStyleSheet("border: none;")
            right_layout.addWidget(percent_label)
            history_btn = StyledButton("История")
            history_btn.clicked.connect(lambda checked, p=partner: self.show_history(p))
            right_layout.addWidget(history_btn)
            right_layout.addStretch()
            card_layout.addLayout(right_layout)

            # --- Открытие окна редактирования по клику на карточку ---
            card.mousePressEvent = lambda event, p=partner: self.edit_partner(p)
            self.cards_layout.addWidget(card)
        self.cards_layout.addStretch()  # Для прилипания карточек к верху

    def add_partner(self):
        dialog = PartnerDialog(self)
        if dialog.exec():
            self.load_partners()
    
    def edit_partner(self, partner_data):
        dialog = PartnerDialog(self, partner_data)
        if dialog.exec():
            self.load_partners()
    
    def show_history(self, partner_data):
        dialog = HistoryDialog(self, partner_data)
        dialog.exec()

    def open_material_calc(self):
        dialog = MaterialCalcDialog(self.db, self)
        dialog.exec()

    def get_partner_discount(self, partner_id):
        history = self.db.get_partner_history(partner_id)
        if not history:
            return 0
        return max([h[5] for h in history])

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 