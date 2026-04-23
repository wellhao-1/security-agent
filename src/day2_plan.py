study_hours = float(input("请输入你今天计划学习的小时数："))

if study_hours < 1:
    print("今天先完成一个很小的任务：学习 3 个术语，写 5 行日志。")
elif study_hours < 3:
    print("今天建议完成 2 个任务：")
    print("1. 学习 Python 条件语句和循环")
    print("2. 写一个简单练习程序并提交到 GitHub")
else:
    print("今天建议完成 3 个任务：")
    print("1. 学习 Python 条件语句和循环")
    print("2. 完成一个练习程序")
    print("3. 更新 README 和第二天学习日志")

print("\n今天的固定小任务：")

tasks = [
    "学习 if / elif / else",
    "学习 for / while",
    "完成 day2_plan.py",
]

for i, task in enumerate(tasks, start=1):
    print(f"{i}. {task}")