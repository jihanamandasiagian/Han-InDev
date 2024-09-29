# import library yang dibutuhkan
import requests
from bs4 import BeautifulSoup
import pandas as pd

# variabel penampung semua html
haruka=[]

max_page = int(input('Mau mengambil sampai halaman: '))
# proses scraping website dari page 1 sampai sesuai input user yang kemudian disimpan pada variabel 'haruka'
for link in range(1,max_page+1):
    print('Web yang sedang discraping')
    url = 'https://anoboy.foundation/category/action/page/' + str(link)
    print(url)
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'html.parser')
    haruka.append(soup)

print('Banyak page yang disraping adalah:', len(haruka))

# variabel penampung data jadwal up anime
jadwal_tayang=[]
for i in haruka:
    # mencari data yang relevan dari elemen yang berada pada class amv
    lis = i.find_all('div', {'class': 'amv'})
    for j in lis:
        items = j.find_all('div', {'class': 'jamup'})
        for item in items:
            jamup = item.text.strip()
            jadwal_tayang.append(jamup[3:])

print('Data telah disimpan pada list dengan jumlah data: ',len(jadwal_tayang))
jadwal_tayang[0]

# variabel penampung link dari tag a href
link_animes=[]

for i in haruka:
    # mencari data link dari elemen yang berada pada tag a href
    lis = i.find_all('div', {'class': 'container'})
    for j in lis:
        items = j.find_all('a',{'rel':'bookmark'})
        for k in items:            
            an = (k['href'])
            link_animes.append(an)
            
print(f'Terdapat {len(link_animes)} link anime, berikut contohnya:', link_animes[0])

# variabel penampung page html setiap anime (bukan katalog tapi per anime)
harukaperanime=[]

# proses scraping website dari setiap link anime yang sudah didapatkan sebelumnya
for link in link_animes:
    res = requests.get(link)
    soup = BeautifulSoup(res.text,'html.parser')
    harukaperanime.append(soup)

print('Banyak page yang sedang discraping adalah:', len(harukaperanime))

animes_info=[]
for i in harukaperanime:
    # mencari data yang relevan dari elemen yang berada pada tabel tbody
    lis = i.find_all('tbody')
    for j in lis:
        items = j.find_all('td')
        for item in items:
            # Cetak teks dari elemen item
            animes_info.append(item.text.strip())

print('Data anime disimpan pada list dengan jumlah data: ',len(animes_info[::7]))
animes_info[0]

nama    = [ animes_info[i] for i in range(0,len(animes_info),7)]
jumlah  = [animes_info[i] for i in range(1,len(animes_info),7)]
studio  = [animes_info[i] for i in range(2,len(animes_info),7)]
sourch  = [animes_info[i] for i in range(3,len(animes_info),7)]
durasi  = [animes_info[i] for i in range(4,len(animes_info),7)]
genre   = [ animes_info[i] for i in range(5,len(animes_info),7)]
rating  = [animes_info[i] for i in range(6,len(animes_info),7)]

print('Semua data telah dikategorikan')

df= pd.DataFrame()

df['Judul anime'] = nama
df['Jumlah anime'] = jumlah
df['Jadwal tayang'] = jadwal_tayang
df['Studio'] = studio
df['Genre'] = genre
df['Durasi per Eps'] = durasi
df['Sourch'] = genre
df['Rating'] = rating
df['Link anime'] = link_animes

df.head()

df.to_csv('anoBoy_action.csv')
print('Data telah disimpan')
