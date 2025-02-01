
i = 0
players_names = []
count = ["First","Second","Third","Forth","Fifth","Sixth"]


players = int(input("How Many Player are gonna play scrow ? Max Is 6 \n"))


for x in count:
    while i < players:
        name = input(f"{x} Player Name is : ")
        players_names.append(name)
        i += 1
        break
i = 0

print(players_names)


players_scores1 = [] # Lens depends on the number of player
players_scores2 = [] # Lens depends on the number of player
players_scores3 = [] # Lens depends on the number of player
players_scores4 = [] # Lens depends on the number of player
players_scores5 = [] # Lens depends on the number of player


print ("First Round Scores =======================================")
for f in players_names:
    while i < players:
        score = int(input(f"What is {f} Score in this round ? \n"))
        players_scores1.append(score)
        i += 1
        break
print(players_scores1)

i = 0
print ("Second Round Scores =======================================")
for g in players_names:
    while i < players:
        score = int(input(f"What is {g} Score in this round ? \n"))
        players_scores2.append(score)
        i += 1
        break
print(players_scores2)

i = 0
print ("Third Round Scores =======================================")
for h in players_names:
    while i < players:
        score = int(input(f"What is {h} Score in this round ? \n"))
        players_scores3.append(score)
        i += 1
        break
print(players_scores3)

i = 0
print ("Forth Round Scores =======================================")
for j in players_names:
    while i < players:
        score = int(input(f"What is {j} Score in this round ? \n"))
        players_scores4.append(score)
        i += 1
        break
print(players_scores4)

i = 0
print ("Fifth Round Scores =======================================")
for a in players_names:
    while i < players:
        score = int(input(f"What is {a} Score in this round ? \n"))
        players_scores5.append(score)
        i += 1
        break
print(players_scores5)

if players == 5:
    players_scores_total = [
        players_scores1[0]+players_scores2[0]+players_scores3[0]+players_scores4[0]+players_scores5[0],
        players_scores1[1]+players_scores2[1]+players_scores3[1]+players_scores4[1]+players_scores5[1],
        players_scores1[2]+players_scores2[2]+players_scores3[2]+players_scores4[2]+players_scores5[2],
        players_scores1[3]+players_scores2[3]+players_scores3[3]+players_scores4[3]+players_scores5[3],
        players_scores1[4]+players_scores2[4]+players_scores3[4]+players_scores4[4]+players_scores5[4] 
    ]


elif players == 6:
    players_scores_total = [
        players_scores1[0]+players_scores2[0]+players_scores3[0]+players_scores4[0]+players_scores5[0],
        players_scores1[1]+players_scores2[1]+players_scores3[1]+players_scores4[1]+players_scores5[1],
        players_scores1[2]+players_scores2[2]+players_scores3[2]+players_scores4[2]+players_scores5[2],
        players_scores1[3]+players_scores2[3]+players_scores3[3]+players_scores4[3]+players_scores5[3],
        players_scores1[4]+players_scores2[4]+players_scores3[4]+players_scores4[4]+players_scores5[4],
        players_scores1[5]+players_scores2[5]+players_scores3[5]+players_scores4[5]+players_scores5[5]
    ]

elif players == 4:
    players_scores_total = [
        players_scores1[0]+players_scores2[0]+players_scores3[0]+players_scores4[0]+players_scores5[0],
        players_scores1[1]+players_scores2[1]+players_scores3[1]+players_scores4[1]+players_scores5[1],
        players_scores1[2]+players_scores2[2]+players_scores3[2]+players_scores4[2]+players_scores5[2],
        players_scores1[3]+players_scores2[3]+players_scores3[3]+players_scores4[3]+players_scores5[3]
    ]


elif players == 3:
    players_scores_total = [
        players_scores1[0]+players_scores2[0]+players_scores3[0]+players_scores4[0]+players_scores5[0],
        players_scores1[1]+players_scores2[1]+players_scores3[1]+players_scores4[1]+players_scores5[1],
        players_scores1[2]+players_scores2[2]+players_scores3[2]+players_scores4[2]+players_scores5[2]
    ]
if players == 4:
    print (f"{players_names[0]} Score Is",players_scores_total[0])
    print (f"{players_names[1]} Score Is",players_scores_total[1])
    print (f"{players_names[2]} Score Is",players_scores_total[2])
    print (f"{players_names[3]} Score Is",players_scores_total[3])

    print ("===============================================")

elif players == 3:
    print (f"{players_names[0]} Score Is",players_scores_total[0])
    print (f"{players_names[1]} Score Is",players_scores_total[1])
    print (f"{players_names[2]} Score Is",players_scores_total[2])

    print ("===============================================")

elif players == 5:
    print (f"{players_names[0]} Score Is",players_scores_total[0])
    print (f"{players_names[1]} Score Is",players_scores_total[1])
    print (f"{players_names[2]} Score Is",players_scores_total[2])
    print (f"{players_names[3]} Score Is",players_scores_total[3])
    print (f"{players_names[4]} Score Is",players_scores_total[4])

    print ("===============================================")

elif players == 6:
    print (f"{players_names[0]} Score Is",players_scores_total[0])
    print (f"{players_names[1]} Score Is",players_scores_total[1])
    print (f"{players_names[2]} Score Is",players_scores_total[2])
    print (f"{players_names[3]} Score Is",players_scores_total[3])
    print (f"{players_names[4]} Score Is",players_scores_total[4])
    print (f"{players_names[5]} Score Is",players_scores_total[5])

    print ("===============================================")


max_index = players_scores_total.index(max(players_scores_total))
min_index = players_scores_total.index(min(players_scores_total))


print(f"{players_names[max_index]} is The KINGGGGGGGGG")
print(f"{players_names[min_index]} is The KOOOOOOOOOOZ")
