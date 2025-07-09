import random
from pathlib import Path
# 创建列表
aim_text = {}
for i in range(1,51):
    aim_text[str(i)] = str(i)
# 创建目标文件
storage = Path('C:\\Users\\al z\\Desktop\\text')
if not storage.is_dir():
    storage.mkdir()
choose = ['A','B','C','D']
for k in range(35):
    text_book = open(storage/f'student_file{k + 1}.txt','w')
    answer_book = open(storage/f'answer_file{k + 1}.txt','w')
    # 建立正确答案列表
    for key, value in aim_text.items():
        #创建选项
        wrong_answer_list = list(aim_text.keys())
        wrong_answer_list.remove(value)
        answer = [value] + random.sample(wrong_answer_list,3)
        random.shuffle(answer)
        text_book.write(f'\n{key}:\t')
        answer_book.write(f'{key}:\t')
        for i in range(4):
            text_book.write(f'{choose[i]}.{answer[i]}\t')
            if value == answer[i] :
                answer_book.write(f'{choose[i]}\n')
    print(answer_book.readline())
    text_book.close()
    answer_book.close()