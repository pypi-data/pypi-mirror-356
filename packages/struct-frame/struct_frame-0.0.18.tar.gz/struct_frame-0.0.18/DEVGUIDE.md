
### Installing
``` py -m pip install --upgrade build twine```

### Building
Update version in pyproject.toml if necessary
```py -m build```

### Uploading
Update version in pyproject.toml if necessary and rebuild.
```py -m twine upload dist/*```

### Running Locally
```py .\src\main.py ```
