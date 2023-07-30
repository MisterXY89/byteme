
from app_init import *

from src.data_loading import (
    load_swipe_items,
    save_swipe_preferences
)

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
    


@app.route('/swipe', methods=['GET', 'POST'])
def swipe():
    # POST request
    if request.method == 'POST':    
        swipe_preferences = request.json
        print(swipe_preferences["user_mail"])

        # save swipe_preferences to file using pandas
        save_swipe_preferences(swipe_preferences)

        return jsonify(
            success=True,
        )
    
    # GET request
    user_name = request.args.get('userName')
    # user_mail = request.args.get('userMail')
    user_mail = user_name + "@test.com"
    effort = request.args.get('effort')
    preference = request.args.get('preference')
    
    print("Effort: ", effort)
    print("Preference: ", preference)

    swipe_items = load_swipe_items(limit = 2)
    return render_template("swipe.html", user_mail=user_mail, user_name=user_name, swipe_items=swipe_items, effort=effort, preference=preference)

if __name__ == '__main__':
    print("Listening on port " + str(cf.PORT))
    print(cf.DEBUG, type(cf.DEBUG))
    app.run(host='0.0.0.0', port=cf.PORT, debug=cf.DEBUG)