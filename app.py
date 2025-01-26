from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd

app = Flask(__name__)

def fetch_stock_data(ticker, market):
    """Fetch stock data for the given ticker and market."""
    try:
        # Add suffix for Indian stocks based on selected market
        if market == "NS":
            ticker += ".NS"
        elif market == "BO":
            ticker += ".BO"

        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo")  # Fetch last 1 month's data
        if hist.empty:
            return "No data found for the given ticker."
        return hist.reset_index()
    except Exception as e:
        return str(e)

def calculate_insights(data):
    """Generate basic stock insights."""
    if data.empty:
        return "No data available to calculate insights."
    
    insights = {
        "latest_price": data["Close"].iloc[-1],
        "highest_price": data["High"].max(),
        "lowest_price": data["Low"].min(),
        "average_volume": data["Volume"].mean()
    }
    return insights

@app.route("/", methods=["GET", "POST"])
def index():
    stock_data = None
    insights = None
    error = None

    if request.method == "POST":
        ticker = request.form.get("ticker").upper()
        market = request.form.get("market")
        if ticker and market:
            data = fetch_stock_data(ticker, market)
            if isinstance(data, pd.DataFrame):
                stock_data = data.to_dict(orient="records")
                insights = calculate_insights(data)
            else:
                error = data  # Use the error message returned by fetch_stock_data

    return render_template("index.html", stock_data=stock_data, insights=insights, error=error)

if __name__ == "__main__":
    app.run(debug=True)