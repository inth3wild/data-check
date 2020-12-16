# data-check
A simple python command line interface tool for checking your data balance.
It ***simultaneously*** checks the data balance for each username and password pair, meaning if there are more
than one account credentials(username and password) provided, the results are ***quickly*** delivered

##### NB:
The credentials.txt format is specified in credentials.example.txt.
The tail payload is gotten by using your browser's DevTools network panel to see the POST
request made to the ``https://netsurf.lmu.edu.ng/ajax/bals.php`` endpoint, copying it and adding to credentials.txt file

example tail payload:
###### surname.firstname:["TuECj7cxlUfZuIFCK2SAHzQ99nE=","lUCmTPidQ249","ndRqubVtsDcXdd6UhbtqTbyn0A=","ndRquF5oDQXbbUhbIP1jA="]



### Installation
1) git clone https://github.com/inth3wild/data-check.git  
2) cd data-check/


### Usage
python check-data.py -f credentials.txt
