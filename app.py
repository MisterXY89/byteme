
from app_init import *

from src.data_loading import load_swipe_items

@app.route('/')
def index():
	return render_template("index.html")
	
@app.route('/results')
def results():
     return "results"
	# return render_template("results.html")


@app.route('/checkResults')
def checkResults():
    # check if all users have swiped & return true/false
    # if true, calculate matches and send along with userMail to all users
    return "checkResults"
    


# swipe post --> read preferences from request and save file
@app.route('/swipe', methods=['POST'])
def swipe_post():
    swipe_preferences = request.form
    print(swipe_preferences)

    # save swipe_preferences to file using pandas
    save_swipe_preferences(swipe_preferences)





@app.route('/swipe')
def swipe():
    # GET userMail from request
    
    userMail = request.args.get('userMail')
    print(userMail)

    # TODO: between swipe Items add: methodIntro and researchInterestIntro as swipe_types

    swipe_items = load_swipe_items()
    print(swipe_items)
    # swipe_items = []
    return render_template("swipe.html", userMail=userMail, swipe_items=swipe_items)

if __name__ == '__main__':
    print("Listening on port " + str(cf.PORT))
    print(cf.DEBUG, type(cf.DEBUG))
    app.run(host='0.0.0.0', port=cf.PORT, debug=cf.DEBUG)