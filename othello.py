# import
import random

# 定数とか.
BOARD_WIDTH = 8
BOARD_HEIGHT = 8
BLACK = 1
WHITE = 0

# 8近傍.
dx8 = [-1,-1,-1,0,0,1,1,1]
dy8 = [-1,0,1,-1,1,-1,0,1]

# リセット.
def reset(board):
  for i in range(BOARD_WIDTH):
    for j in range(BOARD_HEIGHT):
      board[i][j] = '-'
  board[int(BOARD_WIDTH/2-1)][int(BOARD_HEIGHT/2-1)] = 'o'
  board[int(BOARD_WIDTH/2-1)][int(BOARD_HEIGHT/2)] = 'x'
  board[int(BOARD_WIDTH/2)][int(BOARD_HEIGHT/2-1)] = 'x'
  board[int(BOARD_WIDTH/2)][int(BOARD_HEIGHT/2)] = 'o'
  return board

# 描画.
def print_board(board):
  print("  ",end = '')
  for k in range(BOARD_WIDTH):
    print(k+1,end = ' ')
  print()
  for i in range(BOARD_WIDTH):
    print(i+1,end = ' ')
    for j in range(BOARD_HEIGHT):
      print(board[i][j],end = ' ')
    print()

# 自分の石.
def my_stone(player):
  if (player == BLACK):
    return 'x'
  elif (player == WHITE):
    return 'o'
# 敵の石.
def enemy_stone(player):
  if (player == BLACK):
    return 'o'
  elif (player == WHITE):
    return 'x'

# 置かれているか.
def is_placed(x,y,board):
    return board[x][y] != '-'

# 範囲外か.
def is_outside(x,y):
    return not((0 <= x and x < BOARD_WIDTH) and (0 <= y and y < BOARD_HEIGHT))

# 置けるか.
def can_place(x,y,board,player):
  if (is_placed(x,y,board)):
    return False

  me = my_stone(player)
  enemy = enemy_stone(player)

  for i in range(8):
    dx = x + dx8[i]
    dy = y + dy8[i]
    if (is_outside(dx,dy)):
      continue
    if (board[dx][dy] != enemy):
      continue

    while True:
      dx += dx8[i]
      dy += dy8[i]
      if (is_outside(dx,dy)):
        break
      if (board[dx][dy] == '-'):
        break
      if (board[dx][dy] == me):
        return True
  return False

# ひっくり返せるかどうか+ひっくり返す座標.
def get_flips(x,y,board,player):
  if (is_placed(x,y,board)):
    return []

  me = my_stone(player)
  enemy = enemy_stone(player)

  flips = []
  for i in range(8):
    dx = x + dx8[i]
    dy = y + dy8[i]
    temp = []

    while not(is_outside(dx,dy)):
      if (board[dx][dy] == enemy):
        temp.append((dx,dy))
      elif (board[dx][dy] == me):
        if (len(temp) > 0):
          flips.extend(temp)
        break
      else:
        break
      dx += dx8[i]
      dy += dy8[i]

  return flips

# 置く.
def place_stone(x,y,board,player):
  flips = get_flips(x,y,board,player)
  if (len(flips) == 0):
    return False
  stone = my_stone(player)
  board[x][y] = stone
  for i,j in flips:
    board[i][j] = stone
  return True

# 合法手.
def legal_moves(board,player):
  moves = []
  for i in range(BOARD_WIDTH):
    for j in range(BOARD_HEIGHT):
      if (can_place(i,j,board,player)):
        moves.append((i,j))
  return moves

# 石の個数.
def count_stones(board):
  count_black = 0
  count_white = 0
  for i in range(BOARD_WIDTH):
    for j in range(BOARD_HEIGHT):
      if (board[i][j] == 'x'):
        count_black += 1
      elif (board[i][j] == 'o'):
        count_white += 1
  return count_black,count_white

# CPU.
def cpu_move(board,player):
  moves = legal_moves(board,player)
  return random.choice(moves)

def player_turn(board,player):
  while True:
    moves = legal_moves(board,player)
    if (len(moves) == 0):
      print("置ける場所がないためパスします")
      break
    else:
      print("置ける場所:",[(y+1,x+1) for x,y in moves])
      print("黒石(x)を置く座標を指定してください(1-8の間)、先に横の座標、次に縦の座標")
      y = int(input())-1
      x = int(input())-1
      if (is_outside(x,y)):
        print("範囲外です")
        continue
      if (place_stone(x,y,board,player)):
        break
      else:
        print("そこには置けません")
        continue



# 初期化.
board = [['-']*BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
reset(board)
# メインループ.
while True:
  print_board(board)
  # 終了判定.
  black_moves = legal_moves(board,BLACK)
  white_moves = legal_moves(board,WHITE)
  if (len(black_moves) == 0 and len(white_moves) == 0):
    break
  # 黒の番.
  player_turn(board,BLACK)

  print_board(board)

  # 白の番(player)
  # player_turn(board,WHITE)

  # 白の番(CPU).
  moves = legal_moves(board,WHITE)
  if (len(moves) == 0):
    print("CPUはパスしました")
  else:
    x,y = cpu_move(board,WHITE)
    place_stone(x,y,board,WHITE)
# 個数,勝敗判定.
black,white = count_stones(board)
print("黒:",black)
print("白:",white)

if (black > white):
  print("あなたの勝ち(黒の勝ち)")
elif (black == white):
  print("引き分け")
else:
  print("あなたの負け(白の勝ち)")
