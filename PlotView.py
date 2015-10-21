__author__ = 'siyuqiu'
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

    def plotSingleUrlTrend(self, singleUrlDict ):
        """

        :param singleUrlDict: (date: num)
        :return:
        """
        n_groups = len(singleUrlDict)

        means_men = (20, 35, 30, 35, 27)
        std_men = (2, 3, 4, 1, 2)



        fig, ax = plt.subplots()

        index = np.arange(n_groups)
        bar_width = 0.35

        opacity = 0.4
        error_config = {'ecolor': '0.3'}

        rects1 = plt.bar(index, means_men, bar_width,
                         alpha=opacity,
                         color='b',
                         yerr=std_men,
                         error_kw=error_config,
                         label='Men')



        plt.xlabel('Date')
        plt.ylabel('Num')
        plt.title('Single Url Trend')
        # plt.xticks(index + bar_width, ('A', 'B', 'C', 'D', 'E'))
        plt.xticks(index + bar_width, singleUrlDict.keys())
        plt.legend()

        plt.tight_layout()
        plt.show()