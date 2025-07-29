
class Arguments:
    is_version  : bool = False
    is_global   : bool
    debug       : bool

    compile_dir : str
    command     : str
    action      : str
    repo        : str
    init        : str
    src         : str

    _config_args = [
        "global-compile-dir" , # where the compiles will be stored
        "global-commands"    , # where the global commands are stored
        "global-src"         , # where the user repo is stored


        # server settings
        'is-ymvas'           , # if it's server side or not [true or false]
        'ymvas-server-url'   , # url typically https://ymvas.com
        'ymvas-domain'       , # domain typically ymvas.com
        'ymvas-access'       , # access privileges
    ]


    def __init__( self , args ):
        self.command  = args[0] # first statement
        self.args     = args[1:]

        # flags [non required]
        self.args, self.debug       = Arguments.flag(
             self.args , '-d' , '--debug' , False
        )
        self.args, self.is_global   = Arguments.flag(
             self.args , '-g' , '--global' , False
        )
        self.args, self.is_version  = Arguments.flag(
             self.args , '-v' , '--version' , False
        )
        self.args, self.compile_dir = Arguments.keyv(
             self.args , '-c' , '--compile-dir'
        )

        self.args = self.args

    @staticmethod
    def flag(args,short_key,key,default=False):
        trash, value, found = [], default, False
        for i, c in enumerate( args ):
            if ( c == key or c == short_key ) and not found:
                value, found = True, True
            else:
                trash.append(c)
        return trash, value

    @staticmethod
    def keyv(args,short_key,key,default=None):
        trash, value, found = [], default, False
        for i, c in enumerate(args):
            if (c.startswith(key) or c.startswith(short_key)) and not found:
                found = True
                value = c.split('=')[0]
                value = c.replace(value + '=',"")
                if len(value) > 2 and value[0] == value[-1] and value[0] in ["'",'"']:
                    value = value.strip(value[0])
            else:
                trash.append(c)
        return trash, value

    def get_config_args(self):
        # for a in self.args:
        #     if '=' not in a:
        #         continue
        #
        #     k = a.split('=')[0]
        #     v = a.replace(k+'=','').strip()
        #
        #     if v == '':
        #         continue
        #     k = k.strip('--')
        #     stg[k] = v

        pass
