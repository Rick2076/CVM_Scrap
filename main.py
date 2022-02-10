from requests import get
from bs4 import BeautifulSoup
from zipfile import ZipFile
import os

def main():
    url_base = "http://dados.cvm.gov.br/dados/CIA_ABERTA/"
    local = os.path.dirname(__file__) + "\\"

    BIG_LIST = find_zip(url_base)

    extract(local, BIG_LIST)

def find_zip(url_base):
    """
    This function will try to find the zipped files and make a list of them in format [[append, file_names, file_list],[append, file_names, file_list]]
    """
    try:
        appends = ["CAD","DOC/DFP","DOC/FCA","DOC/FRE","DOC/IPE","DOC/ITR"]
        BIG_LIST = []
        for append in appends:
            url = url_base + append + "/DADOS/"
            try:
                response = get(url)
                html_soup = BeautifulSoup(response.text, 'html.parser')
                Zip_collection_list_odd = html_soup.find_all("tr", class_="odd")
                Zip_collection_list_even = html_soup.find_all("tr", class_="even")
            except:
                print("Error in getting the HTML requests")
            file_names = []
            file_list = []

            for link in Zip_collection_list_odd:
                file_names.append(link.a.text)
                file_list.append(url + str(link.a['href']))

            for link in range(1,len(Zip_collection_list_even)):
                file_names.append(Zip_collection_list_even[link].a.text)
                file_list.append(url + str(Zip_collection_list_even[link].a['href']))

            BIG_LIST.append([append[-3:], file_names, file_list])
    except:
        print("Error in Finding the Zipped files!")
    
    return BIG_LIST 

def extract(local,BIG_LIST):
    """
    This function will extract the files to a local folder and deletes de zip file
    """
    for append_list in BIG_LIST:
        file_name = append_list[1][:]
        file_link = append_list[2][:]
        folder_name = local + append_list[0] +'\\'
        try:
            os.makedirs(folder_name, exist_ok=True)
            for i in range(len(file_name)):
                if append_list[0] == "CAD":
                    date = folder_name + '\\'
                else:
                    date = folder_name + file_name[i][-8:-4] + '\\'
                os.makedirs(date, exist_ok=True)
                path = date+file_name[i]
                response = get(file_link[i])
                with open(path, 'wb') as arq:
                    arq.write(response.content)
                    if file_name[i][-4:] == ".zip":
                        ZipFile(path,'r').extractall(date)
                        #os.remove(path) -- can't make it work properly
                try:
                    #delete the Zip files
                    for root ,dir, files in os.walk(local):
                        for name in files:
                            if name[-4:] == ".zip" :
                                os.remove(os.path.join(root, name))
                except:
                    print("Error in finding the zipfile!")
                    
        except:
            print("Problem in creating the folders or Extracting the zip files")

main()