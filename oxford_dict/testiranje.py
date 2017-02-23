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
        first_entry = root.findall('entry')[:3]
        rutovi = []
        for root in first_entry:
            # print(root.attrib['id'])
            rutovi.append(root)

        return rutovi
        print('55555555555555',type(root.attrib))
        # print(first_entry)
        # if not first_entry:
        #     raise MWApiException('No entries found')




class DictionaryAPI(MerriamWebsterAPI):
    base_url = 'http://www.dictionaryapi.com/api/v1/references/collegiate/xml/'
    # sound = self.sound


    def _parse_xml_for_def(self, xml):
        # main_entry = ET.fromstring(xml)
        main_entry = self._get_xml_root(xml)
        # print('ddddddddddddddddd',main_entry)
        defspojeno = []
        for mali in main_entry:
            deftag = mali.findall('.//def/dt')
            # print(']]]]]]]]]]]]]]]]]]]]]]',deftag)
            # defspojeno = []
            long = 0
            for defin in deftag:
                # print("len",len(defin.text))
                long +=len(defin.text)
                # print (long)
                # print('2222222222222222222222',defin.text)
                if type(defin.text) == str and 300>long and len(defin.text)>20:
                    defspojeno.append(defin.text.replace(':',''))
                    # print(defin.text)
                    # nizi0 = mali.findall('.//def/dt/sx')
                    # for nizia in nizi0:
                    #     defspojeno.append(nizia.text.replace(':',''))
                    # # print(len(defin.text))
                elif long<10:
                    nizi = mali.findall('.//def/dt/sx')
                    for nizi in nizi:
                        defspojeno.append(nizi.text.replace(':',''))
        sdefspojeno = '  \u235f '.join(defspojeno)
        # print('defffffffffffffff',defspojeno)
        # print('dfffffffffffffffff',sdefspojeno)
        return sdefspojeno





    def get_definition(self, word):
        result = self._retrieve_xml(word)
        definition = self._parse_xml_for_def(result).replace(word,'\u2055'*len(word))
        print('definition',definition)
        print(type(definition))
        return definition


    def _parse_xml_for_etym(self, xml):
        main_entry = self._get_xml_root(xml)
        spojeno = []
        for ety in main_entry:
            etym = ety.findall('.//et')
            for text in etym:
                # print('==============\r',text.text)
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
                # print(rjc.text)
                zvuci.append(rjc.text)
                #     for ajmo in rjc:
                #         print(ajmo.text)
        # print('-----------',zvuci[0][0])
        baseURL= "http://media.merriam-webster.com/soundc11/"
        # print(baseURL + zvuci[0][0] + '/' + zvuci[0])
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
problem = ['drag']
a.process(problem)
#
# upload_words(rijeci_raw)
# #
# to_mp3(rijeci_raw)



