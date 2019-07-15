import pickle

patches = []

data0 = {"id":"0","title":"trance funk","author":"mat", "0": "30", "1": "35" , "2": "5" , "3": "55" , "4": "127" , "5": "15" , "6": "35" , "7": "105" }
data1 = {"id":"1","title":"trance funk","author":"mat", "0": "30", "1": "35" , "2": "5" , "3": "55" , "4": "127" , "5": "15" , "6": "35" , "7": "105" }
data2 = {"id":"2","title":"trance funk","author":"mat", "0": "30", "1": "35" , "2": "5" , "3": "55" , "4": "127" , "5": "15" , "6": "35" , "7": "105" }
data3 = {"id":"3","title":"trance funk","author":"mat", "0": "30", "1": "35" , "2": "5" , "3": "55" , "4": "127" , "5": "15" , "6": "35" , "7": "105" }
data4 = {"id":"4","title":"trance funk","author":"mat", "0": "30", "1": "35" , "2": "5" , "3": "55" , "4": "127" , "5": "15" , "6": "35" , "7": "105" }
data5 = {"id":"5","title":"trance funk","author":"mat", "0": "30", "1": "35" , "2": "5" , "3": "55" , "4": "127" , "5": "15" , "6": "35" , "7": "105" }

patches.append(data0)
patches.append(data1)
patches.append(data2)
patches.append(data3)
patches.append(data4)
patches.append(data5)

pickle.dump( patches, open( "bank0.flip", "wb" ) )

loaded = pickle.load( open( "bank0.flip", "rb" ) )
print(loaded)