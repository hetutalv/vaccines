from testi import mydb
from testi import run
import os
from datetime import datetime
from pandas import DataFrame
import pdfkit as pdf
import matplotlib.pyplot as plt


def exit():
    n = int(input(" Press 5 to exit: "))

    if n == 5:
        os.system('clear') 
        run()
    else:
        print(" Invalid Option")
        exit()

def newVacs():
    date = input("Give date: (YYYY-MM-DD): ")
    dateo = datetime.strptime(date, '%Y-%m-%d')
    mycursor = mydb.cursor()
   


    print(f'------ Arrived vaccines on {date} ------\n')
    
    mycursor.execute("""SELECT *
      FROM vaccinations.vaccines
      WHERE DATEDIFF(arrived, %s) = 0""", (date,))

    info = mycursor.fetchall()

    if len(info) == 0:
        print(f"No arrived vaccines on {date}")
    else:
         df = DataFrame(info)
         df.columns = ('ID', 'Order Nmbr', 'Responsible Person', 'Vaccine', 'Health Care District', 'Injections', 'Arrived')
         print(df)
         df.to_html('test.html')
         testipdf = "testi.pdf"
         pdf.from_file('test.html', testipdf)
    exit()

def  vacsPerHD():
    
    mycursor = mydb.cursor()
    print('------ Vaccinations per health care district ------\n')
    mycursor.execute("""SELECT o.healthCareDistrict AS "Health District", o.vaccine AS Manufacturer, count(*) AS total
      FROM vaccinations.vaccinations v
		INNER JOIN vaccinations.vaccines o ON v.sourceBottle = o.id
        GROUP BY healthCareDistrict, vaccine
        ORDER BY healthCareDistrict""")

    VacsPerHD = mycursor.fetchall()

    df = DataFrame(VacsPerHD)
    df.columns = ('Health Care District', 'Vaccine', 'Amount of injections')
    print(df)
    df.to_html('test.html')
    testipdf = "testi.pdf"
    pdf.from_file('test.html', testipdf)
    exit()

def VacsMF():
    
    mycursor = mydb.cursor()
    print('------ Given vaccines by vaccine ------\n')
    mycursor.execute("""SELECT o.vaccine AS Vaccine, COUNT(*) AS Total FROM vaccinations.vaccinations v 
    INNER JOIN vaccinations.vaccines o ON v.sourceBottle = o.id
    GROUP BY vaccine
    ORDER BY vaccine""")
    VacsPerMF = mycursor.fetchall()

    df = DataFrame(VacsPerMF)
    df.columns = ['Vaccine', 'Total']
    #plot = df.plot(kind='pie', y='Total', x='Vaccine', figsize=(5,5))
    #plot.figure.savefig('test.png')
    plt.pie(df["Total"], labels = df["Vaccine"], autopct="%.2f%%")
    plt.savefig("testi1.png")
    print(df)
    
    df.to_html('test.html')
    testipdf = "testi.pdf"
    pdf.from_file('test.html', testipdf)

    print()
    print("A plot pie and pdf containing the results are saved to folder")

    print('------ SUCCESS ------\n')
    exit()

def Vacs():
    
    mycursor = mydb.cursor()
  
    mycursor.execute("""SELECT  o.healthCareDistrict, 
                  o.id, 
                  o.injections, 
                  DATE(o.arrived) as Date, 
                  COUNT(v.id) AS numOfVaccsGiven, 
                  o.injections - COUNT(v.id) AS unUsedInjections
          FROM vaccinations.vaccines o
          LEFT JOIN  vaccinations.vaccinations v ON o.id = v.sourceBottle
          GROUP BY healthCareDistrict, id, injections, arrived
          ORDER BY date, healthcaredistrict""")
    postList = mycursor.fetchall()
    df = DataFrame(postList)
    df.columns = ['Health Care District', 'Vaccination ID', 'Injections', 'Date', 'Given Vaccs', 'Unused Vaccs']
    
    print(df)

    df.to_html('test.html')
    testipdf = "testi.pdf"
    pdf.from_file('test.html', testipdf)

    print('------ SUCCESS ------\n')
    exit()
        