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

        # Slot display grid
        self.slot_grid = QGridLayout()
        self.slot_labels = []
        slots = self.get_spin()  # Get initial random symbols
        for i in range(ROWS):
            row_labels = []
            for j in range(COLS):
                label = QLabel(slots[j][i])  # Set initial random symbol
                label.setFont(QFont('Arial', 24))
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet("background-color: #3b3b3b; border-radius: 10px; padding: 20px;")
                self.slot_grid.addWidget(label, i, j)
                row_labels.append(label)
            self.slot_labels.append(row_labels)
        
        grid_widget = QWidget()
        grid_widget.setLayout(self.slot_grid)
        layout.addWidget(grid_widget)

        # Controls
        controls_layout = QHBoxLayout()
        
        # Lines selection
        self.lines_spin = QSpinBox()
        self.lines_spin.setRange(1, MAX_LINES)
        self.lines_spin.setValue(1)
        self.lines_spin.setStyleSheet("background-color: #3b3b3b; padding: 5px;")
        controls_layout.addWidget(QLabel("Lines:"))
        controls_layout.addWidget(self.lines_spin)
        
        # Bet amount selection
        self.bet_spin = QSpinBox()
        self.bet_spin.setRange(MIN_BET, MAX_BET)
        self.bet_spin.setValue(MIN_BET)
        self.bet_spin.setStyleSheet("background-color: #3b3b3b; padding: 5px;")
        controls_layout.addWidget(QLabel("Bet per line:"))
        controls_layout.addWidget(self.bet_spin)
        
        layout.addLayout(controls_layout)