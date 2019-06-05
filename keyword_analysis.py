'''This code generate keywords and assigns it a score based on a normalisation 
we adopted. It takes a .csv file as a input having the titles of 
scientific articles/news headlines/ as rows'''








'''Import the libraries used in the code'''

import pandas
import csv

import re
import nltk
'''downloads stopwords'''
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

#################################################################################

'''Reading the csv file to create pandas dataframe'''

df=pandas.read_csv('Arviv_GRQC_Title_17.csv')

'''From the dataFrame we create a pandas Series where each row is joined'''
df_s = pandas.Series(' '.join(df['Title']))

num=df.shape[0] # saves the number of rows in df as an integer.

##################################################################################


'''This section tests various aspects of the dataset'''



##Fetch wordcount for each Title

# df['word_count'] = df['Title'].apply(lambda x: len(str(x).split(" ")))
# print(df[['Title','word_count']])



'''This gives us the most frequently used words.


This first creates a series by joining the individual rows (using .joint) and 
then using .split, it separates each words and saves it within the series.
Finally value_counts gives the number of elements in the series'''


# freq = pandas.Series(' '.join(df['Title']).split()).value_counts()[:20]
# print(freq)


#############################################################################


'''cleaning and pre-processing the dataset'''


##Creating a list of stop words 
stop_words = set(stopwords.words("english"))


##Creating a list of custom stopwords defined by the user(words that i dont want in ngram)
new_words = ['using','near','new']

#the complete set of stopwords
stop_words = stop_words.union(new_words)


#selecting the significant words by subtracting common words from the stop_words
'''creating an empty list to store the significant words'''
corpus = []
for text in df_s:
    
    #Convert to lowercase
    text = text.lower()
    
 
   
#matches text with words in stop_words and appends corpus[] accordingly 
    if text not in stop_words:   
    	corpus.append(text)

#checking the top 20 words we are left with their occurance frequency  	
# print(pandas.Series(corpus).value_counts()[:20])    


#replaces some of the words with suffixes 

corpus = [word.replace('holes','hole').replace('waves','wave').replace('times','time') 
.replace('models','model').replace('theories','theory').replace('fields','field')
.replace('effects','effect') 
for word in corpus]


######################**********#####################************########################

'''using sklearn to extract the keywords or high frequency n-grams'''


 ##this is to check how the method works


'''using CountVectorizer'''


# cv=CountVectorizer(min_df=5,max_df=0.8,stop_words=stop_words, max_features=2000, ngram_range=(1,2))


'''defining the bag of words i.e all the tokens are represented in a matrix with a 
assigned vector value'''


# X=cv.fit_transform(corpus)

# sum_words = X.sum(axis=0) 

# print([(word, sum_words[0, idx]) for word, idx in     
#                   cv.vocabulary_.items()])


'''saving the matrix into a pandas df and then exporting it to a csv file'''
# pandas.DataFrame(X.todense(),columns=cv.get_feature_names()).to_csv('result.csv')





''' **************  		main part begins below   		****************'''





'''function determining the most frequently occuring n-grams'''
def get_top_words(corpus, n=None):     #n determines the number of top words we want
    
    cv=CountVectorizer(max_features=2000, stop_words=stop_words, ngram_range=(1,3))
#we can change the range of n-grams by changing ngram_range


    X=cv.fit_transform(corpus)
    

#adding all the tokens that are elements of a matrix along axis 0 creating an array
    sum_words = X.sum(axis=0) 
    
#this creates a list having the words in the 1st idx and the corresponding freq as 2nd
#cv.vocab.items() gives the list [(word, column number),...]
    words_freq = [(word, sum_words[0, idx]/num) for word, idx in     
                  cv.vocabulary_.items()]

    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:n]



'''using the get_top_words function for the required dataset'''

keywords = get_top_words(corpus, n=100)



######################################################################################




#words that are insignificant as 1 grams
unwanted_1grams=['hole','black','model','non','time','space','wave','dark'
,'energy','theory','de','sitter','mass','equation','general','solution','field','solutions'
,'type','einstein','gravitational','tensor','modified','effet']





'''removing the 1grams that are not significant'''

######################################################

#if you want just the keywords, comment this out...
for y in unwanted_1grams:
	for x in keywords:
		if x[0]==y:
			keywords.remove(x)

################################################...



'''saving the result as a pandas df'''
top_df = pandas.DataFrame(keywords)
top_df.columns=["keywords", "score"]
pandas.DataFrame(top_df).to_csv('keywords_17.csv')



print(keywords)





































