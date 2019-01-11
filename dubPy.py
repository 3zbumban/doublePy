# dupFinder.py
import os
import sys
import hashlib
import argparse

argparser = argparse.ArgumentParser(description="Find doublicate files, give one or more paths as arguments \nUsage: python dupPy.py -p folder1 folder2 <...>")
argparser.add_argument("-p", "--path", type=str, nargs="+", dest="paths", help="give one or more paths to dirs \nexample: \"I:\\example\\dir\\...\\...\"")

args, unknown = argparser.parse_known_args()

def findDup(parentFolder):
    # Dups in format {hash:[names]}
    dups = {}
    for dirName, subdirs, fileList in os.walk(parentFolder):
        print("[i] Scanning {}...".format(dirName))
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
 
 
def hashfile(path, blocksize = 65536):
    afile = open(path, "rb")
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()
 
 
def printResults(dict1):
    results = list(filter(lambda x: len(x) > 1, dict1.values()))
    if len(results) > 0:
        print('\n\nDuplicates Found:')
        print('The following files are identical. The name could differ, but the content is identical')
        print('_' * 50)
        for result in results:
            for subresult in result:
                print('\t{}' .format(subresult))
            print('_' * 50)
    else:
        print('No duplicate files found.')

def main():
    if args.paths:
        dups = {}
        folders = args.paths
        for i in folders:
            # Iterate the folders given
            if os.path.exists(i):
                # Find the duplicated files and append them to the dups
                joinDicts(dups, findDup(i))
            else:
                print("[e] {}} is not a valid path, please verify".format(i))
                sys.exit()
        printResults(dups)
    else:
        print("[e] no paths given...")
        sys.exit(-1)
 
if __name__ == "__main__":
    main()