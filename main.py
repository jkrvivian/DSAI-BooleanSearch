import pandas
import numpy as np
import time

def brutal_search_title(source, query):
    ret = []
    for i in range(1, len(source)):
        if source[i].find(query) != -1:
            ret.append(i)
    return ret
        
def get_response(source, query):
    q = query.split()
    opt = q[1]
    result = []
    ans = []
    for i in range(0, len(q)):
        if i % 2 == 0:
            result.append(brutal_search_title(source, q[i]))
    ans = result[0]

    if opt == "and":
        for l in range(1, len(result)):
            for a in ans[:]:
                if a not in result[l]:
                    ans.remove(a)
    elif opt == "or":
        for j in range(1, len(result)):
            ans = ans + result[j]
        ans = sorted(list(set(ans)))
    else:
        for l in range(1, len(result)):
            for a in ans[:]:
                if a in result[l]:
                    ans.remove(a)
    return ans
        
def read_source(fin):
    source = pandas.read_csv(fin, header=None, names=["num", "title"], dtype={"num": np.int})
    source = source.set_index("num")["title"].to_dict()
    return source

if __name__ == '__main__':
    # You should not modify this part.
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--source',
                       default='source.csv',
                       help='input source data file name')
    parser.add_argument('--query',
                        default='query.txt',
                        help='query file name')
    parser.add_argument('--output',
                        default='output.txt',
                        help='output file name')
    args = parser.parse_args()
    
    # load source data, build search engine
    start = time.time()
    source = read_source(args.source)
    print("Build time: ", time.time() - start, " sec")

    # compute query result
    query = pandas.read_csv(args.query, header=None, names=["query"])
    query = query["query"].tolist() 
  
    # output result
    with open(args.output, 'w') as output_file:
        start = time.time()
        for i in range(0, len(query)):
            if i != 0:
                output_file.write("\n")
            result = get_response(source, query[i])
            if len(result) == 0:
                output_file.write("0");
            else:
                output_file.write(",".join(str(x) for x in result))
        print("Search time: ", time.time() - start, " sec")
