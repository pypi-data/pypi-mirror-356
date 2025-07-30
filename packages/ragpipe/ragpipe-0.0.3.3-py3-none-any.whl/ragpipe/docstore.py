from pydantic import BaseModel
from typing import Any, List, Set

from .common import get_fpath_items, get_collection_name

class DocSet(BaseModel):
    fpath: str
    items: List[Any]
    item_paths: List[str]
    docpath_pre_filter: Set[str]

    def collection_name_for(self, repname):
        return get_collection_name(self.fpath, repname)



def create_docset(fpath, D, doc_pre_filter):
    docpath_pre_filter = set([d.doc_path for d in doc_pre_filter])
    items_path_pairs = get_fpath_items(fpath, D, docpath_pre_filter=docpath_pre_filter)
    #items, item_paths = items_path_pairs.els, items_path_pairs.paths
    ds = DocSet(fpath=fpath, items=items_path_pairs.els, item_paths=items_path_pairs.paths, docpath_pre_filter=docpath_pre_filter)
    return ds