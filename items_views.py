from fastapi import APIRouter

router = APIRouter(prefix="/items")


@router.get("/")
def get_items_list():
    return {
        "item1": {"id": 1, "title": "item1"},
        "item2": {"id": 2, "title": "item2"},
        "item3": {"id": 3, "title": "item3"},
        "item4": {"id": 4, "title": "item4"},
        "item5": {"id": 5, "title": "item5"},
    }


@router.get("/{item_id}/")
def get_item(item_id: int):
    return {
        "item_id": item_id,
        "item_title": f"item with id = {item_id}",
    }
