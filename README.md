# Auto-Dog-Wash-V2
This is version two of the auto dog wash business, which was built to be more scalable and more reliable. In V1, CSV files were used and uploaded directly into a Jupyter Notebook, where EDA was completed. This time, however, I am back with a more streamlined pipeline (which caused much pain).

# Motivation (again)
This time, I wanted to create a process that automatically updated the tables of the CSV files throughout the day. I discovered that I had a problem with the CSV files, however; they were now normalized, and it became too messy to try and fix them. So, I decided that setting up a SQL server to collect this data would be fun (it was not). The pipeline goes as follows: a Python program is scheduled to run on my local PC twice a day; this is done through the CMD prompt. Once the data is collected, it goes to a SQL server, which has proper primary and secondary keys set up in it, as well as following a star schema (Not making that mistake again). So, the database is fully normalized this time.

# What is new to V2
## SQL and data collection pipeline
Data will be collected using a low-cost Arduino ESP32 with a built-in ESP8266 module for internet connectivity. An ultrasonic sensor is mounted on the container to measure the distance to the soap surface. This data is then uploaded to a mobile dashboard using Blynk, which can send push notifications or emails if the soap level drops below a set threshold. For this project, I have just written a Python script that generates random data subject to constraints I put in place. This script connects to the MySQL server and runs a function that automatically uploads the random data to the desired tables (actually, really happy this worked). If you want to see how this works, it is in the .py file called "data_gen.py."

## Depletion rate prediction 
This Python script fetches data from the SQL database and stores it in a DataFrame in Python. After that, a function was created to calculate the depletion rate, and then the function was applied to the three consumables from the table product_log. Afterward, the earliest refill time was calculated for each machine, but since I don't care about individual products running out, I just set it to when the first product runs out, and I will refill all the products when I show up. The sensors will take a new reading later that day and reset the depletion values. I will be updating this in SQL rather than Python because, at the moment, the Python script downloads to a CSV, which is then uploaded into Power BI. This is the case because the depletion function was an afterthought, and I have not updated the SQL database yet (I will, though…).

## Power BI dashboard
Lastly, I took a shot at creating my first Power BI dashboard outside of course material from Codecademy lectures. This turned out okay, but I still don’t think it is as sharp as I would like it to be. I will continue to make improvements to it as I learn more about Power BI and other people's dashboards.


# What I learned
I learned a lot about the Command Prompt for adding Python files to a file path, as well as adding .aex files to a CMD path. In this project, I did this with Python and pip in order to be able to install my libraries. In the past, I have used RStudio a lot, but all the libraries are already installed, or all you need to do is put install.libraries(" ") into the console, and you’re off. Installing through the CMD was new and interesting to see how everything works together. Also, setting the daily running of the Python script through the CMD was new to me, which was kind of enjoyable but also kind of not.

# Future plans (Freind or Foe)
It is going to get economically in V3 (I am talking causal inference and all the fun stuff, this will be the most over the top EDA for a small business ever!!!)
## Cost and demand function 
In V3, I will do a small bit on modeling these types of functions just because it will be good practice. Also, I have not worked with Cobb-Douglas functions in a while, and I am beginning to get a little too happy with life, so it is time to change that. I do want to try and work out some duality problems using this dataset and try and figure out a utility maximization point. This would mostly be to provide a good timeline of when the business would be able to expand its operations. On the flip side of this, I want to model consumer choice based on surrounding businesses. For example, I have a hypothesis that being located near a Full-Service Dog Grooming service would be a competitor, but in which direction would the advantage go? In my favor because my prices are cheaper, or in the dog groomer’s favor because they offer a more complete service? Alternatively, could being located near a pet supply store be complementary? These are all questions to be asked and answered. As of now, my thinking is to model this behavior using the Slutsky equation because I learned about it in my master’s yet never applied it to anything in real life.

## Lastly, testing elasticities 
The last thing I want to do is test the elasticity of supply and demand the old-fashioned (Econ 101) way.

## Lastly lastly, Regression Discontinuity design 
I want to estimate the effects of a loyalty program on the revenue and customer retention rate of the machines. The treatment group will be the machine in Bray, and the control group will be Howth (yes, I know I will probably have loads of endogeneity problems, but just let me be happy for a minute, and I will fix them as I go).
