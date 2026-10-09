import pandas as pd
import numpy as np

dataset = pd.read_csv('Titanic-Dataset.csv')
dataset.replace(r'^\s*$', np.nan)

#ВОПРОСЫ
# Какой общий процент выживших?
# Влиял ли пол на выживание?
# Влиял ли класс билета (Pclass) на выживание?
# Влияла ли цена билета (Fare) на выживание?
# Как сочетались пол и класс? Кто был в самой уязвимой группе?
# Влиял ли возраст? В каком возрасте выживали чаще?
# Можно ли вытащить что-то из текста? Например, титул из имени (Mr, Mrs, Miss, Master) или палубу из номера каюты.

#==========Процент выживших==========
survive_percent = round(sum(dataset['Survived'])/len(dataset['Survived']) * 100)

#==========Влияние пола на выживаемость========
survive_stat_men = [i for i in dataset[dataset['Sex'] == 'male']['Survived']]
survive_stat_women = [i for i in dataset[dataset['Sex'] == 'female']['Survived']]
sex_survive_stat = {
    'men_of_all':f'{sum(survive_stat_men)/(len(survive_stat_men)+len(survive_stat_women))*100:.2f}%',
    'women_of_all':f'{sum(survive_stat_women)/(len(survive_stat_men)+len(survive_stat_women))*100:.2f}%',
    'men_of_all_survived':f'{sum(survive_stat_men)/(sum(survive_stat_women)+sum(survive_stat_men))*100:.2f}%',
    'women_of_all_survived':f'{sum(survive_stat_women)/(sum(survive_stat_women)+sum(survive_stat_men))*100:.2f}%'
}

#==========Влияние класса на выживаемость=======
pclass_survive_stat = dataset.groupby('Pclass').agg(
    survive_percent=('Survived', lambda x: f'{x.mean()*100:.2f}%'),
)

#==========Влияние цены билета на выживаемость========
dataset['CostCategory'] = pd.cut(
    dataset['Fare'],
    bins=(-1,10,30,100,600),
    labels=['Low','Mid-low','Mid','High']
)
ticket_cost_survive_stat = dataset.groupby('CostCategory').agg(
    survive_percent=('Survived', lambda x: int(x.mean()*100)),
    count_people=('Survived', 'size'),
    count_survived=('Survived', 'sum'),
    ).sort_values(by='survive_percent', ascending=False
    ).assign(survive_percent= lambda x: x["survive_percent"].map('{:.2f}%'.format)).reset_index()


#===========Сочетания пола и класса============
sex_class_survive_stat = dataset.groupby(['Sex','Pclass']).agg(
    survive_percent=('Survived', lambda x: int(x.mean()*100)),
    count_people=('Survived', 'size'),
    count_survived=('Survived', 'sum'),
    ).sort_values(by='survive_percent', ascending=False
    ).assign(survive_percent = lambda x: x["survive_percent"].map('{:.2f}%'.format)).reset_index()

#===========Влияние возраста=========