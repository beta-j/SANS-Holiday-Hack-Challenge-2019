# Objective 6 - Splunk #
#  
## PROCEDURE: ##

>1.	What is the short host name of Professor Banas’ computer?  

Just read through the chat with `#ELFU SOC`: 
**ANS:** **`sweetums`**

#  
>2.	What is the name of the sensitive file that was likely accessed and copied by the attacker?  Please provide the fully qualified location of the file. 

-  Search for “index=main santa”
-  First entry is the following

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/81173f4f-8060-4649-8e69-e9ba4159bb0c)

**ANS:** **`C:\Users\cbanas\Documents\Naughty_and_Nice_2019_draft.txt`**
#  

>3.	What is the fully-qualified domain name(FQDN) of the command and control(C2) server? 

Search for 
``index=main sourcetype=XmlWinEventLog:Microsoft-Windows-Sysmon/Operational powershell EventCode=3`` and Look at `Destination Hostname` under `INTERESTING FIELDS`
**ANS:** **`144.202.46.214.vultr.com`**

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/2a9cf050-16a4-450c-914e-fbc5038678d3)

#  

>4.	What document is involved with launching the malicious PowerShell code? Please provide just the filename.

Search for ``index=main sourcetype="WinEventLog:Microsoft-Windows-Powershell/Operational" | reverse``

Select first entry time and search +/- 5 seconds from the event.  Then run search again for ``index=main sysmon``.  This shows two `process_id` values: `5864` and `6268`.

Convert `5864` and `6268` to hexadecimal:
-  `5864` = `0x16E8`
-  `6268` = `0x187C`
  
Search for ``index=main sourcetype=WinEventLog EventCode=4688 0x16E8``
Search for ``index=main sourcetype=WinEventLog EventCode=4688 0x187C``

This search returns a `WINDOWRD` process for ``C:\Windows\Temp\Temp1_Buttercups_HOL404_assignment (002).zip\19th Century Holiday Cheer Assignment.docm``

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/333ee447-79ce-4ac0-92ea-b6c3eca9a404)

**ANS:** **`19th Century Holiday Cheer Assignment.docm`**

#  
>5.	How many unique email addresses were used to send Holiday Cheer essays to Professor Banas? Please provide the numeric value. 

Search for 
```
index=main sourcetype=stoq | table _time results{}.workers.smtp.to results{}.workers.smtp.from  results{}.workers.smtp.subject results{}.workers.smtp.body | sort - _time "Holiday Cheer Assignment Submission"
```

Count the number of unique email addresses under ``results{}.workers.smtp.from``

**ANS:** **`21`**
#  

>6.	What was the password for the zip archive that contained the suspicious file?

Add `password` to the search term in (5) – i.e. Search for:
```
index=main sourcetype=stoq | table _time results{}.workers.smtp.to results{}.workers.smtp.from  results{}.workers.smtp.subject results{}.workers.smtp.body | sort - _time "Holiday Cheer Assignment Submission" password
```
Password is shown in plain text:
![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/80d64e3c-ba7b-42ab-9255-e1cf417b9140)

**ANS:** **`123465789`**

#  
>7.	What email address did the suspicious file come from? 

The search term in (6) also gives the answer to this question

Following the hints from Alice Bluebird we finally get to  the following search term:
```
index=main sourcetype=stoq  "results{}.workers.smtp.from"="bradly buttercups <bradly.buttercups@eifu.org>" | eval results = spath(_raw, "results{}") | mvexpand results | eval path=spath(results, "archivers.filedir.path"), filename=spath(results, "payload_meta.extra_data.filename"), fullpath=path."/".filename
| search fullpath!="" | table filename,fullpath
```

Follow the archive path for `19th Century Holiday Cheer Assignment.docm` – i.e. `/home/ubuntu/archive/c/6/e/1/7/c6e175f5b8048c771b3a3fac5f3295d2032524af/19th Century Holiday Cheer Assignment.docm`

Opening the downloaded file with a text editor gives us a message pointing us towards `core.xml` instead.  So, follow the archive path for `core.xml`- i.e. `/home/ubuntu/archive/f/f/1/e/a/ff1ea6f13be3faabd0da728f514deb7fe3577cc4/core.xml` and open the file with a text editor to reveal the following message:

![image](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2019/assets/60655500/662ca7d0-1dcb-4e0d-90a1-31df50493cd2)

**ANS:** **`bradly.buttercups@eifu.org`**
#  


