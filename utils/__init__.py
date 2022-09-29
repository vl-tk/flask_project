import time
from werkzeug.security import generate_password_hash
from database import db

from models import User
# from my_blueprints.demo_app.models import


def write_to_db():

    while True:
        time.sleep(1)


def build_sample_db():
    """Populate a small db with some example entries."""

    import string
    import random

    # passwords are hashed, to use plaintext passwords instead:
    # NEEDED FOR SUCCESSFUL TESTS
    test_user = User(login="admin", password=generate_password_hash("123456"))
    db.session.add(test_user)

    """
    first_names = [
        'Harry', 'Amelia', 'Oliver', 'Jack', 'Isabella', 'Charlie','Sophie', 'Mia',
        'Jacob', 'Thomas', 'Emily', 'Lily', 'Ava', 'Isla', 'Alfie', 'Olivia', 'Jessica',
        'Riley', 'William', 'James', 'Geoffrey', 'Lisa', 'Benjamin', 'Stacey', 'Lucy'
    ]
    last_names = [
        'Brown', 'Smith', 'Patel', 'Jones', 'Williams', 'Johnson', 'Taylor', 'Thomas',
        'Roberts', 'Khan', 'Lewis', 'Jackson', 'Clarke', 'James', 'Phillips', 'Wilson',
        'Ali', 'Mason', 'Mitchell', 'Rose', 'Davis', 'Davies', 'Rodriguez', 'Cox', 'Alexander'
    ]

    for i in range(len(first_names)):
        user = User()
        user.first_name = first_names[i]
        user.last_name = last_names[i]
        user.login = user.first_name.lower()
        user.email = user.login + "@example.com"
        user.password = generate_password_hash(
            "".join(
                random.choice(string.ascii_lowercase + string.digits) for i in range(10)
            )
        )
        db.session.add(user)

    sample_text = [
        {
            'title': "de Finibus Bonorum et Malorum - Part III",
            'content': "At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium \
                        voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati."
        },
        {
            'title': "de Finibus Bonorum et Malorum - Part III",
            'content': "At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium \
                        voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati."
        }
    ]

    for entry in sample_text:
        page = Page()
        page.title = entry['title']
        page.content = entry['content']
        db.session.add(page)
    """

    db.session.commit()
