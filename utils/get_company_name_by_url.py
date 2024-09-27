from urllib.parse import urlparse
import traceback












def func_get_company_name(url):
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc

        # Remove "www." if it exists
        if domain.startswith("www."):
            domain = domain[4:]

        # Get the company name (first part of the domain)
        company_name = domain.split('.')[0]

        # Capitalize the company name
        company_name = company_name.capitalize()

        return company_name
    except Exception as e:
        print(f"{str(e)}")
        traceback.print_exc() 
        return "anonymous"