import pandas as pd

def run_transformation():
    data = pd.read_csv(r'zipco_transactions.csv')

    # Removing duplicates
    data.drop_duplicates(inplace=True)

    # Handling missing values (filling missing numeric values with mean or median)

    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
    for col in numeric_columns:
        data.fillna({col: data[col].mean()}, inplace=True)


    # handling missing values (filling missing string/object values with unknown)
    string_columns = data.select_dtypes(include=['object']).columns
    for col in string_columns:
        data.fillna({col: 'unknown'}, inplace=True)


    #cleaning date colunm: assigning the right data type

    data['Date'] = pd.to_datetime(data['Date'])

    
    # creating fact and dimension tables

    # create the product table

    products = data[['ProductName', 'UnitPrice']].drop_duplicates().reset_index(drop=True)
    products.index.name = 'ProductID'
    products = products.reset_index()


    # Create Customers Table

    customers = data[['CustomerName', 'CustomerAddress', 'Customer_PhoneNumber', 'CustomerEmail']].drop_duplicates().reset_index(drop=True)
    customers.index.name = 'CustomerID'
    customers = customers.reset_index()


    # Create Staff Table

    staff = data[['Staff_Name', 'Staff_Email']].drop_duplicates().reset_index(drop=True)
    staff.index.name = 'StaffID'
    staff = staff.reset_index()


    # creating the transactions table

    transactions = data.merge(products, on=['ProductName', 'UnitPrice'], how='left') \
        .merge(customers, on=['CustomerName', 'CustomerAddress', 'Customer_PhoneNumber', 'CustomerEmail'], how='left') \
        .merge(staff, on=['Staff_Name', 'Staff_Email'], how='left')

    transactions.index.name = 'TransactionID'
    transactions = transactions.reset_index() \
                            [['Date', 'TransactionID', 'ProductID', 'Quantity', 'StoreLocation', 'PaymentType', 'PromotionApplied', 'Weather', \
                                'Temperature', 'StaffPerformanceRating', 'CustomerFeedback', 'DeliveryTime_min', 'OrderType', 'CustomerID', 'StaffID', 'DayOfWeek', 'TotalSales']]


    # save data as csv files

    data.to_csv('cleaned_data.csv', index=False)
    products.to_csv('products.csv', index=False)
    customers.to_csv('customers.csv', index=False)
    staff.to_csv('staff.csv', index=False)
    transactions.to_csv('transactions.csv', index=False)


    print('Data Cleaning and Transformation Completed Successfully!')
    
                                  