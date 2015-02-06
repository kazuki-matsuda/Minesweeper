# coding: UTF-8
# コンソールで動くマインスイーパー
# LEVEL 1
	# 1. 基本機能の実装（マスを開く、地雷チェック、クリア判定）
	# 2. フィールドは5x5で固定、地雷も5個固定
# LEVEL 2
	#地雷チェックしたマスは開こうとしても開けない
	#地雷チェックしたマスに再度地雷チェックしようとするとチェック解除

import random

def setMines(height, width, mines):
	#現在の情報cell_matと地雷の情報mine_matを構成

	#行番号と列番号
	alphabetTable = [chr(i) for i in xrange(97, 123)] 
	rownames = alphabetTable[0:height]
	colnames = range(width)

	#cell_matとmine_matの箱を作る
	cell_mat = []
	mine_mat = []
	for i in range(height):
		cell_mat.append(range(width))
		mine_mat.append(range(width))

	#cell_matは"?"、mine_matは0で初期化
	for i in range(height):
		for j in range(width):
			cell_mat[i][j] = "?"
			mine_mat[i][j] = 0

	#地雷の位置をランダムに決定
	random.seed()
	mine_index = random.sample(range(height*width), mines)

	#周囲の地雷数をmine_matに反映
	mine_row = 0
	mine_col = 0
	for l in range(mines):
		mine_row = mine_index[l] // width
		mine_col = mine_index[l] % width
		mine_mat[mine_row][mine_col] -= 10 
		mine_rows = list(set(range(mine_row-1,mine_row+2)) & set(range(height)))
		mine_cols = list(set(range(mine_col-1,mine_col+2)) & set(range(width)))
		for i in mine_rows:
			for j in mine_cols:
				mine_mat[i][j] += 1

	#地雷の位置に"M"を代入
	for i in range(height):
		for j in range(width):
			if mine_mat[i][j] < 0:
				mine_mat[i][j] = "M"
			
	return rownames, colnames, cell_mat, mine_mat

def endSearch(height, width, mines, cell_mat):
	#クリア判定をする
	cnt = 0
	for k in range(9):
		for i in range(height):
			cnt += cell_mat[i].count(k)
	res = cnt < height*width-mines
	return(res)

def main():
	#メイン
	print u"\nマインスイーパーを開始します。"

	height = 5
	width = 5
	mines = 5

	tmp = setMines(height, width, mines)
	rownames = tmp[0]
	colnames = tmp[1]
	cell_mat = tmp[2]
	mine_mat = tmp[3]

	status = 0
	while endSearch(height, width, mines, cell_mat):

		#現在の状態をprint
		print "\n ",
		for j in range(width):
			print colnames[j],
		print #改行

		#行情報&セル情報をprint
		for i in range(height):
			print rownames[i], #行番号のprint
			for j in range(width):
				print cell_mat[i][j], #セル情報のprint
			print #改行
		print #改行

		#操作する行、列、アクションに関する入力
		sel_row = raw_input("選択する行を入力してください（ex. a,b,c）：")
		while sel_row not in rownames:
			sel_row = raw_input("選択する行を 正しく 入力してください（ex. a,b,c）：")

		sel_col = raw_input("選択する列を入力してください（ex. 0,1,2）：")
		while sel_col not in str(colnames):
			sel_col = raw_input("選択する列を 正しく 入力してください（ex. 0,1,2）：")

		act_type = raw_input("開くなら o 、地雷チェックは x 、ゲーム終了は q を入力してください：")
		while act_type not in ["o", "x", "q"]:
			act_type = raw_input("開くなら o 、地雷チェックは x 、ゲーム終了は q を 正しく 入力してください：")

		#入力に基づく処理
		act_row = rownames.index(sel_row)
		act_col = int(sel_col)

		#マスを開くアクション
		if act_type == "o":
			if cell_mat[act_row][act_col] == "x":
				print u"\n選択したマスは地雷チェックされているため開けません"
				print u"地雷チェックを解除する場合は、再度地雷チェックをしてください"
			else:
				if mine_mat[act_row][act_col] == "M":
					cell_mat[act_row][act_col] = "M"
					status = 1
					break
				cell_mat[act_row][act_col] = mine_mat[act_row][act_col]
		#マスを地雷チェックするアクション
		elif act_type == "x":
			if cell_mat[act_row][act_col] == "x":
				print u"\n地雷チェックを解除しました"
				cell_mat[act_row][act_col] = "?"
			else:
				cell_mat[act_row][act_col] = "x"
		#終了
		else:
			status = 1
			break
	
	#status==0ならクリア			
	if status == 0:
		print "Congratulations!\n"
	#status==1なら現在の状態をprintしてゲームオーバー
	else:
		print #改行
		#列情報をprint
		print " ",
		for j in range(width):
			print colnames[j],
		print #改行
		for i in range(height):
			print rownames[i], #行番号のprint
			for j in range(width):
				print mine_mat[i][j], #セル情報のprint
			print #改行
		print #改行

		print "Game over!\n"

main()

