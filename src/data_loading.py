import pandas as pd


def load_swipe_items():
    # exclude userMail from swipe_items
    df = pd.read_csv("data/MOCK_DATA.csv")
    methods_df = pd.read_csv("data/MOCK_methods.csv")
    research_interest_df = pd.read_csv("data/MOCK_DATA_topic.csv")

    methods_df["swipe_type"] = "method"
    research_interest_df["swipe_type"] = "topic"

    methods_dict = methods_df.to_dict(orient="records")
    research_interes_dict = research_interest_df.to_dict(orient="records")

    items = [
        {"swipe_type": "researchInterestIntro"},
        research_interes_dict,
        {"swipe_type": "methodIntro"},
        methods_dict
    ]
    
    df["swipe_type"] = ["researchInterestIntro", "topic", "topic", "methodIntro", "method"]

    print(df)

    return df.to_dict(orient="records")


def save_swipe_preferences(swipe_dict):
    # save swipe_preferences to file using pandas
    df = pd.DataFrame(swipe_dict)
    print(df)
    df.to_csv("data/swipe_preferences.csv", index=False)


if __name__ == "__main__":
    swipe_items = load_swipe_items("bwoollam1d@nytimes.com")
    print(swipe_items)
