from PyQt5.QtCore import QObject, pyqtSignal
import re


class FilterManager(QObject):
    # anzahl moedlle in einer catogry geaendert (id, anzahl)
    changed = pyqtSignal()

    def __init__(self, categories, modelsMetaData):
        super().__init__()
        # setup categories
        self.categories = {}
        for cat in categories:
            self.categories[cat.id] = CategoryFilter(cat.shortname, cat.longname)
        # add modelmetadata
        for metadata in modelsMetaData:
            self.categories[metadata.categoryid].insertModel(metadata)
        # build keywords ba category and accumulate
        keywords = []
        for metadata in modelsMetaData:
            catkwrds = self.categories[metadata.categoryid].buildKeyWords()
            keywords.extend(catkwrds)
        self.keywords = list(dict.fromkeys(keywords))
        self.textFilters = []

    def addTextFilter(self, text):
        self.textFilters.append(text)
        self.changed.emit()

    def removeTextFilter(self, text):
        self.textFilters.remove(text)
        self.changed.emit()

    @property
    def anyfilterActive(self) -> bool:
        '''kein filter ist gresetzt'''
        for cats in self.categories.values():
            if not cats.enabled:
                return True
        return len(self.textFilters) > 0

    @property
    def filteredModelids(self) -> list:
        '''alle modelids die im filter sind'''
        modelids = []
        for cats in self.categories.values():
            if cats.enabled:
                modelids.extend(cats.getFilteredModelIds(self.textFilters))
        return modelids

    def getFilteredModelCount(self, catid):
        '''filtered modelids fuer eine Kategory
        auf self.categoriesEnabled wird keine ruecksicht genommen
        '''
        cat = self.categories[catid]
        ids = cat.getFilteredModelIds(self.textFilters)
        return len(ids)

    def enableCategory(self, catid: int, val: bool):
        if val != self.categories[catid].enabled:
            self.categories[catid].enabled = val
            self.changed.emit()


class CategoryFilter(QObject):
    def __init__(self, shortname, longname):
        super(CategoryFilter, self).__init__()
        self.shortname = shortname
        self.longname = longname
        self.enabled = True
        self.modelKeyWords = {}

    def insertModel(self, metadata):
        united = ' '.join([metadata.artikelnum, metadata.shortdesc, metadata.longdesc])
        self.modelKeyWords[metadata.id] = united

    def buildKeyWords(self):
        united = ' '.join([w for w in self.modelKeyWords.values()])
        alpanum = re.sub(r'[.,;:/"]', ' ', united)
        textlist = [w.strip() for w in alpanum.split(' ')]
        # wort hat min 3 chars
        textlist = [w for w in textlist if len(w) >= 3]
        # remove duplicates
        self.keywords = list(dict.fromkeys(textlist))
        return self.keywords

    def getFilteredModelIds(self, filterTexts):
        matches = []
        for modelid in self.modelKeyWords.keys():
            text = self.modelKeyWords[modelid]
            if _contains(text, filterTexts):
                matches.append(modelid)
        return matches


def _contains(text, words):
    lt = text.lower()
    for word in words:
        if lt.find(word.lower()) == -1:
            return False
    return True
