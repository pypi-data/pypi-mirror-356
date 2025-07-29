def get_api(load_info):
    from .app.Assembly  import Assembly
    from .app           import Errors 
   
    errors = load_info['errors'] 
    if len(errors) > 0:
        errs = Errors.InterpretErrors(errors)
        Errors.RaiseException(errs)
    Assembly.Assemble(load_info)
    return Assembly.api 

