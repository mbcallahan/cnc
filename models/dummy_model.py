class MyBehaviorModel:
    relevant_inputs = ['Clock']
    relevant_outputs = []

    def validate(self, inputs, outputs):
    	return self.relevant_input_values[0].signal.clock_rate <= 20000000 and self.relevant_input_values[0].signal.clock_rate >= 10000000

ModelClass = MyBehaviorModel
