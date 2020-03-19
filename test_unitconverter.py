from converter import *
from glob import glob
from whyis import nanopub

def load_test_pubs(base_dir=".", prefix="test_"):
    base_path = base_dir + "/" + prefix + "*.json"
    test_pub_list = []
    for path in glob(base_path):
        with open(path, "r") as f:
            test_pub_list.append(f.read())
    return test_pub_list

def main():
    test_pubs = []
    pass
