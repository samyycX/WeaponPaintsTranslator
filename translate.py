from keyvalues import KeyValues
import os
import json
import vpk

if not os.path.isdir('output'):
    os.mkdir("output")
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
items = items_game_kv['items_game'][0]['items']
prefabs = items_game_kv['items_game'][0]['prefabs']
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
def find_in_items(def_index):
    for i in items:
        if str(def_index) in i:
            return i[str(def_index)]
def find_in_prefabs(prefab):
    for i in prefabs:
        if prefab in i:
            return i[prefab]
#translate skins


print("正在翻译 skins.json...")
def translate(filename):
    path = os.path.join(skins_path, filename)
    if not os.path.exists(path):
        print(f"未找到 {filename}! 请检查您的路径")
    skins_file = open(path, 'r', encoding='utf-8')
    skins = json.load(skins_file)
    skins_file.close()
    for item in skins:
        
        paint_name = item['paint_name']
        splited_name = paint_name.split(" | ")
        weapon_name = splited_name[0].strip()
        paint_name = splited_name[1].strip()
        
        paint_id = item['paint']
        paint_kit = find_in_paint_kits(paint_id)[0]
        description_tag = paint_kit['description_tag'][0]
        if description_tag[1:] in translation:
            paint_name = translation[description_tag[1:]][0]
        
        weapon_defindex = item['weapon_defindex']
        weapon_translated_name = find_in_items(weapon_defindex)
        if weapon_translated_name != None:
            #print(weapon_translated_name)
            if "item_name" in weapon_translated_name[0]:
                weapon_name = translation[weapon_translated_name[0]["item_name"][0][1:]][0]
            else:
                if "prefab" in weapon_translated_name[0]:
                    prefab = weapon_translated_name[0]["prefab"][0]
                    prefab = find_in_prefabs(prefab)
                    weapon_name = translation[prefab[0]["item_name"][0][1:]][0]
        item['paint_name'] = weapon_name + " | " + paint_name
    with open("output/" + filename, 'w', encoding='utf-8') as f:
        json.dump(skins, f, ensure_ascii=False)
translate("skins.json")
print("翻译成功! 请查看 output/skins.json")

print("正在翻译 gloves.json...")
translate("gloves.json")
print("翻译成功! 请查看 output/gloves.json")

print("正在翻译 music.json...")
with open(os.path.join(skins_path, "music.json"), 'r', encoding="utf-8") as f:
    music = json.load(f)
all_musics = list(filter(lambda x: x.startswith("musickit_") and not x.endswith("_desc"), translation))
for item, key in zip(music, all_musics):
    item['name'] = translation[key][0]
with open("output/" + 'music.json', 'w', encoding="utf-8") as f:
    json.dump(music, f, ensure_ascii=False)
print("翻译成功! 请查看 output/music.json")

print("正在翻译 agents.json...")
with open(os.path.join(skins_path, "agents.json"), 'r', encoding='utf-8') as f:
    agents = json.load(f)
for item in agents:
    model_name = item['model'].split('/')[-1]
    translation_keys = ["CSGO_CustomPlayer_"+model_name, "CSGO_Customplayer_"+model_name]
    for translation_key in translation_keys:
        if translation_key in translation:
            item['agent_name'] = translation[translation_key][0]
with open("output/" + 'agents.json', 'w', encoding='utf-8') as f:
    json.dump(agents, f, ensure_ascii=False)
print("翻译成功！请查看 output/agents.json")