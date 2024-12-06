# Advent of Code 2024
# Day 1 Problem 5

# X|Y means X must be printed before Y
# section 1 is these rules
# section 2 is updates to rules
# which updates are in the right order?

T = ["47|53",
"97|13",
"97|61",
"97|47",
"75|29",
"61|13",
"75|53",
"29|13",
"97|29",
"53|29",
"61|53",
"97|53",
"61|29",
"47|13",
"75|47",
"97|75",
"47|61",
"75|61",
"47|29",
"75|13",
"53|13",
"",
"75,47,61,53,29",
"97,61,53,29,13",
"75,29,13",
"75,97,47,61,53",
"61,13,29",
"97,13,75,29,47"]

# get input
with open("05.txt") as f:
    lines = f.readlines()

def parse_input(lines):
    A = {}
    A["rules"] = {}
    for X,Y in [line.strip().split("|") for line in lines if "|" in line]:
        if int(X) not in A["rules"]:
            A["rules"][int(X)] = []
        A["rules"][int(X)].append(int(Y))
    #print(A["rules"])
    A["updates"] = [
        [int(X) for X in line.split(",")]
        for line in lines
        if "," in line
    ]
    #print(A["updates"])
    return A

parsed_T = parse_input(T)
parsed_lines = parse_input(lines)

def get_middle(update):
    L = len(update)
    return update[L//2]

def p1(inp):
    rules = inp["rules"]
    updates = inp["updates"]
    total = 0

    def check_update(update):
        if len(update) <= 1:
            return True
        head = update[0]
        try:
            if all([later_pages in rules[head] for later_pages in update[1:]]):
                return check_update(update[1:])
        except KeyError:
            return False
        return False

    for update in updates:
        # we need the middle page number
        # print(f"{update}: {check_update(update)}")
        total += get_middle(update) if check_update(update) else 0
    return total

#print(f"Test input part 1: {p1(parsed_T)}")
#print(f"Part 1: {p1(parsed_lines)}")

def p2(inp):
    # now take only the incorrect updates and fix them
    # then get_middle
    rules = inp["rules"]
    updates = inp["updates"]
    total = 0
    ascending_order = []
    
    # Example 47 97 75 61 29 53 13
    # 97 > 75 > 47 > 61 > 53 > 29 > 13
    def sort_rules(rules):
        rules_copy = rules.copy()
        while len(rules_copy) > 0:
            #print(len(rules_copy))
            ##print(f"\t{ascending_order}")
            for key in rules:
                if key in ascending_order:
                    continue
                if len(rules_copy[key]) == 1:
                    ascending_order.append(rules_copy[key][0])
                    ascending_order.append(key)
                    #print(f"popping {key} from rules_copy 1")
                    rules_copy.pop(key)
                elif all([page in ascending_order for page in rules_copy[key]]):
                    ascending_order.append(key)
                    #print(ascending_order)
                    #print(f"popping {key} from rules_copy 2")
                    rules_copy.pop(key)
                else:
                    continue
            #print(rules_copy, ascending_order)
        return list(reversed(ascending_order))

    #descending_order = sort_rules(rules)
    #print(descending_order)

    def check_update(update):
        if len(update) <= 1:
            return True
        head = update[0]
        try:
            if all([later_pages in rules[head] for later_pages in update[1:]]):
                return check_update(update[1:])
        except KeyError:
            return False
        return False
    
    def try_fixing(update):
        update_copy = update.copy()
        L = len(update_copy)
        for i in range(L):
            if check_update(update_copy[i:]) == False:
                try:
                    if update_copy[i+1] in rules[update_copy[i]]:
                        continue
                except KeyError:
                    tmp = update_copy[i+1] 
                    update_copy[i+1] = update_copy[i]
                    update_copy[i] = tmp
                else:
                    tmp = update_copy[i+1] 
                    update_copy[i+1] = update_copy[i]
                    update_copy[i] = tmp
        if check_update(update_copy) == True:
            print(f"Fixed: {update_copy}")
        else:
            print(f"going again... {update_copy}")
            return try_fixing(update_copy)
        return update_copy

    for update in updates:
        # we need the middle page number from the fixed list
        if check_update(update) == False:
            fixed_update = try_fixing(update)
            total += get_middle(fixed_update)
    return total

print(f"Test input part 2: {p2(parsed_T)}")
#for key in parsed_lines["rules"]:
#    print(f"{key}: {len([page for page in parsed_lines['rules'][key] if page in parsed_lines['rules'].keys()])}")
#for i in [11, 12, 13, 14, 15, 18, 19, 23, 26, 28, 29, 32, 33, 34, 35, 36, 37, 38, 39, 41, 42, 43, 45, 48, 51, 53, 54, 55, 58, 59, 61, 62, 68, 69, 72, 73, 74, 76, 78, 82, 83, 85, 87, 88, 92, 96, 97, 98, 99]:
#    print(f"{i}: {len(parsed_lines['rules'][i])}")

print(f"Part 2: {p2(parsed_lines)}")
