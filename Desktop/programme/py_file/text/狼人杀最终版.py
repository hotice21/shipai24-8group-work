import random
import tkinter as tk
from collections import defaultdict

continueing=""
villagers_num,gods,wolves = "", "", ""
# 记录每个编号的历史身份
player_history = defaultdict(list)

def show_input_window(vn=None, gs=None, ws=None):
    root = tk.Tk()
    root.title("输入身份")
    root.geometry("400x300")
    # 创建一个标签
    label = tk.Label(root, text="村民数：")
    label.grid(row=0, column=0, padx=20, pady=15)
    label2 = tk.Label(root, text="神职数：")
    label2.grid(row=1, column=0, padx=20, pady=15)
    label3 = tk.Label(root, text="狼人数：")
    label3.grid(row=2, column=0, padx=20, pady=15)
    # 创建一个输入框
    entry = tk.Entry(root)
    entry.grid(row=0, column=1, padx=20, pady=15)
    entry2 = tk.Entry(root)
    entry2.grid(row=1, column=1, padx=20, pady=15)
    entry3 = tk.Entry(root)
    entry3.grid(row=2, column=1, padx=20, pady=15)
    # 如果有传入默认值，则设置输入框的初始值
    if vn is not None:
        entry.insert(0, vn)
        entry2.insert(0, gs)
        entry3.insert(0, ws)
    def on_button_click():
        global villagers_num, gods, wolves
        # 获取输入框内容
        villagers_num = entry.get()
        gods = entry2.get()
        wolves = entry3.get()
        if villagers_num == "" or gods == "" or wolves == "":
            print("请填写所有字段")
            return
        # 可以将内容保存到变量或文件，这里先打印
        print(f"村民数: {villagers_num}, 神职数: {gods}, 狼人数: {wolves}")
        root.destroy()

    button = tk.Button(root, text="保存", command=on_button_click)
    button.grid(row=3, column=0, columnspan=2, pady=10)
    root.mainloop()

#处理数据
def translate(villagers_num, gods, wolves):
    if "，" not in gods or "，" not in wolves:
        error_output=tk.Tk()
        error_output.title("输入错误")
        error_label = tk.Label(error_output, text="神职或狼人的输入格式不正确，请使用中文逗号分隔。")
        error_label.pack(padx=20, pady=20)
        error_output.mainloop()
        return None, None, None
    villagers_num = int(villagers_num)
    god = gods.split("，")
    wolve = wolves.split("，")
    return villagers_num, god, wolve

def weighted_shuffle(roles, total_players):
    """根据历史记录进行加权随机分配"""
    # 创建权重字典，记录每个玩家对每个身份的权重
    weights = {}
    
    for player_num in range(1, total_players + 1):
        weights[player_num] = {}
        history = player_history[player_num]
        
        for role in set(roles):
            # 计算该玩家获得该身份的次数
            role_count = history.count(role)
            # 权重 = 1 / (获得次数 + 1)，获得次数越多权重越低
            weights[player_num][role] = 1.0 / (role_count + 1)
    
    # 改进的分配算法：多次尝试找到最优解
    best_assignment = None
    best_score = float('-inf')
    
    for attempt in range(100):  # 尝试100次
        assigned_roles = {}
        available_roles = roles.copy()
        players_list = list(range(1, total_players + 1))
        random.shuffle(players_list)  # 随机打乱玩家顺序
        
        assignment_success = True
        current_score = 0
        
        for player_num in players_list:
            if not available_roles:
                assignment_success = False
                break
                
            # 计算当前玩家对剩余身份的权重
            role_weights = []
            available_role_list = []
            
            # 获取所有剩余的不同身份
            unique_roles = list(set(available_roles))
            
            for role in unique_roles:
                available_role_list.append(role)
                role_weights.append(weights[player_num].get(role, 1.0))
            
            # 根据权重随机选择身份
            if available_role_list:
                chosen_role = random.choices(available_role_list, weights=role_weights)[0]
                assigned_roles[player_num] = chosen_role
                available_roles.remove(chosen_role)
                
                # 计算当前分配的得分（权重越高得分越高）
                current_score += weights[player_num].get(chosen_role, 1.0)
            else:
                assignment_success = False
                break
        
        # 如果分配成功且得分更高，则更新最佳分配
        if assignment_success and current_score > best_score:
            best_assignment = assigned_roles.copy()
            best_score = current_score
    
    # 记录到历史
    if best_assignment:
        for player_num, role in best_assignment.items():
            player_history[player_num].append(role)
        return best_assignment
    else:
        # 如果所有尝试都失败，使用简单随机分配作为备选
        simple_roles = roles.copy()
        random.shuffle(simple_roles)
        assigned_roles = {}
        for i, player_num in enumerate(range(1, total_players + 1)):
            assigned_roles[player_num] = simple_roles[i]
            player_history[player_num].append(simple_roles[i])
        return assigned_roles

if __name__ == "__main__":
    #初始化
    while continueing=="":
        show_input_window(villagers_num, gods, wolves)
        villagers_num, god, wolve = translate(villagers_num, gods, wolves)
        villagers = ["村民" for _ in range(villagers_num)]
        total_roles = villagers + god + wolve
        total_players = len(total_roles)
        
        # 使用加权随机分配
        assigned_roles = weighted_shuffle(total_roles, total_players)
        
        print("\n本轮身份分配：")
        for player_num in range(1, total_players + 1):
            role = assigned_roles[player_num]
            history_count = player_history[player_num].count(role)
            print(f"{player_num} 的身份是：{role} (历史获得{history_count}次)")
    print("游戏结束")