from collections import deque 
#Think of neater way to do this. Deep copy?
seat1, seat2,seat3,seat4 = deque(maxlen=2),deque(maxlen=2),deque(maxlen=2),deque(maxlen=2)
seat1.extend([0,0])
seat2.extend([0,0])
seat3.extend([0,0])
seat4.extend([0,0])
seat= [seat1,seat2,seat3,seat4]
print(seat)

occupancy = [1,0,0,1]
for index, i in enumerate(occupancy):
    seat[index].append(i)
    print(index,seat[index],i)
