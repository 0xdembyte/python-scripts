local Discordia = require('discordia')
local Client = Discordia.Client()

local Whitelisted = {
    "https://discord.gift"
}

local Keywords = {
    "gifting nitro",
    "free nitro",
    "nitro free",
    "gift nitro",
    "giving away nitro"
}

local Domains = {
    ".com",
    ".xyz",
    ".tk",
    ".net",
    ".co.nz",
    ".uk",
    ".gift",
    ".gg",
    ".pub",
    ".win",
    ".shop"
}

local Logs = {}

local function SanityCheck(Text)
    for i,  v in next, Keywords do
        if string.find(Text, v) then
            for k,  x in next, Domains do
                if string.find(Text, x) then
                    return true
                end
            end
        end
    end

    return false
end

local IsEnabled = true

Client:on("messageCreate", function(Text)
    if (string.match(Text.content, "-enable")) then
        local Title
        local Color
        IsEnabled = not IsEnabled

        if (IsEnabled) then
            Title = "✅ Enabled message scanning! ✅"
            Color = 0x3FF23F
        else
            Title = "⚠️ Disabled message scanning! ⚠️"
            Color = 0xF03E3D
        end
        Text:reply{
            embed = {
                title = Title,
                color = Color,
                description = ("Bool statement: %s"):format(IsEnabled),
            }
        }
    end

    if (SanityCheck(Text.content) and IsEnabled) then
        Text:reply{
            embed = {
                title = "⚠️ Malicious content detected! ⚠️",
                description = "This message has been flagged for posting a malicious link and has been deleted.",
                color = 0xF03E3D,
                fields = {
                    {
                        name = ("Poster: %s"):format(Text.author.name),
                        value = ("Message: %s"):format(Text.content),
                        inline = true
                    },
                    {
                        name = "False Positive?",
                        value = "Please contact (ayro#8803) for the domain/url to be whitelisted.",
                        inline = true
                    }
                }
            }
        }
        table.insert(Logs, Text)
        Text:delete()
    end

    if string.match(Text.content, "-logs") then
        for i,  v in next, Logs do
            Text:reply{
                embed = {
                    title = ("Log %i"):format(i),
                    description = ("Messenger: %s\n Message: %s"):format(v.author.name, v.content),
                    color = 0x3FF23F,
                }
            }
        end
    end
    if string.match(Text.content, "-clearlogs") then
        local OldTime = os.clock()
        for i,  v in next, Logs do
            Logs[i] = nil
        end
        Text:reply{
             embed = {
                title = "Successfully cleared logs!",
                    description = ("Took %s seconds!"):format(tostring(os.clock() - OldTime)),
                    color = 0x3FF23F,
            }
        }
    end
    if string.match(Text.content, "-turnoff") then
        error()
    end
end)


Client:on("ready", function()
    print("Discord Bot Loaded.")
end)

Client:run("")

