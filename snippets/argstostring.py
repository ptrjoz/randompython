args_iterator = map(str, args_list)
        args_separator = '&'
        args_string = next(args_iterator, '')
        for arg in args_iterator:
            args_string += args_separator + arg
        return args_string