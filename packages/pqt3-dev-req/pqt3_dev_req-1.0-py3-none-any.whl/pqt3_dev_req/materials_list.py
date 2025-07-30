from math import ceil
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, 
                            QMessageBox, QGridLayout, QSpacerItem, QSizePolicy)
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt, pyqtSignal
from database_operations import get_all_materials

class MaterialsList(QWidget):
    materialClicked = pyqtSignal(int)
    
    def __init__(self, db_connection):
        super().__init__()
        self.db_connection = db_connection
        self.setMinimumWidth(600)
        self.initUI()
    
    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(10, 10, 10, 10) 
        self.refresh_data()
    
    def refresh_data(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        try:
            materials = get_all_materials(self.db_connection)
            
            if not materials:
                label = QLabel("Нет данных о материалах")
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet("font-size: 16pt; color: #555;")
                self.layout.addWidget(label)
                return
            
            for material in materials:
                self.create_material_card(material)
            
            self.layout.addStretch()
        
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Ошибка", 
                f"Не удалось загрузить данные:\n{str(e)}\n\nПопробуйте перезапустить приложение.",
                QMessageBox.Ok
            )
    
    def create_material_card(self, material):
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setLineWidth(1)
        card.setMinimumHeight(160)  # Достаточная высота
        card.setCursor(Qt.PointingHandCursor)
        
        palette = card.palette()
        palette.setColor(QPalette.Background, QColor("#BBD9B2"))
        card.setAutoFillBackground(True)
        card.setPalette(palette)
        
        main_layout = QVBoxLayout(card)
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(15, 15, 15, 15)  # Внутренние отступы
        
        title = QLabel(f"{material['type_name']} | {material['material_name']}")
        title.setStyleSheet("""
            font-weight: bold; 
            font-size: 16px;
            margin-bottom: 8px;
        """)
        main_layout.addWidget(title)
        
        grid = QGridLayout()
        grid.setVerticalSpacing(5)
        grid.setHorizontalSpacing(20)
        
        min_lbl = QLabel("Минимальное количество:")
        min_val = QLabel(f"{material['min_quantity']} {material['unit_of_measure']}")
        grid.addWidget(min_lbl, 0, 0)
        grid.addWidget(min_val, 0, 1)
        
        stock_lbl = QLabel("На складе:")
        stock_val = QLabel(f"{material['stock_quantity']} {material['unit_of_measure']}")
        grid.addWidget(stock_lbl, 1, 0)
        grid.addWidget(stock_val, 1, 1)
        
        price_lbl = QLabel("Цена:")
        price_val = QLabel(f"{material['unit_price']:.2f}р / {material['unit_of_measure']}")
        grid.addWidget(price_lbl, 2, 0)
        grid.addWidget(price_val, 2, 1)
        
        main_layout.addLayout(grid)
        
        shortage = max(0, material['min_quantity'] - material['stock_quantity'])
        
        if shortage > 0:
            packages_needed = ceil(shortage / material['package_quantity'])
            purchase_qty = packages_needed * material['package_quantity']
            batch_cost = purchase_qty * material['unit_price']
            
            batch_text = (f"Требуется докупить: {purchase_qty} {material['unit_of_measure']}\n"
                         f"({packages_needed} упаковок)\n"
                         f"Стоимость закупки: {batch_cost:.2f}р")
            
            batch_info = QLabel(batch_text)
            batch_info.setStyleSheet("""
                color: #B71C1C;
                font-weight: bold;
                background-color: #FFEBEE;
                padding: 8px;
                border-radius: 5px;
                margin-top: 10px;
            """)
        else:
            batch_info = QLabel(f"Стоимость партии: 0.00р\n(запасов достаточно)")
            batch_info.setStyleSheet("""
                color: #1B5E20;
                font-weight: bold;
                background-color: #E8F5E9;
                padding: 8px;
                border-radius: 5px;
                margin-top: 10px;
            """)
        
        batch_info.setWordWrap(True)
        main_layout.addWidget(batch_info)
        
        self.layout.addWidget(card)
        
        card.mousePressEvent = lambda event, id=material['id']: self.on_material_clicked(event, id)
    
    def on_material_clicked(self, event, material_id):
        self.materialClicked.emit(material_id)