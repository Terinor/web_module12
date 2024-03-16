import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from src.repository.contacts import (
    create_contact,
    get_contacts,
    get_contact_by_id,
    update_contact,
    delete_contact,
    search_contacts,
    get_contacts_with_upcoming_birthdays,
)
from src.schemas import ContactCreate, ContactUpdate


class TestContactsRepository(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.contact_data = ContactCreate(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="+1234567890",
            birthday=datetime.now().date()
        )
        self.contact_update_data = ContactUpdate(first_name="Jane")

    @patch('src.repository.contacts.Contact')
    def test_create_contact(self, mock_Contact):
        mock_Contact.return_value = MagicMock(**self.contact_data.dict())
        new_contact = create_contact(db=self.mock_db, contact=self.contact_data)
        self.mock_db.add.assert_called_once()
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once()
        self.assertEqual(new_contact.first_name, "John")

    def test_get_contacts(self):
        mock_query = self.mock_db.query.return_value
        get_contacts(db=self.mock_db, skip=0, limit=100)
        mock_query.offset.assert_called_with(0)
        mock_query.limit.assert_called_with(100)

    def test_get_contact_by_id(self):
        mock_query = self.mock_db.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = MagicMock(**self.contact_data.dict())

        contact = get_contact_by_id(db=self.mock_db, contact_id=1)
        mock_query.filter.assert_called_once()
        self.assertEqual(contact.first_name, "John")

    def test_update_contact(self):
        mock_query = self.mock_db.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = MagicMock(**self.contact_data.dict())

        updated_contact = update_contact(db=self.mock_db, contact_id=1, contact=self.contact_update_data)
        self.mock_db.commit.assert_called_once()
        self.assertEqual(updated_contact.first_name, "Jane")

    def test_delete_contact(self):
        mock_query = self.mock_db.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = MagicMock(**self.contact_data.dict())

        deleted_contact = delete_contact(db=self.mock_db, contact_id=1)
        self.mock_db.delete.assert_called_once()
        self.mock_db.commit.assert_called_once()

    def test_search_contacts(self):
        mock_query = self.mock_db.query.return_value
        search_contacts(db=self.mock_db, query="John", skip=0, limit=100)
        self.assertTrue(mock_query.filter.called)

    def test_get_contacts_with_upcoming_birthdays(self):
        mock_query = self.mock_db.query.return_value
        get_contacts_with_upcoming_birthdays(db=self.mock_db, days=7, skip=0, limit=100)
        self.assertTrue(mock_query.filter.called)


if __name__ == "__main__":
    unittest.main()
