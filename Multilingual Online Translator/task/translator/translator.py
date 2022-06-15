import requests
from bs4 import BeautifulSoup
import sys


class Translator:
    lanlist = ["Arabic", "German", "English", "Spanish", "French", "Hebrew", "Japanese", "Dutch", "Polish",
               "Portuguese", "Romanian", "Russian", "Turkish"]

    def __init__(self):
        self.all = False
        self.lanlist = Translator.lanlist
        self.langfrom = None
        self.langto = None
        self.request = None
        self.url = None
        self.word = None
        self.alltrans = None
        self.words = []
        self.sentences = []
        self.greeting_input()

    def get_url(self):
        self.url = "https://context.reverso.net/translation/" + self.langfrom.lower() + "-" + self.langto.lower() + "/" + self.word

    def greeting_input(self):
        self.langfrom = sys.argv[1].capitalize()
        self.langto = sys.argv[2].capitalize()
        self.word = sys.argv[3]
        if self.langto not in self.lanlist and self.langto != "All":
            print(f"Sorry, the program doesn't support {self.langto}")
            sys.exit()
        elif self.langfrom not in self.lanlist:
            print(f"Sorry, the program doesn't support {self.langfrom}")
            sys.exit()
        if self.langto == "All":
            self.lanlist.remove(self.langfrom)
            for lan in self.lanlist:
                self.all = True
                self.langto = lan
                self.get_url()
                self.connect()
                self.print_result()
        else:
            self.get_url()
            self.connect()
            self.print_result()

    def connect(self):
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            r = requests.get(self.url, headers=headers)
        except requests.exceptions.ConnectionError:
            print('Something wrong with your internet connection')
            sys.exit()
        self.request = r
        self.do_request()

    def do_request(self):
        soup = BeautifulSoup(self.request.content, "html.parser")
        self.words = [x.text.strip() for x in soup.select("#translations-content > .translation")]
        self.sentences = [x.text.strip() for x in soup.select("#examples-content > .example >  .ltr")]
        if not self.words:
            print(f"Sorry, unable to find {self.word}")
            if not self.all:
                sys.exit()

    def print_result(self):
        k = 1
        j = 2
        with open(f"{self.word}.txt", "a") as resfile:
            print("\n", file=resfile)
            print(self.langto, "Translations:", file=resfile)
            for w in self.words[:k]:
                print(w, file=resfile)
            print("\n", file=resfile)
            print(self.langto, "Examples:", file=resfile)
            for i, s in enumerate(self.sentences[:j]):
                if i % 2 == 0 and i != 0:
                    print("\n", file=resfile)
                print(s, file=resfile)
        print("\n")
        print(self.langto, "Translations:")
        for w in self.words[:k]:
            print(w)
        print("\n")
        print(self.langto, "Examples:")
        for i, s in enumerate(self.sentences[:j]):
            if i % 2 == 0 and i != 0:
                print("\n")
            print(s)


if __name__ == "__main__":
    Translator()
