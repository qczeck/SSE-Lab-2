from app import process_query


def test_knows_about_dinosaurs():
    din = "Dinosaurs ruled the Earth 200 million years ago"
    assert process_query("dinosaurs") == din


def test_does_not_know_about_asteroids():
    assert process_query("asteroids") == "Unknown"


def test_does_know_your_name():
    assert process_query("What is your name?") == "Mac"


def test_finds_largest_number_out_of_three():
    assert process_query("Which of the following numbers"
                         " is the largest: 24, 47, 98?") == "98"


def test_does_sum_of_numbers_work():
    assert process_query("What is 91 plus 30?") == '121'
