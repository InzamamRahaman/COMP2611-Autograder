import json
import argparse
import os
import glob
import zipfile
import collections
import subprocess
import file_comparator

parser = argparse.ArgumentParser()
parser.add_argument('--config')

def process_python():
    subprocess.call(['python', 'main.py'])

def process_c():
    subprocess.call(['gcc', 'main.c'])
    subprocess.call(['./a.out'])

def process_cpp():
    subprocess.call(['g++', 'main.cpp'])
    subprocess.call(['./a.out'])

def process_java():
    subprocess.call(['javac', 'Main.java'])
    subprocess.call(['java', 'Main.class'])

def get_runner(lang):
    lang = lang.strip().lower()
    langs = {
        'python': process_python,
        'java': process_java,
        'c++': process_cpp,
        'c': process_c,
        'cpp': process_cpp
    }
    return langs[lang]


def unzip_submissions(folder):
    os.chdir(folder)
    os.mkdir('zipped')
    zipped_folder = glob.glob('*.zip')
    print(zipped_folder)
    for zip_folder in zipped_folder:
        name, _ = zip_folder.split('.zip')
        with zipfile.ZipFile(zip_folder, "r") as zip_ref:
            zip_ref.extractall(f'./zipped/')

def process_part(part, config, lang):
    try:
        os.chdir(part)
        text_files = glob.glob('*.txt')
        for file in text_files:
            subprocess.call(['rm', file])
        for file_path in config["cases_input"][part]:
            head, tail = os.path.split(file_path)
            subprocess.call(['cp', file_path, tail])
        runner = get_runner(lang)
        runner()
        text_files = glob.glob('solution*.txt')
        solution_file = text_files[0]
        ideal_solution_file = config['cases_output'][part]
        if file_comparator.comprator(solution_file, ideal_solution_file):
            return 10
    except:
        return 0







def process_student(id, config):
    try:
        os.chdir(id)
        student_config = {'lang': 'python'}
        with open('config.json', 'r') as fp:
            student_config = json.load(fp)
        current_dir = os.getcwd()
        parts = config['parts']
        marks = []
        for part in parts:
            marks.append(process_part(part, config, student_config['lang']))
            os.chdir(current_dir)
        return marks
    except:
        print('Error handling ', id)
        return [0] * int(config["num_parts"])



def process(config):
    unzip_submissions(config['scripts'])
    os.chdir('./zipped')
    ids = os.listdir('.')
    marks = collections.defaultdict(list)
    current_dir = os.getcwd()
    print(current_dir)
    for id in ids:
        mark_for_student = (process_student(config))
        marks[id] = mark_for_student
        os.chdir(current_dir)
    return marks

def mark_dict_to_csv(marks, config):
    parts = list(config['cases_output'].keys())
    content = f"Student ID,{','.join(parts)}\n"
    for id, marks in marks.items():
        content += f"{id},','.join(map(str, marks))\n"
    with open(config['mark_file'], 'w') as fp:
        fp.write(content)



def main():
    args = parser.parse_args()
    with open(args.config, 'r') as fp:
        config = json.load(fp)
        marks = process(config)
        mark_dict_to_csv(marks, config)



if __name__ == '__main__':
    main()