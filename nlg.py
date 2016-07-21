# CK2 Culture Namelist Generator
# Copyright (C) 2016 Gundam Astraea Type F2
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General  Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

# _keys = [] # the keys in the first column
# _culturelist = [] # list of cultures, in order

import copy


class nlg:
    '''
    Call process_file(source), and then generate the useable dictionary mapping
    '''
    def __init__(self, source: str):
        self.process_file(source)
        self.append_keys()
        self.prepare_name_strings()

    '''
    Opens the file, read all the lines, and creates the appropriate lists.
    '''
    def process_file(self, source: str):
        # open the file and extract the contents
        try:
            with open(source, encoding="cp1252") as openedsource:
                namekeystring = "#"
                while(namekeystring[0] == '#'):
                    namekeystring = openedsource.readline()
                culturelinelist = openedsource.readlines()
                #print(culturelinelist)
        except:
            print("Could not open file because it does not exist.")
            exit()
        # Need to remove the newlines
        namekeystring = namekeystring[:-1]
        for i in range(0, len(culturelinelist)):
            culturelinelist[i] = culturelinelist[i][:-1]
        #print(namekeystring)
        #print(culturelinelist)
        namekeylist = namekeystring.split(";")[1:]
        culturedict = {}
        for culturelinestr in culturelinelist:
            culturenamelist = culturelinestr.split(";")
            #print(culturelinestr)
            culturedict[culturenamelist[0]] = culturenamelist[1:]
        self.__culturedict = copy.deepcopy(culturedict)
        self.__namekeylist = copy.deepcopy(namekeylist)
        #print(self.__culturedict)
        #print(self.__namekeylist)

    '''
    Attaches key at the end of each name.
    '''
    def append_keys(self):

        namekeylist = self.__namekeylist
        # Use local copy instead of modifying global instance variables
        culturedict = copy.deepcopy(self.__culturedict)
        for i, culturekey in zip(range(0, len(namekeylist)),
                                 self.__culturedict):
            culturedict[culturekey][i] = \
                self.__append_keys_(namekeylist[i],
                                    self.__culturedict[culturekey][i])
        self.__culturedict_ = copy.deepcopy(culturedict)
        #print(self.__culturedict_)

    '''
    Helper function that appends the key at the end of each name and returns
    names contained in lists.
    '''
    def __append_keys_(self, namekey: str, namestring: str) -> list:
        namelist = namestring.split(",")
        for i in range(0, len(namelist)):
            if "~" in namelist[i]:
                # having any other values would be a a contradiction so this is
                # equivalent to namelist[i] == '~' and avoids the headache of
                # deeper string-checking if the user formats the tuple
                # incorrecty.
                namelist = []
                break
            elif namelist[i] == "@":
                namelist[i] = namekey + "_" + namekey
            else:
                namelist[i] += "_" + namekey
            if " " in namelist[i]:
                namelist[i] = "\"" + namelist[i] + "\""
        return namelist

    def prepare_name_strings(self):
        culturedict = {}
        #print(self.__culturedict_)
        for culturekey in self.__culturedict_:
            culturedict[culturekey] = \
                self.__unpack_list_(self.__culturedict_[culturekey])
        # Finally ready for human consumption
        self.culturedict = copy.deepcopy(culturedict)
        print(self.culturedict)

    def __unpack_list_(self, namelist: list) -> list:
        unpackednamelist = []
        for namesublist in namelist:
            for namestring in namesublist:
                unpackednamelist.append(namestring)
        return unpackednamelist

if __name__ == "__main__":
    import argparse
    from typing.io import TextIO

    '''
    As the name describes, it writes the names to file.
    '''
    def write_names_to_file(target: TextIO, culturedict: dict):
        for culturekey, namelist in culturedict:
            target.write(culturekey+" = {\n    ")
            for name in namelist:
                target.write(name + " ")
            target.write("\n}")

    parser = \
        argparse.ArgumentParser(description="Generate a list of names",
                                formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-s", "--source", type=str,
                        default="male_names_list.csv", help="The file "
                        "containing the namelist along with the path to the "
                        "file. The default is \"male_names_list.csv\".\n")
    parser.add_argument("-t", "--target", type=str,
                        default="male_names_list.txt", help="The file "
                        "containing the namelist with appended keys with the "
                        "path to the file. The default is "
                        "\"male_names_list.txt\". Any existing file with the "
                        "same name will be overwritten.\n")

    args = parser.parse_args()
    nlg_obj = nlg(args.source)
    try:
        with open(args.target, mode="w", encoding="cp1252") as target:
            write_names_to_file(target, nlg_obj.culturedict)
    except:
        print("Some serious error occurred.")
