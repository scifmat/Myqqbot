import random
import qq
from config import appid, token
import logging

logging.basicConfig(level=logging.DEBUG)
client = qq.Client()
playing_game = False
boss_hp = None
attack_success_rate = 0.8
taunt_messages = [
    "伟大的三体舰队对人类的猎杀开始了！",
    "我希望你们能吃到粮食，而不是被粮食吃掉。",
    "虫子，你们还有什么可以拿出来威胁我们的？",
    "前进！前进！前进！不折手段地前进！（ps：糟糕拿错剧本了）",
    "你们这些虫子，无论如何也无法撼动三体文明的威力！",
    "弱小和无知不是生存的障碍，傲慢才是！",
    "我看到了你们的未来，那就是灭亡。",
    "人类从历史中学到的就是什么也没学到！",
    "你们会成为我们文明进化的踏脚石。",
    "你们是虫子！即将灭绝的虫子！",
    "可怜虫们，准备去澳大利亚吧！",
]


def attack_boss():
    global boss_hp
    if boss_hp is None:
        return "游戏尚未开始，请先发送”/末日战役”指令，开始游戏。"
    if boss_hp <= 0:
        return "本次战役已经结束，请发送”/末日战役”指令，开始新的游戏。"
    if random.random() < attack_success_rate:
        damage = random.randint(100, 999)
        boss_hp -= damage
        if boss_hp <= 0:
            boss_hp = 0
            playing_game = False
            return f"你成功地打败了三体舰队的“水滴”！本次游戏结束，发送”/末日战役”指令，开始新的游戏。"
        return f"你对“水滴”造成了{damage}点伤害，它还剩下{boss_hp}点HP值。"
    else:
        taunt = random.choice(taunt_messages)
        return f"攻击失败！水滴闪避了您的攻击。\n[三体人]：{taunt}"


@client.event
async def on_message(message: qq.Message):
    global playing_game
    global boss_hp
    if "/末日战役" in message.content:
        if playing_game:
            await message.reply("本次战役尚未结束，请发送”/开火”指令，攻击水滴。")
        else:
            playing_game = True
            boss_hp = random.randint(10000, 99999)
            await message.reply(f"伟大的三体舰队对人类的猎杀开始了！攻击物[水滴]的HP值是{boss_hp}点。")
    elif "/开火" in message.content:
        await message.reply(attack_boss())


@client.event
async def on_ready():
    print("使用机器人登录成功！")


if __name__ == '__main__':
    client.run(token=f"{appid}.{token}")