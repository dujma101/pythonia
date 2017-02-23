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
        self.key = '============'
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
        first_entry = root.findall('entry')

        # print(first_entry)
        # if not first_entry:
        #     raise MWApiException('No entries found')
        return first_entry




class DictionaryAPI(MerriamWebsterAPI):
    base_url = 'http://www.dictionaryapi.com/api/v1/references/collegiate/xml/'
    # sound = self.sound


    def _parse_xml_for_def(self, xml):
        main_entry = ET.fromstring(xml)

        #main_entry = self._get_xml_root(xml)
        deftag = main_entry.findall('.//def/dt')
        defspojeno = []
        for defin in deftag:
            if type(defin.text) == str and len(defin.text)>10:
                defspojeno.append(defin.text.replace(':',''))
                # print(defin.text.strip())
                # print(len(defin.text))
            elif len(defin.text)<10:
                nizi = main_entry.findall('.//def/dt/sx')
                for nizi in nizi:
                    defspojeno.append(nizi.text.replace(':',''))
        sdefspojeno = ' =>> '.join(defspojeno)
        # print(sdefspojeno)
        return sdefspojeno




        # for all in deftag:
        #     try:
        #         long = long + len(all.text)
        #         # print(long)
        #     except TypeError:
        #         long = 0
        #    #print(all.text)
        # if long < 10:
        #         deftag = main_entry.findall('.entry/def/dt/sx')
        # return deftag


    def get_definition(self, word):
        result = self._retrieve_xml(word)
        definition = self._parse_xml_for_def(result)

        return definition


    def _parse_xml_for_etym(self, xml):
        main_entry = self._get_xml_root(xml)
        spojeno = []
        for ety in main_entry:
            etym = ety.findall('.//et')
            for text in etym:
                print('==============\r',text.text)
                spojeno.append(text.text)
            sspojeno = ' =>> '.join(spojeno)
            # print(sspojeno)
        return sspojeno



    def get_etymology(self, word):
        result = self._retrieve_xml(word)
        etymology = self._parse_xml_for_etym(result)
        # print('\n\n',etymology)
        if etymology is None:
            return
        else:
            return etymology


    def _parse_xml_for_sound(self, xml):
        main_entry = self._get_xml_root(xml)
        zvuci = []
        for zvuk in main_entry:
            sound1 = zvuk.findall('.//wav')
            print(sound1)

            for rjc in sound1:
                print(rjc.text)
                zvuci.append(rjc.text)
                #     for ajmo in rjc:
                #         print(ajmo.text)
        print('-----------',zvuci[0][0])
        baseURL= "http://media.merriam-webster.com/soundc11/"
        print(baseURL + zvuci[0][0] + '/' + zvuci[0])
        urllib.request.urlretrieve(baseURL + zvuci[0][0] + '/' + zvuci[0], '.\\rijeci_sound\\' + zvuci[0])
        return zvuci[0]

    def get_sound(self, word):
        result = self._retrieve_xml(word)
        sound = self._parse_xml_for_sound(result)
        #print("sound2"+sound)

        return sound

    def process(self, rijeci):

        conn = sqlite3.connect('.\\word_database\\words.db')
        c = conn.cursor()  # Create tableS
        c.execute('''CREATE TABLE IF NOT EXISTS words (


              today date,
              word text,
              definition text,
              etymology text,
              sound_file  text,
              UNIQUE (word, definition,etymology,sound_file))''')


        for word in rijeci:
            print(word)
            # self.get_etymology(word)
            # self.get_definition(word)
            #self.get_sound(word)



            c.execute("INSERT or IGNORE INTO words  VALUES (?, ?, ?, ?, ?)",
                      (today, word, self.get_definition(word), self.get_etymology(word), self.get_sound(word)))
            conn.commit()
        conn.close()

a = DictionaryAPI(MerriamWebsterAPI)

from_doc = 'swallow, turd, reek, obfuscate, smear, plaster, breeze, drag'#, tier, preposterous, berserk, cardigan, juggernaut, ooze, loom, accordion, caress, dope, gentry, hideous'

b = from_doc.replace(',','')
rijeci_raw = b.split()

class MWApiException(Exception):
    pass
problem = ['poised']
a.process(rijeci_raw)

upload_words(rijeci_raw)
#
to_mp3(rijeci_raw)



