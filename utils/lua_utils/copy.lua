local copy_utils = {}

copy_utils.deepCopy = function(obj)
    if obj == nil or type(obj) == 'function' then 
        return nil
    end
    if type(obj) ~= 'table' then 
        return obj
    else 
        local result = {}
        for k, v in pairs(obj) do 
            assert(type(k) ~= 'table', string.format("key can't be table. key:%s\n", k))
            result[k] = copy_utils.deepCopy(v)
        end
        return result
    end        
end



return copy_utils
