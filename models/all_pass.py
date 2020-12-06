class MyBehaviorModel:
    relevant_inputs = []
    relevant_outputs = ['Rst','Clock', 'Flag']

    def validate(self, inputs, outputs):
        rst = self.relevant_output_values[0].signal
        clock = self.relevant_output_values[1].signal
        flag = self.relevant_output_values[2].signal
        
        print("reset at ", list(rst.changes()))
        print("first clock at ", list(clock.changes()))
        print("flag changes at ", list(flag.changes()))
        return True

ModelClass = MyBehaviorModel
