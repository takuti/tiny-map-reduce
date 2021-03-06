import time
from multiprocessing import current_process
from tiny_map_reduce import TinyMapReduce

"""Good reference for "inverted index":
http://www.slideshare.net/nokuno/hadoopreading06-data-intensive4
"""

def map_func(txt_filename):
  print('[map] %s: started at %s' % (current_process().name, time.ctime().split()[3]))

  with open(txt_filename, 'r') as f:
    lines = f.readlines()

  # make word counting for the lines
  wc_dict = {}
  for line in lines:
    words = set(line.rstrip().split(' '))
    for word in words:
      if word not in wc_dict: wc_dict[word] = 0
      wc_dict[word] += 1

  # output to temporary file with key-value format as: "<word> <filename>:<count>\n"
  tmp_filename = '%s.tmp' % txt_filename
  with open(tmp_filename, 'w') as f:
    for word, cnt in wc_dict.items():
      f.write('%s %s:%s\n' % (word, txt_filename, cnt))

  # return all keys and temporary file's name
  return (wc_dict.keys(), tmp_filename)

def reduce_func((word, tmp_filenames)):
  print('[reduce] %s: started at %s' % (current_process().name, time.ctime().split()[3]))

  including = []

  # reduce results for the given word from all tmporary files
  for tmp_filename in tmp_filenames:

    with open(tmp_filename, 'r') as f:
      lines = f.readlines()

    for line in lines:
      key, value = line.rstrip().split(' ')
      if key == word: including.append(value)

  # return inverted indices for the given word
  return (word, including)

def main():
  master = TinyMapReduce(map_func, reduce_func)
  txt_filenames = ['texts/1.txt', 'texts/2.txt']
  master(txt_filenames)

if __name__ == '__main__':
  main()
