import random
f = open("store_cut.txt", "r", encoding="utf-8")
train = open("train.txt", "w", encoding="utf-8")
test = open("test.txt", "w", encoding="utf-8")

GROUP_LIMIT = 100
counter = []
group = []
for i in range(GROUP_LIMIT):
    counter.append(0)

all_data = f.readlines()
all_uni = set(all_data)
print(len(all_data))
print(len(all_uni))
all_uni_data = []
for y in all_uni:
    all_uni_data.append(y)
random.shuffle(all_uni_data)
for row in all_uni:
    group = int(row.split(",")[0])
    counter[group] += 1
    if counter[group] % 10 < 8:
        train.write(row)
    else:
        test.write(row)

