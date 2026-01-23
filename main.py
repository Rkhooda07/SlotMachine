import random

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

def get_spin(rows, cols, symbols):  
  all_symbols = []
  for symbol, symbol_count in symbols.items():
    for _ in range(symbol_count):
      all_symbols.append(symbol)

  columns = []

  for _ in range(cols):
    column = []
    current_symbols = all_symbols[:]
    for _ in range(rows):
      value = random.choice(current_symbols)
      current_symbols.remove(value)
      column.append(value)

    columns.append(column)

  return columns

def print_spin(columns):
  for row in range(len(columns[0])):
    for i, column in enumerate(columns):
      if i != len(columns) - 1:
        print(column[row], end=" | ")
      else:
        print(column[row], end="")
    print()

def check_win(columns, lines, bet , values):
  winnings = 0
  winning_lines = []
  for line in range(lines):
    symbol = columns[0][line]
    for column in columns:
      symbol_to_check = column[line]
      if symbol != symbol_to_check:
        break
    else:
      winnings += values[symbol] * bet
      winning_lines.append(line + 1)

  return winnings, winning_lines