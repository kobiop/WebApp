import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time

#credit -  https://scrapeops.io/web-scraping-playbook/403-forbidden-error-web-scraping/#:~:text=Getting%20a%20HTTP%20403%20Forbidden,be%20authorised%20to%20access%20it

def random_user_agent():
    user_agents_list = [
    'Mozilla/5.0 (Linux; Android 7.0; Lenovo TB-7304F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.101 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 8.1.0; Lenovo TB-7104F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.119 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 7.0; Lenovo TB-7304F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.116 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; LCJB; rv:11.0) like Gecko',
    'Mozilla/5.0 (Linux; U; Android 4.4; ru-ru; Lenovo A7600-H Build/KRT16S) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.4 Mobile Safari/E7FBAF',
    'Mozilla/5.0 (Linux; Android 4.2.1; Lenovo P780 Build/JOP40D) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 YaBrowser/17.3.1.383.00 Mobile Safari/E7FBAF',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; MALNJS; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0; Touch; MALNJS)',
    'Mozilla/5.0 (Linux; Android 4.4; Lenovo A7600-H Build/KRT16S) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/E7FBAF',
    'Mozilla/5.0 (Linux; Android 4.4.2; Lenovo A3500-FL Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; MALNJS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Linux; Android 4.4; Lenovo A3500-H Build/KRT16S) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/E7FBAF',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; Tablet PC 2.0; MALC)']
    return { "User-Agent" : random.choice(user_agents_list)}


url = 'https://www.realtor.com/realestateandhomes-search/Chicago_IL/'    

response  = requests.get(url, headers= random_user_agent())
print(response)
soup = BeautifulSoup(response.text, "html.parser")
data = soup.find('section', attrs={'class':'PropertiesList_propertiesContainer__j6ct_'})
urls=[]
i=0
all_links=data.find_all('a',attrs={'class':'LinkComponent_anchor__2uAhr'})
for apart in all_links :
    link ='http://realtor.com'+apart['href']
    urls.append(link)


print("this is before remove dup ",len(urls))
urls=list(dict.fromkeys(urls))
print("this is after remove dup, ",len(urls))
price=[]
year_built=[]
sqft=[]
beds=[]
bathrooms=[]
price_sqft=[]
property_type=[]
garage=[]
HOA_fees=[]
address =[]
time_on_web=[]
sqft_lot=[]  
img_list=[]
k=1
for ur in urls:
    response2 = requests.get(ur, headers=random_user_agent())
    print(response2,k)
    k=k+1
    soup2 =BeautifulSoup(response2.text, "html.parser")
    data2 = soup2.find('div', attrs={'class':'LDPListingSummarystyles__ListingSummaryContainer-sc-6zw8z5-0 TxcCV'})
    
    
    img_link = soup2.find('img', attrs={'class':'carousel-photo'})
    if img_link!=None:
          img_list.append(img_link['src'])
    else:
         img_list.append(None)

    bed = data2.find('li', {'class':"PropertyBedMetastyles__StyledPropertyBedMeta-rui__a4nnof-0 cHVLag"})
    if bed != None:
            beds.append(bed.find("span").text)
    else:
        beds.append(None)
        

    bath = data2.find('li', {'class':"PropertyBathMetastyles__StyledPropertyBathMeta-rui__sc-67m6bo-0 bSPXLm"})
    if bath != None:
            bathrooms.append(bed.find("span").text)
    else:
            bathrooms.append(None)
        
        
    sqftD = data2.find("li", {"class":"PropertySqftMetastyles__StyledPropertySqftMeta-rui__sc-1gdau7i-0 fnhaOV"})
    if sqftD!=None:
        sqft.append(sqftD.find("span").text)
    else:
        sqft.append(None)
        
    sqft_lotD = data2.find("li", {"class": "PropertyLotSizeMetastyles__StyledPropertyLotSizeMeta-rui__sc-1cz4zco-0 cNMyen"})
    if sqft_lotD !=None:
        sqft_lot.append(sqft_lotD.find("span").text)
    else:
        sqft_lot.append(None)
        
    price.append(data2.find('div', attrs={'class':'Pricestyles__StyledPrice-rui__btk3ge-0 bvgLFe LDPListPricestyles__StyledPrice-sc-1m24xh0-1 jyBxDQ'}).text)
    address.append(data2.find('h1', attrs={'class':'LDPHomeFactsstyles__H1-sc-11rfkby-3 ibiqDI'}).text)
    headers=[]

    deats=data2.find('ul', attrs={'class':'ListingKeyFactsstyles__StyledListingKeyFacts-rui__sc-196zwd6-0 hqWKvj LDPHighlightedFactsstyles__StyledListingKeyFacts-sc-ogf6te-0 hSWA-DM'})
    for det in deats.find_all('div',attrs={'base__StyledType-rui__sc-108xfm0-0 bsZLXk listing-key-fact-item__label'}):    
             headers.append(det.find("span").text)

    a=[]        
    for det in deats.find_all('div',attrs={'class':'base__StyledType-rui__sc-108xfm0-0 gMZrrg listing-key-fact-item__value'}):    
                a.append(det.text)
           
    dictv={}
    for i in range(len(a)):
           dictv[headers[i]]=a[i] 
                       
    deats1 = soup2.find('ul', attrs={'class':'ListingKeyFactsstyles__StyledListingKeyFacts-rui__sc-196zwd6-0 hqWKvj LDPHighlightedFactsstyles__StyledListingKeyFacts-sc-ogf6te-0 hSWA-DM'})
    attrib2=['Time on realtor.com','Property type','HOA fees','Price per sqft','Garage','Year built']
    k=0
    for i in dictv:
        if i  in headers:
            if i == 'Property type':
               property_type.append(dictv[i])
            if i == 'Time on Realtor.com':
                time_on_web.append(dictv[i])
            if i == 'HOA fees':
                HOA_fees.append(dictv[i])
            if i == 'Price per sqft':
                price_sqft.append(dictv[i])
            if i == 'Garage':
                garage.append(dictv[i])
            if i == 'Year built':        
                year_built.append(dictv[i])
    print(dictv.keys())
    for i in attrib2:
        if i not in dictv.keys():
            if i == 'Property type':
                property_type.append(None)
            if i == 'Time on Realtor.com':
                time_on_web.append(None)
            if i == 'HOA fees':
                HOA_fees.append(None)
            if i == 'Price per sqft':
                price_sqft.append(None)
            if i == 'Garage':
                garage.append(None)
            if i == 'Year built':   
                year_built.append(None)

print("Length of 'price' array:", len(price))
print("Length of 'year built' array:", len(year_built))
print("Length of 'sqft' array:", len(sqft))
print("Length of 'beds' array:", len(beds))
print("Length of 'bathrooms' array:", len(bathrooms))
print("Length of 'price_sqft' array:", len(price_sqft))
print("Length of 'Property_Type' array:", len(property_type))
print("Length of 'garage' array:", len(garage))
print("Length of 'HOA Fees' array:", len(HOA_fees))
print("Length of 'Address' array:", len(address))
print("Length of 'Time On Web' array:", len(time_on_web))
print("Length of 'sqft lot' array:", len(sqft_lot))
print("Length of 'img_link' array:", len(img_list))                  
df=pd.DataFrame({"price":price,"year_built":year_built, "sqft":sqft,"beds":beds,"bathrooms":bathrooms,
               "price_per_sqft":price_sqft, "property_type":property_type,"garage":garage,"HOA_fees":HOA_fees,
               "address":address,"sqft_lot":sqft_lot ,"img_link":img_list})              

df.to_csv('apartments.csv')
                    
print(df)
