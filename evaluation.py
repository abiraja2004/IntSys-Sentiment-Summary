'''
Module for evaluating rouge and cosine similarity between 
hypothesis entry (what the machine produced) and reference 
entry (gold standard).

Computes rouge-n (up to n=4), rouge-l, and rouge-w
(precision, recall, f-measure) 

Usage: 
import evaluation as ev
ev.evaluate_rouge(<hypothesis>, <reference>) 
ev.evaluate_embeddings(<hyp vector>, <ref vector>)
'''

import rouge
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def get_scores(hyp, ref):
    '''
    obtain various rouge scores containing f, p, r
    for each corresponding entry in hyp (hypothesis entry) 
    and ref (reference entry), both which are strings of 
    text/file paths
    '''

    evaluator = rouge.Rouge(metrics=['rouge-n', 'rouge-l', 'rouge-w'],
                           max_n=4, #stuff is hardcoded off of this, can change later
                           limit_length=True,
                           length_limit=100,
                           length_limit_type='words',
                           apply_avg=True,
                           apply_best=True,
                           alpha=0.5, #default f1_score, TODO: modify
                           weight_factor=1.2,
                           stemming=True)

    return evaluator.get_scores(hyp, ref)

def extract_rtype(r_score, r_type):
    '''
    extract specified rouge type entry containing 
    f, p, r data for r_score object 

    can extract rtypes (specify in second parameter): 
        'rouge-1',
        'rouge-2', 
        'rouge-3', 
        'rouge-4', 
        'rouge-l', 
        'rouge-w'
    '''
    assert r_type in ['rouge-1','rouge-2', 
        'rouge-3', 'rouge-4', 'rouge-l', 'rouge-w']

    return r_score[r_type]



def extract_fpr(r_type, fpr):
    '''
    extract f/p/r (specify char in second parameter) 
    and make list using each entry in r_type list
    '''
    assert fpr in ['f', 'p', 'r']
    return r_type[fpr]



def get_avg(nums):
    '''
    calculate average of nums list
    '''
    assert (all(list(map(lambda c: (type(c) == float) 
                or (type(c) == int), nums))))
    return sum(nums)/len(nums)


def evaluate_rouge(hyp, ref):
    '''
    produce aggregate evaluation of hyp_list and ref_list
    and print to terminal
    '''
    #print("outputting f, p, r for each rouge metric...")

    rouge_types = ['rouge-1','rouge-2', 
                'rouge-3', 'rouge-4', 'rouge-l', 'rouge-w']

    fpr_dict = dict()

    for r in rouge_types:
        score = get_scores(hyp, ref)
        rouge = extract_rtype(score, r)
        # fpr = (r, extract_fpr(rouge, 'f'), extract_fpr(rouge, 'p'), extract_fpr(rouge, 'r'))
        # print("type: {} f: {} p: {} r: {}".format(fpr[0], fpr[1], fpr[2], fpr[3]))
        fpr_dict[r] = (extract_fpr(rouge, 'f'), extract_fpr(rouge, 'p'), extract_fpr(rouge, 'r'))

    return fpr_dict

    

def evaluate_embeddings(hyp_encoding, ref_encoding):
    vec1 = hyp_encoding.reshape(1, -1)
    vec2 = ref_encoding.reshape(1, -1)
    metrics = cosine_similarity(vec1, vec2)
    cs_float = metrics[0][0]
    return cs_float


if __name__ == "__main__" :
    evaluate_rouge("the cat ate the rat", "the fat cat ate the rat")
    print(evaluate_embeddings(np.array([1,2,7,5,6]), np.array([3,5, 4,0,6])))