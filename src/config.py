import argparse
import json

from . import commons


class Config:
    def __init__(self, types):
        self.types = types.copy()
        self.values = {name: None for name in types.keys()}
        self.input_path = None
        self.output_path = None
        self.force_rewrite = False
        self.needs_save = None
        self.train_input_path = None

    def load(self, argv):
        parser = argparse.ArgumentParser()
        parser.add_argument('-uc', '--use-config', type=str, default=None)
        parser.add_argument('-in', '--input', type=str, default=None)
        parser.add_argument('-out', '--output', type=str, default=None)
        parser.add_argument('-fr', '--force-rewrite', action='store_true')
        parser.add_argument('-sc', '--save-config', type=str, default=None)
        parser.add_argument('-ti', '--train-input', type=str, default=None)
        for n, t in self.types.items():
            parser.add_argument(f'-{n}', type=t, default=None)
        parsed_values = vars(parser.parse_args(argv))
        config_name = parsed_values['use_config']
        self.force_rewrite = parsed_values['force_rewrite']
        if config_name is not None:
            with open(f'{commons.CONFIG_PATH / config_name}.json', 'r') as f:
                values_from_file = dict(json.load(f))
                self.input_path = values_from_file.get('input', None)
                self.output_path = values_from_file.get('output', None)
                self.force_rewrite = values_from_file.get('force_rewrite', False)
                self.train_input_path = values_from_file.get('train_input', None)
                for n, t in self.types.items():
                    self.values[n] = t(values_from_file.get(n, None))
        if parsed_values['input'] is not None:
            self.input_path = parsed_values['input']
        if parsed_values['output'] is not None:
            self.output_path = parsed_values['output']
        if parsed_values['save_config'] is not None:
            self.needs_save = commons.CONFIG_PATH / parsed_values['save_config']
            assert not self.needs_save.exists()
        if parsed_values['train_input'] is not None:
            self.needs_save = commons.CONFIG_PATH / parsed_values['train_input']
        assert self.input_path is not None
        assert self.output_path is not None
        self.input_path = commons.INPUT_PATH / (self.input_path + '.csv')
        self.output_path = commons.OUTPUT_PATH / (self.output_path + '.csv')
        if self.train_input_path is not None:
            self.train_input_path = commons.INPUT_PATH / (self.train_input_path + '.csv')
        assert self.input_path.exists()
        assert self.force_rewrite or not self.output_path.exists()
        for n, t in self.types.items():
            if self.values[n] is None:
                self.values[n] = t(parsed_values[n])

    def save(self):
        if self.needs_save is None:
            return
        values = self.values.copy()
        values.update({
            'input': self.input_path,
            'output': self.output_path,
            'train_input': self.train_input_path,
            'force_rewrite': self.force_rewrite,
        })
        with open(self.needs_save) as f:
            json.dump(values, f)
