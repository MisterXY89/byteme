
from app_init import *

from src.data_loading import (
    load_swipe_items,
    save_swipe_preferences,
    load_swipe_preferences
)

from src.recommend import Recommender

USER_TOTAL = 2
GROUP_SIZE = 2

@app.route('/')
def index():
	return render_template("index.html")
	
@app.route('/results')
def results():
    # return "results"
	return render_template("results.html")

@app.route('/getResults/round/<int:matching_round>/user/<string:user_name>')
def getResults(matching_round, user_name):

    swipe_preferences = load_swipe_preferences()
    user_idx = swipe_preferences[swipe_preferences["user_name"] == user_name].index.to_list()[0]

    kind_round_list = ["similar", "motivation", "random"]
    recommender = Recommender()
    recommender.fit()
    results = recommender.recommend(kind=kind_round_list[matching_round-1], group_size=GROUP_SIZE)
    
    # get group for user_idx (where user_idx is in group) - results is a dict with lists
    user_group = 0
    for group in results:
        if user_idx in results[group]:
            user_group = group
            break

    return jsonify({
        "success": True,
        "user_group": user_group
    })


@app.route('/checkResults')
def checkResults():
    # check if all users have swiped & return true/false
    # if true, calculate matches and send along with userMail to all users

    swipe_prefs = load_swipe_preferences()
    number_items = len(swipe_prefs)
    ready = False
    if number_items >= USER_TOTAL:
        ready = True
    
    return jsonify({
        "success": True,
        "number_items": number_items,
        "progress": number_items / USER_TOTAL,
        "ready": ready
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

    swipe_items = load_swipe_items()
    return render_template("swipe.html", user_mail=user_mail, user_name=user_name, swipe_items=swipe_items, effort=effort, preference=preference)

if __name__ == '__main__':
    print("Listening on port " + str(cf.PORT))
    print(cf.DEBUG, type(cf.DEBUG))
    app.run(host='0.0.0.0', port=cf.PORT, debug=cf.DEBUG)