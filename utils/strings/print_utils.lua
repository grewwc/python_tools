local print_utils = {}



function string.lstrip(str)
    if type(str) ~= "string" then
        return str
    end
    return str:match "^%s*(.*)"
end

function string.rstrip(str)
    if type(str) ~= "string" then
        return str
    end
    return str:match "(.-)%s*$"
end

function string.strip(str)
    return str:lstrip():rstrip()
end

local function print_table(tbl, indent)
    local prefix = string.rep(' ', indent + 2)
    io.write('{\n'):flush()
    for k, v in pairs(tbl) do
        if type(v) ~= 'table' then
            io.write(prefix, k, ": ", v, '\n'):flush()
        else
            io.write(prefix, k, ": "):flush()
            print_table(v, indent + 2)
        end
    end
    io.write(string.rep(' ', indent), '}\n'):flush()
end

print_utils.print = function(value)
    local type_ = type(value)
    if type_ == 'table' then
        print_table(value, 0)
    else
        print(value)
    end
end



return print_utils
