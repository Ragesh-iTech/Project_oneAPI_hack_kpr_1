from flask import Flask, request, render_template, send_file
import xlsxwriter
import smtplib
from email.mime.text import MIMEText
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

vehicles = []

def send_email(best_vehicle, worst_vehicle, total_ticket_sales):
    sender_email = "jeevajeeva49308@gmail.com"
    receiver_email = "pragesh124@gmail.com"
    password = "rcedylvcnhuvmnqb"  # Use environment variables for sensitive information

    subject = "Vehicle Efficiency Report"
    body = (
        f"The best vehicle is {best_vehicle['Vehicle_no']} with efficiency {best_vehicle['Efficiency']:.2f} km/l.\n"
        f"The worst vehicle is {worst_vehicle['Vehicle_no']} with efficiency {worst_vehicle['Efficiency']:.2f} km/l.\n"
        f"Total ticket sales amount to: ${total_ticket_sales:.2f}."
    )

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def plot_combined(vehicles):
    vehicle_nos = [vehicle["Vehicle_no"] for vehicle in vehicles]
    ticket_sales = [vehicle["Ticket_sales"] for vehicle in vehicles]
    efficiencies = [vehicle["Efficiency"] for vehicle in vehicles]

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Bar plot for ticket sales
    ax1.bar(vehicle_nos, ticket_sales, color='skyblue', alpha=0.7, label='Ticket Sales ($)')
    ax1.set_xlabel('Vehicle No')
    ax1.set_ylabel('Ticket Sales ($)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Create a second y-axis for efficiency
    ax2 = ax1.twinx()
    ax2.plot(vehicle_nos, efficiencies, color='orange', marker='o', label='Efficiency (km/l)')
    ax2.set_ylabel('Efficiency (km/l)', color='orange')
    ax2.tick_params(axis='y', labelcolor='orange')

    # Title and grid
    plt.title('Ticket Sales and Efficiency of Buses')
    fig.tight_layout()
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    # Save the plot to a file
    plt.xticks(rotation=45)
    plt.savefig('static/plot.png')
    plt.close(fig)  # Close the figure

@app.route('/')
def index():
    return render_template('index.html', vehicles=vehicles)

@app.route('/add_vehicle', methods=['POST'])
def add_vehicle():
    vehicle_no = request.form.get('vehicle_no')
    distance = float(request.form.get('distance'))
    diesel_consume = float(request.form.get('diesel_consume'))
    time_taken = float(request.form.get('time_taken'))
    
    vehicles.append({
        "Vehicle_no": vehicle_no,
        "Distance": distance,
        "Diesel_consume": diesel_consume,
        "Time_taken": time_taken
    })
    
    return index()

@app.route('/finalize', methods=['POST'])
def finalize():
    get_ticket_sales_data()
    calculate_efficiency()
    write_to_excel()

    if vehicles:
        best_vehicle = max(vehicles, key=lambda x: x["Efficiency"])
        worst_vehicle = min(vehicles, key=lambda x: x["Efficiency"])
        
        # Calculate total ticket sales
        total_ticket_sales = sum(vehicle["Ticket_sales"] for vehicle in vehicles)

        # Send email with details of best and worst vehicles and total ticket sales
        send_email(best_vehicle, worst_vehicle, total_ticket_sales)

        # Plot combined ticket sales and efficiency
        plot_combined(vehicles)

    return render_template('result.html', vehicles=vehicles)

def get_ticket_sales_data():
    for vehicle in vehicles:
        ticket_sales = float(request.form.get(f'ticket_sales_{vehicle["Vehicle_no"]}'))
        vehicle["Ticket_sales"] = ticket_sales

def calculate_efficiency():
    for vehicle in vehicles:
        if vehicle["Diesel_consume"] > 0:
            vehicle["Efficiency"] = vehicle["Distance"] / vehicle["Diesel_consume"]
        else:
            vehicle["Efficiency"] = 0

def write_to_excel():
    workbook = xlsxwriter.Workbook("VehicleData.xlsx")
    worksheet = workbook.add_worksheet("Vehicle Details")
    
    worksheet.write(0, 0, "Vehicle No")
    worksheet.write(0, 1, "Distance (km)")
    worksheet.write(0, 2, "Diesel Consumed (liters)")
    worksheet.write(0, 3, "Time Taken (hours)")
    worksheet.write(0, 4, "Efficiency (km/l)")
    worksheet.write(0, 5, "Ticket Sales ($)")

    for index, vehicle in enumerate(vehicles):
        worksheet.write(index + 1, 0, vehicle["Vehicle_no"])
        worksheet.write(index + 1, 1, vehicle["Distance"])
        worksheet.write(index + 1, 2, vehicle["Diesel_consume"])
        worksheet.write(index + 1, 3, vehicle["Time_taken"])
        worksheet.write(index + 1, 4, vehicle["Efficiency"])
        worksheet.write(index + 1, 5, vehicle["Ticket_sales"])

    workbook.close()

@app.route('/download')
def download_file():
    return send_file("VehicleData.xlsx", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
