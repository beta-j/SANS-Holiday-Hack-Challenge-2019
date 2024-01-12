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

#  
#  
#  
## Challenge 4 -	Frosty Keypad: ##

### PROCEDURE: ###
Looking at the keypad, we can tell that the key-code is composed of the digits `1`, `3` and `7`.  Seeing as we also know that only one of the digits is repeated once, the key-code must be 4 digits long. So we have the following parameters:

-  Prime number between 1137 and 7731
-  Using only the digits 7,3 and 1
-  With only one repeated digit

To solve the above, I wrote a [pythion script to calculate the possible keypad combinations](code/keypad_crack.py).

Running this script we only get 5 possible valid combinations which are easy enough to try on the keypad:

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/a8c35a42-95f8-407f-8cc4-d4d4544a3a43)

#  
#  
#  
## Challenge 5 -	Graylog: ##

### PROCEDURE: ###
>**Question 1** - Minty CandyCane reported some weird activity on his computer after he clicked on a link in Firefox for a cookie recipe and downloaded a file.  What is the full-path + filename of the first malicious file downloaded by Minty?

Search for ``TargetFilename:/.cookie.+/`` to find all file names with `cookie` in them.

**Answer: `C:\Users\minty\Downloads\cookie_recipe.exe`**
#  

>**Question 2** - The malicious file downloaded and executed by Minty gave the attacker remote access to his machine. What was the ip:port the malicious file connected to first?

Search for ``ProcessImage:/.+cookie_recipe.exe/ AND EventID:3`` to find Network Events related to `cookie_recipe.exe`.  This returns a single log entry:

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/c05ccfbe-8188-417d-afc3-62699480d588)

**Answer: `192.168.247.175:4444`**
#  

>**Question 3** - What was the first command executed by the attacker?

Search for `ParentProcessImage:/.+cookie_recipe.exe/` to find processes initiated by `cookie_recipe.exe`. 	Looking at the first logs we find this one:

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/694573c6-03c2-4035-b322-e485cf76fb7f)

**Answer: `whoami`**

#  

>**Question 4** - What is the one-word service name the attacker used to escalate privileges?

Looking through the results from **Question 3** we see that the user runs the service `webexservice`.

**Answer: `webexservice`**

#  

>**Question 5** - What is the file-path + filename of the binary ran by the attacker to dump credentials?

Searching for ``ParentProcessImage:/.+cookie_recipe.+/`` and tracking the User over time we see that all of a sudden the user stops being `minty` right after running the `webexservice`.

We see that the user then runs `mimikatz` with the switch `-Outfile C:\cookie.exe`

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/e4759883-75d9-4844-8039-6ab589a1f425)

**Answer: `C:\cookie.exe`**

#  

>**Question 6** - The attacker pivoted to another workstation using credentials gained from Minty's computer. Which account name was used to pivot to another machine?

Search for connections from the attackers IP address; `192.168.247.175`AND searching for successful logon events: `EventID 4624`.
```
SourceNetworkAddress:192.168.247.175 AND EventID:4624
```
![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/0b1dbdae-4371-477c-950a-55c7f536453c)

**Answer: `alabaster`**

#  

>**Question 7:** What is the time ( `HH:MM:SS` ) the attacker makes a Remote Desktop connection to another machine?

Search for connections from the attackers IP address; `192.168.247.175` AND for successful RDP connection: `LogonType:10`
```
SourceNetworkAddress:192.168.247.175 AND LogonType:10
```

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/e89dbf92-9342-4c0e-933a-a02dd3d9bd42)

**Answer: `06:04:28`**

#  

>**Question 8** - The attacker navigates the file system of a third host using their Remote Desktop Connection to the second host. What is the SourceHostName,DestinationHostname,LogonType of this connection?

Search for succesful logon originating from `ELFU-RES-WKS2`: ``SourceHostName:"ELFU-RES-WKS2" AND EventID:4624``

**Answer: `elfu-res-wks2,elfu-res-wks3,3`**

#  

>**Question 9** - What is the full-path + filename of the secret research document after being transferred from the third host to the second host?

Search for `source:"elfu-res-wks2" AND EventID:2`

Look through the entries for something that is not system generated and that happened after `06:04:28`.	After just a couple of entries we come across this log:

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/c9a11ace-c4cd-4389-b6d1-04693145b276)

**Answer:  `C:\Users\alabaster\Desktop\super_secret_elfu_research.pdf`**

#  

>**Question 10** - What is the IPv4 address (as found in logs) the secret research document was exfiltrated to?

Run a search for ``super_secret_elfu_research.pdf``.  The most recent entry shows a powershell `Invoke-Webrequest` to `https://pastebin.com/post.php`.

Searching for logs in the surrounding 5 seconds, we find this log:

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/bf28b687-c239-40b8-8886-25fdafb0fb41)

**Answer:  `104.22.3.84`**

#  
That’s it – task completed!

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/aeb77791-09bb-49ef-802d-bb57952f0a62)


#  
#  
#  
## Challenge 6 -	IOT Braces: ##

### PROCEDURE: ###
Reading the contents of `/home/elfuuser/IOTteethBraces.md` we have a list of steps to follow:

>1.	Set the default policies to DROP for the INPUT, FORWARD, and OUTPUT chains.
```
> sudo iptables –P INPUT DROP
> sudo iptables –P FORWARD DROP
> sudo iptables –P OUTPUT DROP
```

>2.	Create a rule to ACCEPT all connections that are ESTABLISHED,RELATED on the INPUT and the OUTPUT chains.
```
> sudo iptables –A INPUT –m state –state ESTABLISHED,RELATED –j ACCEPT
> sudo iptables –A OUTPUT –m state –state ESTABLISHED,RELATED –j ACCEPT
```

>3.	Create a rule to ACCEPT only remote source IP address 172.19.0.225 to access the local SSH server (on port 22).
```
> sudo iptables –A INPUT –p tcp –s 172.19.0.225 –dport 22 –j ACCEPT
> sudo iptables –A OUTPUT –p tcp –s 172.19.0.225 –dport 22 –j ACCEPT
```

>4.	Create a rule to ACCEPT any source IP to the local TCP services on ports 21 and 80.
```
> sudo iptables –A INPUT –p tcp –m multiport –dports 21,80 –j ACCEPT
> sudo iptables –A OUTPUT –p tcp –m multiport –dports 21,80 –j ACCEPT
```

>5.	Create a rule to ACCEPT all OUTPUT traffic with a destination TCP port of 80.
```
> sudo iptables –A OUTPUT –p tcp –dport 80 –j ACCEPT
```

>6.	Create a rule applied to the INPUT chain to ACCEPT all traffic from the lo interface.
```
> sudo iptables –A INPUT –I lo –j ACCEPT
```
![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/2051368e-ab57-4a2a-9192-45c763a55494)


#  
#  
#  
## Challenge 7 -	Linux Path: ##

### PROCEDURE: ###

I quickly notice that someone has messed with `PATH`:

Running `ls` doesn’t work, but on the other hand `Echo $PATH` gives us: `/usr/local/bin/ls`.

There is something wrong with this – commands such as `ls` should be run in `/bin`

So I simply try running `/bin/ls` and IT WORKS!
 
![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/9ea51226-deba-46fc-8107-c03cfd612c19)


#  
#  
#  
## Challenge 8 -	Xms Cheer Laser: ##

### PROCEDURE: ###
This one was particularly challenging for me as it uses Windows Powershell commands.  I have absolutely no experience with Powershell so I had to do tons of Googling for every command I wanted to run.
```
> Get-Content /home/callingcard.txt
```

This gives a hint to check command history, so…
```
> Get-History
```

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/cca851e6-0aed-4408-9e72-d1333a890092)

It is also worth noting the entry: **`angle?val=65.5`**   - is this the angle to use?

Running ``Get-History | Format-List –Property *`` makes the output more readable.

This is particularly interesting:

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/077c261b-d62d-4853-bb79-c59c9e929a81)

Let’s have a look at the environment variables:
```
> Get-ChildItem Env: | Format-List
```

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/f038f4be-2856-40d9-9d88-2a5b53dfb652)

Looks like we’re looking for a compressed file somewhere…let’s follow the instructions:
```
> Get-ChildItem –R | LastWriteTime
```

And here is the latest entry:

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/70ed57ed-d39a-4e38-b0e4-ca51084fef4d)

Now to uncompress the archive:
```
> Expand-Archive –Path /etc/apt/archive –DestinationPath /tmp
```

We now have a folder containing two files:  `riddle` and `runme.elf`

Setting permissions for `runme.elf` and executing it, we get the following value for refraction: **`1.867`**

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/fd18a329-7502-468a-a537-7c4ed85e06d3)

Let’s have a look at the riddle file now:

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/3a2f1008-3867-4586-a11f-b7af61a5d77c)

It sounds like we need to recursively list the files in the home directory along with their MD5 hashes and compare those to the hash ``25520151A320B5B0D21561F92C8F6224``.

To do this we run: 
```
> Get-ChildItem –R –File | Foreach {Get-FileHash –Algorithm MD5 $_.fullname} | where-Object {$_.Hash –eq ‘25520151A320B5B0D21561F92C8F6224’’} | Format-List
```
![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/8edc3ac1-b73a-4a58-80b7-99a5f339623e)

So let’s have a look at `thhy5hll.txt`. We have a temperature value = **`-33.5`** and another hint:

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/9342af8d-1fa6-4cb1-b29d-b16a09efb164)

So we sort the files in `/home/elf/depths` according to their FullName size:
```
> Get-ChildItem –R –File | Select-Object FullName, @{Name=”length”;Expression={$_.FullName.Length}} | Sort-Object length | select –last 1 | Format-List
```
![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/66cbc822-e188-424d-916c-32320ecda822)

Let’s have a look inside this text file:
![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/07e34a6e-0209-4df1-a9a2-83f4b9226e35)

So let’s follow the instructions:
```
> Get-Process –IncludeUserName
> Stop-Process 24
> Stop-Process 25
> Stop-Process 27
> Stop-Process 29
```
![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/6577b7a6-78f7-420b-b19e-a2178cc4d5af)

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/20460bec-b88d-4870-9dc0-5c38bc79e5d3)

There’s a reference to `/shall/see`  - `/shall` is a root directory so…
```
> Get-Content /shall/see
```
![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/49d8dfae-b5a5-4673-afe6-c652daef3641)

Ok let’s run a recursive search for an xml file in `/etc/`:
```
> Get-ChildItem –R /etc –include *.xml
```
![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/f7c4240f-76f9-47e7-b5b5-ae8eeedd3834)

There’s the event log

We now need to sort and count the event IDs:
```
> Get-Content EventLog.xml | Select-String –Pattern ‘<I32 N=”id”’ | Group-Object | Select-Object –Property Count, Name | Sort-Object –Property Count -Descending
```
![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/cfcac1f0-6c67-496e-9490-c3f0812089ef)

There is only a single instance for event id `1` – so we need to output the lines next to this event entry to find its properties.
I used this command: 
```
 > Get-Content ./EventLog.xml | Select-String -Pattern '<I32 N="id">1' -Context 20,200
```

Reading through the output we find: 
![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/873a76a4-a536-4b88-b2f0-e9ff2e186c81)

Those look like the gas mixtures we need!!

**`O = 6 H = 7 He = 3 N = 4 Ne = 22 Ar = 11 Xe = 10 F = 20 Kr = 8 Rn =9`**

Now we’re ready to input the values – let’s look at the instructions for the laser again:
```
> Invoke-WebRequest –Uri http://localhost:12225/).RawContent
```

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/73c37a46-9c04-429e-b15b-269a65f9db10)

```
PS /home/elf> (Invoke-WebRequest -Uri http://localhost:1225/api/off).RawContent
PS /home/elf> (Invoke-WebRequest -Uri http://localhost:1225/api/refraction?val=1.867).RawContent
PS /home/elf> (Invoke-WebRequest -Uri http://localhost:1225/api/temperature?val=-33.5).RawContent
PS /home/elf> (Invoke-WebRequest -Uri http://localhost:1225/api/angle?val=65.5).RawContent
PS /home/elf> $gasses = @{O=6;H=7;He=3;N=4;Ne=22;Ar=11;Xe=10;F=20;Kr=8;Rn=9;}
PS /home/elf> (Invoke-WebRequest -Uri http://localhost:1225/api/gas -Method POST -Body $gasses).RawContent
PS /home/elf> (Invoke-WebRequest -Uri http://localhost:1225/api/on).RawContent
PS /home/elf> (Invoke-WebRequest -Uri http://localhost:1225/api/output).RawContent
```

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/3b610d00-044e-4755-b2e1-e6305c2439de)

FINALLY!  - That was a tough one!



