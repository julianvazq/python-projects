import requests
import bs4
import smtplib
from email.mime.text import MIMEText

def examine_web_crawler():
    res = requests.get('http://examine.com')
    res.raise_for_status()
    exam = bs4.BeautifulSoup(res.text, 'html.parser')

    dict = {}

    # Finds the "Latests News" section
    faq = exam.find('div', id="faq_newest")

    # Stores in dictionary: titles as keys, links as values
    for elem in faq.find_all("li"):
        link = elem.a['href']
        title = elem.a.text
        dict[title] = "http://examine.com" + link

    content = ''
    # Loops through the dictionary, accesses each site, stores tittle + summary + link in string
    for key in dict:
        content = content + "\n" + "* " + key + "\n"
        req = requests.get(dict[key])
        req.raise_for_status()
        soup = bs4.BeautifulSoup(req.text, 'html.parser')
        summary = soup.find('div', class_='full-text')
        content = content + summary.text + '\n' + dict[key] + '\n'

    return content


def email_me():
    content = examine_web_crawler()

    fromx = 'name@gmail.com'
    to = 'name@gmail.com'
    msg = MIMEText(content)
    msg['Subject'] = 'EXAMINE Weekly Summary'
    msg['From'] = fromx
    msg['To'] = to

    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login('name@gmail.com', 'password')
    mail.sendmail(fromx, to, msg.as_string())
    mail.quit()

email_me()
