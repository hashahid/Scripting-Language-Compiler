# dictionary for storing/accessing global variables
global_scope = {}

# dictionary for storing function bodies and accessing them by their names
function_name_to_body = {}

# list of dictionaries for storing local variables/emulating stack frames
# May be unneeded. Can make local dictionary in Function Node that includes
# the global_scope dictionary for access to local and global variables
local_vars = []
