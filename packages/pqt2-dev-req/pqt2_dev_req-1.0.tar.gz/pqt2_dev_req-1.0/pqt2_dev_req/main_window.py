from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QScrollArea, 
                            QPushButton, QMessageBox)
from materials_list import MaterialsList
from material_form import MaterialForm

class MainWindow(QMainWindow):
    def __init__(self, db_connection):
        super().__init__()
        self.db_connection = db_connection
        self.setWindowTitle("Учет материалов")
        self.setGeometry(100, 100, 800, 600)
        
        self.current_material_id = None
        self.materials_list = None
        self.initUI()
    
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        self.materials_list = MaterialsList(self.db_connection)
        self.materials_list.materialClicked.connect(self.open_edit_form)
        scroll.setWidget(self.materials_list)
        
        layout.addWidget(scroll)
        
        add_button = QPushButton("Добавить материал")
        add_button.setStyleSheet("""
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
        add_button.clicked.connect(self.open_add_form)
        layout.addWidget(add_button)
    
    def open_add_form(self):
        self.current_material_id = None
        self.material_form = MaterialForm(self.db_connection, None)
        self.material_form.materialSaved.connect(self.refresh_materials)
        self.material_form.show()
    
    def open_edit_form(self, material_id):
        self.current_material_id = material_id
        self.material_form = MaterialForm(self.db_connection, material_id)
        self.material_form.materialSaved.connect(self.refresh_materials)
        self.material_form.show()
    
    def refresh_materials(self):
        self.materials_list.refresh_data()