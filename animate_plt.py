import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation



class AnimationPlt():
    def __init__(self, x=0, y=0):
        self.x = np.linspace(0, 2 * np.pi, 5000)
        self.y = np.exp(-self.x) * np.cos(2 * np.pi * self.x)
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.set_ylim(-1.1, 1.1)
        self.line, = self.ax.plot(self.x, self.y, color="cornflowerblue", lw=3)

    # 清空当前帧
    def init(self):
        self.line.set_ydata([np.nan] * len(self.x))

# 更新新一帧的数据
    def update(self, frame):
        self.line.set_ydata(np.exp(-self.x) * np.cos(2 * np.pi * self.x + float(frame)/100))
        return self.line,

# 调用 FuncAnimation

animationPlt1 = AnimationPlt()

ani = FuncAnimation(animationPlt1.fig
                   ,animationPlt1.update
                   ,init_func=animationPlt1.init
                   ,frames=200
                   ,interval=2
                   ,blit=True
                   )
plt.show()
