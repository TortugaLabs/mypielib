#python3



def cidr_to_netmask(cidr:int) -> str:
  '''Convert CIDR prefix to netmask
  :param int cidr: prefix to convert
  :returns str: netmask

  From: https://stackoverflow.com/questions/33750233/convert-cidr-to-subnet-mask-in-python

  Examples:
  
  >>> cidr_to_netmask(32)
  '255.255.255.255'
  >>> cidr_to_netmask(30)
  '255.255.255.252'
  >>> cidr_to_netmask(28)
  '255.255.255.240'
  >>> cidr_to_netmask(24)
  '255.255.255.0'
  >>> cidr_to_netmask(20)
  '255.255.240.0'
  >>> cidr_to_netmask(16)
  '255.255.0.0'
  
  '''
  mask = (0xffffffff >> (32 - cidr)) << (32 - cidr)
  return (str( (0xff000000 & mask) >> 24)   + '.' +
          str( (0x00ff0000 & mask) >> 16)   + '.' +
          str( (0x0000ff00 & mask) >> 8)    + '.' +
          str( (0x000000ff & mask)))

if __name__ == '__main__':
  import doctest
  doctest.testmod()
  
