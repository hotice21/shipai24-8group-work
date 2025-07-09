Board = {'1':' ' , '2':' ' , '3':' ',
         '4':' ' , '5':' ' , '6':' ',
         '7':' ' , '8':' ' , '9':' '}
print(Board)
#输出结果:
def printB(board):
    print(board['1'] + 'I' + board['2'] + 'I'+board['3'])
    print('-+-+-')
    print(board['4' ]+ 'I' + board['5'] +'I'+ board['6'])
    print('-+-+-')
    print(board['7'] + 'I' + board['8'] + 'I'+board['9'])
#判断是否结束：
def check(c):
    a=0
    #竖列进行判断
    for i in range(1,4):
        for j in range(i,i+7,3):
            if Board[str(j)] in c :
                a +=1
        if a>=3:
            return 1
        else:
             a =0
    #横排进行判定
    for i in range(1,8,3):
        for j in range(i,i+3):
            if Board[str(j)] in c :
                a +=1
        if a>=3:
            return 1
        else:
             a =0
    #斜角判断
    if (Board['1'] in c and Board['5']in c and Board['9'] in c) or (Board['3'] in c and  Board['5'] in c and Board['7'] in c) :
        return 1
    else:
        return 0
for k in range(5):
    printB(Board)
    #输入X：
    while True:
       x = input('x is the next step:\n')
       if (x in Board.keys()) and (Board[x]==' '):
           Board[x]='x'
           break
       else:
           print('type the lying name\n')
    if check('x') :
        print('x wins')
        break
    elif k==4:
        print('the game is over because there is not next step')
        break
    printB(Board)
    #输入O
    while True:
        o = input('o is the next step:\n')
        if (o in Board.keys()) and (Board[o] == ' '):
            Board[o] = 'o'
            break
        else:
            print('type the lying name\n')
    if check('o') :
        print('o wins')
        break
    printB(Board)