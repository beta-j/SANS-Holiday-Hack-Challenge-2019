# Objective 3 – Windows Log Analysis: Evaluate Attack Outcome #

#  
## PROCEDURE : ##

We start off by opening the `Security.evtx` file.  Looking through its contents one immediately notices multiple failed login attempts.  Furthermore the attempts have usernames advancing in alphabetical order – the hallmark of an automated attack.

Filtering by `Event ID 4624` brings up the successful logons.  There are some domain controller logins, but we quickly get to a successful login by user: **`supatree`**.
