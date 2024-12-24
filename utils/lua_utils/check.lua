local check = {}

function check.endsWith(str, sub)
    if str == nil or sub == nil then
        return false
    end
    return str:sub(- #sub) == sub
end

function check.startsWith(str, sub)
    if str == nil or sub == nil then
        return false
    end
    return str:sub(0, #sub) == sub
end

return check
