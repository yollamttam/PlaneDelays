







infile = open(whatever.svg)
svg = infile.read()
outfile = open(output.svg,'w')
outfile.write(svg.format(**whateverdict))
outfile.close()
