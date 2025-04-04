from sqlalchemy.orm import Session
from models import Items, Users

def get_all_items_from_db(db: Session, user_id: int):
    try:
        return db.query(Items).filter(Items.owner_id == user_id).all()
    except Exception as e:
        raise Exception(f"Error fetching items: {str(e)}")

def get_item_from_db(db: Session, item_id: int, user_id: int):
    try:
        return db.query(Items).filter(Items.id == item_id, Items.owner_id == user_id).first()
    except Exception as e:
        raise Exception(f"Error fetching item: {str(e)}")

def delete_item_by_id_from_db(db: Session, item_id: int, user_id: int):
    try:
        db.query(Items).filter(Items.id == item_id, Items.owner_id == user_id).delete()
        db.commit()
    except Exception as e:
        raise Exception(f"Error deleting item: {str(e)}")

def get_user_by_username_from_db(db: Session, username: str):
    try:
        return db.query(Users).filter(Users.username == username).first()
    except Exception as e:
        raise Exception(f"Error fetching user: {str(e)}")
