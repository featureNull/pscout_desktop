from PyQt5.QtCore import QObject, pyqtSignal
import re


class FilterManager(QObject):
    # anzahl moedlle in einer catogry geaendert (id, anzahl)
    categoryCountChanged = pyqtSignal(int, int)

    def __init__(self, categories, modelsMetaData):
        super(FilterManager, self).__init__()
        self.categories = categories
        self.modelsMetaData = modelsMetaData
        self._search_tree = {}
        # build search tree
        for m in modelsMetaData:
            catid = m.categoryid
            if catid not in self._search_tree:
                self._search_tree[catid] = {}
            # merge a lowercase build string
            united = ' '.join([m.artikelnum, m.shortdesc, m.longdesc])
            self._search_tree[catid][m.id] = united
        # build word list
        vollelangertext = ''
        for blabla in self._search_tree.values():
            vollelangertext += ' '.join([x for x in blabla.values()])

        alpanumerics = re.sub(r'[.,;:/"]', ' ', vollelangertext)
        textlist = [x.strip() for x in alpanumerics.split(' ')]
        textlist = [x for x in textlist if len(x) >= 3]
        textdict = dict.fromkeys(textlist)
        self.keywords = list(textdict)
        self._wordlist_lowercase = [x.lower() for x in self.keywords]
        self.filterTexts = []
        self.categoriesEnabled = {}
        for cat in categories:
            self.categoriesEnabled[cat.id] = True

    def addTextFilter(self, text):
        self.filterTexts.append(text)
        self._createStatistics()

    def removeTextFilter(self, text):
        self.filterTexts.remove(text)
        self._createStatistics()

    def getModelCount(self, catid):
        '''request modelcount for spexcific filter
        '''
        def contains(text, words):
            lt = text.lower()
            for word in words:
                if lt.find(word.lower()) == -1:
                    return False
            return True
        count = 0
        for text in self._search_tree[catid].values():
            if contains(text, self.filterTexts):
                count += 1
        return count

    def setCategoryEnabled(self, id, enabled):
        self.categoriesEnabled[id] = enabled
        txt = 'enabled' if enabled else 'disabled'
        print(f'setCategoryEnabled: id={id} {txt}')

    def gebmirallemodelidsdiesseinkoennten(self) -> list:
        modelids = []
        for catid in self.categoriesEnabled.keys():
            kjhkjh = self._getModelIdsUndSo(catid)
            if self.categoriesEnabled[catid]:
                modelids.extend(kjhkjh)
        return modelids

    def _getModelIdsUndSo(self, catid):
        def contains(text, words):
            lt = text.lower()
            for word in words:
                if lt.find(word.lower()) == -1:
                    return False
            return True
        possipilities = []
        for modelid in self._search_tree[catid].keys():
            text = self._search_tree[catid][modelid]
            if contains(text, self.filterTexts):
                possipilities.append(modelid)
        return possipilities

    def _createStatistics(self):
        for cat in self.categories:
            count = self.getModelCount(cat.id)
            self.categoryCountChanged.emit(cat.id, count)
