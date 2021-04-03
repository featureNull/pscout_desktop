import pytest
import filter
from dataclasses import dataclass


@dataclass
class Category:
    id: int
    shortname: str
    longname: str


@dataclass
class ModelMetaData:
    id: int
    artikelnum: str
    shortdesc: str
    longdesc: str
    categoryid: int


def test_empty():
    mgr = filter.FilterManager(categories=[], modelsMetaData=[])
    assert len(mgr.categories) == 0
    assert len(mgr.keywords) == 0
    assert mgr.anyfilterActive is False
    assert len(mgr.filteredModelids) == 0


def test_one_category():
    cat = [Category(1, 'sn1', 'ln1')]
    mm = [ModelMetaData(1, 'artikelnum', 'short description', 'long description', categoryid=1)]
    mgr = filter.FilterManager(cat, mm)
    assert len(mgr.categories) == 1
    # artikelnum, short, description, long
    assert len(mgr.keywords) == 4


def test_textfilter():
    cat = [Category(1, 'sn1', 'ln1')]
    m1 = ModelMetaData(1, 'Froh', 'zu sein bedarf-es', ' Wenig, denn wer froh is', categoryid=1)
    m2 = ModelMetaData(2, 'alle', 'menschen', 'san ma zwieda', categoryid=1)
    mgr = filter.FilterManager(cat, [m1, m2])
    assert mgr.getFilteredModelCount(catid=1) == 2
    assert mgr.anyfilterActive is False
    # add different text filters none camelcase
    keywords = ['froh', 'es', 'sein']
    for kw in keywords:
        mgr.addTextFilter(kw)
        assert mgr.getFilteredModelCount(catid=1) == 1
        assert mgr.anyfilterActive
    # remove all filters
    for kw in keywords:
        mgr.removeTextFilter(kw)
    assert mgr.getFilteredModelCount(catid=1) == 2
    assert mgr.anyfilterActive is False
    with pytest.raises(ValueError):
        mgr.removeTextFilter('notinsertedfilter')


def test_categorycount():
    cat = [Category(1, '', ''), Category(2, '', '')]
    m1 = ModelMetaData(1, 'Froh', 'zu sein bedarf-es', ' Wenig, denn wer froh is', categoryid=1)
    m2 = ModelMetaData(2, 'alle', 'menschen', 'san ma zwieda', categoryid=2)
    mgr = filter.FilterManager(cat, [m1, m2])
    assert len(mgr.filteredModelids) == 2
    for id in [1, 2]:
        mgr.enableCategory(id, False)
    assert len(mgr.filteredModelids) == 0
    with pytest.raises(KeyError):
        mgr.enableCategory(666, False)
