
import json 
from loguru import logger 
from parsit .dict2md .ocr_mkcontent import merge_para_with_text 
from openai import OpenAI 
from typing import Optional ,Dict ,Any 
import ast 
import time 
import os 
import base64 
from bs4 import BeautifulSoup 


formula_optimize_prompt ="""请根据以下指南修正LaTeX公式的错误，确保公式能够渲染且符合原始内容：

1. 修正渲染或编译错误：
    - Some syntax errors such as mismatched/missing/extra tokens. Your task is to fix these syntax errors and make sure corrected results conform to latex math syntax principles.
    - 包含KaTeX不支持的关键词等原因导致的无法编译或渲染的错误

2. 保留原始信息：
   - 保留原始公式中的所有重要信息
   - 不要添加任何原始公式中没有的新信息

IMPORTANT:请仅返回修正后的公式，不要包含任何介绍、解释或元数据。

LaTeX recognition result:
$FORMULA

Your corrected result:
"""

text_optimize_prompt =f"""请根据以下指南修正OCR引起的错误，确保文本连贯并符合原始内容：

1. 修正OCR引起的拼写错误和错误：
   - 修正常见的OCR错误（例如，'rn' 被误读为 'm'）
   - 使用上下文和常识进行修正
   - 只修正明显的错误，不要不必要的修改内容
   - 不要添加额外的句号或其他不必要的标点符号

2. 保持原始结构：
   - 保留所有标题和子标题

3. 保留原始内容：
   - 保留原始文本中的所有重要信息
   - 不要添加任何原始文本中没有的新信息
   - 保留段落之间的换行符

4. 保持连贯性：
   - 确保内容与前文顺畅连接
   - 适当处理在句子中间开始或结束的文本
   
5. 修正行内公式：
   - 去除行内公式前后多余的空格
   - 修正公式中的OCR错误
   - 确保公式能够通过KaTeX渲染
   
6. 修正全角字符
    - 修正全角标点符号为半角标点符号
    - 修正全角字母为半角字母
    - 修正全角数字为半角数字

IMPORTANT:请仅返回修正后的文本，保留所有原始格式，包括换行符。不要包含任何介绍、解释或元数据。

Previous context:

Current chunk to process:

Corrected text:
"""

table_summary_prompt ="""Analyze the following table and provide a concise summary:  
  
1. Describe the table's main purpose and content  
2. Highlight key data points or trends  
3. Explain the table structure (rows, columns, headers)  
4. Keep the summary under 100 words  
  
Table content:  
{table_content}  
  
Summary:  
"""

image_summary_prompt ="""Analyze this image and provide a detailed description:  
  
1. Describe what you see in the image  
2. Identify key visual elements (charts, graphs, diagrams, photos)  
3. Explain any text or data visible in the image  
4. Note the image's purpose or context if apparent  
  
Image description:  
"""

text_block_summary_prompt ="""Summarize the following text block:  
  
1. Identify the main topic or theme  
2. Extract key points or arguments  
3. Note any important details or data  
4. Keep summary concise but comprehensive  
  
Text content:  
{text_content}  
  
Summary:  
"""

page_summary_prompt ="""Generate a comprehensive summary of this page:  
  
1. Overview of the page's main content and purpose  
2. Key sections and their topics  
3. Important data, figures, or findings  
4. Overall significance or conclusions  
  
Page content:  
{page_content}  
  
Summary:  
"""




def llm_aided_formula (pdf_info_dict ,formula_aided_config ):
    client =OpenAI (
    api_key =formula_aided_config ["api_key"],
    base_url =formula_aided_config ["base_url"]
    )

    for page_num ,page in pdf_info_dict .items ():
        blocks =page .get ("para_blocks",[])
        for block in blocks :
            if block .get ("type")=="formula":
                formula_text =merge_para_with_text (block )
                if not formula_text :
                    continue 

                prompt =formula_optimize_prompt .replace ("$FORMULA",formula_text )

                try :
                    completion =client .chat .completions .create (
                    model =formula_aided_config ["model"],
                    messages =[{'role':'user','content':prompt }],
                    temperature =0.1 ,
                    max_tokens =formula_aided_config .get ("max_tokens",200 )
                    )
                    fixed_formula =completion .choices [0 ].message .content .strip ()
                    block ["content"]=fixed_formula 
                    logger .info (f"Optimized formula on page {page_num }")
                except Exception as e :
                    logger .error (f"Failed to optimize formula: {e }")


def llm_aided_text (pdf_info_dict ,text_aided_config ):
    client =OpenAI (
    api_key =text_aided_config ["api_key"],
    base_url =text_aided_config ["base_url"]
    )

    for page_num ,page in pdf_info_dict .items ():
        blocks =page .get ("para_blocks",[])
        for block in blocks :
            if block .get ("type")=="text":
                text_content =merge_para_with_text (block )
                if not text_content or len (text_content )<50 :# Skip very short texts
                    continue 

                prompt =text_optimize_prompt .replace ("Current chunk to process:",f"Current chunk to process:\n{text_content }")

                try :
                    completion =client .chat .completions .create (
                    model =text_aided_config ["model"],
                    messages =[{'role':'user','content':prompt }],
                    temperature =0.3 ,
                    max_tokens =text_aided_config .get ("max_tokens",500 )
                    )
                    optimized_text =completion .choices [0 ].message .content .strip ()

                    # Update the spans with optimized text
                    if block .get ("lines"):
                    # Update the first span with optimized text
                        if block ["lines"][0 ].get ("spans"):
                            block ["lines"][0 ]["spans"][0 ]["text"]=optimized_text 
                            # Remove any additional spans to avoid duplication
                            if len (block ["lines"][0 ]["spans"])>1 :
                                block ["lines"][0 ]["spans"]=[block ["lines"][0 ]["spans"][0 ]]

                    logger .info (f"Optimized text block on page {page_num }")
                except Exception as e :
                    logger .error (f"Failed to optimize text: {e }")

def safe_parse_json (json_str ):
    try :
    # Log the raw response for debugging
        logger .debug (f"Raw JSON response: {json_str }")
        # Try to parse as JSON
        return json .loads (json_str )
    except json .JSONDecodeError as e :
        logger .warning (f"Failed to parse JSON: {str (e )}")
        # Try to fix common JSON issues
        try :
        # Try to parse with ast.literal_eval which is more lenient
            return ast .literal_eval (json_str )
        except (ValueError ,SyntaxError )as e2 :
            logger .warning (f"Failed to parse with ast.literal_eval: {str (e2 )}")
            # Return empty dict as fallback
            return {}

def llm_aided_title (pdf_info_dict ,title_aided_config ):
    if not pdf_info_dict or not title_aided_config :
        logger .warning ("Invalid input parameters for llm_aided_title")
        return 

    try :
        client =OpenAI (
        api_key =title_aided_config .get ("api_key",""),
        base_url =title_aided_config .get ("base_url","https://api.openai.com/v1"),
        timeout =30.0 
        )
    except Exception as e :
        logger .error (f"Failed to initialize OpenAI client: {e }")
        return 

    title_dict ={}
    origin_title_list =[]

    for page_num ,page in pdf_info_dict .items ():
        if not isinstance (page ,dict ):
            continue 

        blocks =page .get ("para_blocks",[])
        for i ,block in enumerate (blocks ):
            if not isinstance (block ,dict )or block .get ("type")!="title":
                continue 

            title_text =merge_para_with_text (block )
            if not title_text :
                continue 

            title_key =f"title_{len (origin_title_list )}"
            title_dict [title_key ]=title_text 
            origin_title_list .append (block )


    if not title_dict :
        logger .warning ("No title blocks found in the document")
        return 

    prompt ="""Analyze the following document titles and assign each a heading level (1-4) where:
    1 = Main title
    2 = Major section
    3 = Subsection
    4 = Minor subsection

    Return your response as a JSON object where keys are the title keys and values are the heading levels.
    Example: {"title_0": 1, "title_1": 2, "title_2": 2, "title_3": 3}
    
    Titles:
    """

    for key ,title in title_dict .items ():
        prompt +=f'"{key }": "{title }"\n'

    prompt +="\nYour response (JSON only, no other text):"

    max_retries =3 
    retry_delay =5 
    dict_completion =None 

    for attempt in range (max_retries ):
        try :
            logger .debug (f"Sending title analysis request (attempt {attempt +1 }):\n{prompt }")

            response =client .chat .completions .create (
            model =title_aided_config .get ("model","gpt-3.5-turbo"),
            messages =[
            {"role":"system","content":"You are a helpful assistant that analyzes document structure and assigns heading levels."},
            {"role":"user","content":prompt }
            ],
            temperature =0.3 ,
            max_tokens =2000 ,
            timeout =60 
            )

            response_content =response .choices [0 ].message .content .strip ()
            logger .debug (f"Raw API response: {response_content }")

            dict_completion =safe_parse_json (response_content )

            if not isinstance (dict_completion ,dict ):
                logger .warning (f"Attempt {attempt +1 } failed: Invalid response format")
                if attempt ==max_retries -1 :
                    logger .warning ("Using default title levels after maximum retries")
                    dict_completion ={str (i ):1 for i in range (len (title_dict ))}
                else :
                    time .sleep (retry_delay *(attempt +1 ))
                    continue 

            if len (dict_completion )!=len (title_dict ):
                logger .warning (f"Attempt {attempt +1 } failed: Title count mismatch")
                if attempt ==max_retries -1 :
                    logger .warning ("Using default title levels after maximum retries")
                    dict_completion ={str (i ):1 for i in range (len (title_dict ))}
                else :
                    time .sleep (retry_delay *(attempt +1 ))
                    continue 

            break 

        except Exception as e :
            logger .warning (f"Attempt {attempt +1 } failed: {str (e )}")
            if attempt ==max_retries -1 :
                logger .warning ("Using default title levels after maximum retries")
                dict_completion ={str (i ):1 for i in range (len (title_dict ))}
            else :
                time .sleep (retry_delay *(attempt +1 ))
                continue 

    if dict_completion is not None :
        for i ,origin_title_block in enumerate (origin_title_list ):
            title_key =f"title_{i }"
            if title_key in dict_completion :
                try :
                    level =int (dict_completion [title_key ])
                    origin_title_block ["level"]=max (1 ,min (4 ,level ))
                except (ValueError ,TypeError )as e :
                    logger .warning (f"Invalid level for {title_key }: {dict_completion [title_key ]}. Using default level 1.")
                    origin_title_block ["level"]=1 
            else :
                logger .warning (f"Title key {title_key } not found in response. Using default level 1.")
                origin_title_block ["level"]=1 
    else :
        logger .error ("Failed to process titles: No valid response from API")
        for origin_title_block in origin_title_list :
            origin_title_block ["level"]=1 

def llm_aided_text_block_summary (pdf_info_dict ,summary_config ):
    if not pdf_info_dict or not summary_config :
        logger .warning ("Invalid input parameters for llm_aided_text_block_summary")
        return 

    try :
        client =OpenAI (
        api_key =summary_config .get ("api_key",""),
        base_url =summary_config .get ("base_url","https://api.openai.com/v1"),
        timeout =30.0 
        )
    except Exception as e :
        logger .error (f"Failed to initialize OpenAI client: {e }")
        return 

    max_retries =3 
    retry_delay =5 
    min_text_length =100 

    for page_num ,page in pdf_info_dict .items ():
        if not isinstance (page ,dict ):
            continue 

        blocks =page .get ("para_blocks",[])
        for block in blocks :
            if not isinstance (block ,dict )or block .get ("type")!="text":
                continue 

            text_content =merge_para_with_text (block )
            if not text_content or len (text_content )<min_text_length :
                continue 

            prompt =f"""Please provide a concise summary of the following text. Focus on the main points and key information:
            
            {text_content }
            
            Summary:"""

            for attempt in range (max_retries ):
                try :
                    response =client .chat .completions .create (
                    model =summary_config .get ("model","gpt-3.5-turbo"),
                    messages =[{"role":"user","content":prompt }],
                    temperature =0.3 ,
                    max_tokens =500 ,
                    timeout =60 
                    )

                    if response .choices and len (response .choices )>0 :
                        summary =response .choices [0 ].message .content .strip ()
                        if summary :
                            block ["summary"]=summary 
                            logger .debug (f"Generated summary for text block on page {page_num }")
                            break 

                except Exception as e :
                    logger .warning (f"Attempt {attempt +1 } failed for text summary on page {page_num }: {str (e )}")
                    if attempt ==max_retries -1 :
                        logger .error (f"Failed to generate text summary after {max_retries } attempts")
                    else :
                        time .sleep (retry_delay *(attempt +1 ))
                        continue 

def llm_aided_table_summary (pdf_info_dict ,table_summary_config ):
    if not pdf_info_dict or not table_summary_config :
        logger .warning ("Invalid input parameters for llm_aided_table_summary")
        return 

    try :
        client =OpenAI (
        api_key =table_summary_config .get ("api_key",""),
        base_url =table_summary_config .get ("base_url","https://api.openai.com/v1"),
        timeout =30.0 
        )
    except Exception as e :
        logger .error (f"Failed to initialize OpenAI client: {e }")
        return 

    table_summary_prompt ="""Please provide a concise summary of the following table. Focus on the key information and relationships between the data: """

    for page_num ,page in pdf_info_dict .items ():
        if not isinstance (page ,dict ):
            continue 

        blocks =page .get ("para_blocks",[])
        for block in blocks :
        # Look for table blocks
            if not isinstance (block ,dict )or block .get ("type")!="table":
                continue 

                # Find the table body within the table blocks
            table_body =None 
            for sub_block in block .get ("blocks",[]):
                if sub_block .get ("type")=="table_body":
                    table_body =sub_block 
                    break 

            if not table_body :
                continue 

                # Process each line in the table body
            for line in table_body .get ("lines",[]):
                for span in line .get ("spans",[]):
                    if span .get ("type")=="table"and "html"in span :
                        try :
                            from bs4 import BeautifulSoup 
                            soup =BeautifulSoup (span ["html"],'html.parser')

                            # Extract caption if available
                            caption =""
                            for cap_block in block .get ("blocks",[]):
                                if cap_block .get ("type")=="table_caption":
                                    for cap_line in cap_block .get ("lines",[]):
                                        for cap_span in cap_line .get ("spans",[]):
                                            if cap_span .get ("type")=="text":
                                                caption +=cap_span .get ("content","")+" "

                                                # Extract table data
                            table_data =[]
                            for row in soup .find_all ('tr'):
                                row_data =[cell .get_text (strip =True )for cell in row .find_all (['th','td'])]
                                table_data .append (row_data )

                            if not table_data :
                                continue 

                                # Format table text with caption
                            table_text =f"Table: {caption .strip ()}\n\n"if caption .strip ()else ""
                            table_text +="\n".join ([" | ".join (row )for row in table_data ])

                            prompt =f"{table_summary_prompt }\n\n{table_text }"

                            response =client .chat .completions .create (
                            model =table_summary_config .get ("model","gpt-3.5-turbo"),
                            messages =[{'role':'user','content':prompt }],
                            temperature =0.3 ,
                            max_tokens =table_summary_config .get ("max_tokens",500 ),
                            timeout =60 
                            )

                            if response .choices and len (response .choices )>0 :
                                summary =response .choices [0 ].message .content .strip ()
                                if summary :
                                # Add summary to the table span
                                    span ["summary"]=summary 
                                    logger .debug (f"Generated summary for table on page {page_num }")

                        except Exception as e :
                            logger .warning (f"Failed to generate table summary: {e }")
                            continue 


def llm_aided_image_summary (pdf_info_dict ,image_summary_config ,images_dir ):
    if not pdf_info_dict or not image_summary_config or not images_dir :
        logger .debug ("Skipping image summary: missing required parameters")
        return 

    try :
        client =OpenAI (
        api_key =image_summary_config .get ("api_key",""),
        base_url =image_summary_config .get ("base_url","https://api.openai.com/v1"),
        timeout =60.0 
        )
        logger .debug ("Initialized OpenAI client for image summarization")
    except Exception as e :
        logger .error (f"Failed to initialize OpenAI client: {e }")
        return 

    image_count =0 
    processed_count =0 

    logger .debug (f"Using images directory: {images_dir }")

    if not os .path .exists (images_dir ):
        logger .warning (f"Images directory does not exist: {images_dir }")
        return 

    def extract_image_path_from_block (block ):
        """Recursively extract image path from block structure"""
        # Check if block has direct image_path
        if "image_path"in block and block .get ("type")=="image":
            return block ["image_path"]

            # Check in spans
        if "spans"in block :
            for span in block ["spans"]:
                if isinstance (span ,dict )and span .get ("type")=="image"and "image_path"in span :
                    return span ["image_path"]

                    # Check in lines and their spans
        if "lines"in block :
            for line in block ["lines"]:
                if not isinstance (line ,dict ):
                    continue 

                    # Check line's spans
                if "spans"in line :
                    for span in line ["spans"]:
                        if isinstance (span ,dict )and span .get ("type")=="image"and "image_path"in span :
                            return span ["image_path"]

                            # Check line itself
                if "image_path"in line and line .get ("type")=="image":
                    return line ["image_path"]

                    # Check in blocks array if present
        if "blocks"in block :
            for sub_block in block ["blocks"]:
                result =extract_image_path_from_block (sub_block )
                if result :
                    return result 

        return None 

    for page_num ,page in pdf_info_dict .items ():
        if not isinstance (page ,dict ):
            logger .debug (f"Skipping non-dict page: {page_num }")
            continue 

        blocks =page .get ("para_blocks",[])
        if not blocks :
            logger .debug (f"No blocks found in page {page_num }")
            continue 

        logger .debug (f"Processing page {page_num } with {len (blocks )} blocks")

        for block in blocks :
            if not isinstance (block ,dict ):
                logger .debug ("Skipping non-dict block")
                continue 

                # Extract image path from block structure
            image_filename =extract_image_path_from_block (block )

            if not image_filename :
                logger .debug (f"No image path found in block of type: {block .get ('type','unknown')}")
                continue 

            logger .debug (f"Found image path in block: {image_filename }")

            # Get just the filename part in case it includes a path
            image_basename =os .path .basename (image_filename )
            full_image_path =os .path .join (images_dir ,image_basename )

            # Try alternative paths if needed
            if not os .path .exists (full_image_path ):
            # Try with PDF hash subdirectory
                pdf_hash =os .path .basename (os .path .dirname (images_dir ))
                alt_path =os .path .join (images_dir ,pdf_hash ,image_basename )
                if os .path .exists (alt_path ):
                    full_image_path =alt_path 
                    logger .debug (f"Found image at alternative path: {full_image_path }")
                else :
                    logger .warning (f"Image file not found at either path: {full_image_path } or {alt_path }")
                    continue 
            logger .debug (f"Looking for image at: {full_image_path }")

            if not os .path .exists (full_image_path ):
                logger .warning (f"Image file not found: {full_image_path }")
                continue 

            image_count +=1 

            try :
                logger .debug (f"Processing image: {full_image_path }")
                with open (full_image_path ,"rb")as image_file :
                    image_data =image_file .read ()
                    if not image_data :
                        logger .warning (f"Image file is empty: {full_image_path }")
                        continue 

                    image_b64 =base64 .b64encode (image_data ).decode ('utf-8')
                    logger .debug (f"Image loaded successfully, size: {len (image_data )} bytes")

                    model =image_summary_config .get ("model","gpt-4-vision-preview")
                    logger .debug (f"Using model: {model }")

                    response =client .chat .completions .create (
                    model =model ,
                    messages =[{
                    "role":"user",
                    "content":[
                    {"type":"text","text":"Please describe this image in detail."},
                    {
                    "type":"image_url",
                    "image_url":{
                    "url":f"data:image/jpeg;base64,{image_b64 }"
                    }
                    }
                    ]
                    }],
                    max_tokens =image_summary_config .get ("max_tokens",300 ),
                    temperature =0.3 ,
                    timeout =60 
                    )

                    if response .choices and len (response .choices )>0 :
                        summary =response .choices [0 ].message .content .strip ()
                        if summary :
                            block ["summary"]=summary 
                            processed_count +=1 
                            logger .debug (f"Generated summary for image on page {page_num }")
                        else :
                            logger .warning (f"Empty summary returned for image on page {page_num }")
                    else :
                        logger .warning (f"No choices in response for image on page {page_num }")

            except Exception as e :
                logger .error (f"Failed to generate image summary for {full_image_path }: {str (e )}",exc_info =True )
                continue 

    logger .info (f"Processed {processed_count } out of {image_count } images")


def llm_aided_page_summary (pdf_info_dict ,page_summary_config ):
    if not pdf_info_dict or not page_summary_config :
        logger .warning ("Invalid input parameters for llm_aided_page_summary")
        return 

    try :
        client =OpenAI (
        api_key =page_summary_config .get ("api_key",""),
        base_url =page_summary_config .get ("base_url","https://api.openai.com/v1"),
        timeout =90.0 
        )
    except Exception as e :
        logger .error (f"Failed to initialize OpenAI client: {e }")
        return 

    for page_num ,page in pdf_info_dict .items ():
        if not isinstance (page ,dict ):
            continue 

        blocks =page .get ("para_blocks",[])
        if not blocks :
            continue 

        page_text =extract_text_from_blocks (blocks )
        if not page_text .strip ():
            continue 

        try :
            prompt =f"""Please provide a concise summary of the following page content. 
Focus on the main points and key information. Keep it brief but informative.

Page content:
{page_text }

Summary:"""

            response =client .chat .completions .create (
            model =page_summary_config .get ("model","gpt-3.5-turbo"),
            messages =[{"role":"user","content":prompt }],
            temperature =0.3 ,
            max_tokens =page_summary_config .get ("max_tokens",500 ),
            timeout =90 
            )

            if response .choices and len (response .choices )>0 :
                summary =response .choices [0 ].message .content .strip ()
                if summary :
                    page ["page_summary"]=summary 
                    logger .debug (f"Generated summary for page {page_num }")
                    logger .debug (f"Page text length: {len (page_text )} characters")

        except Exception as e :
            logger .warning (f"Failed to generate page summary for page {page_num }: {str (e )}")
            if 'page_text'in locals ()and page_text :
                logger .debug (f"Page content that caused error: {page_text [:500 ]}...")# Log first 500 chars for debugging
            continue 


def extract_text_from_blocks (blocks ):
    """Extract and concatenate text from all text blocks."""
    page_text =""
    for block in blocks :
        if not isinstance (block ,dict ):
            continue 

        block_type =block .get ("type")

        if block_type =="text":
            text =merge_para_with_text (block )
            if text :
                page_text +=text +"\n\n"
        elif block_type =="table"and "table_body"in block :
        # Handle table content
            for line in block ["table_body"].get ("lines",[]):
                for span in line .get ("spans",[]):
                    if span .get ("type")=="text":
                        page_text +=span .get ("content","")+" "
                page_text +="\n"
            page_text +="\n"

    return page_text .strip ()


def llm_aided_table_enhancement (pdf_info_dict ,table_enhance_config ):
    if not pdf_info_dict or not table_enhance_config :
        logger .warning ("No PDF info or table enhancement config provided")
        return 

    provider =table_enhance_config .get ('provider','openai').lower ()
    provider_config =table_enhance_config .get (provider ,{})

    logger .debug (f"Using {provider } for table enhancement")
    logger .debug (f"Provider config: {provider_config }")

    api_key =provider_config .get ('api_key')
    if not api_key :
        logger .error (f"No API key provided for {provider }")
        return 

    tables_processed =0 
    total_tables_found =0 

    for page_num ,page in pdf_info_dict .items ():
        if not isinstance (page ,dict ):
            logger .debug (f"Skipping page {page_num }: not a dictionary")
            continue 

        blocks =page .get ('para_blocks',[])
        logger .debug (f"Processing page {page_num } with {len (blocks )} blocks")

        if not blocks :
            logger .debug (f"No blocks found on page {page_num }")
            continue 

        for block_idx ,block in enumerate (blocks ):
            if not isinstance (block ,dict ):
                logger .debug (f"Skipping block {block_idx } on page {page_num }: not a dictionary")
                continue 

            block_type =block .get ('type')
            logger .debug (f"Block {block_idx } type: {block_type }")

            if block_type !='table':
                logger .debug (f"Skipping non-table block of type: {block_type }")
                continue 

            table_image_path =block .get ('image_path')
            logger .debug (f"Found table on page {page_num } with image path: {table_image_path }")

            if not table_image_path :
                logger .debug (f"Skipping table without image path on page {page_num }")
                continue 

            total_tables_found +=1 

            try :
                logger .debug (f"Enhancing table {tables_processed +1 } on page {page_num }")
                enhanced_html =enhance_table_with_llm (
                table_image_path =table_image_path ,
                config =provider_config 
                )

                if not enhanced_html :
                    logger .warning (f"Failed to enhance table on page {page_num }")
                    continue 

                # Parse the enhanced HTML and extract the table
                soup =BeautifulSoup (enhanced_html ,'html.parser')
                table =soup .find ('table')
                if table :
                    block ['table_body']=str (table )
                    tables_processed +=1 
                    logger .debug (f"Successfully enhanced table {tables_processed } on page {page_num }")
                else :
                    logger .warning ("No valid table found in LLM response")

            except Exception as e :
                logger .error (f"Error enhancing table: {str (e )}",exc_info =True )
                continue 

    logger .info (f"Table enhancement completed. Found {total_tables_found } tables, processed {tables_processed } tables.")
    if total_tables_found ==0 :
        logger .warning ("No tables were found in the document. Check if the document contains tables and if they are being properly detected.")

TABLE_EXTRACTION_PROMPT = """Extract the table structure from the provided image and return it as a well-formatted HTML table. Most images contain a single table, but occasionally there may be multiple tables. If multiple tables are present, split them into separate tables.

Follow these guidelines:
1. Preserve all text content exactly as shown
2. Maintain the correct row and column structure
3. Use <th> for header cells and <td> for data cells
4. Use rowspan and colspan where cells span multiple rows/columns
5. Do not include any explanations or markdown formatting
6. Do not add any newline characters (\n) between HTML tags
7. Only include newlines within the content of table cells only when needed for readability
8. Return ONLY the HTML table with no additional text or explanations

Example of correct format: <table><tr><th>Header</th></tr><tr><td>Data</td></tr></table>
"""

def enhance_table_with_gemini(table_image_path: str, config: Dict[str, Any]) -> Optional[str]:
    """Enhance table by extracting structure from image using Google's Gemini model.
    
    Args:
        table_image_path (str): Path to the table image
        config (dict): Configuration for Gemini API
        
    Returns:
        str: Extracted HTML table or None if failed
    """
    try:
        import google.generativeai as genai

        genai.configure(api_key=config.get("api_key", ""))
        model = genai.GenerativeModel(config.get("model", "gemini-1.5-flash"))

        if not os.path.exists(table_image_path):
            logger.error(f"Table image not found: {table_image_path}")
            return None

        # Read the image file as binary
        with open(table_image_path, "rb") as image_file:
            image_data = image_file.read()

        # Create the prompt parts
        prompt_parts = [
            TABLE_EXTRACTION_PROMPT,
            {"mime_type": "image/jpeg", "data": base64.b64encode(image_data).decode('utf-8')}
        ]

        # Generate content
        response = model.generate_content(
            prompt_parts,
            generation_config={
                "max_output_tokens": config.get("max_tokens", 8192),
                "temperature": config.get("temperature", 0.1),
            }
        )

        enhanced_html = response.text.strip()

        # Basic validation
        if "<table" not in enhanced_html or "</table>" not in enhanced_html:
            logger.warning("Gemini response doesn't contain a valid table")
            return None

        return enhanced_html

    except Exception as e:
        logger.error(f"Error enhancing table with Gemini: {e}")
        return None

def encode_image_to_base64(image_path: str) -> Optional[str]:
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        logger.error(f"Error encoding image to base64: {e}")
        return None

def enhance_table_with_openai_vision(table_image_path: str, config: Dict[str, Any]) -> Optional[str]:
    """Enhance table by extracting structure from image using OpenAI's Vision API.
    
    Args:
        table_image_path (str): Path to the table image
        config (dict): Configuration for OpenAI API
        
    Returns:
        str: Extracted HTML table or None if failed
    """
    try:
        client = OpenAI(api_key=config.get("api_key"))
        
        # Encode the image to base64
        base64_image = encode_image_to_base64(table_image_path)
        if not base64_image:
            return None
            
        prompt = """Extract the table structure from the provided image and return it as a well-formatted HTML table. 
        Follow these guidelines:
        1. Preserve all text content exactly as shown
        2. Maintain the correct row and column structure
        3. Use <th> for header cells and <td> for data cells
        4. Use rowspan and colspan where cells span multiple rows/columns
        5. Do not include any explanations or markdown formatting
        6. Do not add any newline characters (\n) between HTML tags
        7. Only include newlines within the content of table cells when needed for readability
        8. Return ONLY the HTML table with no additional text or explanations
        Example of correct format: <table><tr><th>Header</th></tr><tr><td>Data</td></tr></table>
        """
        
        response = client.chat.completions.create(
            model=config.get("model", "gpt-4-vision-preview"),
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}",
                                "detail": "high"
                            },
                        },
                    ],
                }
            ],
            max_tokens=config.get("max_tokens", 4000),
            temperature=config.get("temperature", 0.1),
        )

        enhanced_html = response.choices[0].message.content.strip()
        
        # Clean up the response to ensure it's valid HTML
        if "```html" in enhanced_html:
            enhanced_html = enhanced_html.replace("```html", "").replace("```", "").strip()
        
        # Basic validation
        if "<table" not in enhanced_html or "</table>" not in enhanced_html:
            logger.warning("OpenAI Vision response doesn't contain a valid table")
            return None
            
        return enhanced_html
        
    except Exception as e:
        logger.error(f"Error enhancing table with OpenAI Vision: {e}")
        return None

def enhance_table_with_llm(table_image_path: str, config: Dict[str, Any]) -> Optional[str]:
    logger.debug(f"Starting table extraction from image. Config: {json.dumps(config, indent=2)}")

    if not table_image_path:
        logger.warning("No table image path provided")
        return None

    if not config.get("enable", False):
        logger.debug("Table enhancement is disabled in config")
        return None

    provider = config.get("provider", "gemini").lower()
    logger.debug(f"Using LLM provider: {provider}")

    try:
        if provider == "gemini":
            gemini_config = config.get("gemini", {})
            if not gemini_config.get("api_key"):
                logger.error("No API key found for Gemini")
                return None
            return enhance_table_with_gemini(table_image_path, gemini_config)
            
        elif provider == "openai":
            openai_config = config.get("openai", {})
            if not openai_config.get("api_key"):
                logger.error("No API key found for OpenAI")
                return None
            return enhance_table_with_openai_vision(table_image_path, openai_config)
            
        else:
            logger.warning(f"Unsupported LLM provider: {provider}")
            return None

    except Exception as e:
        logger.error(f"Error in table extraction: {str(e)}", exc_info=True)
        return None


def process_enrichments (pdf_info_dict ,enrichment_config ,images_dir =None ):
    if not pdf_info_dict or not enrichment_config :
        logger .debug ("Skipping enrichments: No PDF info or enrichment config provided")
        return 

        # Process table enhancement if enabled
    table_enhance_config =enrichment_config .get ('table_enhancement',{})
    if table_enhance_config and table_enhance_config .get ('enable',False ):
        logger .debug ("Starting table enhancement processing")
        from parsit .post_proc .table_enhancement import llm_aided_table_enhancement 
        llm_aided_table_enhancement (pdf_info_dict ,table_enhance_config ,images_dir )
    else :
        logger .debug (f"Table enhancement not enabled. Config: {table_enhance_config }")

        # Process table summaries if enabled
    table_config =enrichment_config .get ('table_summary',{})
    if table_config and table_config .get ('enable',False ):
        llm_aided_table_summary (pdf_info_dict ,table_config )

        # Process image summaries if enabled
    if enrichment_config .get ('image_summary',{}).get ('enable',False ):
        if not images_dir :
            logger .warning ("No images directory provided for image summarization")
            return 

        llm_aided_image_summary (
        pdf_info_dict ,
        enrichment_config ['image_summary'],
        images_dir 
        )

        # Process page summaries if enabled
    if enrichment_config .get ('page_summary',{}).get ('enable',False ):
        llm_aided_page_summary (
        pdf_info_dict ,
        enrichment_config ['page_summary']
        )

        # Process text block summaries if enabled
    if enrichment_config .get ('text_block_summary',{}).get ('enable',False ):
        llm_aided_text_block_summary (
        pdf_info_dict ,
        enrichment_config ['text_block_summary']
        )