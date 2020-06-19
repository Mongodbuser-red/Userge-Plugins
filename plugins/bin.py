from userge import userge, Message
import requests
import json

async def fix_j(dic_resp,gdn):
    k_scheme = dic_resp.get("scheme",None)
    k_type = dic_resp.get("type",None)
    k_brand = dic_resp.get("brand",None)
    k_prepaid = dic_resp.get("prepaid",None)
    k_l_country = dic_resp.get("country",None)
    if k_l_country is not None:
        k_Country_Code = k_l_country.get("numeric",None)
        if k_Country_Code is not None:
            k_Country_Code = "+"+k_Country_Code
        k_short_Name = k_l_country.get("alpha2",None)
        k_Country = k_l_country.get("name",None)
        k_emoji = k_l_country.get("emoji",None)
        if k_Country is not None:
            k_Country = k_Country+" "+k_emoji
            del k_emoji
        k_currency = k_l_country.get("currency",None)
        k_latitude = k_l_country.get("latitude",None)
        k_longitude = k_l_country.get("longitude",None)
    k_l_bank = dic_resp.get("bank",None)
    if k_l_bank is not None:
        k_bank = k_l_bank.get("name",None)
        k_city_Name = k_l_bank.get("city",None)
    k = locals().copy()
    
    l = []
    for d in k:
        if d.startswith("k"):
            l.append((d,locals()[d]))
           
    strb = f"<u><b>Info About {gdn}</b></u>\n"
    for v in l:
        if v[1] is not None and "l_" not in v[0]:
            strb += "**"+v[0].replace("k_","").capitalize().replace("_"," ")+" :** `"+str(v[1]).capitalize()+"`\n"
    return(strb)

async def bin_search(strin: int):
    if len(str(strin)) <= 16 and len(str(strin)) >= 6:
        if len(str(strin)) <= 16 and len(str(strin)) > 6:
            strin = strin[0:6]
        resp = requests.get(f"https://lookup.binlist.net/{strin}")
        if resp.status_code == 200:
            dic_resp = resp.json()
            m = await fix_j(dic_resp,strin)
            return m
        else:
            return False
    else:
        return False

@userge.on_cmd("bin", about={
    'header': "Bin Search",
    'description': '''Fetch Info About bin''',
    'usage': "{tr}bin [bin]",
    'examples': "{tr}bin 457173",
})
async def check_bin(message: Message):
    bin_c = message.input_str
    if bin_c:
        mb_c = await bin_search(bin_c)
        if mb_c:
            try:
                await message.edit(mb_c)
            except Exception as k:
                await message.edit(k)
        else:
            await message.edit("**Invalid Bin!**")
    else:
        await message.edit("**Give me a bin to search**")
