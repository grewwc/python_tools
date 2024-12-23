
-- package.path = 

local w_utils = {}

local check = require('lua_utils.check')
local print_utils = require('lua_utils.print_utils')
local copy_utils = require('lua_utils.copy')
local cmd_utils = require('lua_utils.cmd')
local split_utils = require('lua_utils.split')
local string_utils = require('lua_utils.strings')

w_utils.EndsWith = check.EndsWith
w_utils.Print = print_utils.print
w_utils.DeepCopy = copy_utils.deepCopy
w_utils.Execute = cmd_utils.execute
w_utils.Split = split_utils.split
w_utils.LStrip = string_utils.lstrip
w_utils.RStrip = string_utils.rstrip
w_utils.Strip = string_utils.strip

return w_utils