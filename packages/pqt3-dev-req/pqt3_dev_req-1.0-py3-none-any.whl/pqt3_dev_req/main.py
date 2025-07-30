import sys
from PyQt5.QtWidgets import QApplication, QTabWidget
from PyQt5.QtGui import QIcon
from main_window import MainWindow
from suppliers_tab import SuppliersTab
from database import create_connection

def main():
    app = QApplication(sys.argv)
    
    font = app.font()
    font.setFamily("Gabriola")
    font.setPointSize(12)
    app.setFont(font)
    
    app.setWindowIcon(QIcon('icon.ico'))
    app.setApplicationName("Приложение")
    app.setApplicationDisplayName("Приложение Учета Материалов")

    conn = create_connection("demoDB.db")
    if conn is None:
        sys.exit(1)
    
    tab_widget = QTabWidget()
    
    # Вкладка материалов
    materials_tab = MainWindow(conn)
    tab_widget.addTab(materials_tab, "Материалы")
    
    # Вкладка поставщиков
    suppliers_tab = SuppliersTab(conn)
    tab_widget.addTab(suppliers_tab, "Поставщики")
    
    tab_widget.setGeometry(100, 100, 800, 600)
    tab_widget.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()