from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Route for home page
@app.route('/')
def index():
    return render_template('index.html', plot_url=None)

# Route to generate the plot
@app.route('/plot', methods=['POST'])
def plot():
    # Print the form data for debugging
    print("Form Data:", request.form)

    # Get parameters from the form, provide default values if keys are missing
    a = float(request.form.get('a', 1))  # Default slope a to 1
    b = float(request.form.get('b', 0))  # Default intercept b to 0
    c = float(request.form.get('c', 1))  # Default noise factor c to 1
    n = int(request.form.get('n', 100))  # Default number of points n to 100
    variance = float(request.form.get('variance', 10))  # Default variance to 10

    # Debug output to check if values are being captured
    print(f"a={a}, b={b}, c={c}, n={n}, variance={variance}")

    # Generate random data points with the user-defined variance
    np.random.seed(42)
    x = np.random.uniform(-25, 25, n)
    noise = np.random.normal(0, np.sqrt(variance), n)
    y = a * x + b + c * noise

    # Generate the plot
    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, label='Data points')

    # Plot regression line
    x_line = np.linspace(-25, 25, 100)
    y_line = a * x_line + b
    plt.plot(x_line, y_line, color='red', label='Regression line')

    # Add labels and title
    plt.title(f'Simple Linear Regression (a={a}, b={b}, c={c}, variance={variance}, n={n})')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()

    # Add the linear regression formula on the plot
    formula = f'y = {a:.2f} * x + {b:.2f} + {c:.2f} * N(0, {variance:.2f})'
    plt.text(-24, max(y), formula, fontsize=12, color='blue')

    # Save the plot to a bytes buffer
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    # Return the template with the plot
    return render_template('index.html', plot_url='data:image/png;base64,{}'.format(plot_url))

if __name__ == '__main__':
    app.run(debug=True)
