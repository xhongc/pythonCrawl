# coding=utf-8
"""
@author: 'wang'
"""
from base.tcp import BaseTcp
from cof.mysocket import MySocket
import json
from cof.rand import CoRand
from api_call.message.packet import *


class ARControl(BaseTcp, MySocket):
    
    def __init__(self):
        BaseTcp.__init__(self)
        MySocket.__init__(self, self.get_host(), self.get_port())
        self.tag = CoRand.get_rand_int(0, 100000)

    #    通用接口调用(请求并接受消息)
    def get_res(self, api_name, json_body):
        params = json.dumps(json_body)
        req = SocketPacket(self.tag, api_name, params)
        recv = self.request(req)
        res = SocketUnPacket(recv)
        return res.param.context

    #    通用接口调用(接收服务端推送)
    def get_rev(self):
        recv = self.recive()
        res = SocketUnPacket(recv)
        return res.param.context

    # -------------------角色---------------------------------

    #   调用用户登录接口

    def login(self, account_id, user_type, uc_id=None):
        api_name = "login"
        json_body = {
            "user_type": user_type,
            "token": "00000",
            "account_id": account_id
        }
        if uc_id is not None:
            json_body["uc_id"] = uc_id
            json_body["uc_token"] = uc_id
        res = self.get_res(api_name, json_body)
        return res
    
    #   调用修改角色信息
    def modify_info(self, nick_name, icon=None, sex=None, sign="API测试"):
        api_name = "modifyInfo"
        json_body = {
            "nick_name": nick_name,
            "sign": sign
        }
        if sex is not None:
            json_body["sex"] = sex
        if icon is not None:
            json_body["icon"] = icon
        else:
            json_body["icon"] = "https://www.baidu.com/"
        res = self.get_res(api_name, json_body)
        return res
    
    #   调用上报位置信息接口
    def update_location(self, latitude, longitude):
        api_name = "updateLocation"
        json_body = {
            "latitude": latitude,
            "longitude": longitude
        } 
        res = self.get_res(api_name, json_body)
        return res
    
    #   调用追踪接口
    def get_random_event(self, latitude, longitude):
        api_name = "getRandomEvent"
        json_body = {
            "latitude": latitude,
            "longitude": longitude
        }
        res = self.get_res(api_name, json_body)
        return res

    #   调用开宝箱接口
    def open_treasure_box(self, event_id, game_result):
        api_name = "openTreasureBox"
        json_body = {
            "event_id": event_id,
            "game_result": game_result
        }
        res = self.get_res(api_name, json_body)
        return res

    #   调用查找附近的人接口
    def people_near_by(self, latitude, longitude):
        api_name = "peopleNearBy"
        json_body = {
            "latitude": latitude,
            "longitude": longitude
        } 
        res = self.get_res(api_name, json_body)
        return res
    
    #   调用获取角色完整信息接口
    def get_user_info(self, user_id):
        api_name = "getUserInfo"
        json_body = {
            "user_id": user_id
        }
        res = self.get_res(api_name, json_body)
        return res

    #   调用获取UC对应角色信息接口
    def get_user_from_uc_id(self, uc_id):
        api_name = "getUserFromUcID"
        json_body = {
            "uc_id": uc_id
        }
        res = self.get_res(api_name, json_body)
        return res

    #   调用获取多玩家简要信息接口
    def get_users(self, user_ids):
        api_name = "getUsers"
        json_body = {
            "user_ids": user_ids
        }
        res = self.get_res(api_name, json_body)
        return res

    #   调用获取玩家体力接口
    def get_energy(self):
        api_name = "getEnergy"
        json_body = {}
        res = self.get_res(api_name, json_body)
        return res

    #   调用获取玩家金币接口
    def get_user_coin(self):
        api_name = "getUserCoin"
        json_body = {}
        res = self.get_res(api_name, json_body)
        return res

    #   调用获取仇人列表接口
    def get_enemy_list(self):
        api_name = "getEnemyList"
        json_body = {}
        res = self.get_res(api_name, json_body)
        return res

    #   调用获取未读消息接口
    def get_unread_msg(self):
        api_name = "getUnReadMsg"
        json_body = {}
        res = self.get_res(api_name, json_body)
        return res

    #   调用获取随机玩家接口
    def get_rand_friend_info(self):
        api_name = "getRandFriendInfo"
        json_body = {}
        res = self.get_res(api_name, json_body)
        return res

    #   调用悬赏接口
    def reward_player(self, reward_type, user_id):
        api_name = "rewardPlayer"
        json_body = {
            "reward_type": reward_type,
            "user_id": user_id
        }
        res = self.get_res(api_name, json_body)
        return res

    #   调用获取悬赏令攻击信息接口
    def get_reward_attack(self, reward_id, page=None):
        api_name = "getRewardAttack"
        json_body = {
            "reward_id": reward_id
        }
        if page is not None:
            json_body["page"] = page
        res = self.get_res(api_name, json_body)
        return res

    #   调用获取悬赏令接口

    def get_reward(self, reward_id):
        api_name = "getReward"
        json_body = {
            "reward_id": reward_id
        }
        res = self.get_res(api_name, json_body)
        return res

    #   调用使用喇叭接口

    def use_trumpet(self):
        api_name = "useTrumpet"
        json_body = {}
        res = self.get_res(api_name, json_body)
        return res
    # -------------------好友关系---------------------------------

    #   调用添加好友接口
    def add_friend(self, user_id):
        api_name = "addFriend"
        json_body = {
            "user_id": user_id
        }
        res = self.get_res(api_name, json_body)
        return res

    #   调用处理添加好友请求接口
    def deal_add_friend(self, user_id, op):
        api_name = "dealAddFriend"
        json_body = {
            "user_id": user_id,
            "op": op
        }
        res = self.get_res(api_name, json_body)
        return res

    #   调用删除好友接口
    def del_friend(self, user_id):
        api_name = "delFriend"
        json_body = {
            "user_id": user_id
        }
        res = self.get_res(api_name, json_body)
        return res

    #   调用获取好友列表接口
    def get_friend_list(self):
        api_name = "getFriendList"
        json_body = {}
        res = self.get_res(api_name, json_body)
        return res

    #   调用赠送体力接口
    def give_friend_energy(self, user_id):
        api_name = "giveFriendEnergy"
        json_body = {
            "user_id": user_id
        }
        res = self.get_res(api_name, json_body)
        return res

    #   调用领取体力接口
    def get_friend_energy(self, user_id):
        api_name = "getFriendEnergy"
        json_body = {
            "user_id": user_id
        }
        res = self.get_res(api_name, json_body)
        return res

    #   调用一键赠送和领取体力接口
    def get_and_give_friends_energy(self):
        api_name = "getAndGiveFriendsEnergy"
        json_body = {}
        res = self.get_res(api_name, json_body)
        return res

    # -------------------宠物---------------------------------

    #   调用人脸扫描接口
    def scan_face(self, url, name="la", scan_advance=None):
        api_name = "scanFace"
        json_body = {
            "url": url,
            "name": name,
        }
        if scan_advance is not None:
            json_body["scan_advance"] = scan_advance
        res = self.get_res(api_name, json_body)
        return res

    #   调用捕获宠物接口
    def capture_pet(self, pet_id):
        api_name = "capturePet"
        json_body = {
            "pet_id": pet_id
        }
        res = self.get_res(api_name, json_body)
        return res

    #   调用设置宠物备注接口
    def set_pet_tag(self, pet_id, tag):
        api_name = "setPetTag"
        json_body = {
            "pet_id": pet_id,
            "tag": tag
        }
        res = self.get_res(api_name, json_body)
        return res
    
    #   调用获取宠物列表接口
    def get_pet_list(self, user_id):
        api_name = "getPetList"
        json_body = {
            "user_id": user_id
        }
        res = self.get_res(api_name, json_body)
        return res
    
    #   调用获取剩余的捕获次数接口
    def get_match_count(self):
        api_name = "getMatchCount"
        json_body = {}
        res = self.get_res(api_name, json_body)
        return res
    
    #   调用获取宠物信息接口
    def get_pet_info(self, pet_id, user_id):
        api_name = "getPetInfo"
        json_body = {
            "pet_id": pet_id,
            "user_id": user_id
        }
        res = self.get_res(api_name, json_body)
        return res
    
    #   调用进化宠物接口
    def evolution_pet(self, pet_id):
        api_name = "evolutionPet"
        json_body = {
            "pet_id": pet_id
        }
        res = self.get_res(api_name, json_body)
        return res
    
    #   调用突破宠物接口
    def refine_pet(self, pet_id):
        api_name = "refinePet"
        json_body = {
            "pet_id": pet_id
        }
        res = self.get_res(api_name, json_body)
        return res

    #   调用出售宠物接口
    def sell_pet(self, pet_ids):
        api_name = "sellPet"
        json_body = {
            "pet_ids": pet_ids
        }
        res = self.get_res(api_name, json_body)
        return res

    #   调用查看默认的宠物队伍接口
    def get_def_pet_team(self):
        api_name = "getDefPetTeam"
        json_body = {}
        res = self.get_res(api_name, json_body)
        return res

    #   调用设置默认的宠物队伍接口
    def set_def_pet_team(self, pet_member, team_code):
        api_name = "setDefPetTeam"
        json_body = {
            "pet_member": pet_member,
            "team_code": team_code
        }
        res = self.get_res(api_name, json_body)
        return res

    #   设置养成宠
    def set_cultivate_pet(self, pet_id):
        api_name = "setCultivatePet"
        json_body = {
            "pet_id": pet_id
        }
        res = self.get_res(api_name, json_body)
        return res

    #   升级部件
    def upgrade_pet_part(self, part):
        api_name = "upgradePetPart"
        json_body = {
            "part": part
        }
        res = self.get_res(api_name, json_body)
        return res

    #   攻击
    def attack_pet(self, part, user_id, reward_id=None):
        api_name = "attackPet"
        json_body = {
            "part": part,
            "user_id": user_id
        }
        if reward_id is not None:
            json_body["reward_id"] = reward_id
        res = self.get_res(api_name, json_body)
        return res

    #   获取攻击次数
    def get_attack_count(self, user_id):
        api_name = "getAttackCount"
        json_body = {
            "user_id": user_id
        }
        res = self.get_res(api_name, json_body)
        return res

    #   修复
    def repair_pet_part(self, part):
        api_name = "repairPetPart"
        json_body = {
            "part": part
        }
        res = self.get_res(api_name, json_body)
        return res

    #   获取富豪列表
    def get_rich_player_list(self):
        api_name = "getRichPlayerList"
        json_body = {}
        res = self.get_res(api_name, json_body)
        return res

    #   获取最富富豪
    def get_richest_player(self):
        api_name = "getRichestPlayer"
        json_body = {}
        res = self.get_res(api_name, json_body)
        return res

    #   捕捉富豪
    def catch_player_list(self, user_ids):
        api_name = "catchPlayerList"
        json_body = {
            "user_ids": user_ids
        }
        res = self.get_res(api_name, json_body)
        return res

    #   出售物品
    def sell_item(self, item_id, item_type, item_count):
        api_name = "sellItem"
        json_body = {
            "item_id": item_id,
            "item_type": item_type,
            "item_count": item_count
        }
        res = self.get_res(api_name, json_body)
        return res

    #   获取原生宠列表
    def get_protozoan_list(self, user_id):
        api_name = "getProtozoanList"
        json_body = {
            "user_id": user_id
        }
        res = self.get_res(api_name, json_body)
        return res

    #   获取灵魂宠列表
    def get_soul_pet_list(self, user_id):
        api_name = "getSoulPetList"
        json_body = {
            "user_id": user_id
        }
        res = self.get_res(api_name, json_body)
        return res

    #   设置人脸宠属性
    def set_pet_mode_ver(self, item_id, ver):
        api_name = "setPetModelVer"
        json_body = {
            "pet_id": item_id,
            "ver": ver
        }
        res = self.get_res(api_name, json_body)
        return res

    # -------------------识花---------------------------------

    #   调用扫描花朵接口
    def match_flower(self, url):
        api_name = "matchFlower"
        json_body = {
            "url": url
        } 
        res = self.get_res(api_name, json_body)
        return res
    
    #   调用获取种子信息接口
    def get_seeds(self):
        api_name = "getSeeds"
        json_body = {}
        res = self.get_res(api_name, json_body)
        return res
        
    #   调用种植花朵接口
    def plant_seed(self, soil_id, seed):
        api_name = "plantSeed"
        json_body = {
            "soil_id": soil_id,
            "seed": seed
        }
        res = self.get_res(api_name, json_body)
        return res
       
    #   调用获取地块信息接口
    def get_soils(self):
        api_name = "getSoils"
        json_body = {}
        res = self.get_res(api_name, json_body)
        return res
    
    #   调用收花接口
    def harvest_flower(self, soil_id):
        api_name = "harvestFlower"
        json_body = {
            "soil_id": soil_id
        }
        res = self.get_res(api_name, json_body)
        return res

    # -------------------神仙居---------------------------------

    #   调用获取神仙居接口
    def get_supply(self, latitude, longitude):
        api_name = "getSupply"
        json_body = {
            "latitude": latitude,
            "longitude": longitude
        }
        res = self.get_res(api_name, json_body)
        return res

    #   调用膜拜神仙居接口
    def visit_supply(self, latitude, longitude, _id):
        api_name = "visitSupply"
        json_body = {
            "latitude": latitude,
            "longitude": longitude,
            "id": _id
        }
        res = self.get_res(api_name, json_body)
        return res

    # -------------------玩家公寓---------------------------------

    #   获取所有公寓列表
    def get_all_apartment(self):
        api_name = "getAllApartment"
        json_body = {}
        res = self.get_res(api_name, json_body)
        return res

    #   获取所有公寓列表
    def get_apartment_list(self, user_id):
        api_name = "getApartmentList"
        json_body = {
            "user_id": user_id
        }
        res = self.get_res(api_name, json_body)
        return res

    #   获取公寓所有楼层信息
    def get_apartment_floor_list(self, apartment_code):
        api_name = "getApartmentFloorList"
        json_body = {
            "apartment_code": apartment_code
        }
        res = self.get_res(api_name, json_body)
        return res

    #   玩家申请入住公寓
    def apply_apartment(self, apartment_code):
        api_name = "applyApartment"
        json_body = {
            "apartment_code": apartment_code
        }
        res = self.get_res(api_name, json_body)
        return res

    #   重命名玩家楼层名称
    def update_floor_name(self, apartment_code, floor_name, floor):
        api_name = "updateFloorName"
        json_body = {
            "apartment_code": apartment_code,
            "floor_name": floor_name,
            "floor": floor
        }
        res = self.get_res(api_name, json_body)
        return res

    #   打扫公寓楼
    def sweep_apartment(self, apartment_code, user_id, floor):
        api_name = "sweepApartment"
        json_body = {
            "apartment_code": apartment_code,
            "user_id": user_id,
            "floor": floor
        }
        res = self.get_res(api_name, json_body)
        return res

    #   查看公寓打扫信息
    def get_apartment_sweep_info(self, apartment_code, user_id, floor):
        api_name = "getApartmentSweepInfo"
        json_body = {
            "apartment_code": apartment_code,
            "user_id": user_id,
            "floor": floor
        }
        res = self.get_res(api_name, json_body)
        return res

    #   查看玩家派出去打扫的宠物信息
    def get_sweeping_pet_info(self, apartment_code):
        api_name = "getSweepingPetInfo"
        json_body = {
            "apartment_code": apartment_code
        }
        res = self.get_res(api_name, json_body)
        return res

    #   获取玩家打扫别人房间的奖励
    def get_sweep_other_rewards(self):
        api_name = "getSweepOtherRewards"
        json_body = {}
        res = self.get_res(api_name, json_body)
        return res

    #   获取其他人打扫自己房间的奖励
    def get_own_floor_rewards(self):
        api_name = "getOwnFloorRewards"
        json_body = {}
        res = self.get_res(api_name, json_body)
        return res

    # -------------------战斗接口-------------------------------------

    #   获取房间列表
    def get_room_list(self):
        api_name = "getRoomList"
        json_body = {}
        res = self.get_res(api_name, json_body)
        return res

    #   加入房间
    def join_room(self, room_id):
        api_name = "joinRoom"
        json_body = {
            "room_id": room_id
        }
        res = self.get_res(api_name, json_body)
        return res

    #   离开房间
    def leave_room(self, room_id):
        api_name = "leaveRoom"
        json_body = {
            "room_id": room_id
        }
        res = self.get_res(api_name, json_body)
        return res

    #   快速加入房间
    def quick_join(self):
        api_name = "quickJoin"
        json_body = {}
        res = self.get_res(api_name, json_body)
        return res

    #   获取房间信息
    def get_room_info(self, room_id):
        api_name = "getRoomInfo"
        json_body = {
            "room_id": room_id
        }
        res = self.get_res(api_name, json_body)
        return res

    #   准备战斗
    def ready_battle(self):
        api_name = "readyBattle"
        json_body = {}
        res = self.get_res(api_name, json_body)
        return res

    #   取消战斗准备
    def cancel_ready(self):
        api_name = "cancelReady"
        json_body = {}
        res = self.get_res(api_name, json_body)
        return res

    # -------------------主题乐园-----------------------------------
    #   获取主题乐园
    def get_theme_park(self, user_id, park_code):
        api_name = "getThemePark"
        json_body = {
            "user_id": user_id,
            "park_code": park_code
        }
        res = self.get_res(api_name, json_body)
        return res

    #   升级玩家建筑
    def upgrade_building(self, building_id):
        api_name = "upgradeBuilding"
        json_body = {
            "building_id": building_id
        }
        res = self.get_res(api_name, json_body)
        return res

    #   装备宠物
    def equip_pet(self, theme_park_id, pet_id, pos):
        api_name = "equipPet"
        json_body = {
            "theme_park_id": theme_park_id,
            "pet_id": pet_id,
            "pos": pos
        }
        res = self.get_res(api_name, json_body)
        return res

    #   卸下宠物
    def tear_down_pet(self, theme_park_id, pet_id):
        api_name = "teardownPet"
        json_body = {
            "theme_park_id": theme_park_id,
            "pet_id": pet_id
        }
        res = self.get_res(api_name, json_body)
        return res

    #   设置随身宠
    def set_follow_pet(self, theme_park_id, pet_id):
        api_name = "setFollowPet"
        json_body = {
            "theme_park_id": theme_park_id,
            "pet_id": pet_id
        }
        res = self.get_res(api_name, json_body)
        return res

    # -------------------其他-------------------------------------

    #   抽奖
    def draw_lottery(self):
        api_name = "drawLottery"
        json_body = {}
        res = self.get_res(api_name, json_body)
        return res

    # -------------------恶人排行榜-------------------------------------
    #   获取排行榜
    def evil_rank_list(self, rank_type):
        api_name = "evilRankList"
        json_body = {
            "rank_type": rank_type
        }
        res = self.get_res(api_name, json_body)
        return res

    # -------------------其他-------------------------------------
    
    #   获取CS的Session
    def get_cs_session(self):
        api_name = "getCSSession"
        json_body = {}
        res = self.get_res(api_name, json_body)
        return res

    #   设置新手导引数据
    def set_newer_code(self, newer_code):
        api_name = "setNewerCode"
        json_body = {
            "newer_code": newer_code
        }
        res = self.get_res(api_name, json_body)
        return res

    #   PM 命令
    def pm_set_role_data(self, key, value):
        api_name = "pm_SetRoleData"
        json_body = {
            "key": key,
            "value": value
        }
        res = self.get_res(api_name, json_body)
        return res

    # -----------------数据库操作---------------------

    #   同步
    def gm_reload_user_data(self, user_id):
        api_name = "gm_reloadUserData"
        json_body = {
            "user_id": user_id
        }
        res = self.get_res(api_name, json_body)
        return res
