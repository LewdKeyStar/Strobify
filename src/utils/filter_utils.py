def filter_input(input_name):
    return f"[{input_name}]"

def filter_output(output_name):
    return f"[{output_name}];"

def filter_option_separator(is_first_option):
    return "=" if is_first_option else ":"

def chain_filters(filters):
    return ",".join([
        filter for filter in filters if filter != ""
    ])
