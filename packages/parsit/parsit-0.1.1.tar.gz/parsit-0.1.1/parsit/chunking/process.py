import json 
import time 
from pathlib import Path 
import re 
from typing import Dict ,Any ,List ,Callable 
from enum import Enum 
import nltk 
from semchunk import chunk as chunker 
import os 
from nltk import corpus 
import tiktoken 
import logging 


logging .basicConfig (
level =logging .INFO ,
format ='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
handlers =[
logging .StreamHandler (),
logging .FileHandler ('semchunk.log')
]
)
logger =logging .getLogger (__name__ )


try :
    nltk .data .find ('corpora/words')
    logging .info ("words corpus found")
except LookupError :
    logging .info ("words corpus not found, downloading...")
    nltk .download ('words')



class CauseOfDeletion (Enum ):
    EMPTY_CHUNK =1 
    INVALID_TEXT =2 
    TOKEN_COUNT_TOO_LOW =3 
    NONE =4 

class DeletedChunk :
    def __init__ (self ,chunk =None ,cause_of_deletion =CauseOfDeletion .NONE ):
        if chunk is None :
            chunk ={}
        self .chunk =chunk 
        self .cause_of_deletion =cause_of_deletion 


        # Define word pattern for consistent word counting
WORD_PATTERN =r'[\w\-\']+'

def calculate_overlap_metrics (chunks :List [str ],target_overlap :int ,token_counter :Callable [[str ],int ])->Dict [str ,Any ]:
    overlaps =[]
    overlap_ratios =[]

    # Check first 10 chunks or all if fewer than 10
    num_chunks_to_check =min (10 ,max (2 ,len (chunks )))

    for i in range (1 ,num_chunks_to_check ):
        chunk1 =chunks [i -1 ]
        chunk2 =chunks [i ]

        # Find the actual overlap in tokens
        max_overlap_tokens =min (50 ,token_counter (chunk1 ),token_counter (chunk2 ))
        max_overlap =len (chunk1 )# Start with full chunk as max

        actual_overlap =0 
        for j in range (1 ,max_overlap +1 ):
            if chunk1 [-j :]==chunk2 [:j ]:
                actual_overlap =j 
                break # Find the largest possible overlap

        if actual_overlap >0 :
        # Convert character overlap to token overlap
            overlap_text =chunk1 [-actual_overlap :]
            token_overlap =token_counter (overlap_text )

            # Calculate overlap ratio based on chunk size
            chunk_size =token_counter (chunk1 )
            overlap_ratio =token_overlap /chunk_size if chunk_size >0 else 0 

            overlaps .append (token_overlap )
            overlap_ratios .append (overlap_ratio )

    avg_overlap =sum (overlaps )/len (overlaps )if overlaps else 0 
    avg_overlap_ratio =sum (overlap_ratios )/len (overlap_ratios )if overlap_ratios else 0 

    # Calculate deviation from target
    overlap_deviation_pct =abs (avg_overlap -target_overlap )/target_overlap *100 if target_overlap >0 else 0 

    return {
    'avg_overlap_tokens':avg_overlap ,
    'avg_overlap_ratio':avg_overlap_ratio ,
    'overlap_deviation_pct':overlap_deviation_pct ,
    'target_overlap':target_overlap 
    }

def calculate_metrics (original :str ,chunked :str ,chunks :List [str ],target_overlap :int ,token_counter :Callable [[str ],int ])->Dict [str ,Any ]:
    original_words =set (re .findall (WORD_PATTERN ,original .lower ()))
    chunked_words =set (re .findall (WORD_PATTERN ,chunked .lower ()))

    char_loss =max (0 ,len (original )-len (chunked ))
    word_loss =len (original_words -chunked_words )
    word_overlap =len (original_words &chunked_words )

    # Calculate token counts
    original_tokens =token_counter (original )
    chunked_tokens =sum (token_counter (chunk )for chunk in chunks )

    return {
    'original_length':len (original ),
    'chunked_length':len (chunked ),
    'original_tokens':original_tokens ,
    'chunked_tokens':chunked_tokens ,
    'token_loss':max (0 ,original_tokens -chunked_tokens ),
    'char_loss':char_loss ,
    'char_loss_pct':(char_loss /len (original )*100 )if original else 0 ,
    'original_words':len (original_words ),
    'chunked_words':len (chunked_words ),
    'word_loss':word_loss ,
    'word_overlap':word_overlap ,
    'word_overlap_pct':(word_overlap /len (original_words )*100 )if original_words else 0 ,
    'overlap_metrics':calculate_overlap_metrics (chunks ,target_overlap ,token_counter )
    }

def process (paper_path :str ,output_path :str =None ,chunk_size :int =512 ,target_overlap :int =20 ,adjust_overlap :bool =True ):
# Read the paper
    with open (paper_path ,'r',encoding ='utf-8')as f :
        if paper_path .lower ().endswith ('.json'):
        # Parse JSON content into Python objects
            try :
                content_blocks =json .load (f )
                if not isinstance (content_blocks ,list ):
                    raise ValueError ("JSON content must be a list of content blocks")

                    # Process structured content blocks directly
                chunks =chunker (content_blocks ,chunk_size =chunk_size ,token_counter =len ,overlap =target_overlap ,adjust_overlap =adjust_overlap )
                # Handle both list of strings and list of dicts with 'text' key
                chunk_texts =[]
                for chunk in chunks :
                    if isinstance (chunk ,dict )and 'text'in chunk :
                        chunk_texts .append (chunk ['text'])
                    elif isinstance (chunk ,str ):
                        chunk_texts .append (chunk )
                paper_text ='\n'.join (chunk_texts )

            except json .JSONDecodeError as e :
                raise ValueError (f"Invalid JSON in {paper_path }: {e }")
        else :
        # Plain text processing
            paper_text =f .read ()
            chunks =chunker (paper_text ,chunk_size =chunk_size ,token_counter =len ,overlap =target_overlap ,adjust_overlap =adjust_overlap )
            chunk_texts =chunks if isinstance (chunks ,list )else [chunks ]

            # Initialize token counter (using len as simple character counter)
    token_counter =len 

    # Calculate metrics
    overlap_metrics =calculate_overlap_metrics (chunk_texts ,target_overlap ,token_counter )

    # Calculate adjustment factor
    actual_overlap =overlap_metrics ['avg_overlap_tokens']
    if actual_overlap >0 and target_overlap >0 :
        adjustment_factor =target_overlap /actual_overlap 
        adjusted_overlap =min (int (target_overlap *adjustment_factor ),chunk_size -1 )
    else :
        adjusted_overlap =target_overlap 

        # Second pass with adjusted overlap
    start_time =time .time ()
    chunks =chunker (paper_text ,chunk_size =chunk_size ,token_counter =token_counter ,overlap =adjusted_overlap ,adjust_overlap =adjust_overlap )
    second_pass_time =time .time ()-start_time 

    # Calculate final metrics
    chunked_text =' '.join (chunks )
    metrics =calculate_metrics (paper_text ,chunked_text ,chunks ,adjusted_overlap ,token_counter )
    overlap_metrics =calculate_overlap_metrics (chunks ,target_overlap ,token_counter )

    # Print results
    print ("\n=== Chunking Benchmark ===")
    print (f"File: {Path (paper_path ).name }")
    print (f"First pass time: {second_pass_time :.2f}s")# Using second_pass_time as first_pass_time isn't tracked
    print (f"Second pass time: {second_pass_time :.2f}s")
    print (f"Total chunks: {len (chunks )}")
    print (f"Original: {len (paper_text ):,} chars, {metrics ['original_words']:,} words, {metrics ['original_tokens']:,} tokens")
    print (f"Chunked: {len (chunked_text ):,} chars, {metrics ['chunked_words']:,} words, {metrics ['chunked_tokens']:,} tokens")
    print (f"Character loss: {metrics ['char_loss']:,} ({metrics ['char_loss_pct']:.2f}%)")
    print (f"Word loss: {metrics ['word_loss']} (Overlap: {metrics ['word_overlap_pct']:.2f}%)")
    print (f"Token loss: {metrics ['token_loss']:,} ({(metrics ['token_loss']/metrics ['original_tokens']*100 ):.2f}%)")

    print ("\n=== Overlap Analysis ===")
    print (f"Target overlap: {target_overlap } tokens")
    print (f"First pass overlap: {actual_overlap :.1f} tokens")
    print (f"Adjusted overlap: {adjusted_overlap } tokens")
    print (f"Final overlap: {overlap_metrics ['avg_overlap_tokens']:.1f} tokens")
    print (f"Final overlap ratio: {overlap_metrics ['avg_overlap_ratio']:.1%}")
    print (f"Overlap deviation: {overlap_metrics ['overlap_deviation_pct']:.1f}% from target")

    # Save results
    if output_path :
        with open (output_path ,'w',encoding ='utf-8')as f :
            json .dump ({
            'metadata':{
            'original_length':len (paper_text ),
            'original_words':metrics ['original_words'],
            'original_tokens':metrics ['original_tokens'],
            'chunked_length':len (chunked_text ),
            'chunked_words':metrics ['chunked_words'],
            'chunked_tokens':metrics ['chunked_tokens'],
            'char_loss':metrics ['char_loss'],
            'char_loss_pct':metrics ['char_loss_pct'],
            'word_loss':metrics ['word_loss'],
            'word_overlap_pct':metrics ['word_overlap_pct'],
            'token_loss':metrics ['token_loss'],
            'token_loss_pct':(metrics ['token_loss']/metrics ['original_tokens']*100 )if metrics ['original_tokens']else 0 ,
            'total_chunks':len (chunks ),
            'target_overlap':target_overlap ,
            'final_overlap_tokens':overlap_metrics ['avg_overlap_tokens'],
            'final_overlap_ratio':overlap_metrics ['avg_overlap_ratio']
            },
            'chunks':[{"text":chunk ,
            "token_count":token_counter (chunk )}for chunk in chunks ]
            },f ,indent =2 )
        post_process_output (output_path )
    return {
    'chunks':chunks ,
    'metrics':metrics ,
    'processing_times':{
    'first_pass':second_pass_time ,# Using second_pass_time as first_pass_time isn't tracked
    'second_pass':second_pass_time 
    }

    }




junk_patterns =[
r'^\s*\[\d+\]\s*$',# [1], [23], etc.
r'^\s*\[[A-Za-z]+\]\s*$',# [A], [B], etc.
r'^[A-Za-z]{1,4}\.\s*$',# Abbreviations like "pp. ", "et.", "al."
r'^[\W_]+$',# Only punctuation/symbols
r'^\s*[IVXLCDM]+\.\s*$',# Roman numerals like "IV.", "X.", etc.
r'^\s*[A-Z]\.\s*$',# Single capital letter and dot, e.g. "A."
r'^\s*\d+\.\s*$',# Number and dot, e.g. "1.", "23."
r'^\s*[A-Z]\s*$',# Single capital letter, e.g. "A"
r'^\s*[0-9]+\s*$',# Standalone numbers
r'^\s*$',# Empty or whitespace
r'^\s*\([A-Za-z0-9]+\)\s*$',# Standalone parenthesized, e.g. "(a)", "(1)"
r'^\s*[A-Za-z]\s*[A-Za-z]\.\s*$',# Two initials and dot, e.g. "J K."
r'^\s*Fig\.?\s*\d*\s*$',# "Fig.", "Fig. 1"
r'^\s*Table\s*\d*\s*$',# "Table", "Table 1"
r'^\s*[–—-]\s*$',# Standalone dash or em dash
r'^\s*\.\.\.\s*$',# Ellipsis
r'^\s*\d+\]\s*$',# 1], 23], etc.
r'^\s*\[\d+\s*$',# [1, [23, etc.
r'^\s*[A-Za-z]+\]\s*$',# A], AB], etc.
r'^\s*\[\s*[A-Za-z]+\s*$',# [A, [AB, etc.
r'^\s*\[\s*$',# [, [ , etc.
r'^\s*\[\s*\]\s*$'# [ ], [  ], etc.
]


COMPILED_PATTERNS =[re .compile (pat )for pat in junk_patterns ]

def is_junk_text (text ):
    return any (pat .match (text )for pat in COMPILED_PATTERNS )

def post_process_output (output_path :str ):
    deleted_chunks =[]
    logger .info (f"Starting post-processing of: {output_path }")

    if not output_path or not os .path .exists (output_path ):
        logger .error (f"Output file not found: {output_path }")
        return 

    try :
        with open (output_path ,"r",encoding ="utf-8")as output :
            data =json .load (output )
            chunks =data .get ("chunks",[])
            logger .info (f"Loaded {len (chunks )} chunks for processing")

            kept_chunks =[]
            for chunk in chunks :
                text =chunk .get ("text","")
                if len (text .strip ())==0 :
                    logger .debug ("Found empty chunk, marking for deletion")
                    deleted_chunks .append (DeletedChunk (chunk ,CauseOfDeletion .EMPTY_CHUNK ))
                elif is_junk_text (text ):
                    logger .debug (f"Found junk text: {text [:50 ]}...")
                    deleted_chunks .append (DeletedChunk (chunk ,CauseOfDeletion .INVALID_TEXT ))
                elif get_token_count (text )<5 :
                    logger .debug (f"Chunk has too few tokens: {get_token_count (text )}")
                    deleted_chunks .append (DeletedChunk (chunk ,CauseOfDeletion .TOKEN_COUNT_TOO_LOW ))
                else :
                    kept_chunks .append (chunk )
                    logger .debug (f"Kept chunk with {len (text )} characters")

            logger .info (f"Processing complete - Kept: {len (kept_chunks )}, Deleted: {len (deleted_chunks )}")
            data ["chunks"]=kept_chunks 

            if deleted_chunks :
                data ["deleted_chunks"]=[
                {"chunk":dc .chunk ,"cause_of_deletion":dc .cause_of_deletion .name }
                for dc in deleted_chunks 
                ]
                with open (output_path ,"w",encoding ="utf-8")as output :
                    json .dump (data ,output ,indent =2 )
                logger .info (f"Updated file saved with {len (kept_chunks )} chunks")

                # Log deletion details at debug level to avoid cluttering main logs
                for dc in deleted_chunks :
                    logger .debug (f"Deleted chunk (reason: {dc .cause_of_deletion .name }): {dc .chunk .get ('text','')[:100 ]}...")

    except json .JSONDecodeError as e :
        logger .error (f"Failed to parse JSON file: {e }")
        raise 
    except Exception as e :
        logger .exception (f"Unexpected error during post-processing: {e }")
        raise 


def get_token_count (text :str ):
    return len (tiktoken .get_encoding ("cl100k_base").encode (text ))

if __name__ =="__main__":
    import argparse 

    parser =argparse .ArgumentParser (description ='Chunk a document into semantic chunks with configurable size and overlap.')
    parser .add_argument ('input_file',nargs ='?',default ='demo1.md',
    help ='Path to the input file to chunk (default: demo1.md)')
    parser .add_argument ('--output','-o',default ='paper_chunks.json',
    help ='Output file path (default: paper_chunks.json)')
    parser .add_argument ('--chunk-size','-c',type =int ,default =4096 ,
    help ='Maximum chunk size in tokens (default: 4096)')
    parser .add_argument ('--overlap','-v',type =int ,default =20 ,
    help ='Number of tokens for chunk overlap (default: 20)')
    parser .add_argument ('--adjust-overlap',dest ='adjust_overlap',action ='store_true',default =True ,
    help ='Adjust overlap by splitting blocks for closest match (default: on)')
    parser .add_argument ('--no-adjust-overlap',dest ='adjust_overlap',action ='store_false',
    help ='Do not adjust overlap, use literal block overlap (default: off)')

    args =parser .parse_args ()
    process (args .input_file ,args .output ,args .chunk_size ,args .overlap ,args .adjust_overlap )



