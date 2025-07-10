# 宫位名称列表
palace_names = ["大安", "留连", "速喜", "赤口", "小吉", "空亡", "病符", "桃花", "天德"]

# 初始化上一次的宫位索引
last_index = 0


# 根据给定的数字序列确定宫位名称
def get_palace_names(sequence):
    global last_index  # 使用全局变量来记住上一次的宫位索引

    # 根据上一次的宫位索引和当前的数字序列来确定新的宫位索引
    new_indices = []
    for x in sequence:
        next_index = (last_index + x - 1) % len(palace_names)
        new_indices.append(next_index)
        last_index = next_index  # 更新当前的宫位索引

    palaces = [palace_names[i] for i in new_indices]

    return palaces


# 示例
sequence1 = (8, 10, 10)
# sequence2 = (9, 1, 1)

# 打印结果
print("[" + ", ".join(get_palace_names(sequence1)) + "]")  # 应该输出：《大安》《大安》《大安》
# print("[" + ", ".join(get_palace_names(sequence2)) + "]")  # 应该输出：《天德》《天德》《大安》