from robo.api import extract_list, extract_one
from robo.extractors import get_extractor_names

# Library API here
# What applications/plugins would need, something like:
#    get_extractors: get a list of possible extractors to show user
#    extract_one: get data for ONE term with given extractor
#    extract_list: get data from a LIST of terms with given extractor

__all__ = ["get_extractor_names", "extract_list", "extract_one"]
