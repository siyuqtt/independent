__author__ = 'siyuqiu'
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
class PlotView:

    def __init__(self):
        self.acnt = None
        self.date = None

    def setAcntName(self, acnt):
        self.acnt = acnt

    def setDate(self, date):
        self.date = date

    def showplot(self, xlable):
        plt.xticks(xlable)
        plt.show()

    def showLegend(self):
        plt.legend()

    def newFigure(self):
        plt.figure()

    def plotLine(self, x, y, lab,mark=None):
        if mark:
            plt.plot(x,y,mark, label=lab)
        else:
            plt.plot(x,y, label=lab)



    def plotBar(self, xlable, means, std, title,lab):
        """

        :param singleUrlDict: (date: num)
        :return:
        """
        n_groups = len(xlable)



       # fig, ax = plt.subplots()

        index = np.arange(n_groups)
        bar_width = 0.35

        opacity = 0.4
        error_config = {'ecolor': '0.3'}
        if std is not None:
            plt.bar(index, means, bar_width,
                         alpha=opacity,
                         color='b',
                         yerr=std,
                         error_kw=error_config,
                         label=lab)
        else:
            plt.bar(index, means, bar_width,
                         alpha=opacity,
                         color='b',
                         label=lab)




        plt.xlabel('Time')
        plt.ylabel('Num')
        plt.title(title)
        # plt.xticks(index + bar_width, ('A', 'B', 'C', 'D', 'E'))
        plt.xticks(index + bar_width, xlable)
        plt.legend()
        plt.tight_layout()