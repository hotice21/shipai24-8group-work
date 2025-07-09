from pathlib import Path
houxuanren = {1:'朱鸣坚',2:'郑沐欣',4:'朱矜翰',5:'高睿涛',6:'倪梓峻',7:'贺贤宇',8:'郭瞬时',9:'陈富荣',10:'谢昕彤'}
xuanpiao = {1:0,2:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0}
a = 1
while a ==1:
    for i,j in houxuanren.items():
        print(i,'\t',j,'\t',xuanpiao[i])
    b = int(input())
    if b in [1,2,4,5,6,7,8,9,10]:
        xuanpiao[b] +=1
    else:
        a = 0
storage = Path('C:\\Users\\al z\\Desktop')
if not storage.is_dir():
    storage.mkdir()
text = open(storage/'text.txt','w')
for i,j in xuanpiao.items():
    print(i,'\t',houxuanren[i],'\t',j)
    text.write(f'{i}\t {houxuanren[i]}\t{j}')