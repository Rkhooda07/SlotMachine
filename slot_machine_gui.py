import sys
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QLabel, QSpinBox, 
                           QMessageBox, QGridLayout, QInputDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Constants from original game
MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1
ROWS = 3
COLS = 3

symbol_count = {
    "🍒": 3,
    "💸": 4,
    " 7": 5,
    "🎱": 6
}

symbol_value = {
    "🍒": 5,
    "💸": 4,
    " 7": 3,
    "🎱": 2
}

class SlotMachine(QMainWindow):
    def __init__(self):
        super().__init__()
        self.balance = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Slot Machine')
        self.setStyleSheet("background-color: #2b2b2b; color: white;")
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Balance display
        self.balance_label = QLabel(f'Balance: ${self.balance}')
        self.balance_label.setAlignment(Qt.AlignCenter)
        self.balance_label.setFont(QFont('Arial', 16))
        self.balance_label.setStyleSheet("color: #00ff00; padding: 10px;")
        layout.addWidget(self.balance_label)