// Constants matching the Python version
const MAX_LINES = 3;
const MAX_BET = 100;
const MIN_BET = 1;
const ROWS = 3;
const COLS = 3;

const SYMBOL_COUNT = {
  "🍒": 3,
  "💸": 4,
  "7️⃣": 5, // Using 7️⃣ emoji for better look than " 7"
  "🎱": 6
};

const SYMBOL_VALUE = {
  "🍒": 5,
  "💸": 4,
  "7️⃣": 3,
  "🎱": 2
};

// State
let balance = 0;
let isSpinning = false;

// DOM Elements
const balanceDisplay = document.getElementById('balance-display');
const linesSelect = document.getElementById('lines-select');
const betInput = document.getElementById('bet-input');
const spinBtn = document.getElementById('spin-btn');
const depositBtn = document.getElementById('deposit-btn');
const messageDisplay = document.getElementById('message-display');
const reels = Array.from({ length: COLS }, (_, col) =>
  Array.from({ length: ROWS }, (_, row) => document.getElementById(`reel-${col}-${row}`))
);

// Initialization
function updateBalance(amount) {
  balance += amount;
  balanceDisplay.textContent = `$${balance}`;

  // Animate balance change
  balanceDisplay.style.transform = 'scale(1.1)';
  setTimeout(() => balanceDisplay.style.transform = 'scale(1)', 200);
}

function showMessage(text, isWin = false) {
  messageDisplay.textContent = text;
  messageDisplay.className = 'message-display' + (isWin ? ' win-message' : '');
}

function getSpin() {
  const allSymbols = [];
  for (const [symbol, count] of Object.entries(SYMBOL_COUNT)) {
    for (let i = 0; i < count; i++) {
      allSymbols.push(symbol);
    }
  }

  const columns = [];
  for (let i = 0; i < COLS; i++) {
    const column = [];
    // Sample without replacement (like random.sample does? Actually sample usually means with replacement if not specified, but Python Version used random.sample(all_symbols, ROWS))
    // random.sample is actually without replacement.
    const pool = [...allSymbols];
    for (let j = 0; j < ROWS; j++) {
      const randomIndex = Math.floor(Math.random() * pool.length);
      column.push(pool.splice(randomIndex, 1)[0]);
    }
    columns.push(column);
  }
  return columns;
}

function checkWin(columns, lines, bet) {
  let winnings = 0;
  const winningLines = [];

  for (let line = 0; line < lines; line++) {
    const symbol = columns[0][line];
    let allSame = true;
    for (let col = 0; col < COLS; col++) {
      if (columns[col][line] !== symbol) {
        allSame = false;
        break;
      }
    }
    if (allSame) {
      winnings += SYMBOL_VALUE[symbol] * bet;
      winningLines.push(line + 1);
    }
  }
  return { winnings, winningLines };
}

async function spin() {
  if (isSpinning) return;

  const lines = parseInt(linesSelect.value);
  const bet = parseInt(betInput.value);
  const totalBet = lines * bet;

  if (isNaN(totalBet) || totalBet <= 0) {
    showMessage('Please enter a valid bet!');
    return;
  }

  if (totalBet > balance) {
    showMessage(`Balance too low! Need $${totalBet}`);
    return;
  }

  // Start spin
  isSpinning = true;
  spinBtn.disabled = true;
  updateBalance(-totalBet);
  showMessage('Spinning...');

  // Visual effect: Random symbols spinning
  const spinDuration = 1000;
  const intervalTime = 100;
  const steps = spinDuration / intervalTime;

  // Animate reels
  const animationInterval = setInterval(() => {
    const tempSlots = getSpin();
    for (let col = 0; col < COLS; col++) {
      for (let row = 0; row < ROWS; row++) {
        reels[col][row].textContent = tempSlots[col][row];
        reels[col][row].classList.add('spinning');
      }
    }
  }, intervalTime);

  // Final result
  setTimeout(() => {
    clearInterval(animationInterval);
    const finalSlots = getSpin();

    // Update display with final symbols
    for (let col = 0; col < COLS; col++) {
      for (let row = 0; row < ROWS; row++) {
        reels[col][row].textContent = finalSlots[col][row];
        reels[col][row].classList.remove('spinning');
      }
    }

    const { winnings, winningLines } = checkWin(finalSlots, lines, bet);

    if (winnings > 0) {
      updateBalance(winnings);
      showMessage(`🎊 JACKPOT! You won $${winnings} on lines ${winningLines.join(', ')}!`, true);
    } else {
      showMessage('Better luck next time! Try again.');
    }

    isSpinning = false;
    spinBtn.disabled = false;
  }, spinDuration);
}

function deposit() {
  const amount = prompt('Enter deposit amount (Max $10,000):', '100');
  const parsedAmount = parseInt(amount);

  if (isNaN(parsedAmount) || parsedAmount <= 0) {
    alert('Please enter a valid number.');
    return;
  }

  if (parsedAmount > 10000) {
    alert('Max deposit is $10,000');
    return;
  }

  updateBalance(parsedAmount);
  showMessage(`Successfully deposited $${parsedAmount}!`, true);
}

// Event Listeners
spinBtn.addEventListener('click', spin);
depositBtn.addEventListener('click', deposit);

// Initial State
updateBalance(100); // Start with $100 for better experience
showMessage('Welcome to Jackpot Slots!');
