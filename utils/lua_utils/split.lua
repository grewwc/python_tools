local split_utils = {}

split_utils.split = function(str, sep)
    if sep == nil then
        sep = '%s'
    end
    local result = {}
    for sub_str in  string.gmatch(str, "([^"..sep.."]+)") do
        table.insert(result, sub_str)
    end
    return result
end

return split_utils
