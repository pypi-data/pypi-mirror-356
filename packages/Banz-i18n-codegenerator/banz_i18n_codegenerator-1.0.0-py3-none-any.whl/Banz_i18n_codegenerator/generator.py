# Constants

CONSTANTS = 'constants'
MESSAGES = 'messages'
VALIDATION = 'validation'
TARGETS = {CONSTANTS: 'Constants',
           MESSAGES: 'Messages',
           VALIDATION: 'ValidationMessages'}

FILES = []
RESOURCE_PATH = ''
TARGET_PATH = ''

# function definitions

"""packs file contents into nested list. Validates:
 * all file entries follow the schema "key = string"
 * all files have the same keys with no duplicates per file
returns list of unique keys"""
def buildKeyList(folder: str):
    err = list()
    path = RESOURCE_PATH + '\\' + folder
    keys = dict()
    masterFile = ''
    master = list()
    for file in FILES:
        ident = path + '\\' + file
        i18nFile = list()
        with open(ident) as i18n:
            for line in i18n:
                ls = line.split('=')
                if len(ls) != 2 or ls[0] == '' or ls[1] == '':
                    err.append(f'Entry "{line}" of file {folder + "/" + file}.')
                i18nFile.append(line.split('=')[0].strip())
        keys[ident] = i18nFile
        if file == FILES[0]:
            masterFile = ident
            master = sorted(i18nFile)
    if len(err) > 0:
        raise Exception('Schema Exception:\n' + '\n'.join(err))
    for k, v in keys.items():
        missingKeys = [x for x in master if x not in v]
        singleKeys = [x for x in v if x not in master]
        print(k)
        for key in missingKeys:
            err.append(f'Entry "{key}" missing in file {k}.')
        for key in singleKeys:
            err.append(f'Entry "{key}" missing in file {masterFile}.')
    if len(err) > 0:
        raise Exception('Validation Exception:\n' + '\n'.join(set(err)))
    return master


def build(folder: str):
    c = 0
    i18nKeys = buildKeyList(folder)
    targetPackage = '.'.join(TARGET_PATH.split('java')[-1].split('\\\\')[1:])
    print(targetPackage)
    with open(TARGET_PATH + '\\' + TARGETS[folder] + '.java', 'w') as file:
        file.write('//generated\n')
        file.write('package ' + targetPackage + ';\n\n')
        file.write('public final class ' + TARGETS[folder] + ' {\n\n')
        for key in i18nKeys:
            constant = '_'.join(key.split('.')).upper()
            file.write(f'    public static final String {constant} = "{key}";\n\n')
            c += 1
        file.write('}')
    return c


def run(files: list, resourcePath: str, targetPath: str):
    global FILES
    FILES = files;
    global RESOURCE_PATH
    RESOURCE_PATH = resourcePath.replace('\\', '\\\\');
    global TARGET_PATH
    TARGET_PATH = targetPath.replace('\\', '\\\\');

    # execution

    print("*------- Generating constants -------*")
    c = build(CONSTANTS)
    print(f"*------- Generated {c} constants -------*\n")

    print("*------- Generating messages -------*")
    c = build(MESSAGES)
    print(f"*------- Generated {c} messages -------*\n")

    print("*------- Generating validation messages -------*")
    c = build(VALIDATION)
    print(f"*------- Generated {c} validation messages -------*\n")

