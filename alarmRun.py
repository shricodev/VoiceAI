import os
import time
import webbrowser
from random import choice
import datetime

# print("Welcome to alarm created by Piyush Acharya(r3alix01)")

if not os.path.isfile("alarm_list.txt"):
    with open("alarm_list.txt", "a") as alarms:
        alarms.write(
            "https://www.youtube.com/watch?v=W_9KR3mYkUo&list=PL9Z_KwF-qaztJlEdtO1Kiw-6UKVZbk75I\nhttps://www.youtube.com/watch?v=7BY64RjfMJI&list=PL9Z_KwF-qaztJlEdtO1Kiw-6UKVZbk75I&index=2\nhttps://www.youtube.com/watch?v=4VDqu7Oa9rs&list=PL9Z_KwF-qaztJlEdtO1Kiw-6UKVZbk75I&index=4\nhttps://www.youtube.com/watch?v=a_Tz8dOVSPI&list=PL9Z_KwF-qaztJlEdtO1Kiw-6UKVZbk75I&index=19"
        )

def alarm_input(alarm_time):
    if len(alarm_time) == 1:
        if alarm_time[0] >= 0 and alarm_time[0] < 24:
            return True
    elif len(alarm_time) == 2:
        if (
            alarm_time[0] >= 0
            and alarm_time[0] < 24
            and alarm_time[1] >= 0
            and alarm_time[1] <= 60
        ):
            return True
    elif len(alarm_time) == 3:
        if (
            alarm_time[0] >= 0
            and alarm_time[0] < 24
            and alarm_time[1] >= 0
            and alarm_time[1] <= 60
            and alarm_time[2] >= 0
            and alarm_time[2] <= 60
        ):
            return True
    return False

while True:
    print('Format: hour:minute:second or hour:minute or hour')
    userInput = input(">> ")
    try:
        a = [int(i) for i in userInput.split(":")]
        if alarm_input(a):
            break
        else:
            raise ValueError
    except ValueError:
        print("Enter the time in the given format Ex: 13:12:00")

time_sec = [3600, 60, 1]
now = datetime.datetime.now()
alarm_sec = sum([a * b for a, b in zip(time_sec[: len(a)], a)])
print(alarm_sec)
current_sec_time = sum(
    [a * b for a, b in zip(time_sec, [now.hour, now.minute, now.second])]
)
print(current_sec_time)
time_diff = alarm_sec - current_sec_time
# print(time_diff)
if time_diff < 0:
    time_diff += 86400
print("Alarm will go off in %s" % datetime.timedelta(seconds=time_diff))
time.sleep(time_diff)
print("Wake up kid..")
with open('alarm_list.txt', 'r') as _:
    vid = _.readlines()
webbrowser.open(choice(vid))


