# -*- coding: utf-8  -*-

def hindi_to_arabic(number):
    return number.replace(u'٠', '0')\
                 .replace(u'١', '1')\
                 .replace(u'٢', '2')\
                 .replace(u'٣', '3')\
                 .replace(u'٤', '4')\
                 .replace(u'٥', '5')\
                 .replace(u'٦', '6')\
                 .replace(u'٧', '7')\
                 .replace(u'٨', '8')\
                 .replace(u'٩', '9')
