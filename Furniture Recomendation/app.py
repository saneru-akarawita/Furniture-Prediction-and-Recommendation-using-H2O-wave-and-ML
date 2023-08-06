from furniture_rec.rec_func import furniture_recommender
from h2o_wave import Q, main, app, ui
from fuzzywuzzy import process
from typing import Any

def search_furniture(furniture_name: str) -> list[tuple[Any, Any | int, Any] | tuple[Any, Any | int]]:
    print("came to search_furniture")
    """
    Find similar furniture items name wise (using Levenshtein distance).
    """
    return process.extract(furniture_name, furniture_recommender.furniture_names)


@app("/recommender")
async def serve(q: Q):
    print("came to /recommender serve")
    """
    Displays the recommended furniture items according to the input.
    If the user cannot find the furniture item, they can find furniture items that match the given input.
    """
    msg = ""
    print(q.args.search)
    if not q.client.initialized:
        q.client.initialized = True
        

    if q.args.search:
        del q.page["furniture"]
        q.args.search_box_input = q.args.search_box_input.strip()
        if q.args.search_box_input in furniture_recommender.furniture_names:
            result = furniture_recommender.recommend(q.args.search_box_input)
            print("did is go here?")
            msg = f"If you like {q.args.search_box_input}, you may also like these furniture items!"
            add_furniture_cards(result, q)

        elif q.args.search_box_input is None or q.args.search_box_input == "":
            msg = "Furniture name cannot be blanked."
            print("did is go here? here?")

        else:
            print("did is go here? here? here?")
            msg = f'"{q.args.search_box_input}" is not in our database or an invalid furniture name.\
            Use the "Find Furniture" button to find furniture items'

    if q.args.find_furniture:
        print("name catched from here?")
        q.args.search_box_input = q.args.search_box_input.strip()
        if q.args.search_box_input is None or q.args.search_box_input == "":
            msg = "Furniture name cannot be blanked."
        else:
            for i in range(1, 6):
                del q.page[f"furniture{i}"]
            add_similar_furniture(q)

    add_search_box(q, msg)
    add_header(q)
    add_footer(q)

    await q.page.save()


def add_similar_furniture(q: Q):
    print("came to add_similar_furniture")
    similar_furniture = search_furniture(q.args.search_box_input)
    q.page["furniture"] = ui.form_card(
        box="2 4 10 7",
        items=[
            ui.copyable_text(
                value=furniture[0],
                name=f"furniture_match{i+1}",
                label=f"{furniture[1]}% match",
            )
            for i, furniture in enumerate(similar_furniture)
        ],
    )


def add_header(q: Q):
    print("came to add_header")
    q.page["header"] = ui.header_card(
        box="2 1 10 1",
        title="Furniture Recommendation System",
        subtitle="Collaborative filtering based recommender system for furniture items",
        icon="Furniture",
        items=[
            ui.link(
                name="github_btn",
                path="https://github.com/YourUsername/furniture-recommendation-system_using_h2o-wave.git",
                label="GitHub",
                button=True,
            )
        ],
    )


def add_furniture_cards(result, q: Q):
    print("came to add_furniture_cards")
    print(result)
    num_items = min(len(result), 5)
    for i in range(1, num_items + 1):
        q.page[f"furniture{i}"] = ui.tall_article_preview_card(
            box=f"{2*i} 4 2 7",
            title=f"{result[i-1].name}",
            subtitle=f"{result[i-1].category}",
            value=f"${result[i-1].price}",
            name="tall_article",
            image=f"{result[i-1].image_url}",
            items=[
                ui.text(f"Material: {result[i-1].material}", size="l"),
                ui.text(f"Furniture ID: {result[i-1].furniture_id}", size="m"),
            ],
        )

def add_search_box(q: Q, msg):
    print("came to add_search_box")
    q.page["search_box"] = ui.form_card(
        box="2 2 10 2",
        items=[
            ui.textbox(
                name="search_box_input",
                label="Furniture Name",
                value=q.args.search_box_input,
            ),
            ui.buttons(
                items=[
                    
                    ui.button(name="find_furniture", label="Find Furniture", primary=False),
                ]
            ),
            ui.text(msg, size="m", name="msg_text"),
        ],
    )


def add_footer(q: Q):
    caption = """__Made with 💛 by Saneru Akarawita__ <br /> using __[h2o Wave](https://wave.h2o.ai/docs/getting-started).__"""
    q.page["footer"] = ui.footer_card(
        box="2 11 10 2",
        caption=caption,
        items=[
            ui.inline(
                justify="end",
                items=[
                    ui.links(
                        label="Contact Me",
                        width="200px",
                        items=[
                            ui.link(
                                name="github",
                                label="GitHub",
                                path="https://github.com/saneru-akarawita",
                                target="_blank",
                            ),
                            ui.link(
                                name="linkedin",
                                label="LinkedIn",
                                path="https://www.linkedin.com/in/saneru-akarawita-17a700216/",
                                target="_blank",
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )
