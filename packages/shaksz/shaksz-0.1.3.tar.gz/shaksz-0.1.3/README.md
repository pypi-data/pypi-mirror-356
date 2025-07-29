# shaksz
All coding and design solutions as package


# Unit Tests
`python -m unittest discover -s tests`

# Build package


    python setup.py sdist bdist_wheel



# Publish Test

    twine upload --repository testpypi dist/*

# Publish Prod
    TBD

    pip install twine

    twine upload dist/*


# Consumption
    pip install git+ssh://git@github.com/vermavarun/shaksz
    pip install git+https://github.com/vermavarun/shaksz.git
    pip install git+https://<TOKEN>@github.com/vermavarun/shaksz.git
    pip install shaksz

    # CODE
    
    import shaksz

    result = shaksz.leetcode.twoSum([2, 7, 11, 15], 9)

    print(result)
