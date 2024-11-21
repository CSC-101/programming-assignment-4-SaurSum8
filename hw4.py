import sys
import build_data
from data import CountyDemographics

#Iterates through current data, summing up and returning the
#population of all its counties
def population_total() -> int:
    cnt = 0
    for i in cData:
        cnt += i.population['2014 Population']

    return cnt

#Given a field value as string, it returns the corresponding dictionary
#from the given CountyDemographics object
def field_map(k: CountyDemographics, fln: str) -> dict[str, float]:
    fmap = {'Education': k.education, 'Ethnicities': k.ethnicities, 'Income': k.income}
    return fmap[fln]

#return population value for a given category, across current data
def population(field: str) -> float:
    fld = field.split('.')
    cnt = 0
    for i in cData:
        cnt += i.population['2014 Population'] * field_map(i, fld[0])[fld[1]] / 100

    return cnt

#Given a field, it returns the percentage of people belonging to it
#as compared to total population of current data
def percent(field: str) -> float:
    x = population(field)
    t = population_total()
    r = 100 * x / t
    return r

#Given some constraints or bounds
#It returns a reduced form of the current data (as a list)
#which satisfies the given requirements
def filterer(fil: str, field: list[str]) -> list:

    l = []
    for i in cData:

        if fil == 'state' and i.state == field[0]: #if we are filtering by state
            l.append(i)

        else: #else we are doing numerical comparison
            FSF = field[0].split('.')
            if fil == 'gt' and field_map(i, FSF[0])[FSF[1]] > float(field[1]):
                l.append(i)
            elif fil == 'lt' and field_map(i, FSF[0])[FSF[1]] < float(field[1]):
                l.append(i)

    return l

#Displays all information of the current data, in a readable format
def display():
    for i in cData:
        print(i.county, ', ', i.state, sep='')
        print('\tPopulation:', i.population['2014 Population'])

        print('\tAge:')
        for k,v in i.age.items():
            print('\t\t',end='')
            print(k[8:], ':', v, '%') #remove the 'percent' substring in print

        print('\tEducation:')
        for k, v in i.education.items():
            print('\t\t', end='')
            print(k, ':', v, '%')

        print('\tEthnicity Percentages:')
        for k, v in i.ethnicities.items():
            print('\t\t', end='')
            print(k, ':', v, '%')

        print('\tIncome:')
        print('\t\t', 'Median Household :', i.income['Median Household Income'])
        print('\t\t', 'Per Capita :', i.income['Per Capita Income'])
        print('\t\t',  'Below Poverty Level:', i.income['Persons Below Poverty Level'], '%')

#Main/Initial Function
if __name__ == '__main__':
    cData = build_data.get_data()
    print(len(cData), "records loaded")

    l = sys.argv

    try:
        f = open("inputs/" + l[1], 'r')
    except IOError as e:
        print('err :', e)
        sys.exit(1)

    ops = f.readlines()
    lno = 0

    for i in ops:
        lno += 1
        t = i.strip() #Remove \n
        l = t.split(':') #Split it at : l[0] is command, l[1]

        try:
            if t == 'population-total':
                print('2014 Population:', population_total())

            elif l[0] == 'population':
                print("2014", l[1], "population:", population(l[1]))

            elif l[0] == 'percent':
                print("2014", l[1], "percent:", percent(l[1]))

            elif l[0] == 'filter-state': #if filter state specifically
                cData = filterer(l[0][7:], l[1:])
                print("Filter:", l[0][7:], '==', l[1], f'({len(cData)} entries)')

            elif l[0][:6] == 'filter':
                cData = filterer(l[0][7:], l[1:]) #when gt, lt filters, len(l) will be > 2
                print("Filter:", l[1], l[0][7:], l[2], f'({len(cData)} entries)')

            elif t == 'display':
                display()
        except:
            print('error computing line', f'{lno}', 'skipping')