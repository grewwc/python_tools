
-- package.path = 

local w_utils = {}

local check = require('strings.check')
local print_utils = require('strings.print_utils')

-- w_utils.split = require('strings/split')

w_utils.EndsWith = check.EndsWith
w_utils.Print = print_utils.print


return w_utils