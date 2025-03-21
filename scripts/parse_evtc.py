import json
import struct
from enum import Enum, auto

# agent struct:
# uint64 addr
# uint32 prof
# uint32 is_elite
# uint16 toughness
# uint16 concentration
# uint16 healing
# uint16 hitbox_width
# uint16 condition
# uint16 hitbox_height
# char name[64]
#

class StateChange(Enum):
    # NoState = auto() # skip None because python starts enums at 1
    EnterCombat = auto()
    ExitCombat = auto()
    ChangeUp = auto() # agent is alive
    ChangeDead = auto() # agent is dead
    ChangeDown = auto() # agent is down
    Spawn = auto() # agent entered tracking
    Despawn = auto() # agent left tracking
    HealthPctUpdate = auto()
    SqCombatStart = auto()
    LogEnd = auto()
    WeapSwap = auto()
    MaxHealthUpdate = auto()
    PointOfView = auto()
    Language = auto()
    GWBuild = auto()
    ShardID = auto()
    Reward = auto()
    BuffInitial = auto()
    Position = auto() # dst_agent is float[3], x/y/z
    Velocity = auto()
    Facing = auto()
    TeamChange = auto()
    AttackTarget = auto()
    Targetable = auto()
    MapID = auto()
    Replinfo = auto()
    StackActive = auto()
    StackReset = auto()
    Guild = auto()
    BuffInfo = auto()
    BuffFormula = auto()
    SkillInfo = auto()
    SkillTiming = auto()
    BreakbarState = auto()
    BreakbarPercent = auto()
    Integrity = auto()
    Marker = auto()
    BarrierPctUpdate = auto()
    StatReset = auto()
    Extension = auto()
    ApiDelayed = auto()
    InstanceStart = auto()
    RateHealth = auto()
    Last90BeforeDown = auto()
    Effect = auto()
    IdToGUID = auto()
    LogNPCUpdate = auto()
    IdleEvent = auto()
    ExtensionCombat = auto()
    FractalScale = auto()
    Effect2 = auto()
    Ruleset = auto()
    SquadMarker = auto()
    ArcBuild = auto()
    Glider = auto()
    StunBreak = auto()
    Unknown = auto()


def parse_evtc(path: str):
    f = open(path, "rb")
    header = f.read(16)
    assert(header[0:4] == b"EVTC")
    date_yyyymmdd = header[4:12]
    revision = struct.unpack("b", header[12:13])[0]
    boss_id = struct.unpack("H", header[13:15])[0]
    print("revision: ", revision, "date: ", date_yyyymmdd, "boss id: ", boss_id)

    agent_count = struct.unpack("I", f.read(4))[0]
    print("num agents: ", agent_count)
    toxic_geysers = []
    ura_ids = []
    agent_names = dict()
    for i in range(agent_count):
        agent = struct.unpack("QLLHHHHHH64s4x", f.read(96))
        (addr, prof, is_elite, toughness, concentration, healing, hitbox_width, condition, hitbox_height, name) = agent
        name = name.decode("utf8")
        toughness = round(toughness / 10) # it is either 10 or 0. 10 if above 66% of the squad's max
        concentration = round(concentration / 10) # it is either 10 or 0. 10 if above 66% of the squad's max
        healing = round(healing / 10) # it is either 10 or 0. 10 if above 66% of the squad's max
        condition = round(condition / 10) # it is either 10 or 0. 10 if above 66% of the squad's max
        # players have a dot in their name
        if False and "." in name:
            print(name, "tough:", toughness, "conc:", concentration, "healing:", healing, "condition:", condition)
        if "Toxic Geyser" in name:
            toxic_geysers.append(addr)
        if "Ura" in name:
            ura_ids.append(addr)
        agent_names[addr] = name
        # if "Ura" in name:
        #     ura_id = addr
        #     print("ura id: ", addr, name)

    skill_count = struct.unpack("I", f.read(4))[0]
    print("num skills: ", skill_count)
    for i in range(skill_count):
        # skill struct is just int32 id + charname[64]
        (id, name) = struct.unpack("i64s", f.read(68))
        name = name.decode("utf8")

    event_count = 0
    combat_start = 0
    last_spawn = 0
    while True:
        event_count += 1
        data = f.read(64)
        if data == b'': # end of file
            break
        event = struct.unpack("QQQiiIIHHHH16B", data)
        time = event[0]             # uint64. timegettime() at event
        src_agent = event[1]        # uint64
        dst_agent = event[2]        # uint64
        value = event[3]            # int32
        buff_dmg = event[4]         # int32
        overstack_value = event[5]  # uint32
        skillid = event[6]          # uint32
        src_instid = event[7]       # uint16. agent id, out-of-range agents can have this set even if src_agent is zero.
        dst_instid = event[8]       # uint16. ^
        src_master_instid = event[9] # uint16
        dst_master_instid = event[10] # uint16
        # all next fields are uint8
        iff = event[11] # affinity
        buff = event[12]
        result = event[13]
        is_activation = event[14]
        is_buffermove = event[15]
        is_ninety = event[16] # src_agent is above 90% hp
        is_fifty = event[17] # dst_agent is below 50% hp
        is_moving = event[18] # src_agent moving if bit0 is set. dst_agent moving if bit1 is set.
        is_statechange = event[19] # will be non-zero for state change events, refer to enum
        is_flanking = event[20] # src_agent is flanking dst_agent
        is_shields = event[21]
        is_offcycle = event[22]

        if is_statechange == StateChange.SqCombatStart.value:
            combat_start = time

        if is_statechange == StateChange.MapID.value:
            print("Map ID: ", src_agent)
        
        # if is_statechange == StateChange.Spawn.value:
        #     if src_agent in toxic_geysers:
        #         print("Toxic spawn at", time - combat_start, src_agent)
        if is_statechange == StateChange.Position.value:
            if src_agent in toxic_geysers:
                position = struct.unpack("fff", data[12:24])
                position_round = []
                for i in range(3):
                    position_round.append(round(position[i]))
                time_from_start = (time - combat_start) / 1000
                time_since_last = (time - last_spawn) / 1000
                last_spawn = time
                print(time_from_start, time_since_last, ":", position_round)
        

    print("num events: ", event_count)
    f.close()

def main():
    path = "./logs/20250319-234628.evtc" # kadenar's
    # path = "./logs/log.evtc"
    parse_evtc(path)
    return

if __name__ == "__main__":
    main()