import math
import numpy as np
import matplotlib.pyplot as plt
import datetime
from scipy.sparse import diags,spdiags
from cvxopt import solvers,matrix

class ReferencePath():
    def __paraInit__(self,lamda):
        self.x = np.array([1.0, 30.0, 50.0, 80.0, 100.0])  # n个点的x值
        self.y = np.array([5.0, 1.0, 10.0, 4.0, 2.0])  # n个点的y值
        self.h = self.x[1:] - self.x[:-1]  # n-1个值
        self.w = 1  # 最优化时候的权重,n维度
        self.lamda = lamda  # 光滑系数，越大代表曲线越光滑
        self.dim = len(self.x)  # 记录一下x的维度，后续都需要使用到

    def __init__(self, lamda):
        self.__paraInit__(lamda)
        self.speedLimitList = []
        self.pathPointList = []
        self.pathPrioirity = 0

    # private

    def gen_coef_matrix(self):
        # 单独定义函数：生成最优化相关的矩阵y,AT,B

        # -----------------------------
        # 生成yT
        yT = np.zeros(2 * self.dim - 2)  # 2n-2维度
        yT[0:self.dim] = self.w * self.y

        # -----------------------------
        # 生成Q，R和A
        h_inverse = 1 / self.h
        QT = diags(diagonals=[h_inverse[:-1], -(h_inverse[:-1] + h_inverse[1:]), h_inverse[1:]],
                   offsets=[0, 1, 2], shape=(self.dim - 2, self.dim)).toarray()
        R = 1 / 6 * diags(diagonals=[self.h[1:], 2 * (self.h[:-1] + self.h[1:]), self.h[1:]],
                          offsets=[-1, 0, 1], shape=(self.dim - 2, self.dim - 2)).toarray()
        AT = np.hstack([QT, -R])
        # -----------------------------
        # 生成B
        B = np.zeros((2 * self.dim - 2, 2 * self.dim - 2))
        B[:self.dim, :self.dim] = np.eye(self.dim) * self.w
        B[self.dim:, self.dim:] = self.lamda * R

        return yT, AT, B

    def solve_g_gamma(self):
        # 利用cvxopt解二次规划问题，求得g_m
        yT, AT, B = self.gen_coef_matrix()
        yT, AT, B = matrix(yT, tc="d"), matrix(AT, tc="d"), matrix(B, tc="d")
        b = matrix(np.zeros(self.dim - 2), tc="d")
        g_gamma = solvers.qp(P=B, q=-yT, A=AT, b=b)["x"]  # 这里求出了x，里面包括样本点的n个拟合函数的值和n-2个二阶导数值
        g_gamma = np.array(g_gamma).reshape(2 * self.dim - 2, )  # 这里reshape一下，array里（n,1）和（n,）是不一样的

        g = g_gamma[:self.dim]  # 前n个是样本点的拟合函数的值
        gamma = np.zeros_like(g)
        gamma[1:-1] = g_gamma[self.dim:]  ##后n-2个是样本点的二阶导数值
        self.g = g
        self.gamma = gamma
        return g, gamma

    def fit(self):
        # 求得g,gamma后，还需要还原实际的ai，bi，ci，di的系数
        g, gamma = self.solve_g_gamma()

        ai = g[:-1]
        bi = (g[1:] - g[:-1]) / self.h - self.h / 6 * (2 * gamma[:-1] + gamma[1:])
        ci = gamma[:-1] / 2
        di = (gamma[1:] - gamma[:-1]) / (6 * self.h)
        coef = np.array([ai, bi, ci, di])
        self.coef = coef

    def eval(self, xn):
        yn = np.zeros(len(xn))
        for i in range(len(xn)):
            if xn[i] <= self.x[0]:  # 支持外插，比样本点的最小值还小时的处理
                a, b = self.coef[:2, 0]  # a0=a1,b0=b1
                yn[i] = a + b * (xn[i] - self.x[0])

            elif xn[i] >= self.x[-1]:  # 支持外插，比样本点的最大值还大时的处理
                a = self.g[-1]  # an = gn
                b = (self.g[-1] - self.g[-2]) / self.h[-1] + self.h[-1] / 6 * (2 * self.gamma[-1] + self.gamma[-2])
                yn[i] = a + b * (xn[i] - self.x[-1])
            else:
                xn_idx = np.where(self.x <= xn[i])[0][-1]  # np.where只有condition时会返回符合条件的索引，不过返回的是2维的元组，[0]获取索引列表
                a, b, c, d = self.coef[:, xn_idx]
                yn[i] = a + b * (xn[i] - self.x[xn_idx]) + c * (xn[i] - self.x[xn_idx]) ** 2 + d * (
                            xn[i] - self.x[xn_idx]) ** 3
        return yn

    def __pathGenerate__(self):
        pass

    def __pathSmoother__(self):
        # DiscretePointsReferenceLineSmoother
        # QpSplineReferenceLineSmoother
        # SpiralReferenceLineSmoother
        pass

    def __pathStich__(self): #参考线拼接
        pass

    def __getPath__(self):
        return self.pathPointList

# path1 = ReferencePath()
# path1.QTCal()

# 程序开始时间
startTime = datetime.datetime.now()
loop_counter = 100
while(loop_counter):
    sm = ReferencePath(lamda=5)
    sm.fit()
    xn = np.linspace(0, 110, 100)  # 插入路径点数量
    yn = sm.eval(xn)
    loop_counter -= 1

# 程序结束时间
# endtime = datetime.datetime.now()
# print("Optimization time is: ", endtime - startTime)
#
# plt.scatter(sm.x,sm.y)
# plt.plot(xn,yn,"--r")
#
# plt.show()