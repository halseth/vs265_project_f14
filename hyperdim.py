# hyperdim.py
# set of experiments using random_idx

# libraries
import random_idx
import utils
import sys
import scipy.io as scio
import numpy as np

N = 10000 # dimension of random index vectors
k = 10 # number of + (or -)
cluster_min = 4
cluster_max = 4 # size of max letter cluster
languages = ['english','german','norwegian','finnish','dutch','french','afrikaans','danish','spanish']

total_vectors = []
unknown_tots = []
varys = []

try:
		unknown_txt = sys.argv[1]
except IndexError:
		unknown_txt = './preprocessed_texts/unknown1.txt'

try:
		new_RI = sys.argv[2]
except IndexError:
		new_RI = 'on'
###############################
# generate random indexing for letters, reused throughout
cluster_sizes = xrange(cluster_min,cluster_max+1)
RI_letters = random_idx.generate_letter_id_vectors(N,k)

'''
##############################
# iterate over cluster sizes
for cluster_sz in cluster_sizes:
		for ordered in [1]:

					print "~~~~~~~~~~"
					# calculate language vectors
					lang_vectors = random_idx.generate_RI_lang(N, RI_letters, cluster_sz, ordered, languages=languages)
					total_vectors.append(lang_vectors)

					# calculate unknown vector
					unknown_vector = random_idx.generate_RI_text(N, RI_letters, cluster_sz, ordered,unknown_txt)
					unknown_tots.append(unknown_vector)

					# print cosine angles 
					print '=========='
					if ordered == 0:
							ord_str = 'unordered!'
					else:
							ord_str = 'ordered!'

					print 'N = ' + str(N) + '; k = ' + str(k) + '; letters clusters are ' + str(cluster_sz) + ', ' + ord_str + '\n'
					cosangles = utils.cosangles(lang_vectors, languages)
					variance = utils.var_measure(cosangles)
					varys.append(variance)
					print "variance of language values: " + str(utils.var_measure(cosangles))

########################
# history vectors
lang_vectors = random_idx.generate_RI_lang_history(N, RI_letters, languages=languages)
total_vectors.append(lang_vectors)
unknown_vector = random_idx.generate_RI_text_history(N, RI_letters, unknown_txt)
unknown_tots.append(unknown_vector)

print "~~~~~~~~~~"
print "history vector information"
cosangles = utils.cosangles(lang_vectors, languages)
variance = utils.var_measure(cosangles)
varys.append(variance)
print "variance of history language values: " + str(utils.var_measure(cosangles))
'''
#############################
# calculate language vectors with words

print "~~~~~~~~~~"
# calculate language vectors
lang_vectors = random_idx.generate_RI_lang_words(N, RI_letters, languages=languages)
total_vectors.append(lang_vectors)

print 'N = ' + str(N) + '; k = ' + str(k) + '; words words words! \n'
cosangles = utils.cosangles(lang_vectors, languages)
variance = utils.var_measure(cosangles)
varys.append(variance)
print "variance of language values: " + str(utils.var_measure(cosangles))

# calculate unknown vector
unknown_vector = random_idx.generate_RI_words(N, RI_letters, unknown_txt)
unknown_tots.append(unknown_vector)
#############################
# final language vector calculations!
final_lang = np.zeros(total_vectors[0].shape)
final_unknown = np.zeros(unknown_tots[0].shape)
for i in xrange(len(varys)):
		final_lang += varys[i]*total_vectors[i]/np.linalg.norm(total_vectors[i])
		final_unknown += varys[i]*unknown_tots[i]/np.linalg.norm(unknown_tots[i])

# generate language pairs
bilinguals = []
for i in xrange(len(languages)):
		for j in xrange(len(languages)):
				if i < j:
						bilinguals.append((languages[i],languages[j]))
#print bilinguals

bilingual_vectors = np.zeros((len(bilinguals),N))
for i in xrange(len(bilinguals)):
		lang1, lang2 = bilinguals[i]

		lang1_idx = languages.index(lang1)
		lang2_idx = languages.index(lang2)

		bilingual_vectors[i,:] = final_lang[lang1_idx,:]/np.linalg.norm(final_lang[lang1_idx,:]) + final_lang[lang2_idx,:]/np.linalg.norm(final_lang[lang2_idx,:])

print '\n'
# compare with "unknown text"
#final_unknown = sum(unknown_tots)
utils.find_language(unknown_txt, final_unknown, final_lang, languages)


print '\n'
# compare with "unknown text" on bilinguals
print '========'
utils.find_language(unknown_txt, final_unknown, np.vstack((final_lang, bilingual_vectors)), languages + bilinguals)


print '========='
print 'N = ' + str(N) + '; k = ' + str(k) + '; max size letters clusters are ' + str(cluster_max) + '\n'
cosangles = utils.cosangles(final_lang, languages, display=0)
print "variance of language values: " + str(utils.var_measure(cosangles))
