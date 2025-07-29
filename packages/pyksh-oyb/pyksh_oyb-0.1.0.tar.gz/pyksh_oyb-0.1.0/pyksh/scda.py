import os


class _SCDA:
    def __init__(self):
        self._data = {
            "t1": """import numpy as np
import matplotlib.pyplot as plt

# 设置中文显示
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 数据准备
x = np.arange(5)
y1 = [1200, 2400, 1800, 2200, 1600]
y2 = [1050, 2100, 1300, 1600, 1340]
labels = ["家庭", "小说", "心理", "科技", "儿童"]

# 绘图
plt.bar(x, y1, width=0.6, color="#FFCC00", label="地区1")
plt.bar(x, y2, width=0.6, bottom=y1, color="#B0C4DE", label="地区2")

# 图表修饰
plt.ylabel("采购数量（本）")
plt.xlabel("图书种类")
plt.title("地区1和地区2对各类图书的采购情况")
plt.xticks(x, labels)
plt.grid(True, axis="y", color="gray", alpha=0.2)
plt.legend()

plt.show()
""",
            "t2": """%matplotlib auto
import numpy as np
import matplotlib.pyplot as plt

# 设置字体为SimHei以支持中文显示
plt.rcParams['font.sans-serif'] = ["SimHei"]

# 定义月份数据
x = list(range(1, 13))
# 定义产品A和产品B的销售额数据
y1 = [20, 28, 23, 16, 29, 36, 39, 33, 31, 19, 21, 25]
y2 = [17, 22, 39, 26, 35, 23, 25, 27, 29, 38, 28, 20]
# 定义月份标签
labels = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']

# 创建子图1，用于展示销售额趋势
ax1 = plt.subplot(211)
ax1.plot(x, y1, 'm--o', lw=2, ms=5, label='产品 A')  # 绘制产品A的销售额趋势
ax1.plot(x, y2, 'g--o', lw=2, ms=5, label='产品 B')  # 绘制产品B的销售额趋势
ax1.set_title("销售额趋势", fontsize=11)  # 设置子图标题
ax1.set_ylim(10, 45)  # 设置y轴范围
ax1.set_ylabel('销售额（亿元）')  # 设置y轴标签
ax1.set_xlabel('月份')  # 设置x轴标签
# 在每个数据点上添加注释
for xy1 in zip(x, y1):
    ax1.annotate("%s" % xy1[1], xy=xy1, xytext=(-5, 5), textcoords='offset points')
for xy2 in zip(x, y2):
    ax1.annotate("%s" % xy2[1], xy=xy2, xytext=(-5, 5), textcoords='offset points')
ax1.legend()  # 添加图例

# 创建子图2，用于展示产品A的销售额饼图
ax2 = plt.subplot(223)
ax2.pie(y1, radius=1, wedgeprops={'width': 0.5}, labels=labels, autopct='%3.1f%%', pctdistance=0.75)
ax2.set_title('产品 A 销售额')  # 设置子图标题

# 创建子图3，用于展示产品B的销售额饼图
ax3 = plt.subplot(224)
ax3.pie(y2, radius=1, wedgeprops={'width': 0.5}, labels=labels, autopct='%3.1f%%', pctdistance=0.75)
ax3.set_title('产品 B 销售额')  # 设置子图标题

# 调整子图布局
plt.tight_layout()
# 显示图表
plt.show()
""",
            "t3": """import numpy as np
import matplotlib.pyplot as plt

# 设置matplotlib支持中文显示和正常显示负号
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体为SimHei以支持中文显示
plt.rcParams["axes.unicode_minus"] = False  # 设置正常显示负号

# 创建一个包含1到12的数组，代表一年中的12个月
month_x = np.arange(1, 13, 1)

# 平均气温数据，单位为摄氏度
data_tem = np.array([12.0, 2.2, 3.3, 4.5, 6.3, 10.2, 20.3, 33.4, 23.0, 16.5, 12.0, 6.2])

# 降水量数据，单位为毫升
data_precipitation = np.array(
    [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3]
)

# 蒸发量数据，单位为毫升
data_evaporation = np.array(
    [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3]
)

# 创建一个图形和一个轴
fig, ax = plt.subplots()

# 绘制蒸发量条形图，颜色为橙色，并设置x轴刻度标签为月份
bar_ev = ax.bar(
    month_x,
    data_evaporation,
    color="orange",
    tick_label=[
        "1月",
        "2月",
        "3月",
        "4月",
        "5月",
        "6月",
        "7月",
        "8月",
        "9月",
        "10月",
        "11月",
        "12月",
    ],
)

# 绘制降水量条形图，颜色为绿色，其底部为蒸发量数据
bar_pre = ax.bar(month_x, data_precipitation, bottom=data_evaporation, color="green")

# 设置y轴标签为"水量(ml)"
ax.set_ylabel("水量(ml)")

# 设置图表标题
ax.set_title("平均气温与降水量、蒸发量的关系")

# 创建第二个y轴，共享x轴
ax_right = ax.twinx()

# 在第二个y轴上绘制平均气温折线图，使用蓝色圆圈和线段表示
line = ax_right.plot(month_x, data_tem, "o-m")

# 设置第二个y轴标签为"气温 ($^\circ$C)"
ax_right.set_ylabel(r"气温 ($^\circ$C)")

# 添加图例，包含蒸发量、降水量和平均气温的图例项，并设置阴影和花式边框
plt.legend(
    [bar_ev, bar_pre, line[0]],
    ["蒸发量", "降水量", "平均气温"],
    shadow=True,
    fancybox=True,
)

# 显示图表
plt.show()
""",
            "t4": """import matplotlib.pyplot as plt
import numpy as np

# 股票一周的收盘价数据
prices = [44.98, 45.02, 44.32, 41.05, 42.08]
days = ["周一", "周二", "周三", "周四", "周五"]

# 创建图形和轴
fig, ax1 = plt.subplots()

# 绘制折线图
ax1.plot(days, prices, marker="o", linestyle="-", color="b", markersize=6)

# 设置x轴的刻度标签为周日期
ax1.set_xticks(range(len(days)))
ax1.set_xticklabels(days)

# 设置坐标轴标签
ax1.set_xlabel("周日期")
ax1.set_ylabel("收盘价（元）")

# 设置标题
plt.title("股票一周收盘价")

# 创建第二个y轴
ax2 = ax1.twinx()

# 在第二个y轴上绘制一些示例数据
ax2.plot(days, np.random.rand(5), color="r", linestyle="--", marker="x")

# 设置第二个y轴的标签
ax2.set_ylabel("示例数据")

# 隐藏坐标轴的上轴脊、右轴脊
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

# 调整布局
plt.tight_layout()

# 显示图形
plt.show()
""",
            "t5": """import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# 设置字体为SimHei以支持中文显示，设置正常显示负号
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 生成测试数据
xx = np.array([13, 5, 25, 13, 9, 19, 3, 39, 13, 271])
yy = np.array([4, 38, 16, 26, 7, 19, 28, 10, 17, 18])
zz = np.array([7, 19, 6, 12, 25, 19, 23, 25, 10, 151])

# 创建图形和3D坐标轴
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# 绘制初始的3D散点图
star = ax.scatter(xx, yy, zz, c="#C71585", marker="*", s=160)


# 定义更新函数，用于动画
def animate(i):
    if i % 2:
        color = "#C71585"
    else:
        color = "white"
    next_star = ax.scatter(
        xx, yy, zz, c=color, marker="*", s=160, linewidth=1, edgecolor="black"
    )
    return (next_star,)


# 定义初始化函数
def init():
    return (star,)


# 创建动画对象
ani = FuncAnimation(
    fig, animate, frames=np.arange(0, 100, 1), init_func=init, interval=1000, blit=False
)

# 设置坐标轴标签
ax.set_xlabel("x轴")
ax.set_ylabel("y轴")
ax.set_zlabel("z轴")

# 设置标题
ax.set_title("3D 散点图", fontproperties="simhei", fontsize=14)

# 调整布局
plt.tight_layout()

# 显示图形
plt.show()
""",
            "t6": """import matplotlib.pyplot as plt

# 汽车热点Top10的搜索指数数据
car_hotspots = [
    "比亚迪 e5",
    "思域",
    "高合 HiPhi X",
    "LYRIQ 锐歌",
    "雅阁",
    "迈腾",
    "帕萨特",
    "朗逸",
    "凯美瑞",
    "速腾",
]
search_indices = [
    144565,
    114804,
    72788,
    70519,
    68742,
    65308,
    64312,
    64102,
    58219,
    56590,
]

# 创建图形和轴
fig, ax = plt.subplots(figsize=(10, 6))  # 设置图形大小

# 绘制柱状图
bars = ax.bar(car_hotspots, search_indices, color="skyblue")

# 在柱状图的顶部添加搜索指数的数值
for bar in bars:
    yval = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        yval,
        f"{yval}",
        ha="center",
        va="bottom",
        fontsize=10,
    )

# 设置y轴的标签为"搜索指数"
ax.set_ylabel("搜索指数")

# 设置x轴的标签为"汽车热点"
ax.set_xlabel("汽车热点")

# 设置标题
plt.title("百度汽车热点Top10的搜索指数")

# 旋转x轴标签，使其更易读
plt.xticks(rotation=45, ha="right")

# 显示图形
plt.tight_layout()  # 调整布局以防止标签被截断
plt.show()
""",
            "t7": """import plotly.graph_objects as go

# 定义收支数据
income = 20000
expenses = {
    "旅行": 2000,
    "深造": 5000,
    "生活": 4000,
    "购物": 1000,
    "聚餐": 500,
    "人情往来": 500,
    "其他": 200,
}
savings = income - sum(expenses.values())

# 准备桑基图数据
labels = ["收入"] + list(expenses.keys()) + ["结余"]

# 源节点 (全部来自收入节点，索引0)
source = [0] * len(expenses) + [0]  # 最后一个是结余
# 目标节点 (依次指向各个支出和结余)
target = list(range(1, len(expenses) + 1)) + [len(labels) - 1]
# 流量值
value = list(expenses.values()) + [savings]

# 创建桑基图
fig = go.Figure(
    go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color=["blue"] + ["red"] * len(expenses) + ["green"],
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color=["rgba(255,0,0,0.3)"] * len(expenses) + ["rgba(0,255,0,0.3)"],
        ),
    )
)

# 更新布局
fig.update_layout(
    title_text="小兰当月收支明细桑基图", font_size=12, width=800, height=500
)

# 显示图表
fig.show()
""",
        }

    @property
    def all(self):
        out = []
        files = [
            ("t1", "4.2.3.py"),
            ("t2", "5.1.2.py"),
            ("t3", "5.3.3.py"),
            ("t4", "6(1).py"),
            ("t5", "7.2.2.py"),
            ("t6", "8(1).py"),
            ("t7", "8(2).py"),
        ]
        for key, fname in files:
            out.append(f"===== {fname} ({key}) =====\n" + self._data[key])
        return "\n\n".join(out)

    @property
    def t1(self):
        return self._data["t1"]

    @property
    def t2(self):
        return self._data["t2"]

    @property
    def t3(self):
        return self._data["t3"]

    @property
    def t4(self):
        return self._data["t4"]

    @property
    def t5(self):
        return self._data["t5"]

    @property
    def t6(self):
        return self._data["t6"]

    @property
    def t7(self):
        return self._data["t7"]

    def __str__(self):
        return self.all


scda = _SCDA()
