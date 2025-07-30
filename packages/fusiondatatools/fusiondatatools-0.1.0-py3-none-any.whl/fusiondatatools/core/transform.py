import copy


class TransformModule(object):
    
    def __init__(self, cfg):
        self.cfg = cfg
        
    def transform(self, x):
        pass

    def configure(self, x):
        pass

    def __call__(self, x):
        x = self.transform(x)
        return x
    
    
class SignalTransformer():
    def __init__(
        self, 
        transformers: dict[str, TransformModule],
        cfg: dict,
        ):
        
        self.transformers = {}
        
        for transformer_type, transformer in transformers.items():
            self.transformers[transformer_type] = copy.deepcopy(transformer(cfg))
    
    def configure(self, sample):
        for transformer_type, transformer in self.transformers.items():
            transformer.configure(sample[transformer_type])
    
    def __getitem__(self, transformer_type):
        return self.transformers[transformer_type]
    
    def __call__(self, x, transformer_type='feature'):
        return self(transformer_type)(x)