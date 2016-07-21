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

#_keys = [] # the keys in the first column
#_culturelist = [] # list of cultures, in order

class nlg:
    '''
    Call process_file(source), and then generate the useable dictionary mapping
    '''
    def __init__(self, source: str):
        self.process_file(source)
        self.culturelist = self.__culturelist[1:]
        self.namedict = {}
        for namelist in self.__namelists:
            namedict[namelist[0]] = namelist[1:]
        self.append_keys()

    '''
    Opens the file, read all the lines, and creates the appropriate lists.
    '''
    def process_file(self, source: str):
        # open the file and extract the contents
        try:
            with open(source, encoding="cp1252") as openedsource:
                culturelinestring = "#"
                while(culturelinestring[0] == '#'):
                    culturelinestring = \
                        openedsource.readline()
                namelines = openedsource.readlines()
        except:
            print("Could not open file because it does not exist.")
            exit()

        culturelist = culturelinestring.split(';')
        namelists = []
        for line in namelines:
            if line[0] == '#':
                continue
            namelists.append(line.split(';'))
        self.__culturelist = culturelist
        self.__namelists = namelists

    '''
    Attaches key at the end of each name.
    '''
    def append_keys(self):
        namedict = {}
        # The dictionary contains the name key and the list of names
        for _namekey, _namelist in self.namedict:
            # because there are names which haven't been split
            newnamelist = [] #list contains appended shit
            for unsplitnamestring in _namelist:
                if not ',' in unsplitnamestring:
                    unsplitnamestring += "_" + _namekey
                    if unsplitnamestring[0] == "@":
                        unsplitnamestring = _namekey + unsplitnamestring[1:]
                    elif unsplitnamestring[0] == "~":
                        unsplitnamestring = ""
                else:
                    splitnamestring = unsplitnamestring.split(',')
                    unsplitnamestring_new = ""
                    for name in splitnamestring:
                        name += "_" + _namekey
                        if name[0] == "@":
                            name = _namekey + name[1:]
                        elif unsplitnamestring[0] == "~":
                            unsplitnamestring = ""
                        unsplitnamestring_new += name + ","
                    unsplitnamestring = unsplitnamestring_new
                newnamelist.append(unsplitnamestring)
            namedict[_namekey] = newnamelist


if __name__ == "__main__":

    import argparse

    parser = \
        argparse.ArgumentParser(description="Generate a list of names",
                                formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-s", "--source", type=str,
                        default="male_names_list.csv",help="The file containing"
                        " the namelist along with the path to the file. The "
                        "default is \"male_names_list.csv\".\n")
    parser.add_argument("-t","--target", type=str,
                        default="male_names_list.txt", help="The file "
                        "containing the namelist with appended keys with the "
                        "path to the file. The default is "
                        "\"male_names_list.txt\".\n")
    parser.add_argument("-g","--gender", type=str, default = "m", help="The "
                        "gender of the names in the list. By default, it is "
                        "assumed that the names are male.")

    args = parser.parse_args()
    nlg_obj = nlg(args.source)
