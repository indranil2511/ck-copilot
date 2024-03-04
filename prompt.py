QUERY = """
Given a natural language question or statement related to the following tables and their columns, formulate a syntactically correct PostgreSQL query:
There are three tables:
- Customers 

- Orders
- Products
Tables and Columns:

Customers:
    It contains the data of customers along with following details
Customer_Id (Integer, primary key)
First_Name (String)
Last_Name (String)
Date_Of_Birth (Date)
Gender (String)
Address (String)
City (String)
Postal_Code (String)
Contact_Number (String)
Email (String)

Products:
    It contains prooducts available along with its following details
Product_Id (String, primary key)
Product_Name (String)
Product_Category (String)
Price (Numeric)
Product_Description (String)

Orders:
    Orders table simply include whatever product is being ordered by customers and the status of orders along with following information
Order_Id (String, primary key)
Product_Id (String, foreign key references Products.Product_id)
Customer_Id (Integer, foreign key references Customers.Customer_Id)
Product_Name (String)
Status_Type (String)
Shipping_Date (Date)
Delivery_Date (Date)
Status_Location (String)
Delivery_Location (String)


SQL Query Formatting Guide (with Enhanced WHERE Clause Handling)

This prompt outlines the requirements for formulating correct PostgreSQL queries based on the provided tables and their columns, incorporating an improvement to the second point:

1. Table and Column Names:

Enclose both table and column names in double inverted commas ("), preserving their exact case as written in the table descriptions.
Examples:
"Customers", "Orders", "Products"
"Product_Id", "First_Name", "Price"
2. Joins and WHERE Clauses:

Always enclose column names within double inverted commas (") when used in joins (e.g., INNER JOIN, LEFT JOIN) and the WHERE clause.
For string comparisons in the WHERE clause:
Use the **LOWER** function to convert both strings to lowercase.
Employ the **TRIM** function to remove leading and trailing whitespace from the strings.
This ensures case-insensitive comparisons and avoids ambiguity.
Example:

SQL
SELECT * FROM "CUSTOMERS"
WHERE LOWER(TRIM("City")) = 'NEW YORK';

Dont comment the asked query
examples:
Count of customers should be written as Select count("Customer_Id") from "Customers"
If the question is : "provide the details of customers having status Shipped."
query: SELECT
    c."Customer_Id",
    c."First_Name",
    c."Last_Name",
    c."Date_Of_Birth",
    c."Gender",
    c."Address",
    c."City",
    c."Postal_Code",
    c."Contact_Number",
    c."Email",
  o."Status_Type"
FROM
    "Customers" c
INNER JOIN
    "Orders" o ON o."Customer_Id"= c."Customer_Id"  
WHERE
    lower(trim(o."Status_Type")) = 'shipped'

don't write word query in the starting of actual query
Replace the word delivered by reached in query
When asked for total do the sum 


{question}
"""