# doublePy

Python script to manage doublicate musik samples.
Works with all files

## Installation

```sh
git clone https://github.com/3zbumban/doublePy.git
cd doublePy
pip install -r requirements.txt
```

## Usage

```sh
python dubPy.py -h
python dubPy.py --help
```

```sh
python dubPy.py -p <"path to folder"> <...> ... -pl -rm -s -td -fl -sf
python dubPy.py --path <"path to folder"> <...> ... --play --remove --strategy --save-file --topdown --links
```

- `-p / --path`: path(s) to folder to scan _"I:\example\dir\...\...\"_
- `-td / --topdown`: use `os.walk(topdown=True)`
- `-fl / --links`: enables following symlinks
- `-pl / --play`: play file dialog
- `-rm / --remove`: move file to trash dialog
- `-s / --strategy`: asks user to rerun process after deleting a file
- `-sf / --save-file`: saves results to `results.txt`

### Find doublicate files (all filetypes)

```sh
python dubPy.py -p <"path to folder"> <...> ...
```

optional: `-td -fl -sf`

### Find doublicate samples, listen and delete

```sh
python dubPy.py -p <"path to folder"> <...> ... -pl -s -rm
```

optional: `-td -fl -sf`