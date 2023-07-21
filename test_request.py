from bs4 import BeautifulSoup
import requests
import pandas as pd

data_append = []
def get_urls(product_url):
    response = requests.get(product_url)
    soup = BeautifulSoup(response.text,'html.parser')
    url_data = []
    for url in soup.find_all('a',class_='btn-gbdr'):
        urls = url['href']
        url_data.append(urls)
    return url_data

# ... (get_urls function remains the same)

def extract_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = {}

    # Handle the case when the name element is not found
    name_element = soup.find('div', class_='fw700 f16')
    if name_element:
        name = name_element.text.strip()
        data['name'] = name
    else:
        data['name'] = 'Name not found'

    specification = soup.find(id='product_details').find_all(class_='col-md-12')
    spec = {}
    for item in specification:
        k_element = item.find(class_='col-md-4 fw700')
        v_element = item.find(class_='col-md-8 fnormal')

        # Handle the case when the key or value element is not found
        k = k_element.text.replace('#', '').strip() if k_element else ''
        v = v_element.text.strip() if v_element else ''
        spec[k] = v

    data.update(spec)

    # Handle the case when images element is not found
    images = soup.find('div', {'data-target': '#carousel'})
    if images:
        img = '|'.join([x['src'] for x in images])
        data['images'] = img
    else:
        data['images'] = ''

    data_append.append(data)
    df = pd.DataFrame(data_append)
    csv_file = 'ops.csv'
    df.to_csv(csv_file,index=False)
    print(df)
    


    
def main():
    # Example usage
    product_url = "https://www.idealfloors.com/products/carpet-flooring"  # Replace this with the desired search term
    main_urls = get_urls(product_url)

    if main_urls:
        # Create an empty list to hold the data dictionaries
        for url in main_urls:
            print(url)
            extract_data(url)

if __name__ == "__main__":
    main()














