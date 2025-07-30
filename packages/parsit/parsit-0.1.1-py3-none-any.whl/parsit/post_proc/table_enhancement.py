import os 
import time 
import json 
import base64 
import re 
from typing import Dict ,Any ,Optional ,List ,Tuple 
from loguru import logger 
from bs4 import BeautifulSoup 

from parsit .post_proc .llm_aided import enhance_table_with_llm 

def clean_llm_output (html_content :str )->str :
    """Clean up LLM output by removing unwanted HTML/Markdown artifacts.
    
    Args:
        html_content: Raw HTML content from LLM
        
    Returns:
        Cleaned HTML content with only the table and its contents, without HTML/BODY tags
    """
    if not html_content :
        return ""

        # Remove markdown code block markers if present
    html_content =re .sub (r'```(?:html)?\s*','',html_content )
    html_content =re .sub (r'\s*```','',html_content )

    # First try to clean with regex for simple cases
    html_content =re .sub (r'<!?doctype[^>]*>','',html_content ,flags =re .IGNORECASE )
    html_content =re .sub (r'<html[^>]*>','',html_content ,flags =re .IGNORECASE )
    html_content =re .sub (r'</html>','',html_content ,flags =re .IGNORECASE )
    html_content =re .sub (r'<head>.*?</head>','',html_content ,flags =re .IGNORECASE |re .DOTALL )
    html_content =re .sub (r'<body[^>]*>','',html_content ,flags =re .IGNORECASE )
    html_content =re .sub (r'</body>','',html_content ,flags =re .IGNORECASE )

    try :
    # Parse the HTML with BeautifulSoup
        soup =BeautifulSoup (html_content ,'html.parser')

        # Find the first table in the document
        table =soup .find ('table')
        if table :
        # Convert table to string and clean any remaining tags
            result =str (table )
            # Final cleanup of any remaining HTML/BODY tags that might have been in table content
            result =re .sub (r'</?html[^>]*>','',result ,flags =re .IGNORECASE )
            result =re .sub (r'</?body[^>]*>','',result ,flags =re .IGNORECASE )
            return result .strip ()

            # If no table found, try to find any HTML content
        body =soup .find ('body')
        if body :
            result =''.join (str (tag )for tag in body .contents )
            result =re .sub (r'</?html[^>]*>','',result ,flags =re .IGNORECASE )
            result =re .sub (r'</?body[^>]*>','',result ,flags =re .IGNORECASE )
            return result .strip ()

            # If no body, return the entire parsed content with cleaned tags
        result =str (soup )
        result =re .sub (r'</?html[^>]*>','',result ,flags =re .IGNORECASE )
        result =re .sub (r'</?body[^>]*>','',result ,flags =re .IGNORECASE )
        return result .strip ()

    except Exception as e :
        logger .warning (f"Error parsing HTML with BeautifulSoup: {str (e )}")
        # Final cleanup of any remaining HTML/BODY tags
        html_content =re .sub (r'</?html[^>]*>','',html_content ,flags =re .IGNORECASE )
        html_content =re .sub (r'</?body[^>]*>','',html_content ,flags =re .IGNORECASE )
        html_content =re .sub (r'<!--.*?-->','',html_content ,flags =re .DOTALL )
        html_content =html_content .strip ()

        # Extract just the table if it exists
        table_match =re .search (r'(<table[^>]*>.*?</table>)',html_content ,re .DOTALL |re .IGNORECASE )
        if table_match :
            return table_match .group (1 )

    return html_content 


def extract_table_html (block :Dict )->Tuple [Optional [str ],Optional [str ]]:
    """Extract table HTML and image path from a block using multiple fallback strategies."""
    # Check nested blocks structure first
    if 'blocks'in block and isinstance (block ['blocks'],list ):
        for b in block ['blocks']:
            if not isinstance (b ,dict ):
                continue 

            if 'lines'in b and isinstance (b ['lines'],list ):
                for line in b ['lines']:
                    for span in line .get ('spans',[]):
                        if isinstance (span ,dict )and 'html'in span and '<table'in span ['html'].lower ():
                            return span ['html'],span .get ('image_path')

                            # Check main block spans
    if 'lines'in block :
        for line in block .get ('lines',[]):
            for span in line .get ('spans',[]):
                if not isinstance (span ,dict ):
                    continue 
                if 'html'in span and '<table'in span ['html'].lower ():
                    return span ['html'],span .get ('image_path')

                    # Check table_body
    if 'table_body'in block and isinstance (block ['table_body'],dict ):
        tb =block ['table_body']
        if 'html'in tb and '<table'in tb ['html'].lower ():
            return tb ['html'],tb .get ('image_path')

            # Last resort: check the block itself
    if 'html'in block and '<table'in block ['html'].lower ():
        return block ['html'],block .get ('image_path')

    return None ,None 

def resolve_image_path (image_path :str ,images_dir :str )->Optional [str ]:
    """Resolve relative image path to absolute path."""
    if not image_path or not images_dir or os .path .isabs (image_path ):
        return image_path 

        # Try direct path first
    potential_path =os .path .join (images_dir ,image_path )
    if os .path .exists (potential_path ):
        return potential_path 

        # Try filename only
    image_name =os .path .basename (image_path )
    potential_path =os .path .join (images_dir ,image_name )
    if os .path .exists (potential_path ):
        return potential_path 

        # Try to find similar filename
    for root ,_ ,files in os .walk (images_dir ):
        for file in files :
            if file ==image_name or file .startswith (os .path .splitext (image_name )[0 ]):
                return os .path .join (root ,file )

    return None 

def llm_aided_table_enhancement (pdf_info_dict :Dict ,table_enhance_config :Dict ,images_dir :str =None )->None :
    """Enhance all tables in the PDF using LLM.
    
    Args:
        pdf_info_dict: Dictionary containing PDF page information
        table_enhance_config: Configuration for table enhancement
        images_dir: Directory containing extracted images (optional)
    """
    logger .debug ("Starting table enhancement process")

    if not pdf_info_dict or not table_enhance_config :
        logger .warning ("No PDF info or config provided - skipping table enhancement")
        return 

    if not table_enhance_config .get ('enable',False ):
        logger .debug ("Table enhancement is disabled in config")
        return 

    logger .debug (f"Table enhancement config: {json .dumps (table_enhance_config ,indent =2 ,default =str )}")

    start_time =time .time ()
    stats ={
    'tables_found':0 ,
    'tables_processed':0 ,
    'tables_skipped':0 ,
    'tables_failed':0 ,
    'pages_processed':0 
    }

    # Process each page in the PDF
    for page_key ,page_info in pdf_info_dict .items ():
        if not page_key .startswith ('page_'):
            continue 

        blocks =page_info .get ('para_blocks',[])
        logger .debug (f"Processing page {page_key } with {len (blocks )} blocks")
        stats ['pages_processed']+=1 

        for block_idx ,block in enumerate (blocks ):
            if not isinstance (block ,dict ):
                logger .debug (f"Skipping non-dict block at index {block_idx } in {page_key }")
                continue 

            block_type =block .get ('type')
            if block_type !='table':
                continue 

            stats ['tables_found']+=1 
            table_num =stats ['tables_found']
            table_id =f"{page_key }_block{block_idx }"

            logger .info (f"Processing table {table_num } ({table_id })")

            # Extract table HTML and image path
            table_html ,table_image_path =extract_table_html (block )

            if not table_html :
                logger .warning (f"Skipping table {table_num }: No HTML content found")
                stats ['tables_skipped']+=1 
                continue 

                # Resolve image path if available
            if table_image_path and images_dir :
                table_image_path =resolve_image_path (table_image_path ,images_dir )
                if table_image_path and not os .path .exists (table_image_path ):
                    logger .warning (f"Table image not found at {table_image_path }")
                    table_image_path =None 

                    # Skip if config requires images but we don't have one
            if table_enhance_config .get ('require_image',False )and not table_image_path :
                logger .warning (f"Skipping table {table_num }: Image required but not found")
                stats ['tables_skipped']+=1 
                continue 

                # Process the table with LLM enhancement
            try :
                logger .debug (f"Enhancing table {table_num } in {page_key }")
                logger .debug (f"Table HTML (first 200 chars): {table_html[:200]}...")
                logger .debug (f"Table image path: {table_image_path}")

                # Get enhanced HTML from LLM - only pass the image path and config
                enhanced_html = enhance_table_with_llm(table_image_path, table_enhance_config)

                # Clean up the LLM output
                if enhanced_html :
                    enhanced_html =clean_llm_output (enhanced_html )
                    logger .debug (f"Cleaned HTML (first 200 chars): {enhanced_html [:200 ]}..."if enhanced_html else "No cleaned HTML")
                else :
                    logger .warning ("No enhanced HTML returned from LLM")

                if not enhanced_html :
                    logger .warning (f"No enhanced HTML returned for table {table_num }")
                    stats ['tables_failed']+=1 
                    continue 

                try:
                    # Parse the enhanced HTML to ensure it's valid
                    soup = BeautifulSoup(enhanced_html, 'html.parser')
                    enhanced_table = soup.find('table')
                    
                    if not enhanced_table:
                        logger.warning(f"No table found in enhanced HTML for table {table_num}")
                        stats['tables_failed'] += 1
                        continue
                        
                    # Update the block with enhanced HTML
                    table_updated = False
                    
                    # Debug log the block structure
                    logger.debug(f"Block structure for table {table_num}: {json.dumps(block, default=str, indent=2)}")
                    
                    # Function to update table in a block
                    def update_table_in_block(block_data):
                        nonlocal table_updated
                        if table_updated:
                            return
                            
                        # Check for nested blocks first
                        if 'blocks' in block_data and isinstance(block_data['blocks'], list):
                            for sub_block in block_data['blocks']:
                                if update_table_in_block(sub_block):
                                    return True
                                    
                        # Check for spans structure
                        if 'spans' in block_data or 'lines' in block_data:
                            lines = block_data.get('lines', [])
                            if not lines and 'spans' in block_data:
                                lines = [{'spans': block_data['spans']}]
                                
                            for line in lines:
                                for span in line.get('spans', []):
                                    if not isinstance(span, dict):
                                        continue
                                        
                                    # Check if this span is a table or contains HTML
                                    if (span.get('type') == 'table' or 'html' in span) and 'html' in span:
                                        span['original_html'] = span.get('html', '')
                                        span['html'] = str(enhanced_table)
                                        span['enhanced'] = True
                                        table_updated = True
                                        logger.info(f"Enhanced table {table_num} in document structure (nested spans)")
                                        return True
                        
                        # Check for direct HTML
                        if 'html' in block_data and not table_updated:
                            block_data['original_html'] = block_data.get('html', '')
                            block_data['html'] = str(enhanced_table)
                            block_data['enhanced'] = True
                            table_updated = True
                            logger.info(f"Enhanced table {table_num} in document structure (direct HTML)")
                            return True
                            
                        # Check for table_body structure
                        if 'table_body' in block_data and isinstance(block_data['table_body'], dict):
                            if 'html' in block_data['table_body']:
                                block_data['table_body']['original_html'] = block_data['table_body'].get('html', '')
                                block_data['table_body']['html'] = str(enhanced_table)
                                block_data['table_body']['enhanced'] = True
                                table_updated = True
                                logger.info(f"Enhanced table {table_num} in document structure (table_body)")
                                return True
                                
                        return False
                    
                    # Start the recursive update
                    update_table_in_block(block)
                    
                    if table_updated:
                        stats['tables_processed'] += 1
                        logger.info(f"Successfully enhanced table {table_num} in {page_key}")
                    else:
                        logger.warning(f"Failed to update table {table_num} in document structure. Block keys: {list(block.keys())}")
                        stats['tables_failed'] += 1

                except Exception as e:
                    logger.error(f"Error processing enhanced HTML for table {table_num}: {str(e)}")
                    stats['tables_failed'] += 1 

            except Exception as e :
                logger .error (f"Error enhancing table {table_num }: {str (e )}")
                stats ['tables_failed']+=1 

                # Log summary statistics
    end_time =time .time ()
    duration =end_time -start_time 

    if stats ['tables_found']==0 :
        logger .warning ("No tables were found in the document. Check if the document contains tables and if they are being properly detected.")
    else :
        summary =(
        f"Table processing complete. "
        f"Pages: {stats ['pages_processed']}, "
        f"Tables: Found={stats ['tables_found']}, "
        f"Processed={stats ['tables_processed']}, "
        f"Skipped={stats ['tables_skipped']}, "
        f"Failed={stats ['tables_failed']}, "
        f"Time: {duration :.2f}s"
        )

        logger .info (summary )

        if stats ['tables_failed']>0 or stats ['tables_skipped']>0 :
            logger .warning (
            f"Some tables were not processed successfully. "
            f"Check the logs for details on skipped or failed tables."
            )


def _find_table_image (images_dir :str ,page_key :str ,bbox :List [float ])->Optional [str ]:
    """Find a table image in the given directory that matches the page key.
    
    Args:
        images_dir: Directory containing table images
        page_key: Page identifier (e.g., 'page_0')
        bbox: Bounding box coordinates [x0, y0, x1, y1]
        
    Returns:
        Full path to the matching image file, or None if not found
    """
    if not images_dir or not os .path .exists (images_dir ):
        return None 

    page_num =page_key .replace ('page_','')

    # Try multiple filename patterns
    patterns =[
    f"table_{page_key }*.png",
    f"table_{page_num }_*.png",
    f"table_*{page_num }*.png",
    f"*table*{page_num }*.png"
    ]

    for pattern in patterns :
        for filename in os .listdir (images_dir ):
            if not filename .lower ().endswith (('.png','.jpg','.jpeg')):
                continue 

            if filename .startswith (('table_',f"table{page_num }"))or f"table_{page_num }"in filename :
                return os .path .join (images_dir ,filename )

    return None 
