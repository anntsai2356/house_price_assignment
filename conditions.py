class Conditions:
    years = ["106", "107", "108", "109"]
    quarters = ["1", "2", "3", "4"]
    real_estate_cities = {
        "A": "臺北市",
        "F": "新北市",
        "E": "高雄市",
    }
    pre_sale_cities = {
        "H": "桃園市",
        "B": "臺中市",
    }
    transaction_types = {
        "A": {
            "name": "real estate sales",
            "cities": real_estate_cities,
        },
        "B": {
            "name": "pre-sale house sales",
            "cities": pre_sale_cities,
        },
    }
