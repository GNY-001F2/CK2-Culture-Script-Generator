# CK2 Culture Script Generator
# Copyright (C) 2016 Gundam Astraea Type F2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import argparse
import os

cwd = os.getcwd()


if __name__ == "__main__":

    parser = \
        argparse.ArgumentParser(description="Generate a CK2 culture script.",
                                formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-p", "--path", default=os.getcwd(), help="the "
                        "Absolute or relative to current directory path "
                        "where all your files are located; default is your "
                        "current working directory.")
    parser.add_argument("-n", "--namelist", default="names.csv", help="the CSV "
                        "file where the list of names for the culture are"
                        "kept; by default it points to names.csv")
    parser.add_argument("-c", "--culturelist", default="culturelist.txt",
                        help="The file containing the culture group and its
                        required attributes.\nSee the wiki page on Culture
                        Modding and the readme for how to make this file.\n"
                        "By default it will look for a file named culturelist."
                        "txt.")
    parser.add_argument("-f", "--filename", default="culturegroup.txt", help=""
                        "The file in which your newly generated culture group "
                        "will be stored.")
