from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import io
import matplotlib.pyplot as plt
from flask.helpers import send_file
import pandas as pd
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        # Read the dataset from Excel
        data = pd.read_excel(file)
        # Perform your data analysis here using the 'data' DataFrame
        # Create a chart (for example, using matplotlib)
        chart = create_chart(data)

        # Save the chart to a temporary file
        chart_path = 'uploads/chart.png'
        chart.savefig(chart_path)
        plt.close()

        # Return the chart to the user
        return send_file(chart_path)
    
def create_chart(df):

    # Specify the target month and year
    target_month = 1  # January
    target_year = 2023

    df['Category'] = df['Category'].str.strip()

    filtered_df = df[(df['Date'].dt.month == target_month) & (df['Date'].dt.year == target_year)]

    # Group the expenses by category and calculate the total expenditure
    category_expenses = filtered_df.groupby('Category')['Expense'].sum().reset_index()


    # Calculate the total expenses
    total_expenses = category_expenses['Expense'].sum()

    # Create labels for the legend combining category and expense percentages
    legend_labels = [f"{category}: {expense / total_expenses * 100:.3f}%" for category, expense in
                    zip(category_expenses['Category'], category_expenses['Expense'])]

    # Sort the categories by expense in descending order
    category_expenses = category_expenses.sort_values(by='Expense', ascending=False)

    # Plot a pie chart
    plt.figure(figsize=(20, 10))
    plt.pie(category_expenses['Expense'])
    plt.title('Expense Categories for {} {}'.format(datetime.date(target_year, target_month, 1).strftime('%B'), (target_year)))
    plt.axis('equal')

    # Create a legend with color-coded labels outside the chart
    plt.legend(legend_labels, title='Categories', loc='center left', bbox_to_anchor=(1, 0.5))


    return plt.gcf()

if __name__ == '__main__':
    app.run(host='localhost', port=8000)
