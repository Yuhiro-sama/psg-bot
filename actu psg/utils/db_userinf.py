import sqlite3
import math

conn = sqlite3.connect('storage.db')
c = conn.cursor()

color = 0xff1100





#CHECK
def add_top(ctx, top, number):
    try:
        for a in top[number]:
            if a['server'] == ctx.guild.id:
                pass
            else:
                number += 1
    except:
        return False
    number += 1
    return number


async def check_rank(ctx, top, value):
    for k in top[0]:
        if k[str(value)] >= 1:
            return True
    else:
        await ctx.send("No top in this server!")
        return False
    
    
        
def check_bot(user):
    if user is None:
        return True
    if user.bot:
        return False
    
    
def check_value(value):
    d = None
    if value == "xp":
        d = 2
    elif value == "lvl":
        d = 3
    elif value == "msg":
        d = 4
    elif value == "coin":
        d = 5
    else:
        raise ValueError("Wrong value !")
    return d
    

#USERINFO

def userid(ctx):
    try:
        return ctx.author.id
    except:
        return ctx.id
    
def get_all_by_serv(ctx):
    c.execute("SELECT * FROM user_inf WHERE guild_id = :guild_id AND user_id = :user_id", {'guild_id': ctx.guild.id, 'user_id': userid(ctx)})
    return c.fetchall()

def get_user_cus(user_id_, guild_id_):
    c.execute("SELECT * FROM user_inf WHERE guild_id = :guild_id AND user_id = :user_id", {'guild_id': guild_id_, 'user_id': user_id_})
    return c.fetchall()

def get_all_server(ctx):
    c.execute("SELECT * FROM user_inf WHERE guild_id = :guild_id", {'guild_id': ctx.guild.id})
    return c.fetchall()


def get_user_serv_cus(user_id, guild_id, value):
    a = get_user_cus(user_id, guild_id)
    d = check_value(value)
    return a[0][d]

def get_user_serv(ctx, value):
    
    a = get_all_by_serv(ctx)
    d = check_value(value)
    return a[0][d]
    


def insert_user(ctx):
    with conn:
        c.execute("INSERT INTO user_inf VALUES (:guild_id, :user_id, :xp, :lvl, :msg, :coin)", {'guild_id': ctx.guild.id, 'user_id': userid(ctx), 'xp': 0, 'lvl':0, 'msg':0, 'coin':0})
        
def check_lvl(ctx):
    xp = get_user_serv(ctx, "xp")
    xp = xp / 100
    lvl = math.floor(xp)
    with conn:
        c.execute(f"""UPDATE user_inf SET lvl = :lvl
                    WHERE guild_id = :guild_id AND user_id = :user_id""",
                {'guild_id': ctx.guild.id, 'user_id': userid(ctx), f'lvl': lvl})
    return 
    
        
def update_user(ctx, value, arg : int):
    try:
        if ctx.bot:
            return
    except:
        pass
    
    a = get_all_by_serv(ctx)
    d = check_value(value)
    arg  = arg + a[0][d]
    with conn:
        c.execute(f"""UPDATE user_inf SET {value} = ({arg})
                    WHERE guild_id = :guild_id AND user_id = :user_id""",
                {'guild_id': ctx.guild.id, 'user_id': userid(ctx), f'{value}': {arg}})


