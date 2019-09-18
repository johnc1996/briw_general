import unittest
import model

# TODO clean db and reinstantiate test db

session = model.make_session()

expected = {'first_name':'Tester',
            'last_name': 'TestFace',
            'email': 'a2@b.co.uk',
            'drink_name' : 'Nigerian Guinness',
             'configured_drink': {'email': 'traceyalansdown@gmail.com',
                                  'original_drink_name':'Godfather', 'new_drink_name': 'Bellini'}}

def clean_env():
    # clean up Person 
        some_person = session.query(model.Person).filter(model.Person.email == expected['email']).first()
        if some_person is not None:
            session.delete(some_person)
            session.commit()
        
        some_person = session.query(model.Person).filter(model.Person.email == expected['email']).first()
        if some_person is not None:
            session.delete(some_person)
            session.commit()


class Test_Methods(unittest.TestCase):
    def test_create_new_user(self):
        # create a new user and db persist
        a_person = model.new_person(session, expected['first_name'], expected['last_name'], expected['email'])

        # query db to check persist
        queried_person = session.query(model.Person).filter(model.Person.email == expected['email']).first()
        
        actual = {'first_name':queried_person.first_name,
                  'last_name': queried_person.last_name,
                  'email': queried_person.email}

        self.assertEqual(expected, actual)
        clean_env()

    def test_get_person_by_email(self):
        # create a new user and db persist
        model.new_person(session, expected['first_name'], expected['last_name'],
                         expected['email'])

        some_person = model.get_person_by_email(session, expected['email'])

        self.assertEqual(some_person.email, expected['email'])

    def test_create_new_drink(self):
        # create a new user and db persist
        a_drink = model.new_drink(session, expected['drink_name'])

        # query db to check persist
        queried_drink = session.query(model.Drink).filter(model.Drink.name == expected['drink_name']).first()
        
        actual = {'first_name':queried_drink.first_name,
                  'last_name': queried_drink.last_name,
                  'email': queried_drink.email}

        self.assertEqual(expected, actual)
        clean_env()
    
    def test_modify_default_configured_drink(self):
        test_email = expected['configured_drink']['email']
        original_drink_name = expected['configured_drink']['original_drink_name']
        new_drink_name = expected['configured_drink']['new_drink_name']

        some_person = model.get_person_by_email(test_email)

        some_person.set_default_configured_drink(new_drink_name)

        actual_name = model.get_default_configured_drink().name

        self.assertEqual(actual_name, new_drink_name)










if __name__ == "__main__":
    clean_env()
    unittest.main()
    clean_env()