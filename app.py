
from app_init import *

from src.data_loading import (
    load_swipe_items,
    save_swipe_preferences,
    load_swipe_preferences
)

from src.recommend import Recommender

USER_TOTAL = 2

@app.route('/')
def index():
	return render_template("index.html")
	
@app.route('/results')
def results():
    # return "results"
	return render_template("results.html")


@app.route('/checkResults')
def checkResults():
    # check if all users have swiped & return true/false
    # if true, calculate matches and send along with userMail to all users

    number_items = len(load_swipe_preferences())
    results = []
    results_ready = number_items >= USER_TOTAL
    if results_ready:
        # recommender = Recommender()
        # recommender.fit()
        # results = recommender.predict()
        pass

    return jsonify({
        "success": True,
        "number_items": number_items,
        "progress": number_items / USER_TOTAL,
        "results": results
    })
    

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