class PrePro():

    def filter(code):
        i = 0
        to_delete = []
        text = list(code)
        while i < len(text):
            if text[i] == "'":
                j = i
                while text[j] != "\n":
                    j += 1
                    if j == len(text):
                        break
                    
                to_delete.append([i,j])
            i += 1                    
        
        for k in reversed(range(len(to_delete))):
            i = to_delete[k][0]
            j = to_delete[k][1]
            del text[i:j+1]

        string = ''.join(text)
        return string