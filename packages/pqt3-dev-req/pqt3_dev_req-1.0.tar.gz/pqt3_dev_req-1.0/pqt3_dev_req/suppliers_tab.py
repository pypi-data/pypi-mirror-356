from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QComboBox, QTableWidget, QTableWidgetItem,
                            QHeaderView, QMessageBox, QLineEdit, QPushButton)
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from database_operations import (get_all_materials, 
                                        get_suppliers_for_material,
                                        calculate_product_count,
                                        get_product_types)

class SuppliersTab(QWidget):
    def __init__(self, db_connection):
        super().__init__()
        self.db_connection = db_connection
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout(self)
        
        self.material_combo = QComboBox()
        self.material_combo.currentIndexChanged.connect(self.load_suppliers)
        layout.addWidget(QLabel("Выберите материал:"))
        layout.addWidget(self.material_combo)
        
        self.suppliers_table = QTableWidget()
        self.suppliers_table.setColumnCount(4)
        self.suppliers_table.setHorizontalHeaderLabels([
            "Поставщик", "Тип", "Рейтинг", "Дата начала работы"
        ])
        self.suppliers_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.suppliers_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.suppliers_table)
        
        calc_layout = QHBoxLayout()
        calc_layout.addWidget(QLabel("Калькулятор продукции:"))
        
        self.product_type_combo = QComboBox()
        self.param1_edit = QLineEdit()
        self.param1_edit.setPlaceholderText("Параметр 1")
        self.param2_edit = QLineEdit()
        self.param2_edit.setPlaceholderText("Параметр 2")
        self.qty_edit = QLineEdit()
        self.qty_edit.setPlaceholderText("Кол-во сырья")
        
        self.calc_button = QPushButton("Рассчитать")
        self.calc_button.setStyleSheet("background-color: #2D6033; color: white;")
        self.calc_button.clicked.connect(self.calculate_product)
        
        self.result_label = QLabel()
        
        calc_layout.addWidget(self.product_type_combo)
        calc_layout.addWidget(self.param1_edit)
        calc_layout.addWidget(self.param2_edit)
        calc_layout.addWidget(self.qty_edit)
        calc_layout.addWidget(self.calc_button)
        calc_layout.addWidget(self.result_label)
        layout.addLayout(calc_layout)
        
        self.load_materials()
        self.load_product_types()
    
    def load_materials(self):
        try:
            materials = get_all_materials(self.db_connection)
            self.material_combo.clear()
            for material in materials:
                self.material_combo.addItem(
                    f"{material['material_name']} ({material['type_name']})", 
                    material['id']
                )
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Ошибка", 
                f"Не удалось загрузить материалы:\n{str(e)}",
                QMessageBox.Ok
            )
    
    def load_product_types(self):
        try:
            product_types = get_product_types(self.db_connection)
            self.product_type_combo.clear()
            for pt in product_types:
                self.product_type_combo.addItem(
                    f"{pt['product_type']} (коэф. {pt['type_coefficient']})", 
                    pt['id']
                )
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Ошибка", 
                f"Не удалось загрузить типы продукции:\n{str(e)}",
                QMessageBox.Ok
            )
    
    def load_suppliers(self):
        material_id = self.material_combo.currentData()
        if not material_id:
            return
            
        try:
            suppliers = get_suppliers_for_material(self.db_connection, material_id)
            self.suppliers_table.setRowCount(len(suppliers))
            
            for row, supplier in enumerate(suppliers):
                self.suppliers_table.setItem(row, 0, QTableWidgetItem(supplier['supplier_name']))
                self.suppliers_table.setItem(row, 1, QTableWidgetItem(supplier['supplier_type']))
                
                rating_item = QTableWidgetItem(str(supplier['rating']))
                if supplier['rating'] is not None:
                    if supplier['rating'] >= 4.5:
                        rating_item.setBackground(QBrush(QColor("#BBD9B2")))
                    elif supplier['rating'] <= 3.0:
                        rating_item.setBackground(QBrush(QColor("#FFCCCB")))
                self.suppliers_table.setItem(row, 2, rating_item)
                
                self.suppliers_table.setItem(row, 3, QTableWidgetItem(supplier['start_date']))
            
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Ошибка", 
                f"Не удалось загрузить поставщиков:\n{str(e)}",
                QMessageBox.Ok
            )
    
    def calculate_product(self):
        try:
            material_id = self.material_combo.currentData()
            product_type_id = self.product_type_combo.currentData()
            param1 = float(self.param1_edit.text())
            param2 = float(self.param2_edit.text())
            qty = int(self.qty_edit.text())
            
            if param1 <= 0 or param2 <= 0 or qty <= 0:
                raise ValueError("Параметры должны быть положительными числами")
            
            result = calculate_product_count(
                self.db_connection,
                product_type_id,
                material_id,
                qty,
                param1,
                param2
            )
            
            if result == -1:
                self.result_label.setText("Ошибка: неверные входные данные")
                self.result_label.setStyleSheet("color: red;")
            else:
                self.result_label.setText(f"Можно произвести: {result} единиц")
                self.result_label.setStyleSheet("color: #2D6033;")
                
        except ValueError as e:
            QMessageBox.warning(
                self,
                "Ошибка ввода",
                f"Некорректные данные:\n{str(e)}",
                QMessageBox.Ok
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка расчета",
                f"Не удалось выполнить расчет:\n{str(e)}",
                QMessageBox.Ok
            )