# Objective 7 – Get Access to the Steam Tunnels #

## PROCEDURE : ##

When walking into the dorm, we see a weird guy running away from us.  Following him into the next room we see that he’s disappeared into another room that needs a key.

Running through the above sequence again I noticed that the guy has a key on his belt and the room is conveniently equipped with a key-cutting machine.  If only we could get a closer look at that key!

Bringing up the **Web Developer** -> **Networks** tab in Firefox we see a number of GET requests for .png files, including [`Krampus.png`](assets/krampus.png), which leads us to `https://2019.kringlecon.com/images/avatars/elves/krampus.png`  which is a conveniently [high-res image of Krampus and his key](assets/krampus.png).

Zooming in on the key (and drawing some straight lines in MS paint) and assuming that the deeper the cut, the higher the number on the cutting machine, we get to the following combination: **`122520`** which, when entered into the key cutter, produces a replica key

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/e9305913-4b30-4617-b2ae-ecf07f51c137)

The replica key could then be used in the next room to gain access to the steam tunnels.
