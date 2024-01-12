# CHALLENGES #

#  

## Challenge 1 - Mongo Pilfer Challenge ##

### PROCEDURE: ###

When logging in to the terminal, the prompt tells us that the system is running MongoDB.  Trying to run `mongo` fails and returns a hint:

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/013a923f-2be3-49fc-b253-e55559795165)

So running `ps –edaf` returns:
```
ID        PID  PPID  C STIME TTY          TIME CMD
elf          1     0  0 15:40 pts/0    00:00:00 /bin/bash
mongo        9     1  0 15:40 ?        00:00:02 /usr/bin/mongod --quiet --fork --port 12121 --bind
elf         84     1  0 15:45 pts/0    00:00:00 ps -edaf
```

So I just run mongo again with a `–port` switch:
```
mongo –port 12121
```

Now that we’re in Mongo we can look around and we get a super helpful hint: **``{"_id" : "You did good! Just run the command between the stars: ** db.loadServerScripts();displaySolution(); **" }``**

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/59886f27-b095-4957-aa7e-d5e36e7560b2)

Happy to oblige:
```
db.loadServerScripts();displaySolution();
```
![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/f3d84589-e83e-4f7b-aa86-d1eea1ce8695)

