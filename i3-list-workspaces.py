#!/home/user/scripts/i3/i3env/bin/python
from i3ipc import Connection

"""
Outputs all active workspaces in i3 session
"""

i3 = Connection()
workspaces = i3.get_workspaces()
for workspace in sorted([w.name for w in workspaces]):
     print(workspace) 
