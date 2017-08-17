# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import getopt
import pypinyin
import urllib2
import json

# Global config dict
CONFIG = {}

# 分割符
SEP = '_'

nummap = {
    '0': 'ling',
    '1': 'yi',
    '2': 'er',
    '3': 'san',
    '4': 'si',
    '5': 'wu',
    '6': 'liu',
    '7': 'qi',
    '8': 'ba',
    '9': 'jiu'
}

type_list = ['str', 'unicode', 'int', 'float', 'list', 'dict', 'bool']
key_list = ['_id', 'uuid', 'datasource', 'version', 'rawdata', 'url', 'key', 'retain1', 'retain2', 'uptime', 'do_time']

def show_help():
    print """\
Syntax: python %s <options>
 -c <className>    the class name
 -h                show this help screen
 -f <filePath>     the fieldname file
 -t <tableName>    the table name
""" % sys.argv[0]


def parse_options(opts):
    global CONFIG
    opts = dict([(k.lstrip('-'), v) for (k, v) in opts])
    if 'h' in opts:
        show_help()
        exit(0)
    if 'c' in opts:
        CONFIG['classname'] = opts['c']
    if 'f' in opts:
        CONFIG['filename'] = opts['f']
    if 't' in opts:
        CONFIG['tablename'] = opts['t']


# 从文件读取字段名和字段类型列表
def get_fields_notes_types_values():
    global CONFIG
    global type_list
    if CONFIG.has_key('tablename'):
        url = 'http://dm.bbdservice.com/dataspec/apitabdesc/?tb=%s&debug=true' % CONFIG['tablename']
        result = urllib2.urlopen(url).read().decode()
        data = json.loads(result)
        rdata = data['rdata']
        rdata_new = list()
        for info in rdata:
            if info['en_keyname'] in key_list:
                print 'Key already exists: %s' % info['en_keyname']
            else:
                rdata_new.append(info)
        fields = map(lambda x: x['en_keyname'], rdata_new)
        if '' in fields or None in fields:
            raise Exception('en_keyname is null')
        notes = map(lambda x: x['keydesc'], rdata_new)
        types = map(lambda x: x['keytype'].replace('py_', ''), rdata_new)
        for t in types:
            if t not in type_list:
                raise Exception('type incorrect')
        tmps = map(lambda x: x['default_value'] if x['default_value'] else 'None', rdata_new)
        values = list()
        for value in tmps:
            if value != 'None':
                try:
                    float(value)
                except:
                    value = 'u' + '\'%s\'' % value
            values.append(value)
        return fields, notes, types, values
    else:
        f = open(CONFIG['filename'])
        lines = map(lambda x: x.replace('\xef\xbb\xbf', '').strip(), filter(lambda x: x.strip(), f))
        f.close()
        fields_notes_types_values = map(lambda x: x.split(), lines)
        for field_note_type_value in fields_notes_types_values:
            if len(field_note_type_value) != 4:
                raise Exception('the number of types is not correct')
            if field_note_type_value[2] not in type_list:
                raise Exception('type incorrect')
        return map(lambda x: x[0], fields_notes_types_values), map(lambda x: x[1], fields_notes_types_values), map(lambda x: x[2], fields_notes_types_values), map(lambda x: x[3], fields_notes_types_values)


def process():
    global nummap
    global SEP
    fields, notes, types, values = get_fields_notes_types_values()
    types = map(lambda x: 'unicode' if x == 'str' else x, types)
    pinyins = map(lambda x: x.replace('__', '_'), map(lambda x: filter(lambda x: x if x.isalnum() or x == SEP else '', x), map(lambda x: nummap[x[0]] + SEP + x[1:] if x[0].isdigit() else x, map(lambda x: pypinyin.slug(x.decode('utf-8'), separator=SEP), fields))))
    set_ = set(pinyins)
    if len(pinyins) != len(set_):
        dict_ = dict(zip(list(set_), [0] * len(set_)))
        for pinyin in pinyins:
            dict_[pinyin] += 1
        for key in dict_.keys():
            if dict_[key] > 1:
                print 'the same name: %s' % key
        raise Exception('variables having the same name')
    make(fields, notes, types, values, pinyins)


# 生成代码文件
def make(fields, notes, types, values, pinyins):
    global CONFIG
    pinyins_types = zip(pinyins, types)
    notes_pinyins_values = zip(notes, pinyins, values)
    f = open('%s.py' % CONFIG['classname'], 'w')
    txt = ''
    txt += '# -*- coding: utf-8 -*-' + '\n'
    txt += '__author__ = \'Lvv\'' + '\n'
    txt += '\n'
    txt += 'import sys' + '\n'
    txt += '\n'
    txt += 'sys.path.append(\'../\')' + '\n'
    txt += '\n'
    txt += 'from BBDSpiderInterface.field.FieldBase import FieldBase' + '\n'
    txt += '\n\n'
    txt += 'class %s(FieldBase):' % CONFIG['classname'] + '\n'
    txt += '    def __init__(self, datasource, version=1, level=1, **kwargs):' + '\n'
    txt += '        FieldBase.__init__(self, datasource, version, level)' + '\n'
    txt += '        ' + '\n        '.join(map(lambda x: '# %s\n        self.%s = %s' % (x[0], x[1], x[2]), notes_pinyins_values))
    txt += '\n'
    txt += '\n        '
    txt += '\n        '.join(map(lambda x: 'self.types[\'%s\'] = %s' % (x[0], x[1]), pinyins_types))
    txt += '\n'
    txt += '\n'
    txt += '    def makemap(self):' + '\n'
    txt += '        return {' + '\n'
    txt += '            ' + '\n            '.join(map(lambda x: 'u\'%s\': self.%s,' % (x[0], x[1]), zip(fields[:-1], pinyins[:-1])))
    txt += '\n            ' + 'u\'%s\': self.%s' % (fields[-1], pinyins[-1]) + '\n'
    txt += '        }'
    txt = txt.replace('_shuai', '_lv')
    f.write(txt)
    f.close()


if '__main__' == __name__:
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:hf:t:')
    except getopt.GetoptError, e:
        print str(e)
        show_help()
        sys.exit(1)
    parse_options(opts)
    process()
