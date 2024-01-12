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

#  
#  
#  
## Challenge 2 - Escape Ed ##

### PROCEDURE: ###

Well this was an easy one – a quick google search to learn some “ed” commands and type `Q` into the terminal – that’s it!

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/d6fc87d7-c149-4708-9154-8f890053176e)

#  
#  
#  
## Challenge 3 - Nyanshell ##

### PROCEDURE: ###

Running `sudo –l` we see that we are only allowed to run `chattr` as root.  A quick Google search shows that this tool is used to change file attributes.

Looking at the `/etc/passwd` file we see that user `alabaster_snowball` is booting with the shell `/bin/nsh` which probably explains the Nyan Cat popping up on logon.  Running  `lsattr –aR` in `/bin` shows us that there is only one immutable file in the directory and unsurprisingly it’s `/nsh`.

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/78ba7fad-170d-40fe-a93b-f07c3a40ba9d)
 
`Chattr` comes in handy now – we run `sudo chattr –i /bin/nsh` to remove the immutable attribute from `nsh`.

We cannot delete `nsh`, but we can edit it.  So the solution is now quite simple:
```
vi /bin/nsh
```

Replace the contents with:
```
#!/bin/bash
/bin/bash
```

I can now log in as `alabaster_snowball`...

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/29c2acc0-911c-4ddd-9d5d-ee80c230f2b6)

...and we're in! 😄
