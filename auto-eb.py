#!/bin/env python
import re
import subprocess

class Parser:

    def __init__(self, input_text, regex=""):
        self.input_text = input_text
        self.regex = regex
        self.output_text = []

    def split_input(self):
        return iter(self.input_text.splitlines())

    def parse(self):
        lines = list(self.split_input())
        for line in lines: 
            if re.search(self.regex, line):
                self.output_text.append(line)
        return self.output_text

"""
This class takes an ebfile as an input and performs a dryrun to obtain the dependency of this ebfile. 

"""
class EbDependency:

    def __init__(self, ebfile):
        self.ebfile = ebfile
        self.dependency = []

    def dryrun(self, keep_installed=False):
        cmd = ["eb", "--dry-run", self.ebfile]
        output = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
        #print(output)
        regex = "\* \[ |x\]"
        #self.dependency = Parser(output, regex).parse()
        # extract ebfile name: "] ebfilename ("
        p = re.compile("\] (.*) \(")
        items = Parser(output, regex).parse()
        # remove the last item which is the ebfile provided
        items.pop()
        for item in items:
            if keep_installed:
                depend = p.search(item).group(1)
                self.dependency.append(depend)
            if re.search("\[ \]", item) is not None:
                depend = p.search(item).group(1)
                self.dependency.append(depend)
        return self.dependency

    def print_dependency(self):
        print(self.dependency)
        
class EbBfsTree:
    
    def __init__(self, ebfile=""):
        self.ebfile = ebfile
        self.dependency = []
        self.current = -1
 
    def build(self, ebfile):
        #eb_dependency = EbDependency(self.ebfile)
        print(ebfile)
        eb_dependency = EbDependency(ebfile)
        deps = eb_dependency.dryrun()
        for dep in deps:
            if dep in self.dependency:
                self.dependency.remove(dep)
        self.dependency = self.dependency + deps
        self.current = self.current + 1
        if self.current < len(self.dependency):
            self.build(self.dependency[self.current])

    def print(self):
        print(self.dependency)
        
        
# make sure EasyBuild is in path

# check the syntax
# auto_eb.py ebfile

# dry run 'eb ebfile' and get the missing dependency. ebfile is obtained from the command line
# parse the dependency output and generate a dependency tree. Do a BFS to build all dependecies. 


 


# test code for EbDependency
#deps = EbDependency("/home/pl543/git-sources/ycrc-ebfiles/easyconfigs/ScaLAPACK/ScaLAPACK-2.1.0-gompi-2020b.eb")
#deps.dryrun()
#deps.print_dependency()

eb_bfs_tree = EbBfsTree()
eb_bfs_tree.build("/home/pl543/git-sources/ycrc-ebfiles/easyconfigs/ScaLAPACK/ScaLAPACK-2.1.0-gompi-2020b.eb")
eb_bfs_tree.print()
# test code for Parser
#input_text = """  * [x] line1
#line2
#* [ ] line3
#"""
#regex = "\* \[ |x\]"
#test = Parser(input_text, regex)
#output = test.parse()
#print(output)
