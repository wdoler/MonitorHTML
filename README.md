# MonitorHTML
This python script will go through a list of websites, find a HTML xpath tag, get all of the text inside of that tag, and return that data and the date for when the program found it. If there are changes, then it will email a user the changes aswell as a list of everything it has found.

  Input: two json files
      1) list of websites to monitor (monitorWebsites.json)
      * the script will fill out the "found" section
      2) Email address and password (passwords.json)

  Todo: change to OOP

Format for monitorWebsites.json :

{
    "Websites": {
        "uniqueID_0": {
            "XpathSearch": "//a[@class=\"posting-title\"]/h5/text()",
            "found": {
            },
            "regexFilter": "(?i)(filter|what|isFound)",
            "url": "https://www.xyz.com/"
        },
        "uniqueID_2": {
            "XpathSearch": "//span[@class=\"Title\"]/a/text()",
            "found": {
            },
            "regexFilter": "(?i)(filter|what|isFound)",
            "url": "https://www.xyz2.com/"
        }
    }
}

Format for passwords.json :

{
    "gmail_user": "xyz@gmail.com",
    "gmail_password": "reallyBadPractice",
    "to": ["xyz@gmail.com"]
}
