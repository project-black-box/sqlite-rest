def analyze(table):
    #stubbed! lel
    return {
      "cols": ['col1', 'col2', 'col3', 'col4'],
      "primary": [['col1', 'col2']],
      "foreign": [{
        "cols": ['col2'],
        "ref": 'b',
        "ref_cols": ['col2']
      }, {
        "cols": ['col3', 'col4'],
        "ref": 'c',
        "ref_cols": ['col3', 'col4']
      }]
    }
