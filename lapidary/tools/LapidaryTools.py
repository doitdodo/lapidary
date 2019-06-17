from argparse import ArgumentParser

class ToolDecorator:
    def __init__(self, name):
        self.name = name

    def __call__(self, arg_fn):
        def invoke(*vargs, **kwargs):
            return arg_fn(*vargs, **kwargs)
        
        invoke.__wrapped__ = True
        invoke.command_name = self.name
        return invoke

class LapidaryTools:

    def __init__(self, parser):
        self.parser = parser
        # add parser args
        subparsers = self.parser.add_subparsers()

        for cmd_name, arg_add_fn in self:
            cmd = subparsers.add_parser(cmd_name)
            arg_add_fn(cmd)
    
    @staticmethod
    @ToolDecorator("create")
    def add_create_args(parser):
        from lapidary.tools import GDBProcess
        GDBProcess.add_args(parser)

        run = lambda args: GDBProcess.main(args)
        parser.set_defaults(fn=run)

    @staticmethod
    @ToolDecorator("simulate")
    def add_simulate_args(parser):
        pass

    def __iter__(self):
        import inspect
        fns = inspect.getmembers(self, inspect.method)
        for fname, fn in fns:
            if not hasattr(fn, '__wrapped__') or not fn.__wrapped__:
                print(fname)
                from IPython import embed
                embed()
                continue
            yield fn.command_name, fn
            
    def parse_args(self):
        return self.parser.parse_args()