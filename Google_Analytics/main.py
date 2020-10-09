from ga_api import readData
from dwh_write import writeData

def main():
    data = readData()
    writeData(data)
    
if __name__ == "__main__":
    main()

