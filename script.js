// Lig4 (Conecta 4) 

const ROWS = 6;
const COLS = 7;
const MAX_DEPTH = 4; // IA mais forte = valor maior, mas mais lenta

let board = [];
let currentPlayer = 1; // 1 = humano, 2 = IA
let gameOver = false;

const boardDiv = document.getElementById('board');
const messageDiv = document.getElementById('message');
const restartBtn = document.getElementById('restart');

function criarTabuleiro() {
  board = [];
  for (let r = 0; r < ROWS; r++) {
    board.push(Array(COLS).fill(0));
  }
}

function renderBoard() {
  boardDiv.innerHTML = '';
  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++) {
      const cell = document.createElement('div');
      cell.classList.add('cell');
      if (board[r][c] === 1) cell.classList.add('player1');
      if (board[r][c] === 2) cell.classList.add('player2');
      cell.dataset.row = r;
      cell.dataset.col = c;
      cell.addEventListener('click', () => handleCellClick(c));
      cell.innerHTML = board[r][c] === 1 ? '★' : (board[r][c] === 2 ? '●' : '');
      boardDiv.appendChild(cell);
    }
  }
}

function colunaValida(col) {
  return board[0][col] === 0;
}

function fazerJogada(col, jogador) {
  for (let r = ROWS - 1; r >= 0; r--) {
    if (board[r][col] === 0) {
      board[r][col] = jogador;
      return true;
    }
  }
  return false;
}

function desfazerJogada(col) {
  for (let r = 0; r < ROWS; r++) {
    if (board[r][col] !== 0) {
      board[r][col] = 0;
      return;
    }
  }
}

function verificarVencedor(tab, jogador) {
  // Horizontal
  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS - 3; c++) {
      if ([0,1,2,3].every(i => tab[r][c+i] === jogador)) return true;
    }
  }
  // Vertical
  for (let c = 0; c < COLS; c++) {
    for (let r = 0; r < ROWS - 3; r++) {
      if ([0,1,2,3].every(i => tab[r+i][c] === jogador)) return true;
    }
  }
  // Diagonal /
  for (let r = 3; r < ROWS; r++) {
    for (let c = 0; c < COLS - 3; c++) {
      if ([0,1,2,3].every(i => tab[r-i][c+i] === jogador)) return true;
    }
  }
  // Diagonal \
  for (let r = 0; r < ROWS - 3; r++) {
    for (let c = 0; c < COLS - 3; c++) {
      if ([0,1,2,3].every(i => tab[r+i][c+i] === jogador)) return true;
    }
  }
  return false;
}

function tabuleiroCheio(tab) {
  return tab[0].every(cell => cell !== 0);
}

function avaliarJanela(janela, jogador) {
  let pontuacao = 0;
  const oponente = jogador === 2 ? 1 : 2;
  const countJ = janela.filter(x => x === jogador).length;
  const countO = janela.filter(x => x === oponente).length;
  const count0 = janela.filter(x => x === 0).length;

  if (countJ === 4) pontuacao += 100;
  else if (countJ === 3 && count0 === 1) pontuacao += 5;
  else if (countJ === 2 && count0 === 2) pontuacao += 2;
  if (countO === 3 && count0 === 1) pontuacao -= 4;
  return pontuacao;
}

function avaliarTabuleiro(tab, jogador) {
  let pontuacao = 0;
  // Centro
  const centro = [];
  for (let r = 0; r < ROWS; r++) centro.push(tab[r][Math.floor(COLS/2)]);
  pontuacao += centro.filter(x => x === jogador).length * 3;

  // Horizontal
  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS - 3; c++) {
      const janela = [tab[r][c], tab[r][c+1], tab[r][c+2], tab[r][c+3]];
      pontuacao += avaliarJanela(janela, jogador);
    }
  }
  // Vertical
  for (let c = 0; c < COLS; c++) {
    for (let r = 0; r < ROWS - 3; r++) {
      const janela = [tab[r][c], tab[r+1][c], tab[r+2][c], tab[r+3][c]];
      pontuacao += avaliarJanela(janela, jogador);
    }
  }
  // Diagonal /
  for (let r = 3; r < ROWS; r++) {
    for (let c = 0; c < COLS - 3; c++) {
      const janela = [tab[r][c], tab[r-1][c+1], tab[r-2][c+2], tab[r-3][c+3]];
      pontuacao += avaliarJanela(janela, jogador);
    }
  }
  // Diagonal \
  for (let r = 0; r < ROWS - 3; r++) {
    for (let c = 0; c < COLS - 3; c++) {
      const janela = [tab[r][c], tab[r+1][c+1], tab[r+2][c+2], tab[r+3][c+3]];
      pontuacao += avaliarJanela(janela, jogador);
    }
  }
  return pontuacao;
}

function copiarTabuleiro(tab) {
  return tab.map(row => row.slice());
}

function minimax(tab, profundidade, alpha, beta, maximizar, jogador) {
  const oponente = jogador === 2 ? 1 : 2;
  if (verificarVencedor(tab, jogador)) return [null, 1000000];
  if (verificarVencedor(tab, oponente)) return [null, -1000000];
  if (tabuleiroCheio(tab) || profundidade === 0) return [null, avaliarTabuleiro(tab, jogador)];

  if (maximizar) {
    let valorMax = -Infinity;
    let melhorCol = null;
    for (let col = 0; col < COLS; col++) {
      if (tab[0][col] === 0) {
        // Simula jogada
        for (let r = ROWS - 1; r >= 0; r--) {
          if (tab[r][col] === 0) {
            tab[r][col] = jogador;
            break;
          }
        }
        const [_, valor] = minimax(tab, profundidade - 1, alpha, beta, false, jogador);
        // Desfaz jogada
        for (let r = 0; r < ROWS; r++) {
          if (tab[r][col] !== 0) {
            tab[r][col] = 0;
            break;
          }
        }
        if (valor > valorMax) {
          valorMax = valor;
          melhorCol = col;
        }
        alpha = Math.max(alpha, valor);
        if (alpha >= beta) break;
      }
    }
    return [melhorCol, valorMax];
  } else {
    let valorMin = Infinity;
    let melhorCol = null;
    for (let col = 0; col < COLS; col++) {
      if (tab[0][col] === 0) {
        // Simula jogada
        for (let r = ROWS - 1; r >= 0; r--) {
          if (tab[r][col] === 0) {
            tab[r][col] = oponente;
            break;
          }
        }
        const [_, valor] = minimax(tab, profundidade - 1, alpha, beta, true, jogador);
        // Desfaz jogada
        for (let r = 0; r < ROWS; r++) {
          if (tab[r][col] !== 0) {
            tab[r][col] = 0;
            break;
          }
        }
        if (valor < valorMin) {
          valorMin = valor;
          melhorCol = col;
        }
        beta = Math.min(beta, valor);
        if (alpha >= beta) break;
      }
    }
    return [melhorCol, valorMin];
  }
}

function melhorJogada(jogador) {
  const tabCopia = copiarTabuleiro(board);
  const [col, _] = minimax(tabCopia, MAX_DEPTH, -Infinity, Infinity, true, jogador);
  return col;
}

function handleCellClick(col) {
  if (gameOver || currentPlayer !== 1) return;
  if (!colunaValida(col)) return;
  fazerJogada(col, 1);
  renderBoard();
  if (verificarVencedor(board, 1)) {
    messageDiv.textContent = "Parabéns! Você venceu!";
    gameOver = true;
    return;
  }
  if (tabuleiroCheio(board)) {
    messageDiv.textContent = "Empate!";
    gameOver = true;
    return;
  }
  currentPlayer = 2;
  messageDiv.textContent = "Computador pensando...";
  setTimeout(() => {
    const colIA = melhorJogada(2);
    if (colIA !== null && colunaValida(colIA)) {
      fazerJogada(colIA, 2);
      renderBoard();
      if (verificarVencedor(board, 2)) {
        messageDiv.textContent = "Computador venceu!";
        gameOver = true;
        return;
      }
      if (tabuleiroCheio(board)) {
        messageDiv.textContent = "Empate!";
        gameOver = true;
        return;
      }
    }
    currentPlayer = 1;
    messageDiv.textContent = "Sua vez!";
  }, 400);
}

function reiniciarJogo() {
  criarTabuleiro();
  currentPlayer = 1;
  gameOver = false;
  messageDiv.textContent = "Sua vez!";
  renderBoard();
}

restartBtn.addEventListener('click', reiniciarJogo);

// Inicialização
criarTabuleiro();
renderBoard();
messageDiv.textContent = "Sua vez!";
