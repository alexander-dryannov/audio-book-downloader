import tqdm
import requests
from os import mkdir, chdir
from sys import argv
from bs4 import BeautifulSoup
from urllib.parse import quote


class Downloader:
    def __init__(self, book_link):
        self.book_link = book_link
        self.book_id = None
        self.website_address = 'https://book.audio-books.club/books/'

    def response(self):
        return requests.get(self.book_link).text

    def getting_soup(self):
        return BeautifulSoup(self.response(), 'lxml')

    @staticmethod
    def change_directory(folder_name):
        try:
            mkdir(folder_name)
        except FileExistsError:
            pass
        chdir(folder_name)

    def downloader(self, file_name):
        r = requests.get(self.website_address + self.book_id + '/' + quote(file_name), stream=True)
        total_size = int(r.headers['content-length'])
        with open(file_name.strip(), 'wb') as f:
            for data in tqdm.tqdm(desc=file_name.strip(), leave=False, iterable=r.iter_content(1024), total=int(total_size/1024), unit='kB', unit_scale=True):
                f.write(data)

    def receiving_files(self):
        self.book_id = self.book_link.split('=')[-1]
        soup = self.getting_soup()
        self.change_directory(soup.find('div', class_='bookName').find('a').text.strip())
        filenames = soup.findAll('span', class_='fileName')
        for file_name in filenames:
            self.downloader(file_name.text[6:])
        print('Все файлы были успешно загружены.')


if __name__ == '__main__':
    Downloader(argv[1]).receiving_files()
