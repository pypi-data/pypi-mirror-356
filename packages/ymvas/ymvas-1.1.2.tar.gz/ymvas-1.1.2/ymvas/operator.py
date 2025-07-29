import os

from pathlib import Path
from os.path import join, exists, dirname, isfile, isdir

from .references import Ref
from .settings   import Settings
from .compiler   import Compiler
from .templates.creator import Creator


class Operator:
    _refs  :dict = {}
    _spaces:dict = {}

    def __init__(self, pwd , debug = False):
        self.settings = Settings(pwd)
        self.settings.debug = debug

    def command(self,args):

        cmd = list(self.settings.get_commands(
            args.is_global,
            args.command
        ))

        if len(cmd) == 0:
            print(
                f'Command [{args.command}] is not setup for this repository!'
                "\nRun [ym info] to show what commands are avaliable"
            )
            return

        cmd = cmd[0]
        os.system(cmd['run'] + " " + cmd['path'])


    def clone(self,args):
        if args.repo is None:
            print('No repo specified!')
            return

        url = self.settings.ymvas_server_url.format(
            repo = args.repo
        )

        os.system(f"git clone {url}")

    def pull(self,argv):
        modules = self.settings.get_modules()
        modules = {k:v for k,v in modules.items() if not v['root'] and v['active']}

        os.system(
            f"git --git-dir={self.settings.git} "
            f"--work-tree={self.settings.root} fetch"
        )

        # for k,v in modules.items():
        #     p = v[ 'path' ]
        #     u = v[ 'url'  ]
        #
        #     if not exists(p):
        #         os.system(
        #             f"cd {self.settings.root} && "
        #             f"git --git-dir={self.settings.git} "
        #             f"--work-tree={self.settings.root} "
        #             f"submodule add {u} {p}"
        #         )


    def setup(self,argv):
        creator = Creator(argv)
        creator.run()

    def config(self,argv,args):
        if argv.action == 'set' and argv.is_global:
            stg = self.settings.get_global_settings()
            for a in args:
                if '=' not in a:
                    continue
                k = a.split('=')[0]
                v = a.replace(k+'=','').strip()

                if v == '':
                    continue
                k = k.strip('--')
                stg[k] = v
            self.settings.set_global_settings(stg)
            print(stg)
        elif argv.action == "show" and argv.is_global:
            print(self.settings.get_global_settings())

        elif argv.action == "get" and argv.is_global:
            for a in args:
                v = self.settings.get_global_settings().get(a,None)
                if v is None: continue
                print(v)

    def compile(self,args):
        if not exists(self.settings.d_endpoints):
            return

        self._append_refs(
            self.settings.alias,
            self.settings.d_references
        )

        self._spaces = self.settings.get_modules()
        Compiler( self , args ).run()

    def _append_refs(self, space, pref ):
        self._refs[space] = []

        if not exists(pref):
            return

        for r,_,files in os.walk( pref ):
            for f in files:
                self._refs[space].append(
                    Ref(join(r,f), self , space )
                )

        pass


    def refs(self,needle = None):
        if needle == None:
            for r in self._refs[self.alias]:
                yield r
            return

        for r in self._refs[self.alias]:
            fpath = r.fpath.replace(self.ref,'')
            if needle in fpath:
                yield r

    def __repr__(self):
        cmds = list(self.settings.get_commands())

        return "\n".join([
            f"config  : {self.settings.f_global_config}" ,
            "",
            f"[avaliable commands]",
            "\n - " +  "\n - ".join(c['cmd'] for c in cmds),
            "",
            f"[{self.settings.alias}]",
            f" - is-repo  : {self.settings.is_repo}",
            f" - is-ymvas : {self.settings.is_ymvas}",
            f" - is-main  : {self.settings.is_main}",
        ]) + "\n"
