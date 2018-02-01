# coding=utf-8
"""
@author: 'wang'
"""
EC_SUCCESS = {
  "code": 0,
  "err_msg": "EC_SUCCESS"   # 成功
}
EC_UNKNOWN_ERROR = {
  "code": 1,
  "err_msg": "EC_UNKNOWN_ERROR"   # 未知错误
}
EC_NO_FOUND_HANDLER = {
  "code": 2,
  "err_msg": "EC_NO_FOUND_HANDLER"   # 没有此命令
}
EC_INVALID_REQUEST_PARAM = {
  "code": 3,
  "err_msg": "EC_INVALID_REQUEST_PARAM"   # 非法参数
}
EC_NOT_LOGIN = {
  "code": 4,
  "err_msg": "EC_NOT_LOGIN"   # 没有登录
}
EC_NOT_FOUND_FRIEND_INFO = {
  "code": 5,
  "err_msg": "EC_NOT_FOUND_FRIEND_INFO"   # 没有找到好友信息
}
EC_NOT_FOUND_PEOPLE_NEARBY = {
  "code": 6,
  "err_msg": "EC_NOT_FOUND_PEOPLE_NEARBY"   # 没有找到附近的人
}
EC_SMS_CALL_FAILURE = {
  "code": 7,
  "err_msg": "EC_SMS_CALL_FAILURE"   # 短信发送失败
}
EC_NOT_FOUND_PET = {
  "code": 8,
  "err_msg": "EC_NOT_FOUND_PET"  # 没有找到宠物
}
EC_NO_CREATE_ROLE = {
  "code": 11,
  "err_msg": "EC_NO_CREATE_ROLE"   # 未创建角色
}
EC_ROLE_ALREADY_EXIST = {
  "code": 12,
  "err_msg": "EC_ROLE_ALREADY_EXIST"   # 角色已存在
}
EC_ILLEGAL_WORD = {
  "code": 21,
  "err_msg": "EC_ILLEGAL_WORD"   # 非法字符
}
EC_NOT_ENOUGH_ENERGY = {
  "code": 42,
  "err_msg": "EC_NOT_ENOUGH_ENERGY"   # 当前体力值不够
}
EC_ROOM_IS_NOT_IDLE = {
  "code": 43,
  "err_msg": "EC_ROOM_IS_NOT_IDLE"   # 当前房间已经满员
}
EC_ROOM_IS_IN_FIGHTING = {
  "code": 44,
  "err_msg": "EC_ROOM_IS_IN_FIGHTING"   # 当前房间已经开始战斗
}
EC_ERROR_CREATE_BATTLE_ROOM = {
  "code": 51,
  "err_msg": "EC_ERROR_CREATE_BATTLE_ROOM"   # 创建战斗房间失败
}
EC_NOT_FOUND_PET_TEAM = {
  "code": 52,
  "err_msg": "EC_NOT_FOUND_PET_TEAM"   # 没有找到符合条件的宠物战队
}
EC_USER_NOT_JOIN_ANY_ROOM = {
  "code": 53,
  "err_msg": "EC_USER_NOT_JOIN_ANY_ROOM"  # 用户未加入任何房间
}
EC_PLAYER_IS_IN_FIGHTING = {
  "code": 54,
  "err_msg": "EC_PLAYER_IS_IN_FIGHTING"   # 当前用户正在战斗中
}
EC_RECOGNIZE_RESULT_MISSING_FLAG = {
  "code": 55,
  "err_msg": "EC_RECOGNIZE_RESULT_MISSING_FLAG"   # 人脸识别结果缺少flag字段信息
}
EC_RECOGNIZE_RESULT_MISSING_CANDIDATE = {
  "code": 56,
  "err_msg": "EC_RECOGNIZE_RESULT_MISSING_CANDIDATE"   # 人脸识别结果缺少candidate字段信息
}
EC_RECOGNIZE_RESULT_CANDIDATE_SIZE_ERROR = {
  "code": 57,
  "err_msg": "EC_RECOGNIZE_RESULT_CANDIDATE_SIZE_ERROR"   # 人脸识别接口返回candidate数组长度错误(小于或者等于0)
}
EC_INVALID_RECOGNIZE_RESULT = {
  "code": 58,
  "err_msg": "EC_INVALID_RECOGNIZE_RESULT"   # 人脸识别接口返回的json格式错误
}
EC_NOT_ENOUGH_SCAN_TIMES = {
  "code": 59,
  "err_msg": "EC_NOT_ENOUGH_SCAN_TIMES"   # 没有足够的扫描次数
}
EC_NO_FOUND_PLAYER_PARK = {
  "code": 60,
  "err_msg": "EC_NO_FOUND_PLAYER_PARK"   # 没有找到该主题乐园
}
EC_NO_FOUND_BUILDING = {
  "code": 61,
  "err_msg": "EC_NO_FOUND_BUILDING"   # 没有找到该建筑
}
EC_MAX_BUILDING_LEVEL = {
  "code": 62,
  "err_msg": "EC_MAX_BUILDING_LEVEL"   # 该建筑已满级
}
EC_NOT_ENOUGH_COIN = {
  "code": 63,
  "err_msg": "EC_NOT_ENOUGH_COIN"   # 金币数量不够
}
EC_PET_NOT_FREE = {
  "code": 64,
  "err_msg": "EC_PET_NOT_FREE"   # 宠物在其他舞台或随身宠
}
EC_USER_NOT_EXIST = {
  "code": 65,
  "err_msg": "EC_USER_NOT_EXIST"   # 用户不存在
}
EC_NOT_ALLOW_ADDSELF = {
  "code": 66,
  "err_msg": "EC_NOT_ALLOW_ADDSELF"   # 玩家不能添加自己为好友
}
EC_PART_BROKEN = {
  "code": 67,
  "err_msg": "EC_PART_BROKEN"   # 宠物部件已经损坏
}
EC_MAX_PART_LEVEL = {
  "code": 68,
  "err_msg": "EC_MAX_PART_LEVEL"   # 该部件已经升级到满级
}
EC_MAX_PET_COUNT = {
  "code": 69,
  "err_msg": "EC_MAX_PET_COUNT"   # 养成宠已经达到上限
}
EC_NOT_COMPLETE_PET = {
  "code": 70,
  "err_msg": "EC_NOT_COMPLETE_PET"   # 当前宠物养成还没完成
}
EC_NOT_PART_BROKEN = {
  "code": 71,
  "err_msg": "EC_NOT_PART_BROKEN"   # 宠物部件未损坏
}
EC_MAX_PET_SET = {
  "code": 72,
  "err_msg": "EC_MAX_PET_SET"   # 养成宠设置达到上限
}
EC_NOT_ALLOW_PET = {
  "code": 73,
  "err_msg": "EC_NOT_ALLOW_PET"   # 该宠物不能设置为养成宠
}
EC_PET_NOT_CAPTURE = {
  "code": 74,
  "err_msg": "EC_PET_NOT_CAPTURE"   # 玩家不能添加自己为好友
}
EC_PLAYER_BE_PROTECTED = {
  "code": 75,
  "err_msg": "EC_PLAYER_BE_PROTECTED"   # 该玩家不可攻击
}
EC_NOT_ALLOW_ATTACK_PART = {
  "code": 76,
  "err_msg": "EC_NOT_ALLOW_ATTACK_PART"   # 当前部位不可攻击
}
EC_NOT_ALLOW_ATTACK_SELF = {
  "code": 77,
  "err_msg": "EC_NOT_ALLOW_ATTACK_SELF"   # 不能攻击自己
}
EC_UCID_INVALID = {
  "code": 78,
  "err_msg": "EC_UCID_INVALID"   # UCID 不合法
}
EC_USER_ID_NOT_ALLOW = {
  "code": 79,
  "err_msg": "EC_USER_ID_NOT_ALLOW"   # 系统保留账号 100000以内的账号为系统保留
}
EC_NOT_ALLOW_STEAL = {
  "code": 80,
  "err_msg": "EC_NOT_ALLOW_STEAL"   # 当前不允许偷取,如未转到捕捉
}
EC_NOT_ALLOW_ATTACK = {
  "code": 81,
  "err_msg": "EC_NOT_ALLOW_ATTACK"   # 当前不允许攻击,如未转到攻击
}
EC_DATA_NOT_IDENTICAL = {
  "code": 82,
  "err_msg": "EC_DATA_NOT_IDENTICAL"   # 客户端与服务端数据不一致
}
EC_USER_IN_REWARD = {
  "code": 83,
  "err_msg": "EC_USER_IN_REWARD"   # 当前玩家已经在被通缉中
}
EC_NOT_ENOUGH_REWARD = {
  "code": 84,
  "err_msg": "EC_NOT_ENOUGH_REWARD"   # 该类型悬赏令数量不足
}
EC_NOT_ALLOW_REWARD_SELF = {
  "code": 85,
  "err_msg": "EC_NOT_ALLOW_REWARD_SELF"   # 不能悬赏自己
}
EC_NOT_CATCH_ANY_ONE = {
  "code": 86,
  "err_msg": "EC_NOT_CATCH_ANY_ONE"   # 未捕捉到任何宠物
}
EC_NOT_USER_ENEMY = {
  "code": 87,
  "err_msg": "EC_NOT_USER_ENEMY"   # 该用户不是你的仇家
}
EC_FRIEND_ALREADY_EXISTED = {
  "code": 88,
  "err_msg": "EC_FRIEND_ALREADY_EXISTED"   # 该用户已经是你的好友
}
EC_MAX_ENERGY = {
  "code": 89,
  "err_msg": "EC_MAX_ENERGY"   # 当前体力值已满
}
EC_NOT_GET_ENERGY = {
  "code": 90,
  "err_msg": "EC_NOT_GET_ENERGY"   # 上次赠送的体力还没领取
}
EC_ENERGY_HAD_GIVE = {
  "code": 91,
  "err_msg": "EC_ENERGY_HAD_GIVE"   # 今天已经给该好友赠送过体力
}
EC_ENERGY_HAD_EXPIRED = {
  "code": 92,
  "err_msg": "EC_ENERGY_HAD_EXPIRED"   # 该好友赠送的体力已经过期
}
EC_NOT_FOUND_FRIEND = {
  "code": 93,
  "err_msg": "EC_NOT_FOUND_FRIEND"   # 没有找到该好友
}
EC_NOT_FOUND_ENERGY = {
  "code": 94,
  "err_msg": "EC_NOT_FOUND_ENERGY"   # 该好友没有赠送体力，或者已经过期
}
EC_ENERGY_HAD_GET = {
  "code": 95,
  "err_msg": "EC_ENERGY_HAD_GET"   # 已经获取过该体力
}
EC_MAX_GET_ENERGY = {
  "code": 96,
  "err_msg": "EC_MAX_GET_ENERGY"   # 当天领取已达上限
}
EC_REQUEST_HAD_DEAL = {
  "code": 97,
  "err_msg": "EC_REQUEST_HAD_DEAL"   # 该请求已处理过
}
EC_REQUEST_NOT_FOUND = {
  "code": 98,
  "err_msg": "EC_REQUEST_NOT_FOUND"   # 不存在该请求
}
EC_NOT_ENOUGH_TRUMPETS = {
  "code": 99,
  "err_msg": "EC_NOT_ENOUGH_TRUMPETS"   #
}
EC_UNKNOWN_ITEM_TYPE = {
  "code": 100,
  "err_msg": "EC_UNKNOWN_ITEM_TYPE"   #
}
EC_NOT_ENOUGH_ITEM = {
  "code": 101,
  "err_msg": "EC_NOT_ENOUGH_ITEM"   #
}



