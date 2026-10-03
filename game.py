
import json
import os
import random

SAVE_FILE = "savegame.json"

RARITY_DATA = {
    "Common": (1.0, 0, 50),
    "Uncommon": (1.1, 2, 90),
    "Rare": (1.3, 5, 160),
    "Super Rare": (1.5, 8, 260),
    "Epic": (1.8, 12, 420),
    "Mythical": (2.2, 18, 700),
    "Legendary": (2.8, 25, 1100)
}

WEAPONS = [
    {"name": "Wooden Sword", "rank": "Common", "damage": 8, "price": 50, "level": 1},
    {"name": "Rusty Axe", "rank": "Common", "damage": 9, "price": 55, "level": 1},
    {"name": "Training Bow", "rank": "Common", "damage": 7, "price": 50, "level": 1},
    {"name": "Iron Sword", "rank": "Rare", "damage": 16, "price": 160, "level": 5},
    {"name": "Steel Axe", "rank": "Rare", "damage": 18, "price": 170, "level": 5},
    {"name": "Long Bow", "rank": "Rare", "damage": 15, "price": 155, "level": 5},
    {"name": "Crystal Blade", "rank": "Super Rare", "damage": 24, "price": 260, "level": 10},
    {"name": "Shadow Dagger", "rank": "Super Rare", "damage": 23, "price": 255, "level": 10},
    {"name": "Lightning Bow", "rank": "Super Rare", "damage": 22, "price": 250, "level": 10},
    {"name": "Flame Sword", "rank": "Epic", "damage": 34, "price": 420, "level": 20},
    {"name": "Ice Spear", "rank": "Epic", "damage": 32, "price": 410, "level": 20},
    {"name": "Thunder Hammer", "rank": "Epic", "damage": 38, "price": 440, "level": 20},
    {"name": "Phoenix Blade", "rank": "Mythical", "damage": 48, "price": 700, "level": 35},
    {"name": "Demon Slayer", "rank": "Mythical", "damage": 52, "price": 760, "level": 35},
    {"name": "Celestial Staff", "rank": "Mythical", "damage": 45, "price": 680, "level": 35},
    {"name": "Dragon King's Sword", "rank": "Legendary", "damage": 65, "price": 1100, "level": 50},
    {"name": "Blade of Eternity", "rank": "Legendary", "damage": 70, "price": 1200, "level": 50},
    {"name": "Bow of the Gods", "rank": "Legendary", "damage": 62, "price": 1080, "level": 50},
    {"name": "Knight's Blade", "rank": "Common", "damage": 11, "price": 75, "level": 3},
    {"name": "Hunter Bow", "rank": "Uncommon", "damage": 13, "price": 110, "level": 4},
    {"name": "Moonlight Staff", "rank": "Uncommon", "damage": 12, "price": 105, "level": 4}
]

ARMOR = [
    {"name": "Cloth Armor", "rank": "Common", "defense": 4, "hp": 10, "mana": 5, "crit_res": 1, "price": 50, "level": 1},
    {"name": "Leather Armor", "rank": "Common", "defense": 6, "hp": 15, "mana": 5, "crit_res": 2, "price": 70, "level": 1},
    {"name": "Iron Armor", "rank": "Rare", "defense": 10, "hp": 30, "mana": 10, "crit_res": 4, "price": 160, "level": 5},
    {"name": "Steel Armor", "rank": "Rare", "defense": 12, "hp": 35, "mana": 10, "crit_res": 5, "price": 180, "level": 7},
    {"name": "Crystal Armor", "rank": "Super Rare", "defense": 17, "hp": 50, "mana": 20, "crit_res": 7, "price": 270, "level": 10},
    {"name": "Shadow Armor", "rank": "Super Rare", "defense": 16, "hp": 45, "mana": 25, "crit_res": 8, "price": 280, "level": 10},
    {"name": "Flame Armor", "rank": "Epic", "defense": 23, "hp": 70, "mana": 25, "crit_res": 10, "price": 430, "level": 20},
    {"name": "Ice Armor", "rank": "Epic", "defense": 25, "hp": 65, "mana": 35, "crit_res": 11, "price": 440, "level": 20},
    {"name": "Phoenix Armor", "rank": "Mythical", "defense": 32, "hp": 100, "mana": 45, "crit_res": 15, "price": 720, "level": 35},
    {"name": "Demon Armor", "rank": "Mythical", "defense": 35, "hp": 90, "mana": 50, "crit_res": 17, "price": 760, "level": 35},
    {"name": "Dragon Armor", "rank": "Legendary", "defense": 45, "hp": 140, "mana": 60, "crit_res": 22, "price": 1150, "level": 50},
    {"name": "Eternal Armor", "rank": "Legendary", "defense": 50, "hp": 125, "mana": 70, "crit_res": 25, "price": 1250, "level": 50}
]

POTIONS = {
    "Small Health Potion": {"type": "health", "value": 50, "price": 30},
    "Medium Health Potion": {"type": "health", "value": 100, "price": 55},
    "Large Health Potion": {"type": "health", "value": 250, "price": 100},
    "Giant Health Potion": {"type": "health", "value": 500, "price": 180},
    "Ultimate Health Potion": {"type": "health_full", "value": 0, "price": 300},
    "Small Mana Potion": {"type": "mana", "value": 30, "price": 30},
    "Medium Mana Potion": {"type": "mana", "value": 75, "price": 55},
    "Large Mana Potion": {"type": "mana", "value": 150, "price": 100},
    "Giant Mana Potion": {"type": "mana", "value": 300, "price": 180},
    "Ultimate Mana Potion": {"type": "mana_full", "value": 0, "price": 300},
    "Elixir": {"type": "mixed", "value": 100, "price": 140},
    "Grand Elixir": {"type": "mixed", "value": 250, "price": 280},
    "Vital Elixir": {"type": "mixed", "value": 500, "price": 500},
    "Battle Tonic": {"type": "attack_buff", "value": 10, "price": 120},
    "Guardian Tonic": {"type": "defense_buff", "value": 10, "price": 120}
}

SKILLS = {
    "Warrior": [
        ("Slash", 10, 1.4),
        ("Shield Bash", 15, 1.6),
        ("Rage", 20, 1.9),
        ("Earthquake", 30, 2.5)
    ],
    "Mage": [
        ("Fireball", 10, 1.5),
        ("Ice Blast", 15, 1.8),
        ("Thunder Strike", 20, 2.1),
        ("Meteor", 30, 2.8)
    ],
    "Archer": [
        ("Multi Shot", 10, 1.4),
        ("Poison Arrow", 15, 1.7),
        ("Explosive Arrow", 20, 2.0),
        ("Sniper Shot", 30, 2.7)
    ],
    "Assassin": [
        ("Backstab", 10, 1.6),
        ("Smoke Bomb", 15, 1.8),
        ("Shadow Strike", 20, 2.2),
        ("Instant Kill", 30, 3.0)
    ]
}

CLASS_STATS = {
    "Warrior": {"hp": 150, "mana": 50, "attack": 18, "defense": 14, "crit": 8},
    "Mage": {"hp": 110, "mana": 120, "attack": 20, "defense": 8, "crit": 12},
    "Archer": {"hp": 120, "mana": 80, "attack": 17, "defense": 10, "crit": 18},
    "Assassin": {"hp": 95, "mana": 85, "attack": 22, "defense": 7, "crit": 25}
}

ENEMY_NAMES = [
    ("Goblin", 1, 10), ("Wolf", 1, 10), ("Slime", 1, 10),
    ("Zombie", 1, 10), ("Skeleton", 1, 10),
    ("Orc", 11, 20), ("Bandit", 11, 20), ("Troll", 11, 20),
    ("Dark Archer", 11, 20), ("Giant Spider", 11, 20),
    ("Vampire", 21, 30), ("Werewolf", 21, 30), ("Necromancer", 21, 30),
    ("Ice Golem", 21, 30), ("Fire Demon", 21, 30),
    ("Sand Beast", 31, 40), ("Ancient Knight", 41, 50),
    ("Lava Beast", 51, 60), ("Frost Wraith", 61, 70),
    ("Sky Serpent", 71, 80), ("Demon Hound", 81, 90),
    ("Dark Mage", 91, 100), ("Chaos Warrior", 91, 100),
    ("Realm Guardian", 91, 100), ("Abyss Walker", 91, 100)
]

BOSSES = {
    10: "Goblin King",
    20: "Forest Guardian",
    30: "Ancient Golem",
    40: "Vampire Lord",
    50: "Dragon Rider",
    60: "Demon General",
    70: "Ice Titan",
    80: "Shadow Emperor",
    90: "Celestial Dragon",
    100: "Ancient Demon King"
}

REGIONS = [
    "Village", "Forest", "Cave", "Desert", "Ruins",
    "Castle", "Volcano", "Frozen Mountain", "Sky Temple", "Demon Realm"
]


def create_player():
    print("Enter Player Name:")
    name = input("> ").strip()

    while name == "":
        print("Name cannot be empty.")
        name = input("> ").strip()

    print("\nChoose Your Class")
    print("1. Warrior")
    print("2. Mage")
    print("3. Archer")
    print("4. Assassin")

    classes = ["Warrior", "Mage", "Archer", "Assassin"]

    while True:
        choice = input("Choose: ").strip()
        if choice in ("1", "2", "3", "4"):
            player_class = classes[int(choice) - 1]
            break
        print("Invalid choice.")

    stats = CLASS_STATS[player_class]

    return {
        "name": name,
        "class": player_class,
        "level": 1,
        "exp": 0,
        "hp": stats["hp"],
        "max_hp": stats["hp"],
        "mana": stats["mana"],
        "max_mana": stats["mana"],
        "attack": stats["attack"],
        "defense": stats["defense"],
        "gold": 200,
        "crit_chance": stats["crit"],
        "crit_damage": 2.0,
        "weapon": None,
        "armor": None,
        "potions": {"Small Health Potion": 3, "Small Mana Potion": 2},
        "inventory": [],
        "bosses_defeated": [],
        "enemies_defeated": 0,
        "region": 0,
        "skill_unlock": 1
    }


def save_game(player):
    try:
        with open(SAVE_FILE, "w") as file:
            json.dump(player, file, indent=4)
        print("Game saved.")
    except OSError:
        print("Could not save the game.")


def load_game():
    if not os.path.exists(SAVE_FILE):
        print("No save file found.")
        return None

    try:
        with open(SAVE_FILE, "r") as file:
            player = json.load(file)
        print("Game loaded.")
        return player
    except (json.JSONDecodeError, OSError):
        print("Could not load the save file.")
        return None


def show_stats(player):
    print("\n========== PLAYER STATS ==========")
    print("Name:", player["name"])
    print("Class:", player["class"])
    print("Level:", player["level"])
    print("EXP:", player["exp"])
    print("HP:", player["hp"], "/", player["max_hp"])
    print("Mana:", player["mana"], "/", player["max_mana"])
    print("Attack:", player["attack"])
    print("Defense:", player["defense"])
    print("Gold:", player["gold"])
    print("Critical Chance:", player["crit_chance"], "%")
    print("Critical Damage:", player["crit_damage"], "x")
    print("Weapon:", player["weapon"]["name"] if player["weapon"] else "None")
    print("Armor:", player["armor"]["name"] if player["armor"] else "None")
    print("Bosses Defeated:", len(player["bosses_defeated"]))
    print("Enemies Defeated:", player["enemies_defeated"])


def show_inventory(player):
    print("\n========== INVENTORY ==========")

    if player["inventory"]:
        print("\nGear:")
        for i, item in enumerate(player["inventory"], 1):
            print(i, item["type"], "-", item["name"], "-", item["rank"])
    else:
        print("\nNo gear in inventory.")

    print("\nPotions:")
    found = False
    for name, count in player["potions"].items():
        if count > 0:
            print(name, "x", count)
            found = True

    if not found:
        print("No potions.")

    print("\nEquipped Weapon:",
          player["weapon"]["name"] if player["weapon"] else "None")
    print("Equipped Armor:",
          player["armor"]["name"] if player["armor"] else "None")


def effective_attack(player):
    attack = player["attack"]
    if player["weapon"]:
        multiplier = RARITY_DATA[player["weapon"]["rank"]][0]
        attack += int(player["weapon"]["damage"] * multiplier)
    return attack


def effective_defense(player):
    defense = player["defense"]
    if player["armor"]:
        defense += player["armor"]["defense"]
    return defense


def effective_crit(player):
    chance = player["crit_chance"]
    if player["weapon"]:
        chance += RARITY_DATA[player["weapon"]["rank"]][1]
    if player["armor"]:
        chance -= player["armor"]["crit_res"]
    return max(1, chance)


def choose_enemy(player):
    possible = [
        item for item in ENEMY_NAMES
        if item[1] <= player["level"] <= item[2]
    ]

    if not possible:
        possible = ENEMY_NAMES[-5:]

    name, low, high = random.choice(possible)
    level = max(low, min(player["level"], high))

    hp = 45 + level * 12
    attack = 7 + level * 3
    defense = 3 + level * 2

    return {
        "name": name,
        "level": level,
        "hp": hp,
        "max_hp": hp,
        "attack": attack,
        "defense": defense,
        "crit": min(30, 5 + level // 4)
    }


def create_boss(level):
    return {
        "name": BOSSES[level],
        "level": level,
        "hp": 500 + level * 45,
        "max_hp": 500 + level * 45,
        "attack": 20 + level * 4,
        "defense": 10 + level * 2,
        "crit": 20,
        "boss": True
    }


def gain_exp(player, amount):
    player["exp"] += amount
    print("You gained", amount, "EXP.")

    while player["level"] < 100:
        needed = player["level"] * 100

        if player["exp"] < needed:
            break

        player["exp"] -= needed
        player["level"] += 1
        player["max_hp"] += 15
        player["max_mana"] += 8
        player["attack"] += 3
        player["defense"] += 2
        player["hp"] = player["max_hp"]
        player["mana"] = player["max_mana"]

        if player["level"] % 5 == 0 and player["skill_unlock"] < 4:
            player["skill_unlock"] += 1
            print("A new skill has been unlocked!")

        print("LEVEL UP! You are now level", player["level"])


def enemy_turn(player, enemy, defend=False, turn_number=1):
    damage = max(1, enemy["attack"] - effective_defense(player))

    if random.randint(1, 100) <= enemy["crit"]:
        damage = int(damage * 1.5)
        print(enemy["name"], "landed a critical hit!")

    if defend:
        damage //= 2
        print("Defend reduced the damage.")

    player["hp"] -= damage
    print(enemy["name"], "dealt", damage, "damage.")

    if turn_number % 3 == 0 and enemy.get("boss", False):
        special = max(1, int(enemy["attack"] * 1.5) - effective_defense(player))
        player["hp"] -= special
        print(enemy["name"], "used a special attack for", special, "damage!")


def player_attack(player, enemy):
    damage = max(1, effective_attack(player) - enemy["defense"])

    if random.randint(1, 100) <= effective_crit(player):
        damage = int(damage * player["crit_damage"])
        print("CRITICAL HIT!")

    enemy["hp"] -= damage
    print("You dealt", damage, "damage.")


def use_skill(player, enemy):
    skills = SKILLS[player["class"]]
    unlocked = skills[:player["skill_unlock"]]

    print("\nSkills:")
    for i, skill in enumerate(unlocked, 1):
        print(i, skill[0], "- Mana:", skill[1])

    choice = input("Choose skill or 0 to cancel: ").strip()

    if choice == "0":
        return False

    try:
        index = int(choice) - 1
        skill = unlocked[index]
    except (ValueError, IndexError):
        print("Invalid skill.")
        return False

    name, mana_cost, multiplier = skill

    if player["mana"] < mana_cost:
        print("Not enough mana.")
        return False

    player["mana"] -= mana_cost
    damage = max(1, int(effective_attack(player) * multiplier)
                 - enemy["defense"])

    if random.randint(1, 100) <= effective_crit(player):
        damage = int(damage * player["crit_damage"])
        print("CRITICAL SKILL!")

    enemy["hp"] -= damage
    print(name, "dealt", damage, "damage.")
    return True


def use_potion(player):
    available = [
        name for name, count in player["potions"].items()
        if count > 0
    ]

    if not available:
        print("You have no potions.")
        return False

    print("\nPotions:")
    for i, name in enumerate(available, 1):
        print(i, name, "x", player["potions"][name])

    choice = input("Choose potion or 0 to cancel: ").strip()

    if choice == "0":
        return False

    try:
        potion_name = available[int(choice) - 1]
    except (ValueError, IndexError):
        print("Invalid potion.")
        return False

    potion = POTIONS[potion_name]

    if potion["type"] == "health":
        old = player["hp"]
        player["hp"] = min(player["max_hp"],
                           player["hp"] + potion["value"])
        print("Recovered", player["hp"] - old, "HP.")

    elif potion["type"] == "health_full":
        player["hp"] = player["max_hp"]
        print("HP fully restored.")

    elif potion["type"] == "mana":
        old = player["mana"]
        player["mana"] = min(player["max_mana"],
                             player["mana"] + potion["value"])
        print("Recovered", player["mana"] - old, "Mana.")

    elif potion["type"] == "mana_full":
        player["mana"] = player["max_mana"]
        print("Mana fully restored.")

    elif potion["type"] == "mixed":
        old_hp = player["hp"]
        old_mana = player["mana"]
        player["hp"] = min(player["max_hp"],
                           player["hp"] + potion["value"])
        player["mana"] = min(player["max_mana"],
                             player["mana"] + potion["value"])
        print("Recovered", player["hp"] - old_hp, "HP and",
              player["mana"] - old_mana, "Mana.")

    elif potion["type"] == "attack_buff":
        player["attack"] += potion["value"]
        print("Attack increased by", potion["value"], "for this battle.")

    elif potion["type"] == "defense_buff":
        player["defense"] += potion["value"]
        print("Defense increased by", potion["value"], "for this battle.")

    player["potions"][potion_name] -= 1
    return True


def battle(player, enemy):
    turn = 0

    print("\n====================")
    print("BATTLE:", enemy["name"])
    print("====================")

    while player["hp"] > 0 and enemy["hp"] > 0:
        turn += 1
        defend = False

        print("\nYOUR TURN")
        print("Your HP:", player["hp"], "/", player["max_hp"])
        print("Your Mana:", player["mana"], "/", player["max_mana"])
        print(enemy["name"], "HP:", enemy["hp"], "/", enemy["max_hp"])
        print("\n1 Attack")
        print("2 Skills")
        print("3 Heal")
        print("4 Use Potion")
        print("5 Defend")
        print("6 Inventory")
        print("7 View Stats")
        print("8 Run")

        choice = input("Choose: ").strip()
        action_done = False

        if choice == "1":
            player_attack(player, enemy)
            action_done = True

        elif choice == "2":
            action_done = use_skill(player, enemy)

        elif choice == "3":
            heal_cost = 10

            if player["mana"] < heal_cost:
                print("Not enough mana.")
            elif player["hp"] == player["max_hp"]:
                print("HP is already full.")
            else:
                player["mana"] -= heal_cost
                amount = int(player["max_hp"] * 0.20)
                old = player["hp"]
                player["hp"] = min(player["max_hp"],
                                   player["hp"] + amount)
                print("You recovered", player["hp"] - old, "HP.")
                action_done = True

        elif choice == "4":
            action_done = use_potion(player)

        elif choice == "5":
            defend = True
            action_done = True
            print("You are defending.")

        elif choice == "6":
            show_inventory(player)

        elif choice == "7":
            show_stats(player)

        elif choice == "8":
            if enemy.get("boss", False):
                print("You cannot run from a boss!")
            elif random.randint(1, 100) <= 50:
                print("You escaped.")
                return "run"
            else:
                print("You failed to escape.")
                action_done = True

        else:
            print("Invalid choice.")

        if not action_done:
            continue

        if enemy["hp"] <= 0:
            break

        enemy_turn(player, enemy, defend, turn)

    if player["hp"] <= 0:
        print("\nYou were defeated.")
        return "lose"

    print("\nYou defeated", enemy["name"] + "!")
    return "win"


def loot_drop(player, boss=False):
    if boss:
        player["gold"] += 300
        print("Boss reward: 300 gold.")

        rare_items = [
            item for item in WEAPONS + ARMOR
            if item["rank"] in (
                "Rare", "Super Rare", "Epic", "Mythical", "Legendary"
            )
            and item["level"] <= player["level"]
        ]

        if rare_items:
            item = random.choice(rare_items).copy()
            item["type"] = "Weapon" if "damage" in item else "Armor"
            player["inventory"].append(item)
            print("Guaranteed rare-or-better reward:", item["name"])

        return

    player["gold"] += random.randint(20, 80)

    roll = random.randint(1, 100)

    if roll <= 50:
        print("Loot: Gold")

    elif roll <= 70:
        potion = random.choice(list(POTIONS.keys()))
        player["potions"][potion] = player["potions"].get(potion, 0) + 1
        print("Loot:", potion)

    elif roll <= 85:
        available = [
            w for w in WEAPONS if w["level"] <= player["level"]
        ]
        item = random.choice(available).copy()
        item["type"] = "Weapon"
        player["inventory"].append(item)
        print("Loot:", item["name"])

    elif roll <= 98:
        available = [
            a for a in ARMOR if a["level"] <= player["level"]
        ]
        item = random.choice(available).copy()
        item["type"] = "Armor"
        player["inventory"].append(item)
        print("Loot:", item["name"])

    else:
        material = {
            "type": "Material",
            "name": random.choice(
                ["Iron Ore", "Crystal", "Demon Bone", "Ancient Rune"]
            )
        }
        player["inventory"].append(material)
        print("Loot:", material["name"])


def shop(player):
    while True:
        print("\n========== SHOP ==========")
        print("Gold:", player["gold"])
        print("1. Buy Weapons")
        print("2. Buy Armor")
        print("3. Buy Potions")
        print("4. Sell Items")
        print("5. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            items = [
                w for w in WEAPONS if w["level"] <= player["level"]
            ]

            for i, item in enumerate(items, 1):
                print(i, item["name"], item["rank"], item["price"])

            try:
                n = int(input("Choose item or 0 to cancel: "))
                if n == 0:
                    continue
                item = items[n - 1]
            except (ValueError, IndexError):
                print("Invalid choice.")
                continue

            if player["gold"] >= item["price"]:
                player["gold"] -= item["price"]
                new_item = item.copy()
                new_item["type"] = "Weapon"
                player["inventory"].append(new_item)
                print("Weapon purchased.")
            else:
                print("Not enough gold.")

        elif choice == "2":
            items = [
                a for a in ARMOR if a["level"] <= player["level"]
            ]

            for i, item in enumerate(items, 1):
                print(i, item["name"], item["rank"], item["price"])

            try:
                n = int(input("Choose item or 0 to cancel: "))
                if n == 0:
                    continue
                item = items[n - 1]
            except (ValueError, IndexError):
                print("Invalid choice.")
                continue

            if player["gold"] >= item["price"]:
                player["gold"] -= item["price"]
                new_item = item.copy()
                new_item["type"] = "Armor"
                player["inventory"].append(new_item)
                print("Armor purchased.")
            else:
                print("Not enough gold.")

        elif choice == "3":
            items = list(POTIONS.keys())

            for i, name in enumerate(items, 1):
                print(i, name, POTIONS[name]["price"])

            try:
                n = int(input("Choose item or 0 to cancel: "))
                if n == 0:
                    continue
                name = items[n - 1]
            except (ValueError, IndexError):
                print("Invalid choice.")
                continue

            price = POTIONS[name]["price"]

            if player["gold"] >= price:
                player["gold"] -= price
                player["potions"][name] = player["potions"].get(name, 0) + 1
                print("Potion purchased.")
            else:
                print("Not enough gold.")

        elif choice == "4":
            gear = [
                item for item in player["inventory"]
                if item.get("type") in ("Weapon", "Armor")
            ]

            if not gear:
                print("No sellable items.")
                continue

            for i, item in enumerate(gear, 1):
                print(i, item["name"], "-", item["price"] // 2)

            try:
                n = int(input("Choose item or 0 to cancel: "))
                if n == 0:
                    continue
                item = gear[n - 1]
            except (ValueError, IndexError):
                print("Invalid choice.")
                continue

            player["gold"] += item["price"] // 2
            player["inventory"].remove(item)
            print("Item sold.")

        elif choice == "5":
            break

        else:
            print("Invalid choice.")


def inventory_menu(player):
    while True:
        show_inventory(player)

        print("\n1. Equip")
        print("2. Unequip Weapon")
        print("3. Unequip Armor")
        print("4. Use Potion")
        print("5. Drop Item")
        print("6. Sell Item")
        print("7. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            gear = [
                item for item in player["inventory"]
                if item.get("type") in ("Weapon", "Armor")
            ]

            if not gear:
                print("No gear available.")
                continue

            for i, item in enumerate(gear, 1):
                print(i, item["type"], item["name"], item["rank"])

            try:
                n = int(input("Choose item or 0 to cancel: "))
                if n == 0:
                    continue
                item = gear[n - 1]
            except (ValueError, IndexError):
                print("Invalid choice.")
                continue

            if item["type"] == "Weapon":
                player["weapon"] = item
                print(item["name"], "equipped.")
            else:
                player["armor"] = item
                print(item["name"], "equipped.")

        elif choice == "2":
            player["weapon"] = None
            print("Weapon unequipped.")

        elif choice == "3":
            player["armor"] = None
            print("Armor unequipped.")

        elif choice == "4":
            use_potion(player)

        elif choice == "5":
            if not player["inventory"]:
                print("Inventory is empty.")
                continue

            for i, item in enumerate(player["inventory"], 1):
                print(i, item["name"])

            try:
                n = int(input("Choose item or 0 to cancel: "))
                if n == 0:
                    continue
                item = player["inventory"][n - 1]
            except (ValueError, IndexError):
                print("Invalid choice.")
                continue

            if item == player["weapon"] or item == player["armor"]:
                print("Unequip the item before dropping it.")
            else:
                player["inventory"].remove(item)
                print("Item dropped.")

        elif choice == "6":
            gear = [
                item for item in player["inventory"]
                if item.get("type") in ("Weapon", "Armor")
            ]

            if not gear:
                print("No sellable gear.")
                continue

            for i, item in enumerate(gear, 1):
                print(i, item["name"], "-", item["price"] // 2)

            try:
                n = int(input("Choose item or 0 to cancel: "))
                if n == 0:
                    continue
                item = gear[n - 1]
            except (ValueError, IndexError):
                print("Invalid choice.")
                continue

            if item == player["weapon"] or item == player["armor"]:
                print("Unequip the item before selling it.")
            else:
                player["gold"] += item["price"] // 2
                player["inventory"].remove(item)
                print("Item sold.")

        elif choice == "7":
            break

        else:
            print("Invalid choice.")


def world_map(player):
    print("\n========== WORLD MAP ==========")

    for i, region in enumerate(REGIONS):
        if i <= player["region"]:
            print(i + 1, region, "- Unlocked")
        else:
            print(i + 1, region, "- Locked")


def check_boss(player):
    level = ((player["level"] + 9) // 10) * 10

    if level > 100:
        return None

    if level in BOSSES and level not in player["bosses_defeated"]:
        if player["level"] >= level:
            return create_boss(level)

    return None


def adventure(player):
    while True:
        if player["level"] >= 100 and 100 in player["bosses_defeated"]:
            victory(player)
            return

        boss = check_boss(player)

        if boss:
            print("\nA BOSS BLOCKS YOUR PATH!")
            result = battle(player, boss)

            if result == "win":
                player["bosses_defeated"].append(boss["level"])
                loot_drop(player, True)

                if boss["level"] < 100:
                    player["region"] = min(9, boss["level"] // 10)
                    print("New region unlocked:",
                          REGIONS[player["region"]])
                else:
                    victory(player)
                    return

            elif result == "lose":
                game_over(player)
                return

            continue

        print("\n========== ADVENTURE ==========")
        print("Current Region:", REGIONS[player["region"]])
        print("1. Explore")
        print("2. World Map")
        print("3. Inventory")
        print("4. Shop")
        print("5. Save Game")
        print("6. Return to Main Menu")

        choice = input("Choose: ").strip()

        if choice == "1":
            enemy = choose_enemy(player)
            result = battle(player, enemy)

            if result == "win":
                player["enemies_defeated"] += 1
                gain_exp(player, 30 + enemy["level"] * 8)
                loot_drop(player)

            elif result == "lose":
                game_over(player)
                return

        elif choice == "2":
            world_map(player)

        elif choice == "3":
            inventory_menu(player)

        elif choice == "4":
            shop(player)

        elif choice == "5":
            save_game(player)

        elif choice == "6":
            return

        else:
            print("Invalid choice.")


def instructions():
    print("\n========== INSTRUCTIONS ==========")
    print("Defeat enemies to gain EXP, gold and loot.")
    print("Level up to increase HP, Mana, Attack and Defense.")
    print("A boss appears every 10 levels.")
    print("Defeat each boss to unlock the next region.")
    print("Reach Level 100 and defeat the Ancient Demon King.")
    print("Use weapons, armor, potions and skills during battles.")
    print("Use Save Game to store your progress.")


def victory(player):
    print("\n==============================")
    print("          VICTORY!")
    print("==============================")
    print("The Ancient Demon King has been defeated!")
    print("Player Name:", player["name"])
    print("Final Level:", player["level"])
    print("Total Gold:", player["gold"])
    print("Bosses Defeated:", len(player["bosses_defeated"]))
    print("Enemies Defeated:", player["enemies_defeated"])
    print("Weapons Collected:",
          sum(1 for i in player["inventory"]
              if i.get("type") == "Weapon"))
    print("Rare Items Found:",
          sum(1 for i in player["inventory"]
              if i.get("rank") in
              ("Rare", "Super Rare", "Epic", "Mythical", "Legendary")))


def game_over(player):
    print("\n==============================")
    print("          GAME OVER")
    print("==============================")

    while True:
        print("1. Retry")
        print("2. Load Save")
        print("3. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            player["hp"] = player["max_hp"]
            player["mana"] = player["max_mana"]
            adventure(player)
            return

        elif choice == "2":
            loaded = load_game()
            if loaded:
                adventure(loaded)
            return

        elif choice == "3":
            return

        else:
            print("Invalid choice.")


def new_game():
    player = create_player()
    print("\nWelcome to Eldoria,", player["name"] + "!")
    print("Your class is", player["class"] + ".")
    adventure(player)


def main():
    while True:
        print("\n==========================")
        print("LEGENDS OF THE FORGOTTEN REALM")
        print("==========================")
        print("1. New Game")
        print("2. Continue")
        print("3. Instructions")
        print("4. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            new_game()

        elif choice == "2":
            player = load_game()
            if player:
                adventure(player)

        elif choice == "3":
            instructions()

        elif choice == "4":
            print("Thank you for playing!")
            break

        else:
            print("Invalid choice.")


main()
