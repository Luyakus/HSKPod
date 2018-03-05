

import os
import re
import shutil
import subprocess
import argparse
import plistlib

SPEC_PATH = '/Users/9188-mac005/Documents/Work/hskspec/Frameworks'

HSKBASIC_PATH = '/Users/9188-mac005/Documents/Work/HSKBasic'
CARDMANAGE_PATH = '/Users/9188-mac005/Documents/Work/CreditCard'
CARDAPPLY_PATH = '/Users/9188-mac005/Documents/Work/CreditCard'
CARDSERVICE_PATH = '/Users/9188-mac005/Documents/Work/CreditCard'
LOAN_PATH = '/Users/9188-mac005/Documents/Work/Loan'
HOUSEMMOUDLE_PATH = '/Users/9188-mac005/Documents/Work/YYHouseIOS'
HOUSETOOL_PATH = '/Users/9188-mac005/Documents/Work/YYHouseIOS'
CREDITQUARY_PATH = '/Users/9188-mac005/Documents/Work/YYCreditIOS'
YYBBSMODULE_PATH = '/Users/9188-mac005/Documents/Work/YYFinanceIOS'


POD_SOURCES = 'http://gitlab.gs.9188.com/caiyi.financial.huishuaka.app/hskspec.git,https://github.com/CocoaPods/Specs'


class PathError(IOError):
    pass


class CmdError(Exception):
    pass

ValueError
class Git(object):
    def __init__(self, git_path):
        if os.path.exists(git_path):
            self.path = git_path
        else:
            raise PathError('git path: %s is not exists' % git_path)

    def execmd(self, cmd):
        os.chdir(self.path)

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (stdoutdata, stderrdata) = process.communicate()

        if stderrdata:
            raise CmdError(stderrdata.decode('utf-8').strip())
        return stdoutdata.decode('utf-8').strip()

    def add(self, file_path = '.'):
        self.execmd('git add %s' % file_path)

    def commit(self, desc = 'commit'):
        self.execmd('git commit -m %s' % desc)

    def pull(self):
        self.execmd('git pull')

    def push(self):
        self.execmd('git push')

    def tag(self, tag_number = None):
        if tag_number is None:
            tag_number = self.create_new_tag()

        self.execmd('git tag %s' % tag_number)
        self.execmd('git push origin --tags')
        print('>>>>> create new tag : %s <<<<<' % tag_number)

    def get_latest_tag(self):
        tags = self.execmd('git tag')
        if tags:
            return tags.split('\n')[-1]
        return None

    def create_new_tag(self):
        old_tag = self.get_latest_tag()
        tagnum = int(old_tag.replace('.', ''))
        tagnum += 1
        l = list('%s' % tagnum)
        new_tag = '.'.join(l)
        return new_tag


class Spec(Git):
    def __init__(self, sepc_path):
        super(Spec, self).__init__(sepc_path)

    def pod_push(self, moudle_name):
        podspec_path = os.path.join(self.path, '%s/%s.podspec' % (moudle_name, moudle_name))
        cmd = 'pod repo push hskspec %s --allow-warnings --sources=%s' % (podspec_path, POD_SOURCES)
        print('>>>>> run %s <<<<<' % cmd)
        self.execmd(cmd)
        print('>>>>> push %s success <<<<<' % moudle_name)

    def copy_framework_to_spec(self, moudle_name, src):
        framework_path = os.path.join(self.path, '%s/%s.framework' % (moudle_name, moudle_name))
        if os.path.exists(framework_path):
            shutil.rmtree(framework_path)
        shutil.copytree(src, framework_path)
        print('>>>>> copy %s.framework to %s' % (moudle_name, self.path))

    def update_spec_file(self, moudle_name, moudle_version):
        tag_number = self.create_new_tag()
        podspec_path = os.path.join(self.path, '%s/%s.podspec' % (moudle_name, moudle_name))

        with open(podspec_path, 'r') as rfp:
            lines = rfp.readlines()

        with open(podspec_path, 'w') as wfp:
            for line_num, line in enumerate(lines):
                if re.match(r'\s*s.version\s*=\s*', line):
                    line = re.sub(r'\d.\d.\d', moudle_version, line)
                    lines[line_num] = line
                    print('>>>>> %s <<<<<' % line)

                if re.match(r'\s*s.source\s*=\s*', line):
                    line = re.sub(r'\d.\d.\d', tag_number, line)
                    lines[line_num] = line
                    print('>>>>> %s <<<<<' % line.strip())

            wfp.writelines(lines)


class Module(Git):
    def __init__(self, moudle_name, moudle_path):
        super(Module, self).__init__(moudle_path)
        self.new_version = ''
        self.name = moudle_name
        self.common_sdk_path = '%s/DerivedData/Build/Products/Common-SDK/%s.framework' % (self.path, self.name)
        self.iphoneos_sdk_path = '%s/DerivedData/Build/Products/Release-iphoneos/%s.framework' % (self.path, self.name)
        self.iphonesimulator_sdk_path = '%s/DerivedData/Build/Products/Release-iphonesimulator/%s.framework' % (self.path, self.name)

    def build(self):
        print('>>>>> start build %s.framework <<<<<' % self.name)

        self.increase_framework_version()

        workspace = [x for x in os.listdir(self.path) if os.path.splitext(x)[1] == '.xcworkspace'][0]

        print('>>>>> building %s.framework <<<<<' % self.name)
        try:
            self.execmd("xcodebuild -workspace %s -scheme %s -configuration Release -destination generic/platform=iOS -destination 'platform=iOS Simulator,name=iPhone 6' clean build" % (workspace, self.name))
        except:
            print('>>>>> build %s.framework failed <<<<<' % self.name)
            exit(0)

        print('>>>>> build %s.framework success <<<<<' % self.name)

        if os.path.exists(self.common_sdk_path):
            shutil.rmtree(self.common_sdk_path)
        shutil.copytree(self.iphoneos_sdk_path, self.common_sdk_path)
        
        self.execmd('lipo -create %s/%s %s/%s -output %s/%s' % (self.iphoneos_sdk_path, self.name, self.iphonesimulator_sdk_path, self.name, self.common_sdk_path , self.name))
        print('>>>>> merge %s.framework to %s <<<<<' % (self.name, self.common_sdk_path))

    def increase_framework_version(self):

        info_plist_path = '%s/Modules/%s/Info.plist' % (self.path, self.name)
        if not os.path.exists(info_plist_path):
            info_plist_path = '%s/%s/Info.plist' % (self.path, self.name)

        with open(info_plist_path, 'rb+') as fp:
            info = plistlib.loads(fp.read())
            old_version = info['CFBundleShortVersionString']
            old_version_num = int(old_version.replace('.', ''))
            new_version = '.'.join(list('%s' % (old_version_num + 1)))
            info['CFBundleShortVersionString'] = new_version
            fp.seek(0)
            plistlib.dump(info, fp)
            self.new_version = new_version
            print('>>>>> increase %s.framework version to %s <<<<<' % (self.name, new_version))


def build(moudle_name, source_path, spec):

    moudle = Module(moudle_name, source_path)
    moudle.build()

    spec.copy_framework_to_spec(moudle_name, moudle.common_sdk_path)
    spec.update_spec_file(moudle_name, moudle.new_version)


def main():

    parser = argparse.ArgumentParser()

    arg_dict = {'-hb': '--hsk_basic',
                '-cm': '--card_manage',
                '-ca': '--card_apply',
                '-cs': '--card_service',
                '-ln': '--loan',
                '-ht': '--house_tool',
                '-hm': '--house_moudle',
                '-cq': '--credit_quary',
                '-bbs': '--finance_bbs'}

    for key, value in arg_dict.items():
        parser.add_argument(key, value, action='store_true')

    args = parser.parse_args()

    spec = Spec(SPEC_PATH)

    moudles = []
    if args.hsk_basic:
        moudles_name = 'HSKBasic'
        build(moudles_name, HSKBASIC_PATH, spec)
        moudles.append(moudles_name)

    if args.card_manage:
        moudles_name = 'CardManage'
        build(moudles_name, CARDMANAGE_PATH, spec)
        moudles.append(moudles_name)

    if args.card_apply:
        moudles_name = 'CardApply'
        build(moudles_name, CARDAPPLY_PATH, spec)
        moudles.append(moudles_name)

    if args.card_service:
        moudles_name = 'CardService'
        build(moudles_name, CARDSERVICE_PATH, spec)
        moudles.append(moudles_name)

    if args.loan:
        moudles_name = 'LoanModule'
        build(moudles_name, LOAN_PATH, spec)
        moudles.append(moudles_name)

    if args.house_tool:
        moudles_name = 'HouseTool'
        build(moudles_name, HOUSETOOL_PATH, spec)
        moudles.append(moudles_name)

    if args.house_moudle:
        moudles_name = 'HouseModule'
        build(moudles_name, HOUSEMMOUDLE_PATH, spec)
        moudles.append(moudles_name)

    if args.credit_quary:
        moudles_name = 'CreditenQuiryModule'
        build(moudles_name, CREDITQUARY_PATH, spec)
        moudles.append(moudles_name)

    if args.finance_bbs:
        moudles_name = 'YYBBSModule'
        build(moudles_name, YYBBSMODULE_PATH, spec)
        moudles.append(moudles_name)

    spec.add()
    spec.commit()
    spec.pull()
    spec.push()
    spec.tag()

    for moudle in moudles:
        spec.pod_push(moudle)


if __name__ == '__main__':
    main()
