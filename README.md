# Analysis-of-debt-repayment-by-credit-card-holders
Project made in Databricks using PySpark.

The actual main file with the extension .py.

### Wstęp

Credit card holders are clients of a large commercial bank in Taiwan operating in the credit market, including issuing credit cards for its customers. The task is to optimize the bank's income from existing customers who have a credit card. The company has a base of 30,000 customers. The aim of the project is to analyze the data set and investigate which customers (with what characteristics) are most likely to default on their loan next month.

The results of the analysis in addition to the predict of default payments by customers due next month on the current credit card can be used to evaluate an application for a new credit card and used to make an overall assessment of the credibility of the customer, eg. when granting consumer credit or other offers for the adjustment of banking products. During the credit card issuance process, a bank employee may decide to grant or deny a credit card to the applicant. The client's default is marked as {1}, and the non-default as {0}.

### Description of the data set

The project uses data from the website: https://archive.ics.uci.edu/ml/datasets/default+of+credit+card+clients.

The author of the data is I-Cheng Yeh from the Department of Information Management, Chung Hua University, Taiwan. The data concerns arrears with payments by bank customers in Taiwan. Data refer to arrears in payments made by the bank's customers in Taiwan

Characteristics of the data set::

- Number of observations: 30,000,
- Attribute types: floating point numbers (Real), integers (Integer),
- Number of attributes: 24,
- Date added: 01/26/2016,
- Data deficiencies: None.

Attributes description:

- Y: Target variable specifying default payment in the next month (October 2005) (1 = Yes, 0 = No),
- ID: row number
- LIMIT_BAL: Amount of the given credit (NT dollar) (it includes both the individual consumer credit and his/her family (supplementary) credit).
- SEX: Gender (1 = male; 2 = female),
- EDUCATION: Education (1 = graduate school; 2 = university; 3 = high school; 4 = others),
- MARRIAGE: marital status (1 = married; 2 = single; 3 = others),
- AGE: Age (in years),
- PAY_0 - PAY_6: History of last payments from April 2005 to September 2005, given as follows: PAY_0 = repayment status in September 2005; PAY_2 = repayment status in August 2005 ... PAY_6 = repayment status in April 2005 (The measurement scale: -1 = pay duly; 1 = payment delay for one month; 2 = payment delay for two months; . . .; 8 = payment delay for eight months; 9 = payment delay for nine months and above. Additionally, there are values -2 and 0, the interpretation of which is given as: -2 and 0 = there is no payment balance.)
- BILL_AMT1 - BILL_AMT6: Amount of bill statement (NT dollar) (BILL_AMT1 = statement in September 2005; BILL_AMT2 = statement in August 2005; ...; BILL_AMT6 = statement in April 2005),
- PAY_AMT1 - PAY_AMT6: Amount of previous payment (NT dollar) (PAY_AMT1 = sum of payments in September 2005, PAY_AMT2 = sum of payments in August 2005; ...; PAY_AMT6 = sum of payments in April 2005).
