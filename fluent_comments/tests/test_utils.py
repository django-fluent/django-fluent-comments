from django.test import SimpleTestCase

from fluent_comments.utils import split_words


class TestUtils(SimpleTestCase):
    def test_split_words(self):
        text = """college scholarship essays - <a href=" https://collegeessays.us/ ">how to write a good introduction for a college essay</a> 
boston university college essay <a href=" https://collegeessays.us/ ">how to write an essay for college</a> 
https://collegeessays.us/ 
http://www.monkeyface.com/__media__/js/netsoltrademark.php?d=collegeessays.us"""
        self.assertEqual(
            split_words(text),
            {
                "__media__",
                "a",
                "an",
                "boston",
                "college",
                "collegeessays",
                "com",
                "d",
                "essay",
                "essays",
                "for",
                "good",
                "how",
                "href",
                "http",
                "https",
                "introduction",
                "js",
                "monkeyface",
                "netsoltrademark",
                "php",
                "scholarship",
                "to",
                "university",
                "us",
                "write",
                "www",
            },
        )
