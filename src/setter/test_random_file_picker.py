import random_file_picker

if __name__ == '__main__':
    obj = random_file_picker.RandomFilePicker(['/home/ingo/Icons'], ['.png'], 'test.cfg')
    
    print obj.file_list