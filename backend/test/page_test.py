import unittest
from backend.page import Page


class MyTestCase(unittest.TestCase):
    def test_insert_one_message(self):
        page = Page()
        page.add_message("hi", "this", "is", "a", "insertion", "test", ".")
        self.assertEqual({'rsa_pub_key': 'hi',
                          'msg_type': 'this',
                          't_stamp': 'is',
                          'file_location_key': 'a',
                          'encrypted_message': 'insertion',
                          'encrypted_aes_key_sender': 'test',
                          'encrypted_aes_key_receiver': '.'}, page.msg[0])

    def test_insert_over_20_messages(self):
        page = Page()
        for i in range(100):
            page.add_message(str(i), str(i), str(i), str(i), str(i), str(i), str(i))
        self.assertEqual(20, page.message_count)

    def test_is_full(self):
        page = Page()
        for i in range(20):
            page.add_message(str(i), str(i), str(i), str(i), str(i), str(i), str(i))
        self.assertTrue(page.is_full())
        # Try to add another message, should return False
        result = page.add_message("extra", "extra", "extra", "extra", "extra", "extra", "extra")
        self.assertFalse(result)

    def test_to_string_and_from_string(self):
        page = Page()
        page.add_message("key1", "type1", "timestamp1", "location1", "message1", "key_sender1", "key_receiver1")
        page.add_message("key2", "type2", "timestamp2", "location2", "message2", "key_sender2", "key_receiver2")
        page_string = page.to_string()
        # Recreate page from string
        new_page = Page.from_string(page_string)
        self.assertEqual(page.msg, new_page.msg)
        self.assertEqual(page.message_count, new_page.message_count)

    def test_sort_by_time(self):
        page = Page()
        page.add_message("key1", "type1", "2024-10-02", "location1", "message1", "key_sender1", "key_receiver1")
        page.add_message("key2", "type2", "2022-01-01", "location2", "message2", "key_sender2", "key_receiver2")
        page.add_message("key3", "type3", "2023-05-15", "location3", "message3", "key_sender3", "key_receiver3")
        # Sort by t_stamp
        page.sort_by_time()
        # Check that messages are sorted in ascending order by timestamp
        self.assertEqual(page.msg[0]['t_stamp'], "2022-01-01")
        self.assertEqual(page.msg[1]['t_stamp'], "2023-05-15")
        self.assertEqual(page.msg[2]['t_stamp'], "2024-10-02")

    def test_insert_edge_case(self):
        page = Page()
        # Insert a message with empty strings
        page.add_message("", "", "", "", "", "", "")
        self.assertEqual(page.msg[0], {
            'rsa_pub_key': '',
            'msg_type': '',
            't_stamp': '',
            'file_location_key': '',
            'encrypted_message': '',
            'encrypted_aes_key_sender': '',
            'encrypted_aes_key_receiver': ''
        })

    def test_empty_page_to_string(self):
        page = Page()
        page_string = page.to_string()
        # Should be an empty dictionary in string form
        self.assertEqual(page_string, "{}")


if __name__ == '__main__':
    unittest.main()
