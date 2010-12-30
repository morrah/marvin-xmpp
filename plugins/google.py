import urllib
import json
import random

class Google:
    ''' Google module
google <string> [results <number>]
translate <string> [lang <language>|<language>]'''
    
    public = ['translate', 'google']
    
    def translate(self, sendfunc, msg):
        '''
translate <string> [lang <language>|<language>]:
    translate <string> using google api.
    lang option specifies the direction of translation. <language> it is 2-character code of language.
    Default direction: en|ru'''
        try: (text, lang) = msg.rsplit(' lang ', 1)
        except ValueError:
            text = msg
            lang = 'en|ru'

        languages = {'az': 'азербайджанский', 'sq': 'албанский', 'ar': 'арабский', 'hy': 'армянский', 'af': 'африкаанс', \
    'eu': 'баскский', 'be': 'белорусский', 'bg': 'болгарский', 'cy': 'валлийский', 'hu': 'венгерский', 'vi': 'вьетнамский', \
    'gl': 'галисийский', 'nl': 'голландский', 'el': 'греческий', 'ka': 'грузинский', 'da': 'датский', 'iw': 'иврит', \
    'yi': 'идиш', 'id': 'индонезийский', 'ga': 'ирландский', 'is': 'исландский', 'es': 'испанский', 'it': 'итальянский', \
    'ca': 'каталанский', 'zh-CN': 'китайский', 'ko': 'корейский', 'ht': 'креольский (Гаити)', 'la': 'латынь', \
    'lv': 'латышский', 'lt': 'литовский', 'mk': 'македонский', 'ms': 'малайский', 'mt': 'мальтийский', 'de': 'немецкий', \
    'no': 'норвежский', 'fa': 'персидский', 'pl': 'польский', 'pt': 'португальский', 'ro': 'румынский', 'ru': 'русский', \
    'sr': 'сербский', 'sk': 'словацкий', 'sl': 'словенский', 'sw': 'суахили', 'tl': 'тагальский', 'th': 'тайский', \
    'tr': 'турецкий', 'uk': 'украинский', 'ur': 'урду', 'fi': 'финский', 'fr': 'французский', 'hi': 'хинди', \
    'hr': 'хорватский', 'cs': 'чешский', 'sv': 'шведский', 'et': 'эстонский', 'ja': 'японский'}

#       translate <string> [lang help]
        if lang == 'help':
            lang_help = ''
            for k, v in languages.iteritems(): lang_help += k + '=' + v + '; '
            sendfunc(lang_help.decode('utf-8'), 'groupchat')
            return

#       translate <string> [lang chain<chain_len>]
        if lang.find('chain') >= 0:
            chain_len = int( lang.rsplit('chain', 1)[1] )
            random.seed
            lang = 'ru|'
            tmp_lst = []
            for i in languages.iterkeys(): tmp_lst.append(i)
            for k in random.sample(tmp_lst, chain_len): lang += k + '|'
            lang += 'ru'
            #sendfunc(lang, 'groupchat')
        
        if lang.find('jp') >= 0:
            sendfunc('Use ja, Luke.', 'groupchat')
            return
        
        langs = lang.split('|')
        response = ''
        for i in range(0, len(langs)-1):
            response = json.loads(self.goUrl('http://ajax.googleapis.com/ajax/services/language/translate?v=1.0&',
                                   {'q' : text,'langpair':langs[i]+'|'+langs[i+1]}))
            if response and response.has_key('responseData') and response['responseData'] and response['responseData'].has_key('translatedText'):
                text = unicode(response['responseData']['translatedText']).encode('utf-8')
            else:
                sendfunc('Translate from ' + langs[i] + ' to ' + langs[i+1] + ' fail. Last: ' + text, 'groupchat')
                return
        if response and response.has_key('responseData') and response['responseData'] and response['responseData'].has_key('translatedText'):
            sendfunc(response['responseData']['translatedText'], 'groupchat')
        else:
            sendfunc('NO WAI!', 'groupchat')
    
    def google(self, sendfunc, msg):
        '''
google <string> [results <number>]:
    google <string> in google.
    results - number of printed search results.'''
        try: (text, numresults) = msg.rsplit(' results ', 1)
        except ValueError:
            text = msg
            numresults = 1
        
        try: numresults = int(numresults)
        except Exception: numresults = 1        
        
        response = json.loads(self.goUrl('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&', 
                                   {'q' : text}))
        
        if response and response.has_key('responseData') and response['responseData'] and response['responseData'].has_key('results'):
            num = 0
            for result in response['responseData']['results']:
                if numresults > 0 and num >= numresults:
                    break
                result['content'] = result['content'].replace('<b>', '').replace('</b>', '')                
                sendfunc(' '.join([result['titleNoFormatting'], result['content'], result['url']]), 'groupchat')
                num += 1
        else:
            sendfunc('NO WAI!', 'groupchat')

    
    def goUrl(self, url=None, params = {}):
        if not url: return
        query = ''
        if len(params):
            query = urllib.urlencode(params)
        url = url + query
        results = urllib.urlopen(url)
        return results.read()
        
        