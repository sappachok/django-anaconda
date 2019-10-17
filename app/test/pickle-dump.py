
import pickle
import pickleout

example_dict  = {1:"6",2:"2",3:"f", 4:"goo"}


pickle_out = open("dict.pickle","wb")
pickle.dump(globals(), pickle_out, protocol=pickle.HIGHEST_PROTOCOL)
#pickle.dump(example_dict, pickle_out)

#allvar = locals()
#pickle.dump(allvar, pickle_out)
pickle_out.close()

#for i in locals():
#    print(i)

# x = locals()

#print()
#pickleout.output()
