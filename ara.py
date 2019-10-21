import re
#from pyoa import aravars # import variables relevant for Arabic processing


#================================================================
# deNoise(text) deletes short vowels from Arabic text
#================================================================

# deNoise(text) deletes short vowels from Arabic text
def deNoise(text):
    noise = re.compile(""" ّ    | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida
                         """, re.VERBOSE)
    text = re.sub(noise, '', text)
    return(text)


#===================================
# Normalization
#===================================

# normalizeArabic(text) - normalizes Arabic by simplifying complex characters 
def normalizeArabic(text):
    text = re.sub("[إأٱآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("(ؤ)", "و", text)
    text = re.sub("(ئ)", "ي", text)
    text = re.sub("(ة)", "ه", text)
    return(text)

# normalizeArabicHeavy(text) - normalizes Arabic by simplifying complex characters 
def normalizeArabicHeavy(text):
    text = re.sub("[إأٱآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("(ؤ)", "و", text)
    text = re.sub("(ئ)", "ي", text)
    text = re.sub("ء", "", text)
    text = re.sub("(ة)", "ه", text)
    return(text)

# normalizeArabicLight(text) - fixing only Alifs, AlifMaqsuras; replacing hamzas on carriers with standalone hamzas
def normalizeArabicLight(text):
    text = re.sub("[إأٱآا]", "ا", text)
    text = re.sub("[يى]ء", "ئ", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("(ؤ)", "ء", text)
    text = re.sub("(ئ)", "ء", text)
    #text = re.sub("(ء)", "", text)
    #text = re.sub("(ة)", "ه", text)
    return(text)

# normalizeArabicLight(text) - fixing only Alifs, AlifMaqsuras; replacing hamzas on carriers with standalone hamzas
def normalizeArabicVeryLight(text):
    text = re.sub("[إأٱآا]", "ا", text)
    text = re.sub("[يى]ء", "ئ", text)
    text = re.sub("ى", "ي", text)
    #text = re.sub("(ؤ)", "ء", text)
    #text = re.sub("(ئ)", "ء", text)
    #text = re.sub("(ء)", "", text)
    #text = re.sub("(ة)", "ه", text)
    return(text)

# deNormalize(text) - deNormalizing Function (adds all possible variations of letters with RegEx)
def deNormalize(text):
    text = re.sub('[إأٱآا]', '[إأٱآا]', text)
    text = re.sub('(ي|ى)\\b', '[يى]', text) # HEAVY '[إأٱآايى]'
    #text = re.sub('ة', '[هة]', text)
    text = re.sub('(ؤ|ئ|ء)', '[ؤئءوي]', text)
    return(text)

# deNormalize(text) - deNormalizing Function (adds all possible variations of letters with RegEx)
def deNormalizeHeavy(text):
    text = re.sub('[إأٱآا]', '[إأٱآا]', text)
    text = re.sub('(ي|ى)\\b', '[يى]', text) # HEAVY '[إأٱآايى]'
    text = re.sub('ة', '[هة]', text)
    text = re.sub('(ؤ|ئ|ء)', '[ؤئءوي]', text)
    return(text)
