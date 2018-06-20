# -*- coding: utf-8 -*-
import numpy as np
import scipy.cluster.hierarchy as hac
import matplotlib.pyplot as plt
import sklearn
from sklearn.feature_extraction.text import CountVectorizer


class Clustering():
    def plotClusters(self, a):
        fig, axes23 = plt.subplots(2, 1)
        z = hac.linkage(a, method='ward')

        # Plotting
        axes23[0].plot(range(1, len(z)+1), z[::-1, 2])
        knee = np.diff(z[::-1, 2], 2)
        print(knee)
        axes23[0].plot(range(2, len(z)), knee)

        num_clust1 = knee.argmax() + 2
        print(knee[knee.argmax()])
        print(knee.argmax())
        knee[knee.argmax()] = 0

        print(num_clust1, z[::-1, 2][num_clust1-1])
        axes23[0].text(num_clust1, z[::-1, 2][num_clust1-1], 'possible\n<- knee point')

        hac.dendrogram(z)

        plt.tight_layout()
        plt.show()

    def returnKnee(self, a, ru):
        z = hac.linkage(a, method='ward')
        knee = np.diff(z[::-1, 2], 2)
        if ru:
            num_clust = knee.argmax()+2
        else:
            num_clust = knee.argmax()-2
        return num_clust

    def namesClustering(self, names, ru, n_clusters):
        ngram_vectorizer = CountVectorizer(min_df=1)  # делаем векторайзер для слов
        counts = ngram_vectorizer.fit_transform(names)  # трансформируем слова в список вектроров
        if n_clusters==None:
            knee = self.returnKnee(counts.toarray(), ru)  # находим количество кластеров, на которое будем делить
        else:
            knee = n_clusters
        print(knee)
        self.plotClusters(counts.toarray())
        affinity = sklearn.cluster.AffinityPropagation().fit(counts.todense())
        n_clusters_aff = len(affinity.cluster_centers_indices_)
        machine = sklearn.cluster.KMeans(n_clusters=n_clusters_aff)  # запукаем машину
        resList = list(machine.fit_predict(counts.todense()))  # получаем список результатов
        groups = [[] for i in range(max(resList) + 1)]  # делаем список списков групп
        for i in range(len(names)):  # для каждого имени
            groups[resList[i]].append(names[i])  # добавляем его в список

        return self.choseClusterName(groups)

    def choseClusterName(self, groups):
        corpus_res = {}  #
        for i in groups:  #
            mainName = self.choseName(i)
            corpus_res[mainName] = i  #
        return corpus_res

    def choseName(self, listOfNames):
        dictNames = dict.fromkeys(set(listOfNames), 0)
        for i in listOfNames:
            dictNames[i] += 1
            if " " in i:
                for j in i.split(" "):
                    try:
                        dictNames[j]+=1
                    except KeyError as e:
                        pass

        val = max(dictNames.values())
        for k, v in dictNames.items():
            if v == val:
                return k

#
# a = np.array([[0.1,   2.5],
#               [1.5,   .4 ],
#               [0.3,   1  ],
#               [1  ,   .8 ],
#               [0.5,   0  ],
#               [0  ,   0.5],
#               [0.5,   0.5],
#               [2.7,   2  ],
#               [2.2,   3.1],
#               [3  ,   2  ],
#               [3.2,   1.3]])
# cl = Clustering()
# print cl.returnKnee(a)
# cl.plotClusters(a)