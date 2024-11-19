import pytest 
from structures import Trie 
from typing import List 
import random 
import string 

@pytest.fixture
def random_words() -> List[str]:
    all_chars = string.ascii_letters
    res = []
    for i in range(100):
        word_len = random.randint(1, 26)
        s = ""
        for j in range(0, word_len):
            s += all_chars[random.randint(0, 25)]
        res.append(s)
    return res 
    

@pytest.fixture
def trie(random_words) -> Trie:
    t = Trie()
    for word in random_words:
        t.add(word)
    return t    
    
    
def test_exists(random_words, trie):
    for word in random_words:
        assert word in trie 
        
    trie.remove(random_words[0])
    assert random_words[0] not in trie