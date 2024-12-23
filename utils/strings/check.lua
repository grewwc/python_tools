local check = {}

function check.EndsWith(str, sub)
    if str == nil or sub == nil then 
        return false
    end
    return str:sub(-#sub) == sub
end

return check