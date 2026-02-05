import random



DATA = [
    {
        "country": "France",
        "city": "Paris",
        "clues": {
            "continent": "Europe",
            "capital": "Yes",
            "climate_hint": "умерена клима, чести дождови",
            "fun_hint": "познат по голема железна кула",
        },
    },
    {
        "country": "Japan",
        "city": "Tokyo",
        "clues": {
            "continent": "Asia",
            "capital": "Yes",
            "climate_hint": "влажно лето, блага зима",
            "fun_hint": "еден од најголемите мегалополиси во светот",
        },
    },
    {
        "country": "Brazil",
        "city": "Rio de Janeiro",
        "clues": {
            "continent": "South America",
            "capital": "No",
            "climate_hint": "топло, близу океан",
            "fun_hint": "познат по огромна статуа на рид",
        },
    },
    {
        "country": "Egypt",
        "city": "Cairo",
        "clues": {
            "continent": "Africa",
            "capital": "Yes",
            "climate_hint": "сува клима, многу сонце",
            "fun_hint": "во близина има древни пирамиди",
        },
    },
    {
        "country": "Australia",
        "city": "Sydney",
        "clues": {
            "continent": "Oceania",
            "capital": "No",
            "climate_hint": "умерено-топло, крај море",
            "fun_hint": "има позната опера со ‘школки’",
        },
    },
]

def create_new_game_payload(difficulty: str = "easy") -> dict:
    item = random.choice(DATA)

    base_clues = {
        "континент": item["clues"]["continent"],
        "главен град?": "да" if item["clues"]["capital"] == "Yes" else "не",
    }


    if difficulty in {"easy"}:
        base_clues["клима"] = item["clues"]["climate_hint"]
        base_clues["фан трага"] = item["clues"]["fun_hint"]
    elif difficulty in {"medium"}:
        base_clues["клима"] = item["clues"]["climate_hint"]
    else:

        pass

    return {
        "target_country": item["country"],
        "target_city": item["city"],
        "clues": base_clues,
    }
