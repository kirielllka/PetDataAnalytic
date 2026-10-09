import numpy as np
import pandas as pd

# Общий процент оттока пользователей
# Самые рискованные типы контрактов
# Влияет ли способ оплаты на отток
# Какие услуги снижают отток
# Средний чек у ушедших vs оставшихся
# Топ 3 сегмента с максимльным риском ухода
telecom_dataset = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")

telecom_dataset.replace(r'^\s*$', np.nan, regex=True, inplace=True)

telecom_dataset['TotalCharges'] = telecom_dataset['TotalCharges'].fillna(0)

telecom_dataset['Churn'] = telecom_dataset['Churn'].map({'Yes': 1, 'No': 0})



#Общая статистика оттока пользователей
churn_stat = [i for i in telecom_dataset['Churn']]
churn_procent_stat = round(churn_stat.count(1)/len(churn_stat)*100,2) #процент оттока пользователей

#Анализ разных типов контракта
contract_types = set(telecom_dataset['Contract'])

contract_churn_two_year = [i for i in telecom_dataset[
    telecom_dataset['Contract'] == 'Two year']['Churn']] #Статистика оттока на двухлетний контракт

contract_churn_month_to_month = [i for i in telecom_dataset[
    telecom_dataset['Contract'] == 'Month-to-month']['Churn']] #Статистика оттока на месячный контракт

contract_churn_one_year = [i for i in telecom_dataset[
    telecom_dataset['Contract'] == 'One year']['Churn']] #Статистика оттока на годовой контракт

#Общая статистика по проценту оттока пользователей при разных контрактах
percent_church_by_contract = {
    'One year': f'{round(contract_churn_one_year.count(1)/len(contract_churn_one_year)*100,2)}%',
    'Two year':f'{round(contract_churn_two_year.count(1)/len(contract_churn_two_year)*100,2)}%',
    'Month-to-month*':f'{round(contract_churn_month_to_month.count(1)/len(contract_churn_month_to_month)*100,2)}%',
}



payment_methods = set(telecom_dataset['PaymentMethod']) #методы оплаты

payment_churn_mail = [ i for i in telecom_dataset[
    telecom_dataset['PaymentMethod'] == 'Mailed check']['Churn']] #Отток при оплате с помощью почты

payment_churn_bank_auto = [ i for i in telecom_dataset[
    telecom_dataset['PaymentMethod'] == 'Bank transfer (automatic)']['Churn']] #Отток при автосписывании с банка

payment_churn_card_auto = [ i for i in telecom_dataset[
    telecom_dataset['PaymentMethod'] == 'Credit card (automatic)']['Churn']] #Отток при автосписывании с карты

payment_churn_electrcheck = [ i for i in telecom_dataset[
    telecom_dataset['PaymentMethod'] == 'Electronic check']['Churn']] #Отток при электронных чеках

#Статистика по проценту оттоку пользователей при разных способах оплаты
percent_churn_by_payment_methods = {
    'Mailed check': f'{round(payment_churn_mail.count(1)/len(payment_churn_mail)*100,2)}%',
    'Bank transfer (automatic)': f'{round(payment_churn_bank_auto.count(1)/len(payment_churn_bank_auto)*100,2)}%',
    'Credit card auto': f'{round(payment_churn_card_auto.count(1)/len(payment_churn_card_auto)*100,2)}%',
    'Electronic check': f'{round(payment_churn_electrcheck.count(1)/len(payment_churn_electrcheck)*100,2)}%',
}



#Средний общий чек у оставшихся и ушедших
avg_check_churn_customers = round(sum(
    [float(i) for i in telecom_dataset[telecom_dataset['Churn'] == 1]['TotalCharges']]
    )
    / len(telecom_dataset[telecom_dataset['Churn'] == 1]),2)#Средний чек у ушедших

avg_check_stay_customers = round(sum(
    [float(i) for i in telecom_dataset[telecom_dataset['Churn'] == 0]['TotalCharges']]
    )
    / len(telecom_dataset[telecom_dataset['Churn'] == 0]),2)#Средний чек у оставшихся

avg_cheks = {
    'churn_customers':avg_check_churn_customers,
    'stay_customers':avg_check_stay_customers,
}#Общее отображение средних чеков


#Влияние услуг на отток пользователей
service_cols = [
    'PhoneService', 'MultipleLines', 'OnlineSecurity', 'OnlineBackup',
    'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
] #Все услуги
stats_services = []
for col in service_cols:
    stats_with_service = telecom_dataset.groupby(col).agg(
        churn_rate = ('Churn', lambda x: round(x.mean() * 100)),
        customers_count = ('Churn', 'count'),

    )

    service = {
        'name': col,
        'with_service': int(stats_with_service['churn_rate']['Yes']),
        'without_service': int(stats_with_service['churn_rate']['No']),
        'different': int(abs(stats_with_service['churn_rate']['No'] - stats_with_service['churn_rate']['Yes'])),
    }#Статистика по каждой услуге, сколько отток с ней сколько без
    stats_services.append(service)

stats_services.sort(key= lambda x: x['different'], reverse=True)



#сегментированная статистика
segments_telecom = telecom_dataset.groupby(['PaymentMethod','Contract','InternetService']).agg(
    churn_rate = ('Churn', lambda x: round(x.mean() * 100,2)),
    ).sort_values('churn_rate', ascending=False)




if __name__ == '__main__':
    # print(churn_procent_stat)   # Общий процент оттока пользователей
    # print(percent_church_by_contract)  #Процент оттока по контрактам
    # print(percent_churn_by_payment_methods)    #Процент оттока по методам оплаты
    # print(stats_services)     #Влияние услуг на отток пользователей
    # print(avg_cheks)  #Средние чеки у оставшихся и ушедших пользователей
    # print(segments_telecom)   #Статистика по сегменту (метод оплаты, контракт, интернет сервис)

