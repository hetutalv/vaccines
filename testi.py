import os
from defs import *
from valikko import *
import mysql.connector


def run():
   displayMainMenu()
   n = int(input("Enter option : "))
   if n == 1:
      os.system('clear')
      newVacs()
   elif n == 2:
      os.system('clear')
      vacsPerHD()
   elif n == 3:
      os.system('clear')
      VacsMF()
   elif n == 4:
      os.system('clear')
      Vacs()
   elif n == 5:
      os.system('clear')
      print(' — — — Thank You — — -')
   else:
      os.system('clear')
      run()


mydb = mysql.connector.connect(
    user='root', 
    password='henu23011',
    host='127.0.0.1',)

def initDB():
    mycursor = mydb.cursor()
    mycursor.execute('USE vaccinations')

if __name__ == '__main__':
    initDB()
    run()