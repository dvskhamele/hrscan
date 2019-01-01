#selected_resume

import docx2txt
import string
import re
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
from textblob import Word # for lemmatize
import nltk
from nltk.corpus import wordnet
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer

lem = WordNetLemmatizer()

def checkDegree(data):
    degree = ['B.E.', 'B.E', 'b.e.', 'B.e.', 'B.e', 'BE', 'M.E.', 'M.E', 'm.e.', 'M.e.', 'M.e', 'ME']
    lkj = []
    for deg in degree:
        if deg in data:
            lkj.append(deg)
    return lkj


def textClean(applicant_cv):
    #nltk.download()
#    nltk.download('omw')

    text_in_resume = []
    i = 1
    for cv in applicant_cv:
        data = docx2txt.process(cv.applicant_cv)
        degg = checkDegree(data)
        data = TextBlob(data.lower()).words
        lemmatized_data = [lem.lemmatize(i, pos=wordnet.ADJ) for i in data]
        s = ""
        for ii in lemmatized_data:
        	s+=ii+' '
        text_in_resume.append(s)
        i+=1
    clean_text=[]
    for i in text_in_resume:
        ct = i.lower()
        ct = re.sub(r"\t+", " ", ct)
        ct = re.sub(r'\n', ' ', ct)
        ct = re.sub(r"\s+", " ", ct)
        ct = re.sub(r'\.', '', ct)
        ct = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', ct)
        clean_text.append(ct)
    clean_text += degg

    return clean_text

def collegeRank(clg, applicant_cv, clean_text):
    college_rankings = clg
    rank_resume_by_college = []
    i=0
    for text in clean_text:
        applicant_clg = []
        r = []
        falg = 0
        for rank, college in college_rankings.items():
            for c in college:
                if (' '+c+' ') in text or (' '+c+'.') in text or (' '+c+',') in text:
                    applicant_clg.append(c)
                    r.append(rank)
                    rank_resume_by = {applicant_cv[i].applicant_name:r, 'college': applicant_clg}
                    flag = 1

        if rank_resume_by not in rank_resume_by_college:
            rank_resume_by_college.append(rank_resume_by)
        i+=1
    return rank_resume_by_college

def degreeRank(deg, applicant_cv, clean_text):
    degree_rankings = deg
    rank_resume_by_degree = []
    i = 0
    for text in clean_text:
        applicant_deg = []
        rr = []
        for rank, degree in degree_rankings.items():
            for d in degree:
                if len(d)>2:
                    if ' '+d+' ' in text:
                        if d=="march":
                            applicant_deg.append('MArch')
                        else:
                            applicant_deg.append(d)
                        rr.append(rank)
        rr = list(set(rr))
        rank_resume_by_degree.append({applicant_cv[i].applicant_name:rr, 'degree': applicant_deg})
        i += 1
    return rank_resume_by_degree
'''
def keywordRank(applicant_cv, cv_keywords, clean_text):
    ku = []
    for i in cv_keywords:
        try:
            wd = i.k_value.lower().split(' ')
            for k in wd:
                ku.append(lem.lemmatize(k, pos=wordnet.ADJ))
        except:
            ku.append(lem.lemmatize(k, pos=wordnet.ADJ))

    similar_keywords = []
    for words in ku:
        k = words.split(' ')
        for i in k:
            l = wordnet.synsets(i)
            for j in l:
                similar_keywords.append(j)


    similar_text = []

    for text in clean_text:
        u = []
        stext = text.split(' ')
        for i in stext:
            for synset in wordnet.synsets(i):
                for lemma in synset.lemmas():
                    if lemma not in u:
                        u.append(lemma)
            #l = wordnet.synsets(i)
            #for j in l:
                #if j.wup_similarity(i) != None and j.wup_similarity(i) >= 0.5:
                #u.append(j)
        if len(u):
            similar_text.append(u)

    print(similar_text)
    print(len(similar_text[0]))


    print('start')
    len_keywords = len(similar_keywords)
    rank_resume_by_keywords = []
    i = 0

    for text in similar_text:
        count = 0
        for word in text:
            for key in similar_keywords:
                count += 1
        print(count)
        rank_resume_by_keywords.append({applicant_cv[i].applicant_name:(count/len_keywords)})
        i += 1

    print('end')
    return rank_resume_by_keywords

'''

# new function
def keywordRank(applicant_cv, cv_keywords, clean_text, neg_keywords):
    ku = []
    for i in cv_keywords:
        try:
            wd = i.k_value.lower().split(' ')
            for k in wd:
                ku.append(lem.lemmatize(k, pos=wordnet.ADJ))
        except:
            ku.append(lem.lemmatize(k, pos=wordnet.ADJ))

    similar_keywords = []
    for words in ku:
        k = words.split(' ')
        for i in k:
            l = wordnet.synsets(i)
            for j in l:
                similar_keywords.append(j)

    s_keywords = [str(i) for i in similar_keywords]
    s_keywords = [i.split("'")[-2] for i in s_keywords]
    s_keywords = [i.split('.')[0] for i in s_keywords]
    similar_keywords = s_keywords + ku
    similar_keywords = list(set(similar_keywords))

    len_keywords = len(similar_keywords)
    rank_resume_by_keywords = []
    i = 0

    neg_key = [neg.n_value for neg in neg_keywords ]

    for text in clean_text:
        count = 0
        keys = []
        for key in similar_keywords:
            if key in text and key not in neg_key:
                count += 1
                keys.append(key+" ")
                #print('cv',i,key)
        rank_resume_by_keywords.append({applicant_cv[i].applicant_name:(count/len_keywords), 'keywords': keys, 'keywordsCount': len(keys)})
        i += 1

    print('end')
    return rank_resume_by_keywords
