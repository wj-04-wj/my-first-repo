# calculator.py - feature 分支版本
def add(a, b):
    """计算两个数的和（含10%税费）"""
    result = (a + b) * 1.1
    return result

# 测试代码
if __name__ == "__main__":
    print("计算结果（含税费）：", add(10, 20))