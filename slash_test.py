import discord
import discord.app_commands
import discord.interactions
from discord.ext import commands
import time
token = 'MTAzODMzOTcyOTE4OTUxOTQyMQ.GC0kkM.ghv0HWIgLg5DA14SEavPfxCIsB4KU9t1xnNdUQ'
client = discord.Client(intents=discord.Intents.all())
tree = discord.app_commands.CommandTree(client)
from discord.ext import tasks
vc_create_list = []

@tree.command(
    name="create",#コマンド名
    description="Send Hello world."#コマンドの説明
)
async def hoge(ctx:discord.Interaction, vc:str):
    message = await ctx.channel.send(f"VC名 {vc} \n<:spe1_megahonn:1029217238915493968> を押すと、VCチャンネルが生成されます。")
    await message.add_reaction("<:spe1_megahonn:1029217238915493968>")
    print(ctx.message)

@client.event
async def on_raw_reaction_add(payload):
    channel = client.get_channel(payload.channel_id)
    msg = await channel.fetch_message(payload.message_id)
    content = msg.content.split()

    overwrites = {
        channel.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        channel.guild.get_role(1027456607166156872): discord.PermissionOverwrite(read_messages=True),
        channel.guild.get_role(1032986688928104459): discord.PermissionOverwrite(read_messages=True)
    }
    
    if msg.author == client.user and payload.member != client.user:
        await msg.remove_reaction(payload.emoji, payload.member)
        if payload.member in vc_create_list: #連続作成防止
            return
        if payload.emoji.id == 1029217238915493968:
            counter = 1

            while True:
                chName = f"🎧{counter}-{content[1]}"
                BefchName = f"🎧{counter - 1}-{content[1]}"
                flag = 0

                for i in channel.category.channels:
                    if chName == i.name:
                        flag = 1
                
                if flag == 0:
                    ch = await channel.guild.create_voice_channel(name=chName, category=channel.category)
                    texch = await channel.guild.create_text_channel(name=f"{chName} 聞き専", category=channel.category, overwrites=overwrites)

                    for i in channel.category.channels:
                        if BefchName == i.name:
                            print(f"{BefchName}は存在します")
                            await ch.move(after=i)
                    break

                counter += 1

@client.event
async def on_voice_state_update(member, before, after):
    print(member.name, before.channel , after.channel)

    if before.channel == None:
        print(f"{member.name} が {after.channel.name} に入室しました")

        chName = after.channel.name #VCのチャンネル名
        category = after.channel.category
        VCtexCh = after.channel
        flag = 0
        for af in category.channels: 
            if chName in af.name:
                VCtexCh = af
                flag = 1
                print(f"{VCtexCh.name}がみつかりました")
                break
        
        if flag == 0:
            return

        await VCtexCh.set_permissions(member, read_messages=True)

        #ここに権限付与のコード
    elif after.channel == None:
        print(f"{member.name} が {before.channel.name} から退出しました")
        chName = before.channel.name #VCのチャンネル名
        category = before.channel.category
        VCtexCh = before.channel
        flag = 0
        for bf in category.channels: 
            if chName in bf.name:
                VCtexCh = bf
                flag = 1
                print(f"{VCtexCh.name}がみつかりました")
                break
        
        if flag == 0:
            return

        await VCtexCh.set_permissions(member, read_messages=False)
        #ここに権限はく奪のコード
    elif before.channel == after.channel:
        print(f"{member.name} が {before.channel.name} でステータスを更新しました")

    elif before.channel != after.channel:
        print(f"{member.name} が {before.channel.name} から {after.channel.name} に移動しました")

        AchName = after.channel.name #VCのチャンネル名
        Acategory = after.channel.category
        AVCtexCh = after.channel
        Aflag = 0
        for af in Acategory.channels: 
            if AchName in af.name:
                AVCtexCh = af
                Aflag = 1
                print(f"{AVCtexCh.name}がみつかりました")
                break
        
        if Aflag == 0:
            return

        await AVCtexCh.set_permissions(member, read_messages=True)

        BchName = before.channel.name #VCのチャンネル名
        Bcategory = before.channel.category
        BVCtexCh = before.channel
        Bflag = 0
        for bf in Bcategory.channels: 
            if BchName in bf.name:
                BVCtexCh = bf
                Bflag = 1
                print(f"{BVCtexCh.name}がみつかりました")
                break
        
        if Bflag == 0:
            return

        await BVCtexCh.set_permissions(member, read_messages=False)

        

@tasks.loop(seconds=600)
async def auto_delete_voiceChannel():
    guild = client.get_guild(1027157448173297664)
    list = guild.voice_channels

    for ch in list:
         if "🎧" in (ch.name) and len(ch.members) == 0:
                print(f"{ch.name}がけされたよ")
                await ch.delete()

                for rom in ch.category.channels:

                    if ch.name in rom.name:
                        VCtexCh = rom
                        print(f"{VCtexCh.name}がみつかりました")
                        if ch == VCtexCh:
                            print("完全一致のためスキップ")
                            continue
                        await VCtexCh.delete()
                        break

@tasks.loop(seconds=60)
async def user_list_reset():
    vc_create_list.clear()


@client.event
async def on_ready():
    await tree.sync()
    print("ready")
    auto_delete_voiceChannel.start()
client.run(token)