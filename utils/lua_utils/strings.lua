local string_utils = {}

string_utils.lstrip = function(str)
    if type(str) ~= "string" then
        return str
    end
    return str:match "^%s*(.*)"
end

function string_utils.rstrip(str)
    if type(str) ~= "string" then
        return str
    end
    return str:match "(.-)%s*$"
end

function string_utils.strip(str)
    str = string_utils.lstrip(str)
    return string_utils.rstrip(str)
end

return string_utils
