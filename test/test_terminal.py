import pytest
from python_tools.small_components.terminal import cd
import os

@pytest.mark.skip(reason='successful')
@pytest.mark.parametrize(
    "to", ['', '../', 'C:/Users', './', '.', '..']
)
def test_cd_valid_path(to):
    """
    valid path
    """
    original = os.getcwd()
    with cd(to):
        pass
    print(original)
    assert os.getcwd() == original


@pytest.mark.skip(reason='successful')    
@pytest.mark.parametrize(
    'to', ['whta','good','gH:/']
)
def test_cd_invalid_path(to):
    '''
    invalid path
    '''
    original = os.getcwd() 
    with pytest.raises((FileNotFoundError, OSError, PermissionError)):
        with cd(to):
            pass 
    assert os.getcwd() == original


