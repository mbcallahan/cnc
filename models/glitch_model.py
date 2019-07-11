class MyBehaviorModel:
    relevant_inputs = []
    relevant_outputs = ['Reset', 'Button', 'Output', 'Clock' ]

    def validate(self, inputs, outputs):
        return self.relevant_output_values[2].signal.final_value

ModelClass = MyBehaviorModel
