import traceback
from collections import Counter
import re




def func_extract_most_common_class(soup):
    try:
        # links = soup.find_all('a', href=True)
        links = soup
        valid_href_pattern = re.compile(r'^\/[^?]*$')
        class_names = []
        for link in links:
            href = link['href']
            if valid_href_pattern.match(href):  # Check if href is valid
                if 'class' in link.attrs:
                    class_names.extend(link['class'])
                
        class_count = Counter(class_names)
        most_common_class, max_count = class_count.most_common(1)[0] if class_count else (None, 0)
        print(f'Most common class: {most_common_class} occurs {max_count} times')
        return most_common_class
    except Exception as e:
        print(f"Some Error {str(e)}")
        traceback.print_exc()
        return None