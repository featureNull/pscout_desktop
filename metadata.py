import metadata_pb2
import metadata_pb2_grpc
import re


categories = None
_models_metadata = None
_search_tree = {}
_wordlist = []
_wordlist_lowercase = []


def init(channel):
    _load_categories(channel)
    _load_model_metadata(channel)
    _build_search_tree()
    _build_word_list()


def get_category_model_count(catid, words):
    def contains(text, words):
        lt = text.lower()
        for word in words:
            if lt.find(word.lower()) == -1:
                return False
        return True

    count = 0
    for text in _search_tree[catid].values():
        if contains(text, words):
            count += 1
    return count


def _load_categories(channel):
    global categories
    pb2 = metadata_pb2
    stub = metadata_pb2_grpc.DatabaseStub(channel)
    request = pb2.GetCategoriesRequest(language=pb2.Language.EN)
    categories = stub.GetCategories(request)


def _load_model_metadata(channel):
    global _models_metadata
    stub = metadata_pb2_grpc.DatabaseStub(channel)
    request = metadata_pb2.GetModelsMetadataRequest()
    _models_metadata = stub.GetModelsMetadata(request)


def _extract_words(text):
    alpanumerics = re.sub(r'[.,;:/]', ' ', text)
    txtlist = [x.strip() for x in alpanumerics.split(' ')]
    return [x for x in txtlist if len(x) > 3]


def _build_search_tree():
    for m in _models_metadata.entities:
        catid = m.categoryid
        if catid not in _search_tree:
            _search_tree[catid] = {}
        # merge a lowercase build string
        united = ' '.join([m.artikelnum, m.shortdesc, m.longdesc])
        _search_tree[catid][m.id] = united


def _build_word_list():
    global _wordlist
    global _wordlist_lowercase

    vollelangertext = ''
    for blabla in _search_tree.values():
        vollelangertext += ' '.join([x for x in blabla.values()])

    alpanumerics = re.sub(r'[.,;:/"]', ' ', vollelangertext)
    textlist = [x.strip() for x in alpanumerics.split(' ')]
    textlist = [x for x in textlist if len(x) >= 3]
    textdict = dict.fromkeys(textlist)
    _wordlist = list(textdict)
    _wordlist_lowercase = [x.lower() for x in _wordlist]


def get_stl_data(channel, modelid: int):
    stub = metadata_pb2_grpc.DatabaseStub(channel)
    request = metadata_pb2.GetStlDataRequest(modelid=modelid)
    reply = stub.GetStlData(request)
    return reply.data
