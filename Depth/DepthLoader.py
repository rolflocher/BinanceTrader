
from Depth.DepthSelector import DepthSelector
from Depth.DepthTransformer import DepthTransformer

class DepthLoader:

    def __init__(self, selector = None, transformer = None):
        if selector == None:
            selector = DepthSelector()
        if transformer == None:
            transformer = DepthTransformer()
        self.selector = selector
        self.transformer = transformer

    def load(self, databaseName, limit = 100000):
        diffs, seed = self.selector.select(databaseName, limit)
        return self.transformer.transform(diffs, seed)
