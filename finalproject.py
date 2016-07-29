from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
app = Flask(__name__)
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
app = Flask(__name__)
import datetime
from sqlalchemy import create_engine, func, Date
from sqlalchemy.orm import sessionmaker
from dbsetup import Shelter, Adopter, Puppy, Profile, Base

engine = create_engine('sqlite:///puppyshelterfinalproject.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

@app.route('/')
@app.route('/puppyproject/')  #flask will render the page with or without the trailing /
def welcome():
    #return "This page will welcome visitors"
    return render_template('welcome.html')

@app.route('/puppyproject/shelters/')
@app.route('/puppyproject/shelters/<int:employee>/') # will have extra editing options for employees
#@app.route('/puppyproject/employees/shelters/')
def showShelters(employee=0):
        #return "This page will list shelters"
    shelters = session.query(Shelter).all()
    return render_template('shelters.html', shelters = shelters, employee = employee)
@app.route('/puppyproject/shelters/<int:shelter_id>/puppies')
@app.route('/puppyproject/shelters/<int:shelter_id>/<int:employee>')
def showShelterPuppies(shelter_id,employee=0):
    pups = session.query(Puppy).filter_by(shelter_id=shelter_id).filter(Puppy.adopters == None)
    if pups.first() == None:
        flash("No Puppies Found at shelter ",shelter_id)
        return redirect(url_for('welcome'))
    else:
        pups = pups.all()
        return render_template('shelter.html', puppies = pups, employee = employee )
        #return "This page will show puppies in shelter : %s"%shelter_id
@app.route('/puppyproject/employees/shelters/new/', methods=['GET','POST'])
def newShelter():
    if request.method == 'POST':
        if request.form['name'] == '':
            flash("Shelter must have a name!")
            return redirect(url_for('newShelter'))
        capacity = request.form['capacity']
        if capacity.isnumeric() == False:
            capacity = 0
            flash("Capacity must be numeric.  Zero set as default.")
        shelter=Shelter(name = request.form['name'], address = request.form['address'], city = request.form['city'], state = request.form['state'], zipCode = request.form['zip'], website = request.form['website'], maximum_capacity = capacity, current_occupancy = 0)
        session.add(shelter)
        session.commit()
        flash("New Shelter Added")
        return redirect(url_for('showShelters', employee = 1))
    else : return render_template('newshelter.html')
@app.route('/puppyproject/employees/shelters/<int:shelter_id>/edit/', methods=['GET','POST'])
def editShelter(shelter_id):
    editedShelter = session.query(Shelter).filter_by(id = shelter_id).one()
        
    if request.method == 'POST':
        
        name = request.form['name']
        if name != '':
            editedShelter.name = name
        address = request.form['address']
        if address != '':
            editedShelter.address = address
        city = request.form['city']
        if city != '':
            editedShelter.city = city
        state = request.form['state']
        if state != '':
            editedShelter.state = state
        zipCode = request.form['zip']
        if zipCode != '':
            editedShelter.zipCode = zipCode
        website = request.form['website']
        if website != '':
            editedShelter.website = website
        capacity = request.form['capacity']
        if capacity != '':
            if capacity.isnumeric():
                editedShelter.maximum_capacity = capacity
            else: 
                flash("Capacity must be numeric!")
                return render_template('editshelter.html',shelter = editedShelter)
        occupancy = request.form['occupancy']
        if occupancy != '':
            if occupancy.isnumeric():
                editedShelter.current_occupancy = occupancy
            else: 
                flash("Occupancy must be numeric!")
                return render_template('editshelter.html',shelter = editedShelter)
        session.add(editedShelter)
        session.commit()
        flash("Shelter Modified")
        return redirect(url_for('showShelters', employee=1))
    else : return render_template('editshelter.html',shelter = editedShelter)
@app.route('/puppyproject/employees/shelters/<int:shelter_id>/delete/', methods=['GET','POST'])
def deleteShelter(shelter_id):
    obsoleteShelter = session.query(Shelter).filter_by(id = shelter_id).one()
        #return "This page will allow user to delete shelter : %s"%shelter_id
    if request.method == 'POST':
        session.delete(obsoleteShelter)
        session.commit()
        flash("Shelter Deleted.")
        return redirect(url_for("showShelters", employee=1))
    else : 
        return render_template('deleteshelter.html', shelter = obsoleteShelter)
@app.route('/puppyproject/employees/adopters/')
def showAdopters():
    adopters = session.query(Adopter).all()
    return render_template('adopters.html',adopters = adopters)
@app.route('/puppyproject/employees/adopters/new/', methods=['GET','POST'])
def newAdopter():
    if request.method == 'POST':
        adopterName = request.form['name']
        if  adopterName == '':
            flash("Adopter must have a name!")
            return redirect(url_for('newAdopter'))
        else:
            adopter = Adopter(name=adopterName, phone = request.form['phone'] )
            session.add(adopter)
            session.commit()
            flash("Adopter added!")
            return redirect(url_for('showAdopters'))
        
    else : return render_template('newadopter.html')
@app.route('/puppyproject/employees/adopters/<int:adopter_id>/edit/', methods=['GET','POST'])
def editAdopter(adopter_id):
    adopter = session.query(Adopter).filter_by(id=adopter_id).one()
    
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        if name != '':
            adopter.name = name
        if phone != '':
            adopter.phone = phone
        session.add(adopter)
        session.commit()
        flash("Adopter edited")
        return redirect(url_for('showAdopters'))
    else : return render_template('editadopter.html', adopter = adopter)
@app.route('/puppyproject/employees/adopters/<int:adopter_id>/delete/', methods=['GET','POST'])
def deleteAdopter(adopter_id):
    adopter = session.query(Adopter).filter_by(id=adopter_id).one()
    if request.method == 'POST':       
        session.delete(adopter)
        session.commit()
        flash("Adopter Deleted.")
        return redirect(url_for("showAdopters"))
    else : return render_template('deleteadopter.html',adopter = adopter)
@app.route('/puppyproject/employees/puppies/new/', methods=['GET','POST'])
def newPuppy():
    if request.method == 'POST':
        newName = request.form['name'].title()
        if newName == '':
            flash("Name cannot be left blank!")
            return redirect(url_for("newPuppy"))
        sex = request.form['gender'].lower()
        if sex == '':
            flash("Gender cannot be left blank!")
            return redirect(url_for("newPuppy"))
        dob = request.form['birth']
        try:
            newDateOfBirth = datetime.datetime.strptime(dob,'%Y-%m-%d')
        except ValueError:
            flash("Incorrect date format! Use yyy-mm-dd")
            return render_template('editpuppy.html', pup = pup)
        newProfile = Profile(picture = request.form['picture'], description = request.form['description'], needs = request.form['needs'])
        session.add(newProfile)
        session.commit()
        newBreed = request.form['breed'].title()       
        newWeight = request.form['weight']
        if newWeight == '': 
            newWeight = 0.0
        else:
            if is_number(newWeight):
                newWeight = float(newWeight)
            else:                
                flash("Weight must be numeric!") 
                return render_template('newpuppy.html')
        pup = Puppy(name = newName, breed = newBreed, gender = sex, dateOfBirth = newDateOfBirth, weight = newWeight, profile_id = newProfile.id)
        session.add(pup)
        session.commit()
        flash("New Puppy Added!")
        return redirect(url_for("showPuppy",puppy_id = pup.id, employee = 1))        
    else : 
        return render_template('newpuppy.html')
@app.route('/puppyproject/employees/puppies/<int:puppy_id>/edit/', methods=['GET','POST'])
def editPuppy(puppy_id):
    
    pup = session.query(Puppy).filter_by(id=puppy_id).one()
        #return "This page will allow user to edit puppy : %s"%puppy_id
    if request.method == 'POST':
        pupPicture = request.form['picture']
        pupDescription = request.form['description']
        pupNeeds = request.form['needs']
        pupName = request.form['name']
        pupBreed = request.form['breed']
        pupGender = request.form['gender']
        pupBirth = request.form['birth']
        pupWeight = request.form['weight']
        if (pupPicture!='' or pupDescription !='' or pupNeeds!= ''):
            if pupPicture != '':
                pup.profile.picture = pupPicture
            if pupDescription != '':
                pup.profile.description = pupDescription
            if pupNeeds != '':
                pup.profile.needs = pupNeeds
            session.add(pup.profile)
            session.commit()
        if pupName != '':
            pup.name = pupName.title()
        if pupBreed != '':
            pup.breed = pupBreed.title()
        if pupGender != '':
            pup.gender = pupGender.lower()
        if pupBirth != '':
            try:
                dob = datetime.datetime.strptime(pupBirth,'%Y-%m-%d')
            except ValueError:
                flash("Incorrect date format! Use yyy-mm-dd")
                return render_template('editpuppy.html', pup = pup)
            pup.dateOfBirth = dob
            
        if pupWeight != '':
            if is_number(pupWeight):
                pup.weight = pupWeight
            else:
                flash("Weight must be numeric") 
                pup.weight = 0.0
        session.add(pup)
        session.commit()
        flash("Puppy updated.")
        return redirect(url_for("showPuppy", puppy_id = pup.id, employee = 1))    
                       
    else : 
        return render_template('editpuppy.html', pup = pup)
@app.route('/puppyproject/employees/puppies/<int:puppy_id>/delete/', methods=['GET','POST'])
def deletePuppy(puppy_id):
    pup = session.query(Puppy).filter_by(id=puppy_id).one()
    if request.method == 'POST':
        session.delete(pup.profile)
        if pup.shelter != None and pup.adopters == []:
            pup.shelter.current_occupancy -= 1
            session.add(pup.shelter)
        session.delete(pup)
        session.commit()
        flash("Puppy deleted.")
        return redirect(url_for("maintainDatabase"))
    else : return render_template('deletepuppy.html',puppy_id=pup.id) 
@app.route('/puppyproject/employees/puppies/<int:puppy_id>/checkin', methods=['GET','POST'])
def checkPuppyIn(puppy_id):
    pup = session.query(Puppy).filter_by(id=puppy_id).one()
    if request.method == 'POST':
        shelter = session.query(Shelter).filter_by(id = request.form['shelter_id']).first()
        if shelter == None:
            flash("No shelter found with that id!")
            return redirect(url_for("showPuppy",puppy_id = puppy_id, employee = 1))
        residents = session.query(func.count(Puppy.id),Puppy.shelter_id).filter(Puppy.adopters == None).filter(Puppy.shelter_id== shelter.id).scalar()
        if residents < shelter.getCapacity():
            if pup.shelter != None:
                pup.shelter.current_occupancy -= 1 #remove puppy from old shelter
                session.add(pup.shelter)
            pup.shelter_id = shelter.id
            pup.adopters = []
            session.add(pup)
            shelter.current_occupancy = residents + 1
            session.add(shelter)
            session.commit()
            flash("Puppy checked in to shelter.")
            return redirect(url_for("showShelterPuppies",shelter_id = shelter.id, employee=1))
        else:
            flash("Shelter full.  Please select alternate.")
            return redirect(url_for("alternateCheckPuppyIn",puppy_id = puppy_id))
    else:
        return render_template('checkin.html',puppy = pup)
@app.route('/puppyproject/employees/puppies/<int:puppy_id>/alternatecheckin', methods=['GET','POST'])
def alternateCheckPuppyIn(puppy_id):
    pup = session.query(Puppy).filter_by(id=puppy_id).one()
    shelters = session.query(Shelter).filter(Shelter.current_occupancy<Shelter.maximum_capacity).order_by((100*Shelter.current_occupancy)/Shelter.maximum_capacity).all()
    if request.method == 'POST':
        shelter = session.query(Shelter).filter_by(id = request.form['shelter_id']).first()
        if shelter == None:
            shelters = session.query(Shelter).filter_by(current_occupancy<maximum_capacity).all()
            flash("No shelter found with that id!")
            return redirect(url_for("alternateCheckPuppyIn",puppy_id = puppy_id, shelters = shelters))
        residents = session.query(func.count(Puppy.id),Puppy.shelter_id).filter(Puppy.adopters == None).filter(Puppy.shelter_id== shelter.id).scalar()
        if residents < shelter.getCapacity():
            pup.shelter_id = shelter.id
            pup.adopters = []
            shelter.current_occupancy = residents + 1
            session.add(pup)
            session.add(shelter)
            session.commit()
            flash("Puppy checked in to shelter.")
            return redirect(url_for("showShelterPuppies",shelter_id = shelter.id, employee=1))
        else:
            flash("Shelter full.  Please select alternate from chocies below.")
            return redirect(url_for("alternateCheckPuppyIn",puppy_id = puppy_id, shelters = shelters))
    else:
        return render_template('alternatecheckin.html', puppy = pup, shelters = shelters)
@app.route('/puppyproject/findpuppy/', methods=['GET','POST'])
def searchPuppies(employee = 0):   
    if request.method == 'POST':
        puppy_id = request.form['puppy_id']
        breed = request.form['breed'].title()
        name = request.form['name'].title()
        if puppy_id != '':
            pup = session.query(Puppy).filter(Puppy.id == puppy_id).first()
            if pup == None:
                flash("No puppy found with that ID!")
                return redirect(url_for("searchPuppies"))
            else:
                return redirect(url_for("showPuppy",puppy_id = puppy_id))
        if name != '': 
            pups = session.query(Puppy).filter(Puppy.adopters == None).filter_by(name = name)
            pup = pups.first()
            pups = pups.all()
            if pup == None:
                flash("No puppy found with that name!")
                return redirect(url_for("searchPuppies"))            
            else:
                if len(pups)  == 1 :
                    return redirect(url_for("showPuppy",puppy_id = pup.id))
                else:
                    return render_template('puppies.html',puppies = pups,employee = employee)
        if breed != '': 
            pups = session.query(Puppy).filter(Puppy.adopters == None).filter_by(breed = breed)
            pup = pups.first()
            pups = pups.all()
            if pup == None:
                flash("No puppies of that breed found ")
                return redirect(url_for("searchPuppies"))            
            else:
                if len(pups)  == 1 :
                    return render_template('puppy.html',pup = pup, employee = employee)  
                else:
                    return render_template('puppies.html',puppies = pups,employee = 0)
        return redirect(url_for("searchPuppies"))
    else:  
        return render_template('findpuppy.html')  
@app.route('/puppyproject/findpuppy/puppy/<int:puppy_id>')
@app.route('/puppyproject/findpuppy/puppy/<int:puppy_id>/<int:employee>')
def showPuppy(puppy_id, employee = 0):
    pup = session.query(Puppy).filter_by(id=puppy_id).one()
        #return "This page will show user puppy id: %s"%puppy_id
    return render_template('puppy.html',pup = pup, employee = employee)  
@app.route('/puppyproject/findpuppy/puppylist')
@app.route('/puppyproject/employees/findpuppy/puppylist')
def showPuppies(puppy_list):
    return render_template('puppies.html',puppies = puppy_list)  
@app.route('/puppyproject/employees/<int:puppy_id>/adopt/', methods=['GET','POST'])
def adoptPuppy(puppy_id):
    pup = session.query(Puppy).filter(Puppy.id == puppy_id).one()
    if request.method == 'POST':
        adopter_id = request.form['adopter_id']
        owner = session.query(Adopter).filter_by(id = adopter_id).first()
        if owner == None:
            flash("Adopter not found!")
            return redirect(url_for("adoptPuppy",puppy_id = puppy_id))
        else:
            pup.adopters.append(owner)
            shelter = session.query(Shelter).filter_by(id = pup.shelter_id).first()
            if shelter != None:
                shelter.current_occupancy -= 1
            session.add(shelter)
            session.add(pup)
            session.commit()
            flash("Puppy adopted!")
            return redirect(url_for("showPuppy",puppy_id = puppy_id, employee = 1))
    else : 
        return render_template('adopt.html',pup= pup)  
@app.route('/puppyproject/employees/', methods=['GET','POST'])
def maintainDatabase():
        #return render_template('maintenance.html')
    if request.method == 'POST':
        pup_id = request.form['puppy_id']
        shelter_id = request.form['shelter_id']
        if pup_id != '':
            puppy = session.query(Puppy).filter_by(id=pup_id).first()
            if puppy == None:
                flash("No puppy found with that ID!")
                return redirect(url_for('maintainDatabase'))
            else:
                return(redirect(url_for('showPuppy',puppy_id = pup_id, employee = 1)))
        if shelter_id != '':
            shelter = session.query(Shelter).filter_by(id=shelter_id).first()
            if shelter == None:
                flash("No shelter found with that ID!")
                return redirect(url_for('maintainDatabase'))
            else:
                return redirect(url_for('editShelter', shelter_id = shelter_id))
        
        return redirect(url_for('maintainDatabase' ))
    else : return render_template('maintenance.html')
@app.route('/puppyproject/employees/count/<int:shelter_id>')
def countResidents(shelter_id):
    residents = session.query(func.count(Puppy.id),Puppy.shelter_id).filter(Puppy.adopters == None).filter(Puppy.shelter_id== shelter_id).scalar() 
    flash(residents)
    print residents
    return redirect(url_for('editShelter', shelter_id = shelter_id)) 
@app.route('/puppyproject/employees/capacity')
def capacityReport():
    shelters = session.query(Shelter).order_by((100*Shelter.current_occupancy)/Shelter.maximum_capacity).all()
    return render_template('capacities.html',shelters = shelters)
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
if __name__ == '__main__':  #only executed if run from interpreter, not if imported
    app.secret_key = 'super_secret_key'
    app.debug = True  # server will reload automatically each time the code changed!
    app.run(host = '0.0.0.0', port = 5000)