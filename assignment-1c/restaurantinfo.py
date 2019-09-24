import csv

def restaurantInfo(filename):
    #import the restaurant info from the csv file, export as a dictionary
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = True #bool indicates if weŕe reading the header
        headers = []
        restaurants = dict()
        for row in reader:
            if header:
                #save the headers after the name
                headers = row[1:]
                header = False
            else:
                #save the info about this restaurant
                infodict = dict() # a dict with the restaurant info
                data = row[1:]
                for i in range(len(data)):
                    infodict[headers[i]] = data[i] #zip the headers with the corresponding field
                restaurants[row[0]]  = infodict #save the data under the restaurant name

    return restaurants

#import restaurant data
rdata = restaurantInfo('./restaurantinfo.csv')

#extract known preference options
priceranges = set()
areas = set()
foods = set()

for restaurant in rdata:
    priceranges.add(rdata[restaurant]['pricerange'])
    areas.add(rdata[restaurant]['area'])
    foods.add(rdata[restaurant]['food'])

areas.remove('') #some restaurants have blank area field

priceranges = list(priceranges)
areas = list(areas)
foods = list(foods)



#for restaurant in restaurants:
#    if restaurants[restaurant]['pricerange'] == 'expensive':
#        print(restaurant)
