import random


# 定义所有角色
villagers = ["村民"] * 4
gods = ["女巫", "守卫", "预言家", "猎人","白痴"]
wolves = ["白狼王", "狼美人", "狼人", "狼人"]

# 合并所有角色
all_roles = villagers + gods + wolves

# 随机打乱角色顺序
random.shuffle(all_roles)

# 生成1-13的号码并与角色配对
player_roles = list(zip(range(1, 14), all_roles))

# 按号码排序（虽然shuffle后已经随机，但为了确保按1-13展示）
player_roles.sort(key=lambda x: x[0])

def display_roles(player_roles):
    print("===== 狼人杀角色分配结果 =====")
    print("号码\t角色")
    print("-" * 20)
    for number, role in player_roles:
        print(f"{number}\t{role}")
    print("-" * 20)
    
    # 统计各阵营数量
    villager_count = sum(1 for _, role in player_roles if role == "村民")
    god_count = sum(1 for _, role in player_roles if role in gods)
    wolf_count = sum(1 for _, role in player_roles if role in wolves)
    
    print(f"村民阵营: {villager_count}人")
    print(f"神职阵营: {god_count}人")
    print(f"狼人阵营: {wolf_count}人")

if __name__ == "__main__":
    # 设置随机种子以便测试（实际使用时可移除）
    # random.seed(42)
    
    # 分配角
    
    # 显示结果
    display_roles(player_roles)