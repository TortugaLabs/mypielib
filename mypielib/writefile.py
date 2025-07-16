
def writefile(name:str, data:str|bytes, offset:int=0, mode:str = 'w', truncate:bool = False):
  '''Write the contents of a file as whole

  :param name: File name to write
  :param data: data to write
  :param offset: start writing at the given offset
  :param truncate: will truncate the file

  '''
  with open(name,f'{mode}{"b" if isintance(data,bytes) else ""}') as fp:
    if offset: fp.seek(offset)
    fp.write(data)
    if truncate: fp.truncate()
