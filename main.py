
import datetime
import glob
import os
import time
from scrape import scrapeData
from details import sort, process_and_append
from getImage import getImage
from description import getDesc
from compile import combineANDsave
from transfer import Transfer
from blogUpdate import updateBlog




def clearData():
    folder_path = "DATA"

    print("Refresh Content Initiated:")
    time.sleep(2)

    files = glob.glob(os.path.join(folder_path, '*'))

    # Iterate over the list of files and delete each one, except "previousdata.jsonl"
    for file in files:
        if os.path.basename(file) != "previousdata.jsonl":
            try:
                os.remove(file)
                print(f"Deleted: {file}")
            except Exception as e:
                print(f"Error deleting {file}: {e}")
        else:
            print(f"Skipped deletion of {file}")

    file1 = 'DATA/filtered_data.jsonl'
    file2 = 'DATA/process.json'
    time.sleep(2)

    if os.path.exists(file1):
        os.remove(file1)
        print(f"{file1} has been deleted.")
    else:
        print(f"{file1} does not exist.")

    # Delete the second file
    if os.path.exists(file2):
        os.remove(file2)
        print(f"{file2} has been deleted.")
    else:
        print(f"{file2} does not exist.")
    
    print("Project is Initialized")
    time.sleep(5)





def main():
    scrapeData()  # Run scrapeData() if the folder is empty
    time.sleep(2)
    sort()  
    time.sleep(2)
    process_and_append()  # Continue with the rest of the function
    time.sleep(2)
    getImage()
    time.sleep(2)
    getDesc()

def run():
    clearData()
    time.sleep(2)
    main()
    time.sleep(2)
    print("Compiling Article...")
    time.sleep(5)
    combineANDsave()
    time.sleep(2)
    print("Setting Up Transfer")
    Transfer()
    print("Mail has been sent :)")
    time.sleep(2)
    print("constructing Blog Page")
    updateBlog()
    time.sleep(2)
    print("PROCESS COMPLETE")


