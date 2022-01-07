from flask import Flask, render_template, request, redirect, url_for , flash
from mysql.connector import connect, Error
from db import db_con
import os
from datetime import date,timedelta 
from random import randint 


UPLOAD_FOLDER = os.getcwd() +  "/static/expenses/"

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('500.html'), 500

@app.route("/")
def index():
    hospitals1,plans1=db_con([
                                "select * from Hospital;",
                                "Select Type_plan, Price, Other_Plan_details from sub_Plan ;"
                                ])
    
    return render_template('index.html', hospitals=hospitals1,plans=plans1)



@app.route("/add-claim.html")
def addClaim():
    customer_id=request.args.get("customer_id")
    user1,hospitals1,dependents1=db_con([
                            f"select fname,lname from Customer where Cust_id='{customer_id}';",
                            f"select hospital_id,hospital_name from Hospital;",
                            f"select D_name,Dept_id from Dependents where Cust_id='{customer_id}';"
                            ])

    return render_template('add-claim.html',username=user1,hospitals=hospitals1,customer=customer_id,dependents=dependents1)

@app.route("/newclaim", methods = ['POST'])
def newclaim():
    customer_id=request.form.get("customer_id")
    claim_title=request.form.get('claim_title')
    claim_description=request.form.get('claim_description')
    hospital_id=request.form.get('hospital_name')
    expense=request.form.get('expense')
    beneficiary=request.form.get('for')
    receipt=request.files['receipt']
    claim_id = db_con(["select count(*) from Claims;"])[0][0][0] + 1 #retrieve claim id
    if not claim_title:
        flash("Missing data: Claim Title")
        return redirect(request.referrer)
    elif not beneficiary:
        flash("Missing data: For")
        return redirect(request.referrer)    
    elif not claim_description:
        flash("Missing data: Claim Description")
        return redirect(request.referrer)
    elif not hospital_id:
        flash("Missing data: Hospital Name")
        return redirect(request.referrer)      
    elif not expense:
        flash("Missing data: Amont of expense")
        return redirect(request.referrer)
    elif  receipt=='':
        flash("Missing data: Receipt")
        return redirect(request.referrer)
    else:
        if beneficiary=='me':
            plan=db_con([f"select Plan_id from Customer where Cust_id='{customer_id}';"])[0][0][0]
        else:
            plan=db_con([f"select Plan_id from Dependents where Cust_id='{customer_id}' and Dept_id='{beneficiary}';"])[0][0][0]
        receipt.save(os.path.join(app.config['UPLOAD_FOLDER'], str(claim_id)+".png"))
        print(f"insert into Claims   values('{claim_id}', {expense}, '{claim_title}','{plan}','New','{beneficiary}','{date.today()}','{customer_id}',{hospital_id});")
        x=db_con([f"insert into Claims   values('{claim_id}', {float(expense)}, '{claim_title}','{plan}','New','{beneficiary}','{date.today()}','{customer_id}',{hospital_id});"]) # add query here
        flash("Successfully claimed")
        return redirect(f"/claim.html?claim_id={claim_id}") 



@app.route("/addhospital.html")
def addHospital():
    return render_template('addhospital.html') 

@app.route("/newhospital", methods = ['POST'])
def newhospital():
    hospital_name=request.form.get('hospital_name')
    hospital_location=request.form.get('hospital_location')
    phone=request.form.get('phone')
    time_of_work=request.form.get('time_of_work')
    specialization=request.form.get('specialization')
    hospital_description=request.form.get('hospital-description')
    plan_type=request.form.get("plan_type")
    hospital_id= db_con(["select count(*) from Hospital;"])[0][0][0] + 1
    if not hospital_name:
        flash("Missing data: Hospital Name")
        return redirect(request.referrer)
    elif not hospital_location:
        flash("Missing data: Hospital Location")
        return redirect(request.referrer)     
    elif not phone:
        flash("Missing data: Hospital Phone")
        return redirect(request.referrer)
    elif not time_of_work:
        flash("Missing data: Available at")
        return redirect(request.referrer)
    elif not specialization:
        flash("Missing data: Specialization")
        return redirect(request.referrer)
    elif not hospital_description:
        flash("Missing data: Hospital Description")
        return redirect(request.referrer)
    elif not plan_type:
        flash("Missing data: Hospital Plan Type")
        return redirect(request.referrer)
    else:
        
        x = db_con([
                    f"insert into  Hospital values  ({hospital_id},'{hospital_name}','{phone}','{hospital_location}','{time_of_work}','{specialization}','{hospital_description}');",
                    f"insert into enroll values({hospital_id},'{plan_type}');"
                    ]) # add query here
        flash("Successfully added")
        return redirect(request.referrer)  


@app.route("/admin.html")
def admin():
    claims1,users1,hospitals1=db_con([
                                        "select status,count(Claim_id) from Claims group by status;",
                                        "select status,count(Claim_id) from Claims group by Cust_id;",
                                        "select hospital_name,count(Claim_id) from Claims natural right outer join Hospital group by hospital_id;",
                                        ]) #list of queries
    
    return render_template('admin.html' , claims= claims1 , users=users1 , hospitals=hospitals1)   

@app.route("/claim.html")
def claim():
    claim_id=request.args.get('claim_id')
    record= db_con([f"select Claim_id,date_claim,hospital_name,amount_of_expense,status from Claims natural join Hospital where claim_id={int(claim_id)}"])[0] #query here
    return render_template('claim.html',claim=record)

@app.route("/claims.html")
def claims():
    status=request.args.get('type')
    user=request.args.get('user')
    if user and not status :
        claims1=db_con([f"select Claim_id,status from Claims where Cust_id='{user}';"])
    elif status and not user:
        claims1=db_con([f"select Claim_id,status from Claims where status='{status}';"])
    else:
        claims1=db_con(["select Claim_id,status from Claims;"])   
    return render_template('claims.html',claims=claims1)            
@app.route('/resolve')
def resolve():
    claim_id=request.args.get('claim_id')
    x=db_con([f"update Claims set status ='Resolved' where claim_id={int(claim_id)};"])
    return redirect(request.referrer)
@app.route('/unresolve')
def unresolve():
    claim_id=request.args.get('claim_id')
    x=db_con([f"update Claims set status ='Unresolve' where claim_id={int(claim_id)};"])
    return redirect(request.referrer)


@app.route("/customer.html")
def customer():
    customer_id=request.args.get('customer_id')
    if not customer_id:
        return redirect("/login.html")
    else:
        user1,plans1,plan1,claims1,dependents1,purchased1=db_con([
                                                    f"select fname,Cust_id,Gender,date_of_birth,Phone,Money,lname from Customer where Cust_id='{customer_id}';",
                                                    "Select Type_plan, Price, Other_Plan_details from sub_Plan;",    
                                                    f"select Customer.Plan_id,expire_date,Type_plan from Customer join Plan on Customer.Plan_id=Plan.Plan_id where Customer.Cust_id='{customer_id}';",
                                                    f"select Claim_id,amount_of_expense,date_claim from Claims where Cust_id='{customer_id}' order by Claim_id; ",
                                                    f"select * from Dependents where Cust_id='{customer_id}' order by Dept_id;",
                                                    f"Select Plan_id,expire_date,Type_plan from Plan where purchase_cust_id='{customer_id}' order by Plan_id;"
                                                    ]) #list of queries


        return render_template('customer.html', user=user1 , plans=plans1 , plan=plan1 , claims=claims1 ,purchased=purchased1, dependents=dependents1)  



#gggggggg/customer.html?cu_id=sdfdf
@app.route("/newdependent", methods = ['POST'])
def newdependent():
    customer_id=request.form.get('custId')
    fname=request.form.get('fname')
    bday=request.form.get('bday')
    gender=request.form.get('gender')
    relation=request.form.get('relation')
    plan_id=request.form.get('plan_id')
    if not fname:
        flash("Missing data: Name")
        return redirect(request.referrer)
    elif not bday:
        flash("Missing data: Date of birth")
        return redirect(request.referrer)
    elif not gender:
        flash("Missing data: Gender")
        return redirect(request.referrer)     
    elif not relation:
        flash("Missing data: Relationship")
        return redirect(request.referrer)
    elif not plan_id:
        flash("Missing data: Plan ID")
        return redirect(request.referrer)
    else:
        dept_id=db_con(["select count(*) from Dependents;"])[0][0][0]+10
        
        x=db_con([f"insert into Dependents values('{customer_id}','{dept_id}' ,'{fname}' ,'{bday}','{gender}','{relation}','{plan_id}');"]) # add query here
        flash("Successfully added")
        return redirect(request.referrer)   


@app.route("/addplan.html")
def addplan():
    customer_id=request.args.get("customer_id")
    plan_type1=request.args.get("plan_type")
    print(customer_id)
    user1,dependents1=db_con([
                f"select fname,lname from Customer where Cust_id='{customer_id}';",
                f"select D_name from Dependents where Cust_id='{customer_id}';"
                ])
    return render_template('addplan.html', user=user1,customer=customer_id,plan_type=plan_type1,dependents=dependents1)

@app.route("/newplan", methods = ['POST'])
def newplan():
    customer_id=request.form.get("custId")
    plan_type=request.form.get("plan_type")
    ssn=request.form.get('ssn')
    dependent_name=request.form.get('dependent_name')
    if not ssn:
        flash("Missing data: ID")
        return redirect(request.referrer)
    elif not dependent_name:
        flash("Missing data: Dependent Name")
        return redirect(request.referrer)      
    else:
        plan_id,price,money=db_con([
                            "select count(*) from Plan",
                            f"Select price from sub_Plan where Type_plan = '{plan_type}';",
                            f"select Money from Customer where Cust_id='{customer_id}';"
                            ])
        expired = date.today() +  timedelta(days=365)
        if dependent_name=="me":
            x=db_con([
                    f"insert into Plan values('{plan_id[0][0]+1}','{plan_type}','{expired}','{customer_id}');",
                    f"update Customer set Plan_id='{plan_id[0][0]+1}' where Cust_id='{customer_id}';",
                    f"update Customer set Money={money[0][0]-price[0][0]} where Cust_id='{customer_id}';"


                    ])
        else:
            x=db_con([
                    f"insert into Plan values('{plan_id[0][0]+1}','{plan_type}','{expired}','{customer_id}');",
                    f"update Dependents set Plan_id='{plan_id[0][0]+1}' where D_name='{dependent_name}' and Cust_id='{customer_id}';",
                    f"update Customer set Money={money[0][0]-price[0][0]} where Cust_id='{customer_id}';"


                    ])
        flash("Successfully added")
        return redirect(f"/customer.html?customer_id={customer_id}")    




@app.route("/login.html")
def login():
    return render_template('login.html')

@app.route("/login" , methods = ['POST'])
def login_action():
    customer_id= request.form.get('uname')
    if not customer_id:
        flash("Missing data: User_id")
        return redirect(request.referrer)
    elif customer_id =='admin':
        return redirect('admin.html')       
    else:
        users=db_con(["select Cust_id from Customer;"])[0]
        if (customer_id,) in users:
            return redirect(f'/customer.html?customer_id={customer_id}')
        else:
            flash("User is not in our Database")
            return redirect(request.referrer)        

@app.route("/register.html")
def register():
    return render_template('register.html')  
 


@app.route("/newuser", methods = ['POST'])
def newuser():
    cust_id=request.form.get('id')
    fname=request.form.get('fname')
    lname=request.form.get('lname')
    visa_card=request.form.get('visa_card')
    phone=request.form.get('phone')
    gender=request.form.get('gender')
    bday=request.form.get('bday')
    plan_type=request.form.get("plan_type")
    if not cust_id:
        flash("Missing data: SSN ID")
        return redirect(request.referrer)
    elif not fname:
        flash("Missing data: First Name")
        return redirect(request.referrer)
    elif not lname:
        flash("Missing data: Last Name")
        return redirect(request.referrer)  
    elif not visa_card:
        flash("Missing data: Visa card Number")
        return redirect(request.referrer) 
    elif not phone:
        flash("Missing data: Phone Number")
        return redirect(request.referrer)
    elif not gender:
        flash("Missing data: Gender")
        return redirect(request.referrer) 
    elif not bday:
        flash("Missing data: Date Of Birth")
        return redirect(request.referrer) 
    else:
        plan_id,price=db_con([
                            "select count(*) from Plan",
                            f"Select price from sub_Plan where Type_plan = '{plan_type}';",
                            ])
        expired = date.today() +  timedelta(days=365)
        
        money=randint(1,9)*10000
        
        x=db_con([
                f"insert into  Customer values('{cust_id}','{fname}' ,'{lname}' ,{money} ,'{visa_card}' ,'{phone}' , '{gender}','{bday}' ,'{plan_id[0][0]+1}'); ",
                f"insert into Plan values('{plan_id[0][0]+1}','{plan_type}','{expired}','{cust_id}');",
                f"update Customer set Money={money-price[0][0]} where Cust_id='{cust_id}';"
                    ])
        return redirect(f'/login.html')
@app.route("/users.html")
def users():
    data1=db_con(["select fname,lname,(select count(Claim_id) from Claims as c where status='New' and c.Cust_id=Claims.Cust_id) as n,(select count(Claim_id) from Claims as c where status='Resolved' and c.Cust_id=Claims.Cust_id) as r,(select count(Claim_id) from Claims as c where status='Unresolved' and c.Cust_id=Claims.Cust_id) as u,count(Claim_id),Customer.Cust_id from Customer natural join Claims group by Cust_id ;"])
    return render_template('users.html' , data=data1)  


