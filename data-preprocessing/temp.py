import re

def filter_transaction_description(transaction_description):
    cib_ref_number_regex = r"^FT.{12}$"
    generic_ref_regex = r"\w*\d\w*[a-zA-Z]\w*|\w*[a-zA-Z]\w*\d\w*"
    numbers_regex = r"\d+"
    single_letter_regex = r"\b\w\b"

    text = re.sub(cib_ref_number_regex, '', transaction_description)
    text = re.sub(generic_ref_regex, '', text)
    text = re.sub(numbers_regex, '', text)
    text = re.sub(single_letter_regex, '', text)
    text = text.replace("-", "")
    text = re.sub("\s\s+" , " ", text)
    return text.strip()
    
print(filter_transaction_description("FT23054QW6N9 - ACH(ACH07000005537) RTIN(SALARY FO"))
