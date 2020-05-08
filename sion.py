import click
import json
import os.path
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from tabulate import tabulate
from datetime import datetime


def decode_login():
    with open("login_info.json") as j:
        data = json.load(j)
        username = data['username']
        password = data['password']
    return username, password


def login():
    opt = Options()
    opt.headless = True
    browser = webdriver.Firefox(options=opt)
    browser.get('http://sion.stikom-bali.ac.id/')
    u = browser.find_element_by_id('usern')
    p = browser.find_element_by_id('passw')
    # isi data
    u.send_keys(decode_login()[0])
    p.send_keys(decode_login()[1])
    # submit
    browser.find_element_by_id('wp-submit').click()
    # close notifikasi
    browser.find_element_by_css_selector(
        'button.ajs-button:nth-child(1)').click()

    # save dashboard html
    with open("tmp/dashboard.html", 'w') as w:
        html = browser.execute_script("return document.body.outerHTML;")
        w.write(html)

    # save hasil ujian html
    time.sleep(2)
    with open("tmp/hasil_ujian.html", "w") as w:
        browser.get(
            'http://sion.stikom-bali.ac.id/reg/perkuliahandet.php?optsrc=h_ujian&find=Lihat&user='+decode_login()[0])
        html = browser.execute_script("return document.body.outerHTML;")
        w.write(html)

    # save krs html
    time.sleep(2)
    with open("tmp/krs.html", "w") as w:
        browser.get(
            'http://sion.stikom-bali.ac.id/reg/perkuliahandet.php?optsrc=krs&find=Lihat&user='+decode_login()[0])
        html = browser.execute_script("return document.body.outerHTML;")
        w.write(html)

    # save jadwal kuliah
    time.sleep(2)
    with open("tmp/jadwal_kuliah.html", "w") as w:
        browser.get(
            'http://sion.stikom-bali.ac.id/reg/perkuliahandet.php?optsrc=jd&find=Lihat&user='+decode_login()[0])
        html = browser.execute_script("return document.body.outerHTML;")
        w.write(html)

    # save jadwal uts
    time.sleep(2)
    with open("tmp/jadwal_uts.html", "w") as w:
        browser.get(
            'http://sion.stikom-bali.ac.id/reg/perkuliahandet.php?optsrc=jduts1&find=Lihat&user='+decode_login()[0])
        html = browser.execute_script("return document.body.outerHTML;")
        w.write(html)

    # save jadwal uas
    time.sleep(2)
    with open("tmp/jadwal_uas.html", "w") as w:
        browser.get(
            'http://sion.stikom-bali.ac.id/reg/perkuliahandet.php?optsrc=jduas&find=Lihat&user='+decode_login()[0])
        html = browser.execute_script("return document.body.outerHTML;")
        w.write(html)

    # save sisa matkul
    time.sleep(2)
    with open("tmp/sisa.html", "w") as w:
        browser.get(
            'http://sion.stikom-bali.ac.id/reg/perkuliahandet.php?optsrc=sisa&find=Lihat&user='+decode_login()[0])
        html = browser.execute_script("return document.body.outerHTML;")
        w.write(html)

    browser.quit()


def parseInfo():
    if os.path.exists("tmp/dashboard.html"):
        html = open("tmp/dashboard.html")
        soup = BeautifulSoup(html, 'lxml')
        tabel = soup.find("table")

        data = []
        rows = tabel.findAll('tr')
        for row in rows:
            cols = row.findAll('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        for x in data:
            print(' '.join(x))
    else:
        login()
        parseInfo()


def parseHasil():
    if os.path.exists("tmp/hasil_ujian.html"):
        html = open("tmp/hasil_ujian.html")
        soup = BeautifulSoup(html, 'lxml')
        tabel = soup.find('table')

        data = []
        rows = tabel.findAll('tr')
        for row in rows:
            cols = row.findAll('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        print(tabulate(data, headers=[
            "Kode", "Matkul", "Semester", "Sks", "Uts", "Uas", "Tugas", "Kuis", "Total", "Grade"]))
    else:
        login()
        parseHasil()


def parseKrs():
    if os.path.exists("tmp/krs.html"):
        html = open("tmp/krs.html")
        soup = BeautifulSoup(html, 'lxml')
        tabel = soup.find("table")

        data = []
        header = [th.text.strip() for th in tabel.findAll("th")]
        rows = tabel.findAll('tr')
        for row in rows:
            cols = row.findAll('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        print(tabulate(data, header))
    else:
        login()
        parseKrs()


def parseJadwal():
    if os.path.exists("tmp/jadwal_kuliah.html"):
        html = open("tmp/jadwal_kuliah.html")
        soup = BeautifulSoup(html, 'lxml')
        tabel = soup.find("table")

        data = []
        header = [th.text.strip() for th in tabel.findAll("th")]
        rows = tabel.findAll('tr')
        for row in rows:
            cols = row.findAll('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        print(tabulate(data, header))
    else:
        login()
        parseJadwal()


def parseUts():
    if os.path.exists("tmp/jadwal_uts.html"):
        html = open("tmp/jadwal_uts.html")
        soup = BeautifulSoup(html, 'lxml')
        tabel = soup.find("table")

        if tabel == None:
            print('Data kosong')
        else:
            data = []
            header = [th.text.strip() for th in tabel.findAll("th")]
            rows = tabel.findAll('tr')
            for row in rows:
                cols = row.findAll('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele])
            print(tabulate(data, header))
    else:
        login()
        parseUts()


def parseUas():
    if os.path.exists("tmp/jadwal_uas.html"):
        html = open("tmp/jadwal_uas.html")
        soup = BeautifulSoup(html, 'lxml')
        tabel = soup.find("table")

        if tabel == None:
            print('Data kosong')
        else:
            data = []
            header = [th.text.strip() for th in tabel.findAll("th")]
            rows = tabel.findAll('tr')
            for row in rows:
                cols = row.findAll('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele])
            print(tabulate(data, header))
    else:
        login()
        parseUas()


def parseSisa():
    if os.path.exists("tmp/sisa.html"):
        html = open("tmp/sisa.html")
        soup = BeautifulSoup(html, 'lxml')
        tabel = soup.find("table")

        if tabel == None:
            print('Data kosong')
        else:
            data = []
            header = [th.text.strip() for th in tabel.findAll("th")]
            rows = tabel.findAll('tr')
            for row in rows:
                cols = row.findAll('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele])
            print(tabulate(data, header))
    else:
        login()
        parseUas()


@click.command()
@click.option("--update", is_flag=True, help="update data sion")
@click.option("--info", is_flag=True, help="get info mahasiswa")
@click.option("--hasil-ujian", is_flag=True, help="get hasil ujian mahasiswa")
@click.option("--krs", is_flag=True, help="get data kartu rencana studi")
@click.option("--jadwal-kuliah", is_flag=True, help="get data jadwal kuliah")
@click.option("--jadwal-uts", is_flag=True, help="get data jadwal uts")
@click.option("--jadwal-uas", is_flag=True, help="get data jadwal uas")
@click.option("--sisa", is_flag=True, help="get data sisa mata kuliah")
def main(update, info, hasil_ujian, krs, jadwal_kuliah, jadwal_uts, jadwal_uas, sisa):
    """ Tools for get data from sion.stikom-bali.ac.id """
    if info:
        parseInfo()
    elif hasil_ujian:
        parseHasil()
    elif update:
        login()
        today = datetime.today()
        print("data updated at", today)
    elif krs:
        parseKrs()
    elif jadwal_kuliah:
        parseJadwal()
    elif jadwal_uts:
        parseUts()
    elif jadwal_uas:
        parseUas()
    elif sisa:
        parseSisa()
    else:
        print("type :\n sion.py --help for help usage")

# def main():
#     parseInfo()


if __name__ == "__main__":
    main()
