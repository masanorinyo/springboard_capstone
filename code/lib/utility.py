import unicodedata
import numpy as np
import pandas as pd
import re
import math
from functools import partial

def get_data_in_chunks(list_data, extract_data_from, chunk=50000, ):
    
    ''' 
    Generator function
    Des: extract color information from product_ids while using color dataframe
    and return color list in a specified chunk in order to save memory 
    @list_data: list
    @extract_data_from: func
    @chunk: integer
    '''
    prev_chunk = 0
    next_chunk = chunk
    last_loop = False
    max_chunk=len(list_data)

    while True: # loop through product_ids until all values are evaluated
        results = []

        # if the next chunk is over the size of product_id list,
        # then re-define the next chunk with the product_id list size
        if next_chunk > max_chunk:
            last_loop = True
            next_chunk = max_chunk
            
        # - extract size letter
        # - extract sub-category and clean it
        for value in list_data[prev_chunk:next_chunk]:
            results.append(extract_data_from(value))
            
        yield results

        if last_loop:
            print("{} data has been extracted".format(next_chunk))
            break
        else:
            print("Extracting data currently: {}".format(next_chunk))
        
        # defining the next chunk
        prev_chunk = next_chunk
        next_chunk = next_chunk + chunk   
    

def convert_chunks_to_list(chunks):
    '''
    convert chunks into a list
    @chunks: chunk
    return list
    '''
    chunk_list = []
    for chunk in chunks:
        chunk_list = chunk_list + chunk
    return chunk_list

    
def convert_col_to_list(col):
    ''' 
    Converts panda dataframe column to a list
    @col: panda.dataframe
    return list
    '''
    return [str(w).replace('\u3000', ' ') for w in col.tolist()]


def combine_two_lists(lista, listb):
    '''
    combine same length two lists into one
    @lista: list
    @listb: list
    return: list
    '''
    def _add_to_lista(value_b, value_a, index):
        if value_b not in value_a and value_b is not None:  
            if type(value_a) is not list:
                lista[index] = []
            lista[index].append(value_b)
    
    for index,a_value in enumerate(lista.copy()):
        if a_value is None or type(a_value) is not list:
            a_value = lista[index] = []
            
        if listb[index] is None or type(listb[index]) is not list:
            listb[index] = []
        
        
        for b_value in listb[index]:
            if b_value not in a_value and b_value is not None:  
                lista[index].append(b_value)

        if not lista[index]:
            lista[index] = None

    return lista

def convert_to_unique_list(values):
    '''
    convert list to unique list
    @values: list
    return list
    '''
    
    return list(set(values))
    

def find_matched_group_and_name_from_df( df, name ):
    '''
    return the index value of keyword that appeared in name
    @df: pandas.dataframe
    @name: string
    return list
    '''
    matches = [[],[]]
    for index, value in enumerate(df['query_keywords'].values):
        if value in name:
            matches[0].append(df.iloc[index, 0])
            matches[1].append(df.iloc[index, 1])

    for index, match in enumerate(matches):
        if not match:
            matches[index] = None
    return matches

def get_column(matrix, i):
    '''
    returns a specified index column
    @matrix: list
    @i: numeric
    '''
    return [row[i] for row in matrix]

def filter_by_another_list(original, another_list):

    '''
    Filter list by another list
    @original: list
    @another_list: list
    return: list
    '''

    removing_indexes = []
    for index, c in enumerate(original.copy()):
        for s in another_list:
            if s in c:
                removing_indexes.append(index)

    for index in sorted(list(set(removing_indexes)), reverse=True):
        del original[index]
    
    return original


def get_groups(values,group_dict):
    '''
    Get group list based on defined dictionary
    @values: list
    @group_dist: object
    return list
    '''
    groups = []
    for value in values:
        group_holder = []

        for key in group_dict:
            for query in group_dict[key]:
                if query in value:
                    group_holder.append(key)
                    break

        if group_holder:
            groups.append(",".join(group_holder))
        else:
            groups.append(value)
    return groups


def normalize_strings(values):
    '''
    return list of NFKC converted string values
    @values: list
    return list
    '''
    return [ unicodedata.normalize('NFKC', value) for value in [ k.lower().replace(" ","") for k in values.copy()]]

def convert_to_float(value):
    '''
    converting string values in panda dataframe to float type
    @value: object
    return: object || float
    '''
    if type(value) is str:
        try:
          value = float(value)
        except ValueError as verr:
          pass
        except Exception as ex:
          pass 
    return value

def filter_by_invalid_numerics_in_df(df, columns):
    return df[df[columns].applymap(np.isreal).all(1)]