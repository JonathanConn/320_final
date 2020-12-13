# app.py
import robin as rb
from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__)             # create an app instance

@app.route("/success/<ticker>/<norm>/<interval>/<span>/<bound>")
def success(ticker, norm, interval, span, bound):
    rb.login()    
    
    data = rb.get_data([ticker], norm, "close_price", interval, span, bound)

    if len(data) == 0:
        return 'robin error'

    for d in data:
        x, y, l = d
        rb.plot_data(x, y, l)

    file_path = '/' + rb.save_plot()
    rb.clear_plot()
    
    return render_template('plot.html', url=file_path)



@app.route("/index", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        tick = request.form["tick"]
        norm = request.form["norm"]
        interval = request.form["interval_form"]
        span = request.form["span_form"]
        bound = request.form["bound_form"]

        return redirect(url_for("success", ticker=tick, norm=norm, interval=interval, span=span, bound=bound))
    
    else:
        tick = request.args.get("tick")
        norm = request.args.get("norm")
        interval = request.get("interval_form")
        span = request.get("span_form")
        bound = request.get("bound_form")
        
        return redirect(url_for("success", ticker=tick, norm=norm, interval=interval, span=span, bound=bound))


if __name__ == "__main__":        # on running python app.py
    app.run(debug=True)           # run the flask app
