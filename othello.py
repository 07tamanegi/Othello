# import.
import random

# 定数とか.
# 必ず偶数にすること!.
BOARD_WIDTH = 8
BOARD_HEIGHT = 8
BLACK = 1
WHITE = 0
ONEPLAYER = 0
TWOPLAYER = 1

# 8近傍.
dr8 = [-1,-1,-1,0,0,1,1,1]
dc8 = [-1,0,1,-1,1,-1,0,1]

# リセット.
def reset(board):
  for i in range(BOARD_WIDTH):
    for j in range(BOARD_HEIGHT):
      board[j][i] = '・'
  board[int(BOARD_HEIGHT/2-1)][int(BOARD_WIDTH/2-1)] = '◯'
  board[int(BOARD_HEIGHT/2-1)][int(BOARD_WIDTH/2)] = '●'
  board[int(BOARD_HEIGHT/2)][int(BOARD_WIDTH/2-1)] = '●'
  board[int(BOARD_HEIGHT/2)][int(BOARD_WIDTH/2)] = '◯'
  return board

# 描画.
def print_board(board):
  print("　 ",end = '')
  for c in range(BOARD_WIDTH):
    print(c+1,end = ' ')
  print()
  for r in range(BOARD_HEIGHT):
    print(r+1,end = ' ')
    for c in range(BOARD_WIDTH):
      print(board[r][c],end = '')
    print()

# 自分の石.
def my_stone(player):
  if (player == BLACK):
    return '●'
  elif (player == WHITE):
    return '◯'
# 敵の石.
def enemy_stone(player):
  if (player == BLACK):
    return '◯'
  elif (player == WHITE):
    return '●'

# 置かれているか.
def is_placed(row,col,board):
  return board[row][col] != '・'

# 範囲外か.
def is_outside(row,col):
  return not((0 <= row and row < BOARD_HEIGHT) and (0 <= col and col < BOARD_WIDTH))

# 置けるか.
def can_place(row,col,board,player):
  if (is_placed(row,col,board)):
    return False

  me = my_stone(player)
  enemy = enemy_stone(player)

  for i in range(8):
    dr = row + dr8[i]
    dc = col + dc8[i]
    if (is_outside(dr,dc)):
      continue
    if (board[dr][dc] != enemy):
      continue

    while True:
      dr += dr8[i]
      dc += dc8[i]
      if (is_outside(dr,dc)):
        break
      if (board[dr][dc] == '・'):
        break
      if (board[dr][dc] == me):
        return True
  return False

# ひっくり返せるかどうか+ひっくり返す座標.
def get_flips(row,col,board,player):
  if (is_placed(row,col,board)):
    return []

  me = my_stone(player)
  enemy = enemy_stone(player)

  flips = []
  for i in range(8):
    dr = row + dr8[i]
    dc = col + dc8[i]
    temp = []

    while not(is_outside(dr,dc)):
      if (board[dr][dc] == enemy):
        temp.append((dr,dc))
      elif (board[dr][dc] == me):
        if (len(temp) > 0):
          flips.extend(temp)
        break
      else:
        break
      dr += dr8[i]
      dc += dc8[i]

  return flips

# 置く.
def place_stone(row,col,board,player):
  flips = get_flips(row,col,board,player)
  if (len(flips) == 0):
    return False
  stone = my_stone(player)
  board[row][col] = stone
  for r,c in flips:
    board[r][c] = stone
  return True

# 合法手.
def legal_moves(board,player):
  moves = []
  for r in range(BOARD_HEIGHT):
    for c in range(BOARD_WIDTH):
      if (can_place(r,c,board,player)):
        moves.append((r,c))
  return moves

# 石の個数.
def count_stones(board):
  count_black = 0
  count_white = 0
  for r in range(BOARD_HEIGHT):
    for c in range(BOARD_WIDTH):
      if (board[r][c] == '●'):
        count_black += 1
      elif (board[r][c] == '◯'):
        count_white += 1
  return count_black,count_white

# CPU.
def cpu_move(board,player):
  moves = legal_moves(board,player)
  return random.choice(moves)

# 人間の手番.
def player_turn(board,player):
  if (player == BLACK):
    player_desc = "黒"
  elif (player == WHITE):
    player_desc = "白"
  print(player_desc,"の番です")
  while True:
    moves = legal_moves(board,player)
    if (len(moves) == 0):
      print("置ける場所がないためパスします")
      break
    else:
      print("置ける場所:",[(col+1,row+1) for row,col in moves])

      while True:
        try:
          user_input = input("横の座標を入力してください")
          col = int(user_input)-1
          break
        except ValueError:
          print("半角英数字を入力してください")
      while True:
        try:
          user_input = input("縦の座標を入力してください")
          row = int(user_input)-1
          break
        except ValueError:
          print("半角英数字を入力してください")

      if (is_outside(row,col)):
        print("範囲外です")
        continue
      if (place_stone(row,col,board,player)):
        break
      else:
        print("そこには置けません")
        continue

# モード選択.
def select_mode():
  while True:
    try:
      mode = int(input("モードを選択してください(1P(Player vs CPU):0,2P(Player vs Player):1)"))
      if (mode == ONEPLAYER or mode == TWOPLAYER):
        return mode
      else:
        print("0か1を入力してくだdさい")
    except ValueError:
      print("半角英数字を入力してください")



# 初期化.
board = [['・']*BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
reset(board)
mode = select_mode()
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

  # 白の番(player).
  if (mode == TWOPLAYER):
    player_turn(board,WHITE)

  # 白の番(CPU).
  elif (mode == ONEPLAYER):
    moves = legal_moves(board,WHITE)
    if (len(moves) == 0):
      print("CPUはパスしました")
    else:
      row,col = cpu_move(board,WHITE)
      place_stone(row,col,board,WHITE)
      print("CPUは",col+1,row+1,"に置きました")
# 個数,勝敗判定.
black,white = count_stones(board)
print("黒:",black,"白:",white)

if (black > white):
  print("黒の勝ち")
elif (black == white):
  print("引き分け")
else:
  print("白の勝ち")
