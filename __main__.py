# To test if there will be a crash after import
try:
    import cairosvg
except Exception as err:
    print(repr(err))
