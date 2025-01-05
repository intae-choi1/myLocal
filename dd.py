class Hi():
    def __init__(self, value):
        self.value = value
        

hi = Hi(50)

func1 = lambda: print(hi.value)

hi.value = 60

func2 = lambda: print(hi.value)


func1()
func2()



