local cmd_utils = {}

local _ = require('lua_utils.print_utils')

cmd_utils.execute = function(cmd)
    local handler = io.popen(cmd .. ' 2>&1')
    if handler ~= nil then
        local res = handler:read("*a")
        handler:close()
        return res:rstrip()
    end
end

return cmd_utils
