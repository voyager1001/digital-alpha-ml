# Digital-Alpha-ML


### Files Description

1. dict-sentiment.ipynb  -> For sentiment analysis(6 classes - lexicon based)

    - Input: The input of the file is specified in the `temp_text` variable. 
    - Output: The input is passed to the `get_class_counter` function, which returns the sentiment dictionary containing the results.


2. finbert_inference.ipynb -> For sentiment analysis(3 classes - transformer)

    - Input: The input of the file is specified in the `temp_text` variable.
    - Output; The input is passed to the `get_output` function, which returns the sentiment dictionary.


3. mdna_extractor.ipynb -> For extracting contents(section wise)

    - Input: The input to the function is the `filing_url` and `section_name`, where the names have their usual meanings
    - Output: The output is obtained from the `get_section` function, which returns the desired section text

4. find_company_trends_using_lda.py -> For extracting the latest trending topics relevant to the company

    - Input: The input to the file is the company title and the number of tweets we want to extract
    - Output: The output of the file is the top 5 topics relevant to the company

5. extract_metrics_from_fillings.ipynb -> For extracting metrics from the fillings

    - Input: The inputs are:
        * `api_key` - for accessing the fillings using sec-api
        * `url` - url to the filing
        * `metric` - name of the metric in lowercase
        * `val_type` - metric data type - one of ['PERCENT', 'MONEY', 'NUMBER', 'RATIO']
        * `k` - window size for metric search, default = 6
        * `relevant_sections` - list of sections to search for the metric
    - Output: The output of the file is value of the metric extracted from the filing stored in `correct_value` variable