
import os
import pandas as pd

# get absolute dir of data ( parent of parent of this file)
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data")) + "/"


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


def save_swipe_preferences(swipe_dict):
    # save swipe_preferences to file using pandas
    df = pd.DataFrame(swipe_dict)
    print(df)
    df.to_csv("data/swipe_preferences.csv", index=False)


if __name__ == "__main__":
    print(DATA_PATH)

    swipe_items = load_swipe_items()
    print(swipe_items)
