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

        # Buttons
        button_layout = QHBoxLayout()
        
        self.deposit_btn = QPushButton('Deposit')
        self.deposit_btn.clicked.connect(self.deposit)
        self.deposit_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 15px 32px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.deposit_btn.setCursor(Qt.PointingHandCursor)

        self.spin_btn = QPushButton('SPIN')
        self.spin_btn.clicked.connect(self.spin)
        self.spin_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                border: none;
                color: white;
                padding: 15px 32px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        self.spin_btn.setCursor(Qt.PointingHandCursor)
        

        button_layout.addWidget(self.deposit_btn)
        button_layout.addWidget(self.spin_btn)
        layout.addLayout(button_layout)

        # Result label
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("color: #ffd700; padding: 10px;")
        layout.addWidget(self.result_label)
        
        self.setMinimumSize(400, 500)
        self.center()
        
    def center(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2,
                 (screen.height() - size.height()) // 2)
        
    def deposit(self):
        amount, ok = QInputDialog.getInt(
            self, 'Deposit',
            'Enter deposit amount:',
            value=100, min=1, max=10000
        )
        if ok:
            self.balance += amount
            self.balance_label.setText(f'Balance: ${self.balance}')
            self.result_label.setText(f'Deposited ${amount} successfully!')

    def get_spin(self):
        all_symbols = []
        for symbol, count in symbol_count.items():
            all_symbols.extend([symbol] * count)

        columns = []
        for _ in range(COLS):
            column = random.sample(all_symbols, ROWS)
            columns.append(column)

        return columns
    
    def check_win(self, columns, lines, bet):
        winnings = 0
        winning_lines = []
        for line in range(lines):
            symbol = columns[0][line]
            for column in columns:
                symbol_to_check = column[line]
                if symbol != symbol_to_check:
                    break
            else:
                winnings += symbol_value[symbol] * bet
                winning_lines.append(line + 1)
        return winnings, winning_lines
    
    def spin(self):
        lines = self.lines_spin.value()
        bet = self.bet_spin.value()
        total_bet = bet * lines
        
        if total_bet > self.balance:
            QMessageBox.warning(self, 'Insufficient Funds',
                              f'You need ${total_bet} to play. Current balance: ${self.balance}')
            return
        
        self.balance -= total_bet
        slots = self.get_spin()
        
        # Update the display with symbols
        for i in range(ROWS):
            for j in range(COLS):
                self.slot_labels[i][j].setText(slots[j][i])
                
        winnings, winning_lines = self.check_win(slots, lines, bet)
        self.balance += winnings
        
        # Update balance and result
        self.balance_label.setText(f'Balance: ${self.balance}')
        if winning_lines:
            self.result_label.setText(
                f'You won ${winnings} on lines {", ".join(map(str, winning_lines))}!')
        else:
            self.result_label.setText('Try again!')