# dupFinder.py
import os
import sys
import hashlib
import argparse
import winsound
import platform
import subprocess
from send2trash import send2trash

BLOCK_SIZE = 65536
CHAR_KONST = 97
cols, rows = os.get_terminal_size()

argparser = argparse.ArgumentParser(description="Find doublicate files, give one or more paths as arguments \nUsage: python dupPy.py -p folder1 folder2 <...>")
argparser.add_argument("-p", "--path", type=str, nargs="+", dest="paths", help="give one or more paths to dirs \nexample: -p \"I:\\example\\dir\\...\\...\"")
argparser.add_argument("-td", "--topdown", action="store_true", dest="topdown", help="add '-r' to scan topdown")
argparser.add_argument("-fl", "--links", action="store_true", dest="followlinks", help="add '-f' to follow symlinks")
argparser.add_argument("-pl", "--play", action="store_true", dest="player", help="add '-p' or '--path' flag to user system own player")
argparser.add_argument("-rm", "--remove", action="store_true", dest="rem", help="add '-r' or '--remove' flag to enable remove dialog")
argparser.add_argument("-s", "--strategy", action="store_true", dest="strat", help="add '-s' or '--strategy' flag to ask for restart after removing a file")
argparser.add_argument("-sf", "--save-file", action="store_true", dest="tofile", help="add '-sf' or '--save-file' flag to save to a file")


args, unknown = argparser.parse_known_args()

# play file with winsound
def play(file):
    print("[>] playing: \t{}...".format(file))
    if platform.system() == "Windows":
        winsound.PlaySound(file, winsound.SND_FILENAME)
    else:
        sysPlay(file)

# open file with shell
def sysPlay(file):
    print("[d] sysPlay: {}".format(file))
    subprocess.call("\"{}\"".format(file), shell=True)

def findDup(parentFolder):
    # Dups in format {hash:[names]}
    if args.topdown:
        print("[I] using topdown method")
        t = True
    else:
        t = False
    if args.followlinks:
        print("[I] including sym-links")
        f = True
    else:
        f = False
    # start scanning:
    dups = {}
    for dirName, subdirs, fileList in os.walk(parentFolder, topdown=t, followlinks=f):
        print("[i] Scanning: {}...".format(dirName))
        for filename in fileList:
            # Get the path to the file
            path = os.path.join(dirName, filename)
            # Calculate hash
            file_hash = hashfile(path)
            # Add or append the file path
            if file_hash in dups:
                dups[file_hash].append(path)
            else:
                dups[file_hash] = [path]
    return dups
 
# Joins two dictionaries
def joinDicts(dict1, dict2):
    for key in dict2.keys():
        if key in dict1:
            dict1[key] = dict1[key] + dict2[key]
        else:
            dict1[key] = dict2[key]
 
# hash the file
def hashfile(path, blocksize = BLOCK_SIZE):
    afile = open(path, "rb")
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()
 
# returns result array with pairs
def createResults(dict1):
    return list(filter(lambda x: len(x) > 1, dict1.values()))

def playResult(result):
    try:
        if len(result) > 1:
            p = True
            while p:
                a = ord(input("[?] wich one to play? (a/b/c/...)? ")) - CHAR_KONST
                if a <= len(result) - 1 and a >= 0:
                    if(result[a].endswith(".wav")):
                        play(result[a])
                    else:
                        print("[e] the file is not playable...")
                        if(input("[?] do you want to open the file in the explorer? (y/n) ") == "y"):
                            print("[i] opening in explorer...")
                            subprocess.Popen("explorer /select, \"{}\"".format(result[a]))
                        else:
                            continue
                    p = True
                else:
                    p = False
            if(args.rem):
                r = ord(input("[?] wich one do you want to delete? (a/b/c/...) ")) - CHAR_KONST
                if r <= len(result) - 1 and r >= 0:
                    if(os.path.isfile(result[r])):
                        print("[i] removing: {}".format(result[r]))
                        send2trash(result[r])
                    else:
                        print("[e] {} ist not a valid file".format(result[r]))
            if(args.strat):
                if(input("[?] do you want to restart? (y/n) ") == "y"):
                    return True
                else:
                    return False
    except KeyError:
        print("[E] KeyError...")
        pass

def showResults(results):
    if len(results) > 0:
        c = 0
        print('\n\n[A] Duplicates Found:')
        print('[>] The following files are identical. The name could differ, but the content is identical')
        for result in results:
            ch = 'a'
            print("_" * cols)
            print("Nr: {}\t{} duplicates...".format(c, len(result)))
            for subresult in result:
                print('{}) \t{}' .format(ch ,subresult))
                ch = chr(ord(ch) + 1)
            print("_" * cols)
            c += 1
            if(args.player):
                if playResult(result):
                    return True
                else:
                    continue
    else:
        print('[A] No duplicate files found.')
    return False

def toFile(results):
    with open("results.txt", "w") as f:
        for result in results:
            ch = 'a'
            f.write("{}\n".format("_" * cols))
            f.write("Nr: {}\t{} duplicates...".format(c, len(result)))
            for subresult in result:
                f.write('{}) \t{}' .format(ch ,subresult))
                ch = chr(ord(ch) + 1)
            f.write("{}".format("_" * cols))
            c += 1

def main():
    if args.paths:
        print("[I] starting scan. quit with [ctrl + c]")
        e = True
        while e:
            try:
                dups = {}
                folders = args.paths
                for i in folders:
                    if os.path.exists(i):
                        joinDicts(dups, findDup(i))
                    else:
                        print("[e] {} is not a valid path, please verify".format(i))
                        sys.exit()
                results = createResults(dups)
                if(args.tofile):
                    toFile(results)
                e = showResults(results)
            except KeyboardInterrupt:
                print("[e] KeyboardInterrupt...")
    else:
        print("[e] no paths given...")
        sys.exit(-1)
 
if __name__ == "__main__":
    main()