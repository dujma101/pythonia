from urllib.parse import quote_plus
from urllib.request import urlopen
import xml.etree.ElementTree as ET
import sqlite3
from datetime import date
import urllib.request
from tomp31 import to_mp3
from words_upload import upload_words
today = str(date.today())
ittag = str.encode('<it>')
itclose = str.encode('</it>')
empty = bytes('', 'utf-8')


class MerriamWebsterAPI:
    def __init__(self, key):
        self.key = 'b90ca8c7-b0cb-44c4-bc1b-06cb655d0301'
        self.cachedXML = {}

    def _wrap_url(self, url):
        encoded_key = quote_plus(self.key)
        return url + "?key={}".format(encoded_key)

    def _retrieve_xml(self, word):
        if word in self.cachedXML:
            return self.cachedXML[word]
        endpoint_url = self._wrap_url(self.base_url + quote_plus(word))
        xmlre = urlopen(endpoint_url).read()
        #clean out the <it> tags which aren't completely compliant xml
        fullxml =  xmlre.replace(ittag, empty).replace(itclose, empty)
        self.cachedXML[word] = fullxml
        return fullxml

    def _get_xml_root(self, xml):
        root = ET.fromstring(xml)
        # print(root)
        first_entry = root.findall('entry')
        rutovi = []
        for root in first_entry:
            rutovi.append(root)
        return rutovi



class DictionaryAPI(MerriamWebsterAPI):
    base_url = 'http://www.dictionaryapi.com/api/v1/references/collegiate/xml/'


    def _parse_xml_for_def(self, xml,word):
        print(word)
        main_entry = self._get_xml_root(xml)


        # for root in first_entry:
        #    if len(root.attrib['id']) < len(word) + 3:
        #        print('korijen',root.attrib['id'])
        #        rutovi.append(root)
        usage1 = []
        defspojeno = []

        long = 0
        znakovi = ['\u24f5','\u24f6','\u24f7','\u24f8','\u24f9']
        count = 0
        newcount = 0
        for mali in main_entry:

            if len(mali.attrib['id']) < len(word) + 4 and mali.attrib['id'][0].islower():
                # print(mali.attrib['id'])
                duzina1 = 0

                count = count+1
                # print(count)
                deftag = mali.findall('.//def/dt')
                # print(deftag)
                # print('222222222222222222')
                # print(deftag)
                for defin in deftag:
                    if defin.text == None:
                        continue
                    # print('prvi             ',defin.text)
                    long +=len(defin.text)
                    duzina1 +=len(defin.text.strip())
                    # print(duzina1)
                    # print(len(defin.text))
                    # print(long)
                    if type(defin.text) == str  and duzina1 <250 and len(defin.text)>10:
                        if count > newcount:
                            newcount +=1
                            defspojeno.append(' ' + znakovi[count-1])
                        defspojeno.append('\u25b6 ' + defin.text.replace(':',''))
                if long<10:
                    nizi = mali.findall('.//def/dt/sx')
                    for nizi in nizi:
                        defspojeno.append(nizi.text.replace(':',''))
                usage = mali.findall('.//def/dt/vi')
                for primjer in usage:
                    usage1.append(primjer.text)
        sdefspojeno = ' '.join(defspojeno)
        # print(defspojeno)
        # print(sdefspojeno)

        if len(usage1) > 0:
            primjerspojeno = '  \u25b6 '.join(usage1[:3])
            oba_spojeno = sdefspojeno + ' \u23fa\u23e9 Usage: ' + primjerspojeno
            return oba_spojeno
        return sdefspojeno


    def get_definition(self, word):
        result = self._retrieve_xml(word)
        definition = self._parse_xml_for_def(result,word).replace(word,'\u204e'*len(word))
        print('definition',definition)
        return definition


    def _parse_xml_for_etym(self, xml):
        main_entry = self._get_xml_root(xml)
        spojeno = []
        for ety in main_entry:
            etym = ety.findall('.//et')
            for text in etym:
                # print('==============\r',text.text)
                if type(text.text) != str:
                    continue
                spojeno.append(text.text)
        # print(spojeno)
        sspojeno = '  \u235f '.join(spojeno)
        return sspojeno



    def get_etymology(self, word):
        result = self._retrieve_xml(word)
        etymology = self._parse_xml_for_etym(result)
        if etymology is None:
            return
        else:
            return etymology

    def _parse_xml_for_date(self, xml):
         main_entry = self._get_xml_root(xml)
         datum = main_entry[0].find('def/date').text
         return datum





    def get_date(self, word):
        result = self._retrieve_xml(word)
        date = self._parse_xml_for_date(result)
        print(date)
        return date


    def _parse_xml_for_sound(self, xml):
        main_entry = self._get_xml_root(xml)
        zvuci = []
        for zvuk in main_entry:
            sound1 = zvuk.findall('.//wav')
            for rjc in sound1:
                zvuci.append(rjc.text)
        baseURL= "http://media.merriam-webster.com/soundc11/"
        urllib.request.urlretrieve(baseURL + zvuci[0][0] + '/' + zvuci[0], '.\\rijeci_sound\\' + zvuci[0])
        return zvuci[0]

    def get_sound(self, word):
        result = self._retrieve_xml(word)
        sound = self._parse_xml_for_sound(result)
        return sound

    def process(self, rijeci):

        conn = sqlite3.connect('.\\word_database\\words.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS words (


              today date,
              word text,
              definition text,
              word_date text,
              etymology text,
              sound_file  text,
              UNIQUE (word, definition, word_date, etymology,sound_file))''')


        for word in rijeci:
            print(word)
            c.execute("INSERT or IGNORE INTO words  VALUES (?, ?, ?, ?, ?, ?)",
                      (today, word, self.get_definition(word), self.get_date(word), self.get_etymology(word), self.get_sound(word)))
            conn.commit()
        conn.close()

a = DictionaryAPI(MerriamWebsterAPI)

from_doc = 'tardy foliage pond contempt illicit evasive conjure cram daunt ghastly ominous pickle pantry'

b = from_doc.replace(',','')
rijeci_raw = b.split()

class MWApiException(Exception):
    pass
problem = ['beet']
a.process(rijeci_raw)


# for proba in problem:
#
#     a.get_date(proba)
#
upload_words(rijeci_raw)
# # #
to_mp3(rijeci_raw)
#
#
#
