from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from page import Page, from_string 

def test_page_class():
    page = Page()

    # Add some messages
    sender_user_name1 = "SenderUserName1"
    msg_type1 = "TEXT"
    timestamp1 = "2025-01-14 16:44:19"
    message1 = "Hello, this is a text message."
    encrypted_aes_key_sender1 = "EncryptedAESKey1"
    encrypted_aes_key_receiver1 = "EncryptedAESKey2"

    # Add message to the page
    page.add_message(sender_user_name1, msg_type1, timestamp1, message1, encrypted_aes_key_sender1, encrypted_aes_key_receiver1)

    sender_user_name2 = "SenderUserName2"
    msg_type2 = "FILE"
    timestamp2 = "2025-01-13 16:44:19"
    message2 = '{"file_size": 12356, "file_name": "test.txt", "cid": 12345678}'
    encrypted_aes_key_sender2 = "EncryptedAESKey1"
    encrypted_aes_key_receiver2 = "EncryptedAESKey2"

    # Add another message to the page
    page.add_message(sender_user_name2, msg_type2, timestamp2, message2, encrypted_aes_key_sender2, encrypted_aes_key_receiver2)

    # Print page details
    print("Page Details:")
    print(page.to_string())

    # Test is_full()
    print("\nIs Page Full?", page.is_full())

    # Test sorting by time
    page.sort_by_time()
    print("\nPage Details After Sorting:")
    print(page.to_string())

    # Convert to string and back
    page_string = page.to_string()
    reconstructed_page = from_string(page_string)
    print("\nReconstructed Page Details:")
    print(reconstructed_page.to_string())

    # Test all_messages()
    print("\nAll Messages:")
    print(reconstructed_page.all_messages())

if __name__ == "__main__":
    test_page_class()
