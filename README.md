Description
This application is a web-based tool that allows users to input and manage vehicle data for efficiency analysis. The data entered includes vehicle number, distance traveled, diesel consumed, and time taken. After submitting vehicle data, the system calculates each vehicle's fuel efficiency in kilometers per liter (km/l) and generates reports, including visualizations and an Excel export of the data. Additionally, the application sends an email summarizing the most efficient and least efficient vehicles, along with total ticket sales.

Key Features
1. Vehicle Data Input
The main interface allows users to add vehicle information such as:
Vehicle No: The identification number of the vehicle.
Distance: The total distance traveled in kilometers.
Diesel Consumed: The amount of diesel consumed in liters.
Time Taken: The time taken for the journey in hours.
Vehicles added are listed dynamically.
2. Ticket Sales Entry
Users can input the ticket sales for each vehicle in a second form.
After input, the system calculates each vehicle's efficiency and generates reports.
3. Efficiency Calculation
The efficiency of each vehicle is calculated as:
Efficiency (km/l)
=
Distance (km)
Diesel Consumed (liters)
Efficiency (km/l)= 
Diesel Consumed (liters)
Distance (km)
​
 
Vehicles with zero diesel consumption will have zero efficiency.
4. Report Generation
After finalizing the data, a report is generated:
Displays each vehicle’s efficiency in km/l.
Identifies the best and worst-performing vehicles based on fuel efficiency.
The report is available as an Excel file download and includes the following fields:
Vehicle No
Distance (km)
Diesel Consumed (liters)
Time Taken (hours)
Efficiency (km/l)
Ticket Sales ($)
5. Email Notification
Upon finalizing the data, the application sends an email with:
Details of the most efficient and least efficient vehicles.
Total ticket sales.
Emails are sent securely using Gmail's SMTP service.
6. Data Visualization
A plot combining vehicle ticket sales and efficiency is generated:
Ticket Sales: Shown as a bar chart.
Efficiency: Shown as a line chart on the same graph.
The plot is saved and displayed on the result page.
7. Excel Export
All the vehicle data, including efficiency and ticket sales, can be downloaded as an Excel file using xlsxwriter.
How to Use
Home Page: Enter vehicle details (vehicle number, distance traveled, diesel consumed, time taken) into the form and submit.
Vehicles Added: The added vehicles are displayed below the form.
Ticket Sales: Enter ticket sales data for each vehicle and submit the form.
Finalizing Data: Once all data is entered, submit the ticket sales form to generate the final report.
View Reports:
Efficiency data for each vehicle is displayed on the result page.
Download the Excel file for detailed records.
View a plot of ticket sales and efficiency.
Email Notification: An email is sent with the report details.
Dependencies
Flask: Web framework to handle routing and rendering templates.
xlsxwriter: Library for creating and writing Excel files.
smtplib: Python library for sending emails via SMTP.
matplotlib: Library for creating data visualizations.
File Structure
index.html: HTML page for vehicle data input and ticket sales entry.
result.html: HTML page displaying the vehicle efficiency results and download options.
static/plot.png: Image generated by matplotlib containing the ticket sales and efficiency plot.
Security Considerations
Ensure sensitive information such as email credentials (e.g., passwords) is stored securely using environment variables. Avoid hardcoding sensitive data in the code.
How to Run the Application
Clone or download the code.
Install the required dependencies:
bash
Copy code
pip install flask xlsxwriter matplotlib
Run the Flask server:
bash
Copy code
python app.py
