from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QComboBox, QPushButton, QMessageBox,
                            QDoubleSpinBox, QFormLayout)
from PyQt5.QtCore import Qt, pyqtSignal
from database_operations import (get_material_by_id, get_material_types,
                                        insert_material, update_material)

class MaterialForm(QWidget):
    materialSaved = pyqtSignal()
    
    def __init__(self, db_connection, material_id=None):
        super().__init__()
        self.db_connection = db_connection
        self.material_id = material_id
        self.setWindowTitle("Редактировать материал" if material_id else "Добавить материал")
        self.setGeometry(200, 200, 400, 400)
        
        self.initUI()
        self.load_data()
    
    def initUI(self):
        layout = QVBoxLayout(self)
        
        form_layout = QFormLayout()
        
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Введите наименование материала")
        form_layout.addRow("Наименование:", self.name_edit)
        
        self.type_combo = QComboBox()
        try:
            types = get_material_types(self.db_connection)
            for type in types:
                self.type_combo.addItem(type['material_type'], type['id'])
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Ошибка", 
                f"Не удалось загрузить типы материалов:\n{str(e)}",
                QMessageBox.Ok
            )
        form_layout.addRow("Тип материала:", self.type_combo)
        
        self.stock_qty_edit = QDoubleSpinBox()
        self.stock_qty_edit.setMinimum(0)
        self.stock_qty_edit.setMaximum(999999)
        self.stock_qty_edit.setDecimals(3)
        form_layout.addRow("Количество на складе:", self.stock_qty_edit)
        
        self.unit_edit = QLineEdit()
        self.unit_edit.setPlaceholderText("кг, л, шт и т.д.")
        form_layout.addRow("Единица измерения:", self.unit_edit)
        
        self.package_qty_edit = QDoubleSpinBox()
        self.package_qty_edit.setMinimum(0.001)
        self.package_qty_edit.setMaximum(999999)
        self.package_qty_edit.setDecimals(3)
        form_layout.addRow("Количество в упаковке:", self.package_qty_edit)
        
        self.min_qty_edit = QDoubleSpinBox()
        self.min_qty_edit.setMinimum(0)
        self.min_qty_edit.setMaximum(999999)
        self.min_qty_edit.setDecimals(3)
        form_layout.addRow("Минимальное количество:", self.min_qty_edit)
        
        self.price_edit = QDoubleSpinBox()
        self.price_edit.setMinimum(0.01)
        self.price_edit.setMaximum(999999)
        self.price_edit.setDecimals(2)
        self.price_edit.setPrefix("₽ ")
        form_layout.addRow("Цена единицы:", self.price_edit)
        
        layout.addLayout(form_layout)
        
        buttons_layout = QHBoxLayout()
        
        save_button = QPushButton("Сохранить")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #2D6033;
                color: white;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3E7A47;
            }
        """)
        save_button.clicked.connect(self.save_material)
        buttons_layout.addWidget(save_button)
        
        cancel_button = QPushButton("Отмена")
        cancel_button.setStyleSheet("padding: 8px;")
        cancel_button.clicked.connect(self.close)
        buttons_layout.addWidget(cancel_button)
        
        layout.addLayout(buttons_layout)
    
    def load_data(self):
        if self.material_id:
            try:
                material = get_material_by_id(self.db_connection, self.material_id)
                if material:
                    self.name_edit.setText(material['material_name'])
                    
                    index = self.type_combo.findData(material['material_type_id'])
                    if index >= 0:
                        self.type_combo.setCurrentIndex(index)
                    
                    self.stock_qty_edit.setValue(material['stock_quantity'])
                    self.unit_edit.setText(material['unit_of_measure'])
                    self.package_qty_edit.setValue(material['package_quantity'])
                    self.min_qty_edit.setValue(material['min_quantity'])
                    self.price_edit.setValue(material['unit_price'])
            except Exception as e:
                QMessageBox.critical(
                    self, 
                    "Ошибка", 
                    f"Не удалось загрузить данные материала:\n{str(e)}",
                    QMessageBox.Ok
                )
                self.close()
    
    def save_material(self):
        try:
            data = {
                'material_name': self.name_edit.text().strip(),
                'material_type_id': self.type_combo.currentData(),
                'stock_quantity': self.stock_qty_edit.value(),
                'unit_of_measure': self.unit_edit.text().strip(),
                'package_quantity': self.package_qty_edit.value(),
                'min_quantity': self.min_qty_edit.value(),
                'unit_price': self.price_edit.value()
            }
            
            if not data['material_name']:
                QMessageBox.warning(
                    self, 
                    "Не заполнено поле", 
                    "Пожалуйста, укажите наименование материала",
                    QMessageBox.Ok
                )
                return
            
            if not data['unit_of_measure']:
                QMessageBox.warning(
                    self, 
                    "Не заполнено поле", 
                    "Пожалуйста, укажите единицу измерения",
                    QMessageBox.Ok
                )
                return
            
            if self.material_id:
                data['id'] = self.material_id
                update_material(self.db_connection, data)
                QMessageBox.information(
                    self, 
                    "Успешно", 
                    "Данные материала успешно обновлены",
                    QMessageBox.Ok
                )
            else:
                insert_material(self.db_connection, data)
                QMessageBox.information(
                    self, 
                    "Успешно", 
                    "Материал успешно добавлен",
                    QMessageBox.Ok
                )
            
            self.materialSaved.emit()
            self.close()
            
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Ошибка", 
                f"Не удалось сохранить материал:\n{str(e)}",
                QMessageBox.Ok
            )