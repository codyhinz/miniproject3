import sqlite3
import os

class AddressBook:
    def __init__(self, db_name="address_book.db"):
        """Initialize the AddressBook with a database connection."""
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.setup_database()
    
    def setup_database(self):
        """Create the contacts table if it doesn't exist."""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone_number TEXT,
            email TEXT,
            address TEXT
        )
        ''')
        self.conn.commit()
    
    def add_contact(self, name, phone_number, email, address):
        """Add a new contact to the database."""
        self.cursor.execute('''
        INSERT INTO contacts (name, phone_number, email, address)
        VALUES (?, ?, ?, ?)
        ''', (name, phone_number, email, address))
        self.conn.commit()
        print(f"Contact '{name}' added successfully!")
    
    def view_contacts(self):
        """Display all contacts in the database."""
        self.cursor.execute('SELECT * FROM contacts')
        contacts = self.cursor.fetchall()
        
        if not contacts:
            print("No contacts found in the address book.")
            return
        
        print("\n===== CONTACTS =====")
        for contact in contacts:
            print(f"ID: {contact[0]}")
            print(f"Name: {contact[1]}")
            print(f"Phone: {contact[2]}")
            print(f"Email: {contact[3]}")
            print(f"Address: {contact[4]}")
            print("-------------------")
    
    def update_contact(self, contact_id, name, phone_number, email, address):
        """Update an existing contact by ID."""
        # Check if contact exists
        self.cursor.execute('SELECT * FROM contacts WHERE id = ?', (contact_id,))
        if not self.cursor.fetchone():
            print(f"No contact found with ID {contact_id}")
            return False
        
        # Update the contact
        self.cursor.execute('''
        UPDATE contacts
        SET name = ?, phone_number = ?, email = ?, address = ?
        WHERE id = ?
        ''', (name, phone_number, email, address, contact_id))
        self.conn.commit()
        print(f"Contact with ID {contact_id} updated successfully!")
        return True
    
    def delete_contact(self, contact_id):
        """Delete a contact by ID."""
        # Check if contact exists
        self.cursor.execute('SELECT * FROM contacts WHERE id = ?', (contact_id,))
        if not self.cursor.fetchone():
            print(f"No contact found with ID {contact_id}")
            return False
        
        # Delete the contact
        self.cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
        self.conn.commit()
        print(f"Contact with ID {contact_id} deleted successfully!")
        return True
    
    def find_contact_by_id(self, contact_id):
        """Find a contact by ID and return it."""
        self.cursor.execute('SELECT * FROM contacts WHERE id = ?', (contact_id,))
        return self.cursor.fetchone()
    
    def close_connection(self):
        """Close the database connection."""
        self.conn.close()


def get_contact_info(existing_contact=None):
    """Get contact information from user input."""
    print("\n=== Enter Contact Information ===")
    
    if existing_contact:
        # For update operations, show current values
        name = input(f"Name [{existing_contact[1]}]: ") or existing_contact[1]
        phone = input(f"Phone [{existing_contact[2]}]: ") or existing_contact[2]
        email = input(f"Email [{existing_contact[3]}]: ") or existing_contact[3]
        address = input(f"Address [{existing_contact[4]}]: ") or existing_contact[4]
    else:
        # For new contacts
        name = input("Name: ")
        while not name:  # Ensure name is not empty
            print("Name is required.")
            name = input("Name: ")
            
        phone = input("Phone number: ")
        email = input("Email: ")
        address = input("Address: ")
    
    return name, phone, email, address


def main():
    """Main function to run the address book application."""
    print("\n===== Welcome to Address Book Application =====")
    address_book = AddressBook()
    
    while True:
        print("\nAddress Book Menu:")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            # Add a new contact
            name, phone, email, address = get_contact_info()
            address_book.add_contact(name, phone, email, address)
            
        elif choice == '2':
            # View all contacts
            address_book.view_contacts()
            
        elif choice == '3':
            # Update an existing contact
            contact_id = input("Enter the ID of the contact to update: ")
            try:
                contact_id = int(contact_id)
                contact = address_book.find_contact_by_id(contact_id)
                if contact:
                    name, phone, email, address = get_contact_info(contact)
                    address_book.update_contact(contact_id, name, phone, email, address)
                else:
                    print(f"No contact found with ID {contact_id}")
            except ValueError:
                print("Invalid ID. Please enter a number.")
            
        elif choice == '4':
            # Delete a contact
            contact_id = input("Enter the ID of the contact to delete: ")
            try:
                contact_id = int(contact_id)
                address_book.delete_contact(contact_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
            
        elif choice == '5':
            # Exit the application
            print("Thank you for using the Address Book Application!")
            address_book.close_connection()
            break
            
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()