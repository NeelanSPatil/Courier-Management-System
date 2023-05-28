import streamlit as st
import mysql.connector
from random import randint
from pandas import DataFrame

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="cms",
    auth_plugin='mysql_native_password'
)


# Function to authenticate admin login
def authenticate_admin(username, password):
    query = "SELECT * FROM admin_login WHERE Username = %s AND Password = %s"
    values = (username, password)
    cursor = db.cursor()
    cursor.execute(query, values)
    result = cursor.fetchone()
    cursor.close()
    return result


# Function to authenticate customer login
def authenticate_customer(username, password):
    query = "SELECT * FROM customer_login WHERE Username = %s AND Password = %s"
    values = (username, password)
    cursor = db.cursor()
    cursor.execute(query, values)
    result = cursor.fetchone()
    cursor.close()
    return result


# Function to authenticate delivery person login
def authenticate_delivery_person(username, password):
    query = "SELECT * FROM deliverper_login WHERE Username = %s AND Password = %s"
    values = (username, password)
    cursor = db.cursor()
    cursor.execute(query, values)
    result = cursor.fetchone()
    cursor.close()
    return result


# Admin Login Page
# Admin Login Page
def admin_login():
    st.title("Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        result = authenticate_admin(username, password)
        if result:
            st.success("Login Successful")
            admin_dashboard(result)  # Pass the result (admin credentials) to the dashboard
        else:
            st.error("Invalid Username or Password")



# Customer Login Page
def customer_login():
    st.title("Customer Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    customer_id = st.text_input("Customer ID")
    if st.button("Login"):
        result = authenticate_customer(username, password)
        if result:
            st.success("Login Successful")
            customer_dashboard(customer_id)
        else:
            st.error("Invalid Username or Password")


# Delivery Person Login Page
def delivery_person_login():
    st.title("Delivery Person Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    delivery_person_id = st.text_input("Delivery_id")
    if st.button("Login"):
        result = authenticate_delivery_person(username, password)
        if result:
            st.success("Login Successful")
            delivery_person_dashboard(delivery_person_id)
            # Redirect to delivery person dashboard or perform other actions
        else:
            st.error("Invalid Username or Password")

# Function to get assigned parcel details for a delivery person
def get_assigned_parcel_details(delivery_person_id):
    query = f"SELECT * FROM item WHERE Delivery_id = {delivery_person_id}"
    cursor = db.cursor()
    cursor.execute(query)
    df = DataFrame(cursor.fetchall(), columns=['Parcel_id', 'Sender_Address', 'Receiver_Address', 'Phone_no', 'Status', 'Item_type',
                            'Delivery_id'])
    cursor.close()
    return df
    cursor.close()


# Delivery Person Dashboard
def delivery_person_dashboard(delivery_person_id):
    st.title("Delivery Person Dashboard")

    # Get assigned parcel details
    assigned_parcel_details = get_assigned_parcel_details(delivery_person_id)
    st.header("Assigned Parcel Details")
    st.table(assigned_parcel_details)

    # Add other functionalities or actions specific to the delivery person dashboard

    # Logout
    if st.button("Logout"):
        logout()
        st.success("Logged out successfully.")
        main()

# Admin Dashboard
def customer_dashboard(customer_id):
    st.title("Customer Dashboard")

    # Get Customer Details
    customer_details = get_customer_details(customer_id)
    st.header("Customer Details")
    st.table(customer_details)

    # Get Assigned Delivery Person
    assigned_delivery_person = get_assigned_delivery_person(customer_id)
    st.header("Assigned Delivery Person")
    st.table(assigned_delivery_person)

    # Add New Parcel
    st.header("Add New Parcel")
    parcel_sender_address = st.text_input("Sender Address")
    parcel_receiver_address = st.text_input("Receiver Address")
    parcel_phone_no = st.text_input("Phone Number")
    parcel_item_type = st.text_input("Item Type")
    if st.button("Add Parcel"):
        assigned_delivery_person_id = assign_delivery_person_randomly()
        parcel_id = randint(1, 10000)
        add_parcel(parcel_id, parcel_sender_address, parcel_receiver_address, parcel_phone_no, parcel_item_type,
                   assigned_delivery_person_id)
        st.success("Parcel added successfully.")

    # Logout
    if st.button("Logout"):
        st.success("Logged out successfully.")
        main()


# Customer Dashboard
# Admin Dashboard
def admin_dashboard(admin_credentials):
    st.title("Admin Dashboard")

    # Display Customer Details
    st.header("Customer Details")
    customer_details = get_customer_details()
    st.table(customer_details)

    # Add Delivery Person
    st.header("Add Delivery Person")
    delivery_person_name = st.text_input("Name")
    delivery_person_phone = st.text_input("Phone Number")
    delivery_person_Delivery_id = st.text_input("Delivery_id")
    delivery_person_Parcel_id = st.text_input("Parcel_id")
    if st.button("Add"):
        add_delivery_person(delivery_person_name, delivery_person_phone, delivery_person_Delivery_id, delivery_person_Parcel_id)
        st.success("Delivery Person added successfully.")

    # Delete Delivery Person
    st.header("Delete Delivery Person")
    delivery_person_id = st.number_input("Delivery Person ID")
    if st.button("Delete"):
        delete_delivery_person(delivery_person_id)
        st.success("Delivery Person deleted successfully.")

    # Display Parcel Details
    st.header("Parcel Details")
    parcel_details = get_parcel_details()
    st.table(parcel_details)

    if st.button("Logout"):
        logout()
        st.success("Logged out successfully.")
        main()


# Function to fetch customer details from the database
# Function to fetch all customer details from the database
def logout():
    pass
def get_customer_details():
    query = "SELECT * FROM customer"
    cursor = db.cursor()
    cursor.execute(query)
    df = DataFrame(cursor.fetchall(), columns=['Name', 'Phone_no', 'Customer_id', 'Parcel_id', 'Delivery_id'])
    cursor.close()
    return df


# Function to add a delivery person to the delivery_person table
def add_delivery_person(name, phone_no, parcel_id):
    count = get_delivery_person_count()
    if count >= 15:
        st.warning("Maximum limit of delivery persons reached. Cannot add new delivery person.")
    else:
        query = "INSERT INTO delivery_person (Name, Phone_no, Parcel_id) VALUES (%s, %s, %s)"
        values = (name, phone_no, parcel_id)
        cursor = db.cursor()
        cursor.execute(query, values)
        db.commit()
        cursor.close()


# Function to delete a delivery person from the delivery_person table
def delete_delivery_person(delivery_person_id):
    query = "DELETE FROM delivery_person WHERE Delivery_id = %s"
    values = (delivery_person_id,)
    cursor = db.cursor()
    cursor.execute(query, values)
    db.commit()
    cursor.close()


# Function to fetch parcel details from item table
def get_parcel_details():
    query = "SELECT * FROM item"
    cursor = db.cursor()
    cursor.execute(query)
    df = DataFrame(cursor.fetchall(),
                   columns=['Parcel_id', 'Sender_Address', 'Receiver_Address', 'Phone_no', 'Status', 'Item_type',
                            'Delivery_id'])
    cursor.close()
    return df


# Function to get the count of delivery persons
def get_delivery_person_count():
    cursor = db.cursor()
    query = "SELECT COUNT(*) FROM delivery_person"
    cursor.execute(query)
    count = cursor.fetchone()[0]
    cursor.close()
    return count


# Function to get the assigned delivery person for a customer
def get_assigned_delivery_person(customer_id):
    query = f"SELECT dp.Name, dp.Phone_no FROM delivery_person dp INNER JOIN customer c ON dp.Delivery_id = c.Delivery_id WHERE c.Customer_id = {customer_id}"
    cursor = db.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results


# Function to assign a delivery person randomly to a customer
def assign_delivery_person_randomly():
    cursor = db.cursor()
    query = "SELECT Delivery_id FROM delivery_person"
    cursor.execute(query)
    delivery_person_ids = cursor.fetchall()
    assigned_delivery_person_id = delivery_person_ids[randint(0, len(delivery_person_ids) - 1)][0]
    cursor.close()
    return assigned_delivery_person_id


# Function to add a new parcel to the item table
def add_parcel(parcel_id, sender_address, receiver_address, phone_no, item_type, assigned_delivery_person_id):
    query = "INSERT INTO item (Parcel_id, Sender_Address, Receiver_Address, Phone_no, Status, Item_type, Delivery_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (parcel_id, sender_address, receiver_address, phone_no, "Pending", item_type, assigned_delivery_person_id)
    cursor = db.cursor()
    cursor.execute(query, values)
    db.commit()
    cursor.close()


# Main function to handle the application flow
def main():
    st.title("Courier Management System")
    option = st.selectbox("Select User Type", ("Admin", "Customer", "Delivery Person"))

    if option == "Admin":
        admin_login()
    elif option == "Customer":
        customer_login()
    elif option == "Delivery Person":
        delivery_person_login()


# Run the application
if __name__ == "__main__":
    main()
