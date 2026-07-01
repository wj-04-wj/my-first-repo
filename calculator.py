# calculator.py - main 分支版本
def add(a, b):
    """计算两个数的和（四舍五入）"""
    result = round(a + b, 2)
    return result

# 测试代码
if __name__ == "__main__":
    print("计算结果（四舍五入）：", add(10, 20))