
import os
import pandas as pd

# get absolute dir of data ( parent of parent of this file)
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data")) + "/"

# get absolute path of swipe_preferences.csv
SWIPE_PREFERENCES_FILE = DATA_PATH + "data.csv"
SWIPE_PREFERENCES_FILE_SEP = ";"


def explode_items(df, column):
    df[column] = df[column].str.split('\n')
    expanded_df = df.explode(column)
    expanded_df.dropna(inplace=True)
    expanded_df.reset_index(drop=True, inplace=True)
    return expanded_df

def add_swipe_type_id(df, swipe_type):    
    df["swipe_type_id"] = df[swipe_type].apply(lambda x: x.replace(" ", "_").lower()[:15])
    return df

def load_swipe_items(limit=0):
    # exclude userMail from swipe_items
    df = pd.read_csv(
        DATA_PATH + "methods_topics.csv",
        names=["time", "research_interest", "method"],
        header=0
    )
    methods_df = df[["method"]]
    research_interest_df = df[["research_interest"]]

    print(methods_df)

    methods_df = explode_items(methods_df, "method")
    research_interest_df = explode_items(research_interest_df, "research_interest")

    methods_df = add_swipe_type_id(methods_df, "method")
    research_interest_df = add_swipe_type_id(research_interest_df, "research_interest") 

    methods_df["swipe_type"] = "method"
    research_interest_df["swipe_type"] = "research_interest"

    if limit > 0:
        methods_df = methods_df.head(limit)
        research_interest_df = research_interest_df.head(limit)

    methods_dict = methods_df.to_dict(orient="records")
    research_interes_dict = research_interest_df.to_dict(orient="records")

    items = [
        {"swipe_type": "research_interest_intro", "swipe_type_id": "research_interest_intro"},
        *research_interes_dict,
        {"swipe_type": "method_intro", "swipe_type_id": "method_intro"},
        *methods_dict
    ]

    return items

def get_name2id_dict(prefs, force=False):
    # check if file exists
    # if not, create file with default values

    # prepend "research_" or "method_" to key depending on swipe_type
    get_key = lambda swipe_type, key: swipe_type.split("_")[0].upper() + "_" + key

    if not os.path.isfile(DATA_PATH + "topic_to_id.csv") or force:
        print("topic_to_id.csv does not exist")
        topic_to_id = {
            get_key(prefs[key]["swipe_type"], key): prefs[key]["text_full"] for key in prefs
        }

        topic_to_id_df = pd.DataFrame.from_dict(topic_to_id, orient="index", columns=["name"])
        # save topic_to_id_df to file using pandas 
        print(topic_to_id_df)

        topic_to_id_df.to_csv(DATA_PATH + "topic_to_id.csv", index=True, header=False)
    else:
        print("topic_to_id.csv exists")
        topic_to_id_df = pd.read_csv(DATA_PATH + "topic_to_id.csv", names=["name_id", "name"])
    
    return topic_to_id_df

def prepare_pref_file(interest_keys, force=False):
    header_cols = ["user_mail", "user_name", "preference", "effort", "full_text"] + interest_keys

    if not os.path.isfile(SWIPE_PREFERENCES_FILE) or force:
        print("swipe_preferences.csv does not exist")
        swipe_preferences_df = pd.DataFrame(columns=header_cols)
        swipe_preferences_df.to_csv(SWIPE_PREFERENCES_FILE, index=False, sep=SWIPE_PREFERENCES_FILE_SEP)
    else:
        print("swipe_preferences.csv exists")
        swipe_preferences_df = pd.read_csv(SWIPE_PREFERENCES_FILE, sep=SWIPE_PREFERENCES_FILE_SEP)
        if list(swipe_preferences_df.columns) != header_cols:
            prepare_pref_file(interest_keys, force=True)

def load_swipe_preferences():
    return pd.read_csv(SWIPE_PREFERENCES_FILE, sep=SWIPE_PREFERENCES_FILE_SEP)

def save_swipe_preferences(swipe_dict):
    # append new line to file // create new if not exists

    user_mail = swipe_dict["user_mail"]
    user_name = swipe_dict["user_name"]
    swipes = swipe_dict["swipes"]
    # interest_keys = get_interest_keys(swipes)

    name2id = get_name2id_dict(swipes, force=True)

    print(name2id)

    # check if file exists and create if not
    prepare_pref_file(name2id.index.to_list())

    with open(SWIPE_PREFERENCES_FILE, "+a") as fi:
        user_swipes_line = SWIPE_PREFERENCES_FILE_SEP.join([
            user_mail, 
            user_name, 
            str(swipe_dict["preference"]),
            str(swipe_dict["effort"])
        ])
        user_swipes_line += SWIPE_PREFERENCES_FILE_SEP
        for swipe_key in swipes:
            print(str(swipes[swipe_key]["value"]))
            user_swipes_line += SWIPE_PREFERENCES_FILE_SEP.join([                
                str(swipes[swipe_key]["value"])
            ])
            user_swipes_line += SWIPE_PREFERENCES_FILE_SEP

        user_swipes_line += "\n"
        fi.write(user_swipes_line)


if __name__ == "__main__":
    print(DATA_PATH)

    swipe_items = load_swipe_items()
    print(swipe_items)
