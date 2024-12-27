import io
import yaml
import os
import copy
import argparse
import hashlib
import pickle
import pprint
from tqdm import tqdm

class ProgressFileWrapper(io.TextIOBase):
    def __init__(self, file, callback):
        self.file = file
        self.callback = callback
    def read(self, size=-1):
        buf = self.file.read(size)
        if buf:
            self.callback(len(buf))
        return buf
    def readline(self, size=-1):
        buf = self.file.readline(size)
        if buf:
            self.callback(len(buf))
        return buf
    def write(self, s):
        self.callback(len(s))
        self.file.write(s)


def resolve_refs(
    data,
    base_dir,
    root_data,
    processed_refs = set(),
    entry_ref = False
):
    """Рекурсивно разрешает $ref в структуре данных."""

    if isinstance(data, dict):
        if '$ref' in data:
            ref_path = data['$ref']

            if ref_path.startswith("#"):
                ref_path = ref_path[2:]
                file_name = hashlib.md5(ref_path.encode()).hexdigest() + '.yaml';
                save_path = 'refs/' + file_name
                file_path = file_name if entry_ref else save_path

                if file_name in processed_refs:
                    return {'$ref': file_path}

                processed_refs.add(file_name)

                current = root_data
                for part in ref_path.split('/'):
                    if part in current:
                        current = current[part]
                    else:
                        return data

                ref_data = resolve_refs(
                    current,
                    base_dir,
                    root_data,
                    processed_refs,
                    True
                )

                output = os.path.join(base_dir, save_path)
                with open(output, 'w') as out_file:
                    size = estimate_yaml_size(ref_data)
                    with tqdm(
                        total=size,
                        unit='B',
                        unit_scale=True,
                        desc=f"Dump {output}"
                    ) as bar:
                        yaml.dump(
                            ref_data,
                            ProgressFileWrapper(out_file, bar.update),
                            sort_keys=False,
                            allow_unicode=True
                        )

                    return {'$ref': file_path}

        for k, v in data.items():
            data[k] = resolve_refs(
                v,
                base_dir,
                root_data,
                processed_refs,
                entry_ref
            )
    elif isinstance(data, list):
        for i, item in enumerate(data):
            data[i] = resolve_refs(
                item,
                base_dir,
                root_data,
                processed_refs,
                entry_ref
            )

    return data


def load_yaml_with_progress(input_file):
    """Загружает YAML с отображением прогресса."""
    with open(input_file, 'r') as file:
        size = os.stat(file.fileno()).st_size
        with tqdm(total=size, unit='B', unit_scale=True, desc=f'Loading {input_file}') as bar:
            try:
                data = yaml.load(
                    ProgressFileWrapper(file, bar.update),
                    Loader=yaml.SafeLoader
                )
            except yaml.YAMLError as e:
                 print(f"Error during YAML load: {e}")
                 return None

    return data


def calculate_file_hash(path):
    with open(path, 'rb') as file:
        return hashlib.md5(file.read()).hexdigest()


def read_cache(path):
    if os.path.exists(path):
        with open(path, 'rb') as file:
            size = os.stat(file.fileno()).st_size
            with tqdm(
                total=size,
                unit='B',
                unit_scale=True,
                desc='Reading cache...'
            ) as bar:
                return pickle.load(ProgressFileWrapper(file, bar.update))

    return None


def estimate_yaml_size(data, indent_level=0):
    size = 0
    indent = "  " * indent_level  # Предполагаем отступ в 2 пробела

    if isinstance(data, dict):
        size += 2 # "{" + "}"
        keys = list(data.keys())
        for i, key in enumerate(keys):
            size += len(str(key).encode('utf-8')) + 2  # key:
            size += estimate_yaml_size(data[key], indent_level + 1)
            if i < len(keys) -1:
                 size += 2
        size += len(indent)
    elif isinstance(data, list):
        size += 2 # "[" + "]"
        for i, item in enumerate(data):
           size += estimate_yaml_size(item, indent_level + 1)
           if i < len(data) - 1:
                size += 2
        size += len(indent)
    elif isinstance(data, str):
        size += len(data.encode('utf-8')) + 2 # "string"
    elif isinstance(data, (int, float)):
         size += len(str(data))
    elif isinstance(data, bool):
        size += 4 if data else 5
    elif data is None:
        size += 4
    return size


def split_openapi_by_tags(input_file, output_dir, cache_file):
    data = read_cache(cache_file)

    write_cache = False
    if data is None:
        data = load_yaml_with_progress(input_file)
        write_cache = True

    if data is None:
        return None

    refs_dir = output_dir + '/refs'
    if not os.path.exists(refs_dir):
        os.makedirs(refs_dir)

    main_openapi = {
        'openapi': data.get('openapi', '3.0.0'),
        'info': data.get('info'),
        'components': data.get('components', {}),
        'paths': {}
    }

    tag_data = {} # Данные (пути) данных разделенных на теги
    processed_paths = set() # Набор для отслеживания обработанных путей
    processed_refs = set() # Набор для отслеживания ссылок

    if 'paths' in data:
        paths_list = list(data['paths'].items())

        for path_name, path_data in paths_list:

            methods = ['get', 'post', 'put', 'delete', 'patch']

            for method in methods:
                if method in path_data and path_data[method]:
                    tags = path_data[method]['tags']
                    break
            else:
                tags = ['default']

            for tag in tags:
                if tag not in tag_data:
                    tag_data[tag] = {}

                if path_name not in processed_paths:

                    path_data_copy = copy.deepcopy(path_data)

                    for method in methods:
                        if method in path_data_copy and path_data_copy[method]:
                            path_data_copy[method]['tags'].remove(tag)
                            path_data_copy[method]['tags'].append(method)

                    resolved_path_data = resolve_refs(
                        path_data_copy,
                        output_dir,
                        data,
                        processed_refs
                    )

                    tag_data[tag][path_name] = resolved_path_data
                    processed_paths.add(path_name)

                main_openapi['paths'][path_name] = {'$ref': f"{tag}.yaml"}

    # Запись данных в файлы
    for tag, tag_content in tag_data.items():
        output = f"{output_dir}/{tag}.yaml"
        with open(output, 'w') as out_file:
            size = estimate_yaml_size(tag_content)
            with tqdm(total=size, unit='B', unit_scale=True, desc=f'Dump {output}') as bar:
                yaml.dump(
                    tag_content,
                    ProgressFileWrapper(out_file, bar.update),
                    sort_keys=False,
                    allow_unicode=True
                )

    output = f"{output_dir}/openapi.yaml"
    with open(output, "w") as out_file:
        size = estimate_yaml_size(main_openapi)

        with tqdm(total=size, unit='B', unit_scale=True, desc=f'Dump {output}') as bar:
            yaml.dump(
                main_openapi,
                ProgressFileWrapper(out_file, bar.update),
                sort_keys=False,
                allow_unicode=True
            )

    if write_cache:
        return data

    return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='openapi-splitter',
        description='Разделяет большую openapi.yaml спецификацию на составные части по тегам',
    )

    parser.add_argument('openapi', help='Конфиг openapi.yaml')
    parser.add_argument('outDir', help='В какую директорию сохранять')

    args = parser.parse_args()

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    hash_openapi_spec = calculate_file_hash(args.openapi);

    cache_dir = f"{ROOT_DIR}/.cache";
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    if os.path.exists(args.openapi):
        cache_file = cache_dir + '/' + calculate_file_hash(args.openapi) + '.pkl';

        data = split_openapi_by_tags(
            args.openapi,
            args.outDir,
            cache_file
        )

        if data is not None:
            with open(cache_file, 'wb') as file:
                print('Dump cache...')
                pickle.dump(data, file)
