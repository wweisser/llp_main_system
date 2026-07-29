import queue

class que_item:
    def __init__(self, cm_type, command, data):
        self.type = cm_type
        self.command = command
        self.data = data

    def get_data(self):
        return self.data
    
    def get_command(self):
        return self.command
    
    def get_cm_type(self):
        return self.type


class db_que:
    def __init__(self):
        self.que = queue.Queue()

    def put_db_item(self, cm_type, command, data):
        self.que.put(que_item(cm_type, command, data))
    
    def get_db_item(self):
        return self.que.get()


if __name__ == "__main__":
    test_que = db_que()
    test = que_item('test_type', 'test_command', 'test_data')
    test_que.put_db_item('cm_type', 'command', 'data')
    test_item = test_que.get_db_item()
    print(test_item.get_cm_type())
    print(test_item.get_command())
    print(test_item.get_data())