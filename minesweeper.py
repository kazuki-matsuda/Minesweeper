#coding: UTF-8
#コンソールで動くマインスイーパー
#LEVEL 1
	#基本機能の実装（マスを開く、地雷チェック、クリア判定）
	#フィールドは5x5で固定、地雷も5個固定
#LEVEL 2
	#地雷チェックしたマスは開こうとしても開けない
	#地雷チェックしたマスに再度地雷チェックしようとするとチェック解除
#LEVEL 3
	#フィールドの大きさ、地雷の数をゲーム開始時に指定できる
	#それぞれの上限は自由に決めて良い
#LEVEL 4
	#空白マスを開いた場合に、隣接マスも自動的に開かれる

import random

def setMines(height, width, mines):
	#フィールドを設定

	alphabetTable = [chr(i) for i in xrange(97, 123)] 
	rownames = range(height)
	colnames = alphabetTable[0:width]

	cell_mat = []
	mine_mat = []
	for i in range(height):
		cell_mat.append(range(width))
		mine_mat.append(range(width))

	for i in range(height):
		for j in range(width):
			cell_mat[i][j] = "?"
			mine_mat[i][j] = 0

	random.seed()
	mine_index = random.sample(range(height*width), mines)

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

	for i in range(height):
		for j in range(width):
			if mine_mat[i][j] < 0:
				mine_mat[i][j] = "M"
			
	return rownames, colnames, cell_mat, mine_mat

def autoOpen(height, width, act_row, act_col, cell_mat, mine_mat):
	#空白マスを開いたときに周辺のマスを自動的に開く
	open_rows = list(set(range(act_row-1,act_row+2)) & set(range(height)))
	open_cols = list(set(range(act_col-1,act_col+2)) & set(range(width)))
	for i in open_rows:
		for j in open_cols:
			if cell_mat[i][j] == "?":
				cell_mat[i][j] = mine_mat[i][j]
				if cell_mat[i][j] == 0:
					autoOpen(height, width, i, j, cell_mat, mine_mat)

def judgeEnd(height, width, mines, cell_mat):
	#クリア判定をする
	cnt = 0
	for k in range(9):
		for i in range(height):
			cnt += cell_mat[i].count(k)
	res = cnt < height*width-mines
	return(res)

def printNow(height, width, rownames, colnames, cell_mat):
	#現在の状況をprintする
	if height < 11:
		print "\n ",
		for j in range(width):
			print "\033[33m%s\033[0m" % colnames[j],
		print 
		for i in range(height):
			print "\033[33m%s\033[0m" % rownames[i], 
			for j in range(width):
				if cell_mat[i][j] in range(9):
					print "\033[32m%d\033[0m" % cell_mat[i][j], 
				elif cell_mat[i][j] in ["x", "M"]:
					print "\033[31m%s\033[0m" % cell_mat[i][j], 
				else:
					print cell_mat[i][j], 
			print 
		print 
	else:
		print "\n  ",
		for j in range(width):
			print "\033[33m%s\033[0m" % colnames[j],
		print #改行
		for i in range(height):
			if i < 10:
				print "\033[33m %d\033[0m" % rownames[i],
			else:
				print "\033[33m%s\033[0m" % rownames[i],
			for j in range(width):
				if cell_mat[i][j] in range(9):
					print "\033[32m%d\033[0m" % cell_mat[i][j],
				elif cell_mat[i][j] in ["x", "M"]:
					print "\033[31m%s\033[0m" % cell_mat[i][j],
				else:
					print cell_mat[i][j],
			print 
		print 


def printEnd(height, width, rownames, colnames, mine_mat, status):
	if status == 0:
		print "\n\033[32m********************\033[0m"
		print "\033[32m* Congratulations! *\033[0m"
		print "\033[32m********************\033[0m\n"
	else:
		printNow(height, width, rownames, colnames, mine_mat)

		print "\033[31mGame over!\033[0m\n"	

def main():
	print u"\nマインスイーパーを開始します。"
	print u"途中で終了する場合は \033[33mexit\033[0m を入力してください。\n"

	height_max = 20
	width_max = 20
	height_min = 5
	width_min = 5
	mines_min = 5
	status = 0

	while status == 0:
		height_text = "行の数を入力してください（%d ~ %d）：\n" % (height_min, height_max)
		height_text_re = "行の数を \033[33m正しく\033[0m 入力してください（%d ~ %d）：\n" % (height_min, height_max)
		height = raw_input(height_text)
		while (height not in str(range(height_max+1)) or height in str(range(height_min))) and height != "exit":
			height = raw_input(height_text_re)
		if height == "exit":
			status = 1
			break
		height = int(height)

		width_text = "列の数を入力してください（%d ~ %d）：\n" % (width_min, width_max)
		width_text_re = "列の数を \033[33m正しく\033[0m 入力してください（%d ~ %d）：\n" % (width_min, width_max)
		width = raw_input(width_text)
		while (width not in str(range(width_max+1)) or width in str(range(width_min))) and width != "exit":
			width = raw_input(width_text_re)
		if width == "exit":
			status = 1
			break
		width = int(width)

		mines_max = height * width
		mines_text = "地雷の数を入力してください（%d ~ %d）：\n" % (mines_min, mines_max)
		mines_text_re = "地雷の数を \033[33m正しく\033[0m 入力してください（%d ~ %d）：\n" % (mines_min, mines_max)
		mines = raw_input(mines_text) 
		while (mines not in str(range(mines_max+1)) or mines in str(range(mines_min))) and mines != "exit":
			mines = raw_input(mines_text_re)
		if mines == "exit":
			status = 1
			break
		mines = int(mines)

		if mines == height*width:
			status = 2
			break

		tmp = setMines(height, width, mines)
		rownames = tmp[0]
		colnames = tmp[1]
		cell_mat = tmp[2]
		mine_mat = tmp[3]

		break

	if status == 1:  
		print "\n\033[31mGame over!\033[0m\n"	
	elif status == 2:
		print "\n\033[31mFilled with mines!\033[0m\n"	

	#メインループ
	while status == 0:
		while judgeEnd(height, width, mines, cell_mat): 

			printNow(height, width, rownames, colnames, cell_mat)

			sel_row = raw_input("選択する行を入力してください（0,1,2,...）：\n")
			while (sel_row not in str(rownames) or sel_row == "" or sel_row == " ") and sel_row != "exit":
				sel_row = raw_input("選択する行を \033[33m正しく\033[0m 入力してください（0,1,2,...）：\n")
			if sel_row == "exit":
				status = 1
				break

			sel_col = raw_input("選択する列を入力してください（a,b,c,...）：\n")
			while sel_col not in colnames and sel_col != "exit":
				sel_col = raw_input("選択する列を \033[33m正しく\033[0m 入力してください（a,b,c,...）：\n")
			if sel_col == "exit":
				status = 1
				break

			act_type = raw_input("開くなら o を、地雷チェックは x を入力してください：\n")
			while act_type not in ["o", "x"] and act_type != "exit":
				act_type = raw_input("開くなら o を、地雷チェックは x を \033[33m正しく\033[0m 入力してください：\n")
			if act_type == "exit":
				status = 1
				break

			act_row = int(sel_row)
			act_col = colnames.index(sel_col)

			if act_type == "o":
				if cell_mat[act_row][act_col] == "x":
					print u"\n選択したマス %s の %s は地雷チェックをされているため開けません" % (sel_row, sel_col)
					print u"地雷チェックを解除する場合は、再度地雷チェックをしてください"
				elif cell_mat[act_row][act_col] in range(9):
					print u"\n選択したマス %s の %s はすでに開かれています" % (sel_row, sel_col)				
				elif mine_mat[act_row][act_col] == "M":
					status = 1
					break
				else:
					cell_mat[act_row][act_col] = mine_mat[act_row][act_col]
					if cell_mat[act_row][act_col] == 0: 
						autoOpen(height, width, act_row, act_col, cell_mat, mine_mat)

			elif act_type == "x":
				if cell_mat[act_row][act_col] == "x":
					print u"\n地雷チェックを解除しました"
					cell_mat[act_row][act_col] = "?"
				elif cell_mat[act_row][act_col] in range(9):
					print u"\n選択したマス %s の %s はすでに開かれています" % (sel_row, sel_col)				
				else:
					cell_mat[act_row][act_col] = "x"
			else:
				status = 1
				break
		
		printEnd(height, width, rownames, colnames, mine_mat, status)
		break

main()

