from keyvalues import KeyValues
import os
import json
import vpk

weapon_translation = {
    "PP-Bizon": "PP-野牛",
    "Desert Eagle": "沙漠之鹰",
    "R8 Revolver": "R8 左轮手枪",
    "Dual Berettas": "双持贝瑞塔",
    "Nova": "新星",
    "Negev": "内格夫",
    "Sawed-Off": "截短霰弹枪",
    "Bayonet": "刺刀",
    "Classic Knife": "海报短刀",
    "Flip Knife": "折叠刀",
    "Gut Knife":"穿肠刀",
    "Karambit": "爪子刀",
    "M9 Bayonet": "M9 刺刀",
    "Huntsman Knife": "猎杀者匕首",
    "Falchion Knife": "弯刀",
    "Bowie Knife": "鲍伊猎刀",
    "Butterfly Knife": "蝴蝶刀",
    "Shadow Daggers": "暗影双匕",
    "Paracord Knife": "系绳匕首",
    "Survival Knife": "求生匕首",
    "Ursus Knife": "熊刀",
    "Navaja Knife": "折刀",
    "Nomad Knife": "流浪者匕首",
    "Stiletto Knife": "短剑",
    "Talon Knife": "锯齿爪刀",
    "Skeleton Knife": "骷髅匕首",
    "Kukri Knife": "廊尔喀刀",
    "Default Gloves": "默认手套",
    "Broken Fang Gloves": "狂牙手套",
    "Bloodhound Gloves": "血猎手套",
    "Sport Gloves": "运动手套",
    "Driver Gloves": "驾驶手套",
    "Hand Wraps": "手部束带",
    "Moto Gloves": "摩托手套",
    "Specialist Gloves": "专业手套",
    "Hydra Gloves": "九头蛇手套"
}

vpk_path = input("请输入 pak01_dir.vpk 的路径 (以pak01_dir.vpk结束): ")
pak01 = vpk.open(vpk_path)
skins_path = input("请输入插件网站json文件所在的目录 (如果在此脚本同一目录请直接回车):")
print("正在提取VPK...")

if not os.path.isdir('./extracted'):
    os.mkdir('extracted')
with open("extracted/items_game.txt", 'w', encoding='utf-8') as f:
    file = pak01['scripts/items/items_game.txt']
    f.write(file.read().decode('utf-8'))
with open("extracted/csgo_schinese.txt", 'w', encoding='utf-8') as f:
    file = pak01['resource/csgo_schinese.txt']
    f.write(file.read().decode('utf-8'))

print("正在解析文件...")

items_game_kv = KeyValues(filename="./extracted/items_game.txt")
paint_kits = items_game_kv['items_game'][0]['paint_kits']

# fix translation parse
with open('./extracted/csgo_schinese.txt',  encoding='utf-8', mode='r+') as f:
    head = f.readline()
    if bytes(head, encoding='utf-8') != bytes("\"lang\"\n", encoding='utf-8'):
        content = f.read()
        f.seek(0,0)
        f.write(head[1:]+content)

translation_kv = KeyValues(filename="./extracted/csgo_schinese.txt")
translation = translation_kv['lang'][0]['Tokens'][0]

def find_in_paint_kits(paint_id):
    for i in paint_kits:
        if str(paint_id) in i:
            return i[str(paint_id)]

#translate skins


print("正在翻译 skins.json...")
def translate(filename):
    if not os.path.exists(skins_path + filename):
        print(f"未找到 {filename}! 请检查您的路径")
    skins_file = open(skins_path + filename, 'r', encoding='utf-8')
    skins = json.load(skins_file)
    skins_file.close()
    for item in skins:
        paint_id = item['paint']
        paint_kit = find_in_paint_kits(paint_id)[0]
        description_tag = paint_kit['description_tag'][0]
        if description_tag[1:] in translation:
            translated = translation[description_tag[1:]][0]
        else:
            translated = None
        paint_name = item['paint_name']
        weapon_name = paint_name.split(" |")[0].strip()
        if weapon_name in weapon_translation:
            weapon_name = weapon_translation[weapon_name]
        elif weapon_name.removeprefix("★ ") in weapon_translation:
            weapon_name = "★ "+weapon_translation[weapon_name.removeprefix("★ ")]
        if translated:
            translated_full = weapon_name+" | "+translated
        else:
            translated_full = weapon_name+" | "+paint_name.split(" |")[1]
        item['paint_name'] = translated_full
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(skins, f, ensure_ascii=False)
translate("skins.json")
print("翻译成功! 请查看 skins.json")

print("正在翻译 gloves.json...")
translate("gloves.json")
print("翻译成功! 请查看 gloves.json")

print("正在翻译 music.json...")
with open(skins_path + "music.json", 'r', encoding="utf-8") as f:
    music = json.load(f)
all_musics = list(filter(lambda x: x.startswith("musickit_") and not x.endswith("_desc"), translation))
for item, key in zip(music, all_musics):
    item['name'] = translation[key][0]
with open('music.json', 'w', encoding="utf-8") as f:
    json.dump(music, f, ensure_ascii=False)
print("翻译成功! 请查看 music.json")

print("正在翻译 agents.json...")
with open(skins_path + 'agents.json', 'r', encoding='utf-8') as f:
    agents = json.load(f)
for item in agents:
    model_name = item['model'].split('/')[-1]
    translation_keys = ["CSGO_CustomPlayer_"+model_name, "CSGO_Customplayer_"+model_name]
    for translation_key in translation_keys:
        if translation_key in translation:
            item['agent_name'] = translation[translation_key][0]
with open('agents.json', 'w', encoding='utf-8') as f:
    json.dump(agents, f, ensure_ascii=False)
print("翻译成功！请查看 agents.json")