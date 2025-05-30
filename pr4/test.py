import uuid
from datetime import datetime, timedelta
from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")
db = client["personal_calendar"]


db.users.delete_many({})
db.categories.delete_many({})
db.events.delete_many({})



def create_test_users():
    users = [
        {
            "_id": str(uuid.uuid4()),
            "username": "alice_smith",
            "email": "alice@example.com",
            "full_name": "Alice Smith"
        },
        {
            "_id": str(uuid.uuid4()),
            "username": "bob_jones",
            "email": "bob@example.com",
            "full_name": "Bob Jones"
        },
        {
            "_id": str(uuid.uuid4()),
            "username": "charlie_brown",
            "email": "charlie@example.com",
            "full_name": "Charlie Brown"
        },
        {
            "_id": str(uuid.uuid4()),
            "username": "diana_ross",
            "email": "diana@example.com",
            "full_name": "Diana Ross"
        }
    ]

    db.users.insert_many(users)
    return users



def create_test_categories():
    categories = [
        {
            "_id": str(uuid.uuid4()),
            "name": "Work",
            "color": "#FF5733"
        },
        {
            "_id": str(uuid.uuid4()),
            "name": "Personal",
            "color": "#33FF57"
        },
        {
            "_id": str(uuid.uuid4()),
            "name": "Family",
            "color": "#3357FF"
        },
        {
            "_id": str(uuid.uuid4()),
            "name": "Health",
            "color": "#F033FF"
        }
    ]

    db.categories.insert_many(categories)
    return categories



def create_test_events(users, categories):
    now = datetime.now()
    events = []

    work_category = next(c for c in categories if c["name"] == "Work")
    events.append({
        "_id": str(uuid.uuid4()),
        "title": "Team Meeting",
        "description": "Weekly sync with the team",
        "start_time": now.replace(hour=10, minute=0, second=0) + timedelta(days=1),
        "end_time": now.replace(hour=11, minute=0, second=0) + timedelta(days=1),
        "location": "Conference Room A",
        "category_id": work_category["_id"],
        "owner_id": users[0]["_id"],
        "participants": [
            {"user_id": users[1]["_id"], "status": "accepted"},
            {"user_id": users[2]["_id"], "status": "pending"}
        ]
    })

    events.append({
        "_id": str(uuid.uuid4()),
        "title": "Project Deadline",
        "description": "Submit final project deliverables",
        "start_time": now.replace(hour=15, minute=0, second=0) + timedelta(days=3),
        "end_time": now.replace(hour=17, minute=0, second=0) + timedelta(days=3),
        "category_id": work_category["_id"],
        "owner_id": users[1]["_id"],
        "participants": [
            {"user_id": users[0]["_id"], "status": "accepted"}
        ]
    })

    personal_category = next(c for c in categories if c["name"] == "Personal")
    events.append({
        "_id": str(uuid.uuid4()),
        "title": "Gym Session",
        "description": "Weekly workout",
        "start_time": now.replace(hour=7, minute=30, second=0) + timedelta(days=2),
        "end_time": now.replace(hour=8, minute=30, second=0) + timedelta(days=2),
        "category_id": personal_category["_id"],
        "owner_id": users[2]["_id"],
        "participants": []
    })

    family_category = next(c for c in categories if c["name"] == "Family")
    events.append({
        "_id": str(uuid.uuid4()),
        "title": "Family Dinner",
        "description": "Monthly family gathering",
        "start_time": now.replace(hour=18, minute=0, second=0) + timedelta(days=5),
        "end_time": now.replace(hour=21, minute=0, second=0) + timedelta(days=5),
        "location": "Home",
        "category_id": family_category["_id"],
        "owner_id": users[3]["_id"],
        "participants": [
            {"user_id": users[0]["_id"], "status": "accepted"},
            {"user_id": users[1]["_id"], "status": "declined"},
            {"user_id": users[2]["_id"], "status": "pending"}
        ]
    })

    health_category = next(c for c in categories if c["name"] == "Health")
    events.append({
        "_id": str(uuid.uuid4()),
        "title": "Doctor Appointment",
        "description": "Annual checkup",
        "start_time": now.replace(hour=9, minute=0, second=0) + timedelta(days=4),
        "end_time": now.replace(hour=10, minute=0, second=0) + timedelta(days=4),
        "location": "City Hospital",
        "category_id": health_category["_id"],
        "owner_id": users[0]["_id"],
        "participants": []
    })

    db.events.insert_many(events)
    return events


def populate_database():
    print("Creating test users...")
    users = create_test_users()
    print(f"Created {len(users)} users")

    print("\nCreating test categories...")
    categories = create_test_categories()
    print(f"Created {len(categories)} categories")

    print("\nCreating test events...")
    events = create_test_events(users, categories)
    print(f"Created {len(events)} events")

    print("\nDatabase populated successfully!")
    print(f"Total users: {db.users.count_documents({})}")
    print(f"Total categories: {db.categories.count_documents({})}")
    print(f"Total events: {db.events.count_documents({})}")


if __name__ == "__main__":
    populate_database()