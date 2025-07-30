from matplotlib import pyplot as plt
from scipy.stats import norm
import numpy as np
from abetter import SampleMean
from abetter.sample_mean import SSMean
from abetter.io.format import to_str


def plot_two_mean(s1: SampleMean, s2: SampleMean, points: int = 200) -> tuple[plt.Figure, plt.Axes]:
    """
    绘制两个均值型样本的总体均值分布
    :param s1: 样本1
    :param s2: 样本2
    :param points: 绘图精度，越大精度越高，默认200
    :return:
    """
    with plt.ioff():
        c1, c2 = '#118ab2', '#bc4749'
        # 计算
        std1, std2 = s1.std / np.sqrt(s1.n), s2.std / np.sqrt(s2.n)
        x_min = min(s1.mean - std1 * 5, s2.mean - std2 * 5)
        x_max = max(s1.mean + std1 * 5, s2.mean + std2 * 5)
        x = np.linspace(x_min, x_max, points)
        y1 = norm.pdf(x, loc=s1.mean, scale=std1)
        y2 = norm.pdf(x, loc=s2.mean, scale=std2)
        y_max = np.max([y1, y2]) * 1.1

        # 绘制密度函数
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.plot(x, 0 * x, c='k', lw=1)

        sd1, = ax.plot(x, y1, c=c1, label=r'$\overline{X}_1$')
        sd2, = ax.plot(x, y2, c=c2, label=r'$\overline{X}_2$')
        ax.set_xlim(x_min, x_max)

        # 绘制辅助线
        ax.vlines(s1.mean, 0, y_max, lw=0.5, ls='-', color='k', alpha=0.5)
        ax.vlines(s2.mean, 0, y_max, lw=0.5, ls='-', color='k', alpha=0.5)
        ax.hlines(y_max * 0.95, s1.mean, s2.mean, lw=1, ls='-', color='k', alpha=0.5)
        ax.text((s1.mean + s2.mean) / 2, y_max * 0.95, f'Diff={to_str(s2.mean - s1.mean)}', ha='center', va='bottom')

        # 填充
        alpha = 0.05 if s1.alpha is None else s1.alpha
        label1, label2 = f'{100 * (1 - alpha):.0f}%' + r' CI of $\overline{X}_1$', f'{100 * (1 - alpha):.0f}%' + r' CI of $\overline{X}_2$'
        z = norm.isf(alpha / 2)
        x1 = np.linspace(s1.mean - std1 * z, s1.mean + std1 * z, points)
        y1 = norm.pdf(x1, loc=s1.mean, scale=std1)
        x2 = np.linspace(s2.mean - std2 * z, s2.mean + std2 * z, points)
        y2 = norm.pdf(x2, loc=s2.mean, scale=std2)
        f1 = ax.fill_between(x1, y1, 0, color=c1, alpha=0.5, label=label1)
        f2 = ax.fill_between(x2, y2, 0, color=c2, alpha=0.5, label=label2)
        ax.text(s1.mean, np.max(y1) * 0.3, '95%', ha='center', va='center')
        ax.text(s2.mean, np.max(y2) * 0.3, '95%', ha='center', va='center')

        # 坐标刻度
        ax.set_frame_on(False)
        ax.set_axis_off()

        ax.vlines(s1.mean, 0 - y_max * 0.02, 0, lw=0.5, ls='-', color='k', alpha=0.5)
        ax.text(s1.mean, 0 - y_max * 0.02, to_str(s1.mean), ha='center', va='top')

        ax.vlines(s2.mean, 0 - y_max * 0.06, 0, lw=0.5, ls='-', color='k', alpha=0.5)
        ax.text(s2.mean, 0 - y_max * 0.06, to_str(s2.mean), ha='center', va='top')

        # 设置
        plt.title('Distributions of 2 Sample Means')
        ax.legend([sd1, sd2, f1, f2], [r'$\overline{X}_1$', r'$\overline{X}_2$', label1, label2])

        return fig, ax


def plot_diff_mean(ss: SSMean, points: int = 200) -> tuple[plt.Figure, plt.Axes]:
    with plt.ioff():
        c1, c2 = '#118ab2', '#bc4749'
        # 计算
        sem = ss.dict_test_best.get('sem')
        mde = ss.dict_test_best.get('mde')
        alpha = 0.05 if ss.s1.alpha is None else ss.s1.alpha
        beta = 0.20 if ss.s1.beta is None else ss.s1.beta
        z = norm.isf(alpha / 2)

        x_min, x_max = -sem * 5, mde + sem * 5
        x = np.linspace(x_min, x_max, points)
        y1 = norm.pdf(x, loc=0.0, scale=sem)
        y2 = norm.pdf(x, loc=mde, scale=sem)
        y_max = np.max([y1, y2])

        # 绘制密度函数
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(x, 0 * x, c='k', lw=1)
        sd1, = ax.plot(x, y1, c=c1, label='H0')
        sd2, = ax.plot(x, y2, c=c2, label='H1', ls='--')

        # 绘制辅助线
        ax.vlines(0.0, 0, y_max, lw=0.5, ls='-', color='k', alpha=0.5)
        ax.vlines(mde, 0, y_max, lw=0.5, ls='-', color='k', alpha=0.5)
        ax.vlines(sem * z, 0, y_max * 1.05, lw=0.5, ls='-', color='k', alpha=0.5)
        ax.text(sem * z, y_max * 1.05, f'c={to_str(sem * z)}', ha='center', va='bottom')

        # 填充
        label1, label2 = r'Error Ⅰ: $\alpha={alpha}$'.format(alpha=f'{alpha: .2f}'), r'Error Ⅱ: $\beta={beta}$'.format(beta=f'{beta: .2f}')
        x1 = np.linspace(sem * z, sem * z * 5, points)
        y1 = norm.pdf(x1, loc=0, scale=sem)
        x2 = np.linspace(-sem * z * 5, sem * z, points)
        y2 = norm.pdf(x2, loc=mde, scale=sem)
        f1 = ax.fill_between(x1, y1, 0, color=c1, alpha=0.5, label=label1)
        f2 = ax.fill_between(x2, y2, 0, color=c2, alpha=0.5, label=label2)

        # 坐标刻度
        ax.set_frame_on(False)
        ax.set_axis_off()
        ax.vlines(0, 0 - y_max * 0.02, 0, lw=0.5, ls='-', color='k', alpha=0.5)
        ax.text(0, 0 - y_max * 0.02, '0', ha='center', va='top')

        ax.vlines(mde, 0 - y_max * 0.06, 0, lw=0.5, ls='-', color='k', alpha=0.5)
        ax.text(mde, 0 - y_max * 0.06, f'MDE={to_str(mde)}', ha='center', va='top')
        ax.text(sem * z + mde * 0.05, y_max * 0.03, r'$\alpha=${alpha}%'.format(alpha=f'{100 * alpha:.0f}'), ha='left', va='center')
        ax.text(sem * z - mde * 0.05, y_max * 0.03, r'$\beta=${beta}%'.format(beta=f'{100 * beta:.0f}'), ha='right', va='center')

        # 设置
        plt.title('Distribution of the Difference Between 2 Sample Means')
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(-y_max * 0.06, y_max * 1.15)
        ax.legend([sd1, sd2, f1, f2], [
            r'$H_0: \overline{X}_2$ - $\overline{X}_1 = 0$',
            r'$H_1: \overline{X}_2$ - $\overline{X}_1 \geqslant MDE$',
            r'Error Ⅰ: $\alpha=${alpha}'.format(alpha=f'{100*alpha:.0f}%'),
            r'Error Ⅱ: $\beta=${beta}'.format(beta=f'{100*beta:.0f}%')
        ])
        return fig, ax