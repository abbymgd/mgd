import secrets;
from app import app;
from .rvp import pvr;
from .algo import finalList;

from flask import render_template, request, redirect, flash

@app.route("/", methods=["GET","POST"])
def index():
    mains_rank = ""
    advanced_rank = ""
    secret_key=secrets.token_hex(16)
    app.config["SECRET_KEY"] = secret_key

    if(request.method == "POST"):
        req = request.form

        percentile = req["mains_percentile"]
        if(req["mains_rank"]):
            mains_rank = req["mains_rank"]
        if(req["advanced_rank"]):
            advanced_rank = req["advanced_rank"]
            
        home_state = req["inputState"]
        pwd = req["pwd"]
        gender = req["gender"]
        category = req["category"]
        limit = int(req["limit"])
         
        if(percentile == "" and mains_rank == "" and advanced_rank==""):
            flash("Please enter either your Mains Rank or your Mains Percentile or Advanced rank","error")
            return redirect(request.url)
    
        if(mains_rank and advanced_rank==""):
            advanced_rank = 0
            percentile = 0
        elif(mains_rank=="" and advanced_rank):
            mains_rank = 0
            percentile = 0
        
        if(mains_rank == "" and advanced_rank==""):
            advanced_rank = 0
            ranks = pvr(float(percentile),pwd,category);
            mains_rank = int(ranks);
            if(mains_rank <= 0):
                mains_rank = 2;
        
        if(percentile==""):
            percentile=0
        result = finalList(int(mains_rank),float(percentile),category,home_state,gender,pwd,limit,int(advanced_rank)); 
        
        if(result.shape[0] > 0):
            if(int(advanced_rank) > 0):
                ranks = advanced_rank
            else:
                ranks = mains_rank
            return render_template("public/result.html",ranks=ranks,category=category,tables=[result.to_html(classes='data')], titles=result.columns.values)
        else:
            flash("Sorry we do not have historic data to predict for this case","error")
            return redirect(request.url)

    return render_template("public/index.html")
