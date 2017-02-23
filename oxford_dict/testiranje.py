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

    def _get_xml_root(self, xml, word):
        # print(word)
        root = ET.fromstring(xml)
        first_entry = root.findall('entry')
        rutovi = []
        for root in first_entry:
            if len(root.attrib['id']) < len(word) + 3:
                print('korijen',root.attrib['id'])
                rutovi.append(root)
            # print('ovajjjjjjjjjj',root.attrib)
        return rutovi
        # print('55555555555555',type(root.attrib))



class DictionaryAPI(MerriamWebsterAPI):
    base_url = 'http://www.dictionaryapi.com/api/v1/references/collegiate/xml/'


    def _parse_xml_for_def(self, xml,word):
        main_entry = self._get_xml_root(xml,word)
        defspojeno = []
        usage1 = []
        for mali in main_entry:
            # print(mali)
            deftag = mali.findall('.//def/dt')
            long = 0
            for defin in deftag:
                long +=len(defin.text)
                if type(defin.text) == str and 300>long and len(defin.text)>20:
                    defspojeno.append(defin.text.replace(':',''))
            if long<10:
                nizi = mali.findall('.//def/dt/sx')
                for nizi in nizi:
                    defspojeno.append(nizi.text.replace(':',''))
            usage = mali.findall('.//def/dt/vi')
            for primjer in usage:
                usage1.append(primjer.text)
        primjerspojeno = '  \u25c9 '.join(usage1[:3])
        sdefspojeno = '  \u235f '.join(defspojeno)
        oba_spojeno = sdefspojeno + ' \u21f6Usage: ' + primjerspojeno
        return oba_spojeno


    def get_definition(self, word):
        result = self._retrieve_xml(word)

        definition = self._parse_xml_for_def(result,word).replace(word,'\u204e'*len(word))
        print('definition',definition)
        return definition


    def _parse_xml_for_etym(self, xml,word):
        main_entry = self._get_xml_root(xml,word)
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
        etymology = self._parse_xml_for_etym(result,word)
        if etymology is None:
            return
        else:
            return etymology


    def _parse_xml_for_sound(self, xml,word):
        main_entry = self._get_xml_root(xml,word)
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
        sound = self._parse_xml_for_sound(result,word)
        return sound

    def process(self, rijeci):

        conn = sqlite3.connect('.\\word_database\\words1.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS words (


              today date,
              word text,
              definition text,
              etymology text,
              sound_file  text,
              UNIQUE (word, definition,etymology,sound_file))''')


        for word in rijeci:
            print(word)
            c.execute("INSERT or IGNORE INTO words  VALUES (?, ?, ?, ?, ?)",
                      (today, word, self.get_definition(word), self.get_etymology(word), self.get_sound(word)))
            conn.commit()
        conn.close()

a = DictionaryAPI(MerriamWebsterAPI)

from_doc = 'earnest, dandelion, banner, flinch, tout'#, smother, gleam, repent, dash, beet, timber, scurvy, foreman, toil, goblin, bemoan, redemption, unduly, spurious, pois, enliven, incipient, retain, swallow, turd, reek, obfuscate, smear, plaster, breeze, drag, tier, preposterous, berserk, cardigan, juggernaut, ooze, loom, accordion, caress, dope, gentry, hideous'

b = from_doc.replace(',','')
rijeci_raw = b.split()

class MWApiException(Exception):
    pass
problem = ['strain']
a.process(problem)
# #
# upload_words(rijeci_raw)
# # #
# to_mp3(rijeci_raw)
#


