import os
import sys
import glob
import argparse
import configparser
import re


dirCalled = os.path.dirname(__file__)

class ExamManager(object):

    def __init__(self, argv=None):

        self.dbFile = os.path.join(dirCalled, 'texmodule.db')
        if os.path.exists(self.dbFile):
            self.database = configparser.ConfigParser()
            self.database.read(self.dbFile, encoding='utf-8')
        else:
            print('{} is not found.'.format(self.dbFile))
            sys.exit()

        self.parse_args(argv)

        if self.args.insert_bool:
            self.insert_new()
        elif self.args.update_bool:
            self.update()
        elif self.args.remove_bool:
            self.remove()
        elif self.args.list_bool:
            print('\n'.join(sorted(self.database.sections(), key=str.casefold)))
        elif self.args.burst_bool:
            self.burst()
        elif self.args.assemble_bool:
            self.assemble()


    def parse_args(self, argv=None):

        parser = argparse.ArgumentParser(
            description = 'Manage the examination database.'
        )
        parser.add_argument(
            'sections',
            nargs = '*',
            help = 'Specify one or more sections or files.'
        )
        parser.add_argument(
            '-l',
            dest = 'list_bool',
            action = 'store_true',
            default = False,
            help = 'Enumerate sections.'
        )
        parser.add_argument(
            '-i',
            dest = 'insert_bool',
            action = 'store_true',
            default = False,
            help = "Insert new TeX files into the database file. Stems of filenames are used as section labels in the database."
        )
        parser.add_argument(
            '-u',
            dest = 'update_bool',
            action = 'store_true',
            default = False,
            help = 'Update the dabase with the files whose names are the same as specified.'
        )
        parser.add_argument(
            '-r',
            dest = 'remove_bool',
            action = 'store_true',
            default = False,
            help = 'Remove the section from the database.'
        )
        parser.add_argument(
            '-a',
            dest = 'assemble_bool',
            action = 'store_true',
            default = False,
            help = 'Assemble sections to build a document.'
        )
        parser.add_argument(
            '-o',
            dest = 'output',
            default = 'assembled.tex',
            help = 'Specify a filename. This option is available only with "-a". The default is "assembled.tex".'
        )
        parser.add_argument(
            '-b',
            dest = 'burst_bool',
            action = 'store_true',
            default = False,
            help = 'Take out every section.'
        )

        self.args = parser.parse_args(argv)


    def update_database(self, msg):

        with open(self.dbFile, mode='w', encoding='utf-8') as f:
            self.database.write(f)
            print(msg)


    def file_to_database(self, filename, section):

        with open(filename, mode='r', encoding='utf-8') as f:
            content = f.read()

        content = re.sub('%', '%%', content)
        content = re.sub('^', '```', content, flags=re.MULTILINE)
        self.database.set(section, 'tex', content)


    def section_from_database(self, section):

        content = self.database.get(section, 'tex', fallback='')
        content = re.sub('^```', '', content, flags=re.MULTILINE)
        return content


    def insert_new(self):

        cnt = 0
        for i in self.args.sections:
            if len(glob.glob(i)) == 0:
                print('There is no file with the name "{}".'.format(i))
                continue

            for filepath in glob.glob(i):
                section = os.path.splitext(os.path.basename(filepath))[0]
                if self.database.has_section(section):
                    print('"{}" is already included in the database.'.format(section))
                else:
                    self.database.add_section(section)
                    self.file_to_database(filepath, section)
                    cnt += 1

        self.update_database('{} files have been inserted'.format(cnt))


    def update(self):

        cnt = 0
        for i in self.args.sections:
            if len(glob.glob(i)) == 0:
                print('There is no file with the name "{}".'.format(i))
                continue

            for filepath in glob.glob(i):
                section = os.path.splitext(os.path.basename(filepath))[0]
                if not self.database.has_section(section):
                    print('"{}" is not included in the database.'.format(section))
                else:
                    self.file_to_database(filepath, section)
                    cnt += 1

        self.update_database('{} sections have been updated'.format(cnt))


    def select(self, section):

        regex = section.replace('*', '.*')
        p = re.compile(regex)
        return list(filter(p.match, self.database.sections()))


    def remove(self):

        cnt = 0

        for i in self.args.sections:
            target_sections = self.select(i)
            for section in target_sections:
                self.database.remove_section(section)
                cnt += 1

        self.update_database('{} sections have been removed'.format(cnt))


    def burst(self):

        for section in self.database.sections():
            content = self.section_from_database(section)            
            filename = section + '.tex'
            with open(filename, mode='w', encoding='utf-8') as f:
                f.write(content)


    def assemble(self):

        tail = False
        if 'head-' in self.args.sections[0]:
            tail = self.args.sections[0].replace('head-', 'tail-')

        content = ''
        for i in self.args.sections:
            target_sections = self.select(i)
            for section in target_sections:
                content += self.section_from_database(section)

        if tail:
            if self.database.has_section(tail):
                content += self.section_from_database(tail)
            else:
                content += '\\end{document}'

        with open(self.args.output, mode='w', encoding='utf-8') as f:
            f.write(content)
            print('"{}" is created.'.format(self.args.output))



if __name__ == '__main__':
    ExamManager()
