-- simple lua chat logger

function log(source, content)
    local file = io.open("logs.txt", "w")
    if file then
        local timestamp = os.date("%Y-%m-%d %H:%M:%S")
        local clean = content:gsub("/n", " ")
        file:write(string.format("[%s] %s: %s\n", timestamp, source, clean))
        file:close()
        return true
    end
    return false
end
