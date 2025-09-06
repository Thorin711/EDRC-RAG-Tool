# -*- coding: utf-8 -*-
"""
This script processes PDF files using the GROBID client.

It takes an input directory of PDF files, processes them using the GROBID
service, and saves the output as XML files in a specified output directory.
This is the first step in the document processing pipeline, preparing the
raw PDF documents for further analysis and inclusion in the vector database.
"""

from grobid_client.grobid_client import GrobidClient

#----------------PDF process-------------------
# Create client instance
client = GrobidClient(grobid_server="http://localhost:8070")

in_path = r"C:\Users\td00654\OneDrive - University of Surrey\Documents\EDRC LLM Project\Papers\EDRC - PDF"
out_path = r"C:\Users\td00654\OneDrive - University of Surrey\Documents\EDRC LLM Project\Papers\EDRC - HTML"
# Process documents
client.process("processFulltextDocument", in_path, out_path, n=10)
