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
        except Exception as e:
            print("Could not open file because it does not exist.")
            print(e)
            exit()
        # Need to remove the newlines
        # use ";" to terminate the line
        namekeylist = namekeystring.split(";")[1:-1]
        culturedict = {}
        for culturelinestr in culturelinelist:
            culturenamelist = culturelinestr.split(";")
            culturedict[culturenamelist[0]] = culturenamelist[1:-1]
        self.__culturedict = copy.deepcopy(culturedict)
        self.__namekeylist = copy.deepcopy(namekeylist)

    '''
    Attaches key at the end of each name.
    '''
    def append_keys(self):

        namekeylist = copy.deepcopy(self.__namekeylist)
        # Use local copy instead of modifying global instance variables
        culturedict = copy.deepcopy(self.__culturedict)
        for i in range(0, len(namekeylist)):
            for culturekey in culturedict:
                culturedict[culturekey][i] = \
                    self.__append_keys_(namekeylist[i],
                                        self.__culturedict[culturekey][i])
        self.__culturedict_ = copy.deepcopy(culturedict)

    '''
    Helper function that appends the key at the end of each name and returns
    names contained in lists.
    '''
    def __append_keys_(self, namekey: str, namestring: str) -> list:
        # Having any other values would be a a contradiction so first check if
        # there should be no variant of this name for this culture. If the user
        # makes a mistake in the CSV file then the function presumes that this
        # should not be used.
        if "~" in namestring:
            return []
        namelist = namestring.split(",")
        for i in range(0, len(namelist)):
            if namelist[i] == "@":
                namelist[i] = namekey + "_" + namekey
            else:
                namelist[i] += "_" + namekey
            if " " in namelist[i]:
                namelist[i] = "\"" + namelist[i] + "\""
        return namelist

    def prepare_name_strings(self):
        culturedict = {}
        for culturekey in self.__culturedict_:
            culturedict[culturekey] = \
                self.__unpack_list_(self.__culturedict_[culturekey])
        # Finally ready for human consumption
        self.culturedict = copy.deepcopy(culturedict)

    def __unpack_list_(self, namelist: list) -> list:
        unpackednamelist = []
        for namesublist in namelist:
            for namestring in namesublist:
                unpackednamelist.append(namestring)
        return unpackednamelist

if __name__ == "__main__":
    import argparse

    '''
    As the name describes, it writes the names to file.
    '''
    def write_names_to_file(target: str, culturedict: dict):
        try:
            with open(target, mode="w", encoding="cp1252") as opentarget:
                for culturekey, namelist in culturedict.items():
                    opentarget.write(culturekey + " = {\n    ")
                    namelistlen = len(namelist)
                    for i in range(0, namelistlen):
                        if i < namelistlen-1:
                            opentarget.write(namelist[i] + " ")
                        else:
                            opentarget.write(namelist[i])
                    opentarget.write("\n}")
        except Exception as e:
            print("Some serious error occurred.")
            print(e)
            exit()

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
    write_names_to_file(args.target, nlg_obj.culturedict)
