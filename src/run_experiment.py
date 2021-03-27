import numpy as np
from . import ficnn
from collections import namedtuple
from tqdm import tqdm


model_spec = namedtuple('model_spec', 'config build')
specs = {
    'ficnn': model_spec(ficnn.get_config, ficnn.build)
}


def run(argv):
    name = argv[0]
    config = specs[name].config()
    config.load(argv[1:])
    model = specs[name].build(config)
    if config.train_input_path is not None:
        data = np.loadtxt(config.train_input_path, delimiter=',')
        N = len(data)
        for t in tqdm(range(N)):
            x = data[t:t + 1, :-1]
            y = data[t:t + 1, -1:]
            model.predict(x)
            model.observe(y)
    data = np.loadtxt(config.input_path, delimiter=',')
    N = len(data)
    result = np.zeros((N, 5))
    for t in tqdm(range(N)):
        x = data[t:t + 1, :-1]
        y = data[t:t + 1, -1:]
        result[t] = model.predict(x)
        model.observe(y)
    np.savetxt(config.output_path, result, delimiter=',')
